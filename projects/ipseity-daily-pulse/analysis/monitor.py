#!/usr/bin/env python3
"""Monitor and describe the public Ipseity Daily canonical microdata.

The default mode checks the live homepage, downloads the canonical gzip to a
temporary file, validates it, appends one monitoring-history row, and replaces
the current derived outputs.  ``--input`` analyzes an already retrieved gzip;
HTTP statuses are then required so that a local replay cannot masquerade as a
network check.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import hashlib
import html
import json
import math
import re
import statistics
import tempfile
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


PROJECT = Path(__file__).resolve().parents[1]
MAIN_URL = "https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/"
DATASET_URL = MAIN_URL + "files/ipseity.csv.gz"
EXPECTED_COLUMNS = [
    "endorsed",
    "signifier",
    "observation_date",
    "hashed_respondent_id",
    "demographics_status",
    "age",
    "sex",
    "ethnicity",
    "birth_country",
    "residence_country",
    "nationality",
    "language",
    "student",
    "employment",
    "time_on_task",
    "approvals",
]
HISTORY_FIELDS = [
    "checked_at_utc",
    "main_url",
    "main_http_status",
    "main_site_reachable",
    "canonical_url",
    "canonical_http_status",
    "canonical_dataset_retrieved",
    "parsed_successfully",
    "observations",
    "earliest_observation_date",
    "most_recent_observation_date",
    "data_lag_days",
    "unique_respondents",
    "signifiers",
    "duplicate_keys",
    "validation_error_count",
    "dataset_bytes",
    "dataset_sha256",
    "anomaly",
]
MIN_TREND_OBSERVATIONS = 300
MIN_TREND_SPAN_DAYS = 180
MIN_TREND_DATES = 30
LEADER_SENSITIVITY_PER_TAIL = 10
DAYS_PER_YEAR = 365.2425
TREND_EPOCH_ORDINAL = dt.date(2020, 1, 1).toordinal()
COMPOSITION_FIELDS = ["demographics_status", "sex", "ethnicity", "student", "employment"]


@dataclass
class SignifierStats:
    observations: int = 0
    yes_count: int = 0
    sum_x: int = 0
    sum_x2: int = 0
    sum_xy: int = 0
    earliest: dt.date | None = None
    latest: dt.date | None = None
    dates: set[int] = field(default_factory=set)
    # respondent -> [n, sum_x, sum_y, sum_x2, sum_xy].  These sufficient
    # statistics permit respondent-clustered inference without retaining every
    # response row in memory.
    respondent_sums: dict[str, list[int]] = field(default_factory=dict)

    def add(self, date: dt.date, endorsed: int, respondent: str) -> None:
        # A recent fixed epoch avoids cancellation between very large, nearly
        # equal floating-point quantities in the centered sums.
        x = date.toordinal() - TREND_EPOCH_ORDINAL
        self.observations += 1
        self.yes_count += endorsed
        self.sum_x += x
        self.sum_x2 += x * x
        self.sum_xy += x * endorsed
        self.earliest = date if self.earliest is None else min(self.earliest, date)
        self.latest = date if self.latest is None else max(self.latest, date)
        self.dates.add(x)
        cluster = self.respondent_sums.get(respondent)
        if cluster is None:
            cluster = [0, 0, 0, 0, 0]
            self.respondent_sums[respondent] = cluster
        cluster[0] += 1
        cluster[1] += x
        cluster[2] += endorsed
        cluster[3] += x * x
        cluster[4] += x * endorsed


@dataclass
class DatasetAudit:
    path: Path
    checked_at: dt.datetime
    rows: int = 0
    earliest: dt.date | None = None
    latest: dt.date | None = None
    respondents: set[str] = field(default_factory=set)
    daily: Counter = field(default_factory=Counter)
    signifiers: dict[str, SignifierStats] = field(default_factory=dict)
    duplicate_keys: int = 0
    errors: list[str] = field(default_factory=list)
    sha256: str = ""
    byte_count: int = 0

    @property
    def parsed_successfully(self) -> bool:
        return not self.errors


def utc_timestamp(value: str | None) -> dt.datetime:
    if value is None:
        return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("--checked-at must include a UTC offset or trailing Z")
    return parsed.astimezone(dt.timezone.utc).replace(microsecond=0)


def iso_z(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def retrieve(url: str, destination: Path | None = None) -> tuple[int | None, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "Virtual-CSSERG-Ipseity-Pulse/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            status = response.status
            if destination is None:
                response.read(1)
            else:
                with destination.open("wb") as output:
                    while chunk := response.read(1024 * 1024):
                        output.write(chunk)
        return status, None
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        status = getattr(exc, "code", None)
        return status, f"{type(exc).__name__}: {exc}"


def audit_dataset(path: Path, checked_at: dt.datetime) -> DatasetAudit:
    audit = DatasetAudit(path=path, checked_at=checked_at)
    audit.byte_count = path.stat().st_size
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    audit.sha256 = digest.hexdigest()

    seen_keys: set[tuple[str, str, str]] = set()
    error_examples: Counter[str] = Counter()
    try:
        with gzip.open(path, "rt", encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames != EXPECTED_COLUMNS:
                audit.errors.append(
                    "schema mismatch: expected "
                    + repr(EXPECTED_COLUMNS)
                    + ", received "
                    + repr(reader.fieldnames)
                )
                return audit
            for row_number, row in enumerate(reader, start=2):
                audit.rows += 1
                if None in row:
                    error_examples[f"row {row_number}: extra CSV fields"] += 1
                    continue
                endorsed_text = row["endorsed"]
                if endorsed_text not in {"0", "1"}:
                    error_examples[f"row {row_number}: invalid endorsed value"] += 1
                    continue
                try:
                    observation_date = dt.date.fromisoformat(row["observation_date"])
                except ValueError:
                    error_examples[f"row {row_number}: invalid observation_date"] += 1
                    continue
                if observation_date > checked_at.date():
                    error_examples[f"row {row_number}: future observation_date"] += 1
                    continue
                respondent = row["hashed_respondent_id"]
                if re.fullmatch(r"[0-9a-f]{12}", respondent) is None:
                    error_examples[f"row {row_number}: invalid hashed_respondent_id"] += 1
                    continue
                if row["demographics_status"] not in {
                    "available",
                    "consent_revoked",
                    "data_expired",
                }:
                    error_examples[f"row {row_number}: invalid demographics_status"] += 1
                    continue
                signifier = row["signifier"]
                if not signifier:
                    error_examples[f"row {row_number}: empty signifier"] += 1
                    continue
                key = (respondent, row["observation_date"], signifier)
                if key in seen_keys:
                    audit.duplicate_keys += 1
                else:
                    seen_keys.add(key)
                endorsed = int(endorsed_text)
                audit.respondents.add(respondent)
                audit.daily[observation_date] += 1
                audit.earliest = (
                    observation_date if audit.earliest is None else min(audit.earliest, observation_date)
                )
                audit.latest = observation_date if audit.latest is None else max(audit.latest, observation_date)
                audit.signifiers.setdefault(signifier, SignifierStats()).add(
                    observation_date, endorsed, respondent
                )
    except (gzip.BadGzipFile, EOFError, UnicodeDecodeError, csv.Error, OSError) as exc:
        audit.errors.append(f"could not parse gzip CSV: {type(exc).__name__}: {exc}")
        return audit

    if audit.rows == 0:
        audit.errors.append("dataset contains no observations")
    if audit.duplicate_keys:
        audit.errors.append(f"dataset contains {audit.duplicate_keys} duplicate canonical keys")
    if error_examples:
        total = sum(error_examples.values())
        examples = "; ".join(message for message, _ in error_examples.most_common(5))
        audit.errors.append(f"{total} malformed rows; examples: {examples}")
    return audit


def trend_row(signifier: str, stats: SignifierStats) -> dict[str, object]:
    assert stats.earliest is not None and stats.latest is not None
    n = stats.observations
    span_days = (stats.latest - stats.earliest).days
    date_count = len(stats.dates)
    reasons = []
    if n < MIN_TREND_OBSERVATIONS:
        reasons.append(f"fewer than {MIN_TREND_OBSERVATIONS} observations")
    if span_days < MIN_TREND_SPAN_DAYS:
        reasons.append(f"span shorter than {MIN_TREND_SPAN_DAYS} days")
    if date_count < MIN_TREND_DATES:
        reasons.append(f"fewer than {MIN_TREND_DATES} dates")
    if len(stats.respondent_sums) < 2:
        reasons.append("fewer than 2 respondent clusters")
    centered_x2 = stats.sum_x2 - stats.sum_x * stats.sum_x / n
    centered_xy = stats.sum_xy - stats.sum_x * stats.yes_count / n
    if centered_x2 <= 0:
        reasons.append("no date variance")
    slope = centered_xy / centered_x2 if centered_x2 > 0 else math.nan
    annual_pp = slope * DAYS_PER_YEAR * 100
    ci_low = ci_high = math.nan
    if n > 2 and centered_x2 > 0:
        centered_y2 = stats.yes_count - stats.yes_count * stats.yes_count / n
        residual_ss = max(0.0, centered_y2 - slope * centered_xy)
        slope_se = math.sqrt((residual_ss / (n - 2)) / centered_x2)
        margin = 1.96 * slope_se * DAYS_PER_YEAR * 100
        ci_low, ci_high = annual_pp - margin, annual_pp + margin
    eligible = not reasons
    return {
        "signifier": signifier,
        "observations": n,
        "yes_count": stats.yes_count,
        "prevalence_percent": stats.yes_count / n * 100,
        "earliest_observation_date": stats.earliest.isoformat(),
        "latest_observation_date": stats.latest.isoformat(),
        "span_days": span_days,
        "observation_dates": date_count,
        "respondent_clusters": len(stats.respondent_sums),
        "max_responses_per_respondent": max(cluster[0] for cluster in stats.respondent_sums.values()),
        "eligible": eligible,
        "exclusion_reason": "; ".join(reasons),
        "annual_change_percentage_points": annual_pp if eligible else None,
        "annual_change_ci95_lower": ci_low if eligible else None,
        "annual_change_ci95_upper": ci_high if eligible else None,
    }


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    """Return monotone Benjamini-Hochberg adjusted p-values in input order."""
    adjusted = [math.nan] * len(p_values)
    ranked = sorted(enumerate(p_values), key=lambda item: item[1])
    running = 1.0
    for rank in range(len(ranked), 0, -1):
        index, p_value = ranked[rank - 1]
        running = min(running, p_value * len(ranked) / rank)
        adjusted[index] = running
    return adjusted


def add_robust_inference(
    trends: list[dict[str, object]], signifiers: dict[str, SignifierStats]
) -> None:
    """Add respondent-clustered CR1 inference and multiplicity sensitivity.

    Point estimates remain the unweighted linear probability slopes.  The
    sandwich variance groups score contributions by hashed respondent and uses
    the common G/(G-1) * (N-1)/(N-K) finite-sample correction with K=2.
    """
    tested_rows: list[dict[str, object]] = []
    p_values: list[float] = []
    for row in trends:
        stats = signifiers[str(row["signifier"])]
        row.update(
            {
                "annual_change_cluster_se": None,
                "annual_change_cluster_ci95_lower": None,
                "annual_change_cluster_ci95_upper": None,
                "cluster_robust_p_value": None,
                "benjamini_hochberg_q_value": None,
                "bonferroni_adjusted_p_value": None,
                "fdr_05": False,
                "bonferroni_05": False,
            }
        )
        if not row["eligible"]:
            continue
        n = stats.observations
        clusters = len(stats.respondent_sums)
        centered_x2 = stats.sum_x2 - stats.sum_x * stats.sum_x / n
        if clusters <= 1 or n <= 2 or centered_x2 <= 0:
            continue
        x_bar = stats.sum_x / n
        y_bar = stats.yes_count / n
        slope = (stats.sum_xy - stats.sum_x * stats.yes_count / n) / centered_x2
        meat = 0.0
        for cluster_n, sum_x, sum_y, sum_x2, sum_xy in stats.respondent_sums.values():
            sum_z = sum_x - cluster_n * x_bar
            sum_zy = sum_xy - x_bar * sum_y
            sum_z2 = sum_x2 - 2 * x_bar * sum_x + cluster_n * x_bar * x_bar
            slope_score = sum_zy - y_bar * sum_z - slope * sum_z2
            meat += slope_score * slope_score
        correction = clusters / (clusters - 1) * (n - 1) / (n - 2)
        slope_se = math.sqrt(max(0.0, correction * meat / (centered_x2 * centered_x2)))
        annual_se = slope_se * DAYS_PER_YEAR * 100
        annual_change = float(row["annual_change_percentage_points"])
        if annual_se == 0:
            p_value = 0.0 if annual_change != 0 else 1.0
        else:
            p_value = math.erfc(abs(annual_change / annual_se) / math.sqrt(2))
        row["annual_change_cluster_se"] = annual_se
        row["annual_change_cluster_ci95_lower"] = annual_change - 1.96 * annual_se
        row["annual_change_cluster_ci95_upper"] = annual_change + 1.96 * annual_se
        row["cluster_robust_p_value"] = p_value
        tested_rows.append(row)
        p_values.append(p_value)

    q_values = benjamini_hochberg(p_values)
    tests = len(tested_rows)
    for row, q_value, p_value in zip(tested_rows, q_values, p_values):
        bonferroni = min(1.0, p_value * tests)
        row["benjamini_hochberg_q_value"] = q_value
        row["bonferroni_adjusted_p_value"] = bonferroni
        row["fdr_05"] = q_value <= 0.05
        row["bonferroni_05"] = bonferroni <= 0.05


def independent_column_indexes(matrix: list[list[float]]) -> list[int]:
    """Select linearly independent columns using modified Gram-Schmidt."""
    if not matrix:
        return []
    selected: list[int] = []
    basis: list[list[float]] = []
    for column_index in range(len(matrix[0])):
        column = [row[column_index] for row in matrix]
        original_norm = math.sqrt(sum(value * value for value in column))
        residual = column[:]
        # Reorthogonalization makes the small rank check more stable when time
        # and seasonal indicators are strongly associated.
        for _ in range(2):
            for vector in basis:
                projection = sum(value * axis for value, axis in zip(residual, vector))
                for index, axis in enumerate(vector):
                    residual[index] -= projection * axis
        residual_norm = math.sqrt(sum(value * value for value in residual))
        if residual_norm <= 1e-9 * max(1.0, original_norm):
            continue
        selected.append(column_index)
        basis.append([value / residual_norm for value in residual])
    return selected


def invert_matrix(matrix: list[list[float]]) -> list[list[float]]:
    """Invert a small dense matrix with partial-pivoted Gauss-Jordan steps."""
    size = len(matrix)
    augmented = [
        row[:] + [1.0 if row_index == column_index else 0.0 for column_index in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    scale = max(abs(value) for row in matrix for value in row)
    for column in range(size):
        pivot = max(range(column, size), key=lambda index: abs(augmented[index][column]))
        if abs(augmented[pivot][column]) <= max(1.0, scale) * 1e-12:
            raise ValueError("adjusted model matrix is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row_index in range(size):
            if row_index == column:
                continue
            factor = augmented[row_index][column]
            if factor == 0:
                continue
            augmented[row_index] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row_index], augmented[column])
            ]
    return [row[size:] for row in augmented]


def adjusted_design(rows: list[dict[str, str]]) -> tuple[list[list[float]], list[str]]:
    """Build the composition-and-calendar sensitivity design matrix."""
    ordinals = [dt.date.fromisoformat(row["observation_date"]).toordinal() for row in rows]
    mean_ordinal = statistics.mean(ordinals)
    parsed_ages = [int(row["age"]) if row["age"].isdigit() else None for row in rows]
    known_ages = [age for age in parsed_ages if age is not None]
    mean_age = statistics.mean(known_ages) if known_ages else 0.0

    calendar_values = {
        "weekday": [str(dt.date.fromisoformat(row["observation_date"]).weekday()) for row in rows],
        "month_of_year": [row["observation_date"][5:7] for row in rows],
    }
    category_values = {
        field: [row[field] for row in rows]
        for field in COMPOSITION_FIELDS
    }
    names = ["intercept", "time_years", "age_decades", "age_missing"]
    specifications: list[tuple[str, list[str], str]] = []
    for field, values in {**calendar_values, **category_values}.items():
        counts = Counter(values)
        if field in calendar_values:
            levels = sorted(counts)
        else:
            levels = sorted(counts, key=lambda value: (-counts[value], value))
        if not levels:
            continue
        baseline = levels[0]
        for level in levels[1:]:
            names.append(f"{field}={level}")
            specifications.append((field, values, level))

    matrix = []
    for index, ordinal in enumerate(ordinals):
        age = parsed_ages[index]
        features = [
            1.0,
            (ordinal - mean_ordinal) / DAYS_PER_YEAR,
            0.0 if age is None else (age - mean_age) / 10,
            float(age is None),
        ]
        features.extend(float(values[index] == level) for _, values, level in specifications)
        matrix.append(features)
    return matrix, names


def fit_adjusted_trend(rows: list[dict[str, str]]) -> dict[str, object]:
    """Fit one adjusted linear-probability trend with clustered uncertainty."""
    full_matrix, full_names = adjusted_design(rows)
    selected = independent_column_indexes(full_matrix)
    if 1 not in selected:
        raise ValueError("adjusted model could not identify the time trend")
    matrix = [[row[index] for index in selected] for row in full_matrix]
    names = [full_names[index] for index in selected]
    outcomes = [float(row["endorsed"]) for row in rows]
    terms = len(names)
    cross_product = [[0.0] * terms for _ in range(terms)]
    cross_outcome = [0.0] * terms
    for features, outcome in zip(matrix, outcomes):
        for left in range(terms):
            cross_outcome[left] += features[left] * outcome
            for right in range(left, terms):
                cross_product[left][right] += features[left] * features[right]
    for left in range(terms):
        for right in range(left):
            cross_product[left][right] = cross_product[right][left]
    inverse = invert_matrix(cross_product)
    coefficients = [
        sum(inverse[row][column] * cross_outcome[column] for column in range(terms))
        for row in range(terms)
    ]
    residuals = [
        outcome - sum(coefficient * feature for coefficient, feature in zip(coefficients, features))
        for features, outcome in zip(matrix, outcomes)
    ]
    cluster_scores: dict[str, list[float]] = {}
    for source_row, features, residual in zip(rows, matrix, residuals):
        score = cluster_scores.setdefault(source_row["hashed_respondent_id"], [0.0] * terms)
        for index, feature in enumerate(features):
            score[index] += feature * residual
    clusters = len(cluster_scores)
    observations = len(rows)
    if clusters <= 1 or observations <= terms:
        raise ValueError("adjusted model lacks residual degrees of freedom or respondent clusters")
    time_index = names.index("time_years")
    inverse_time_column = [inverse[index][time_index] for index in range(terms)]
    slope_variance = sum(
        sum(weight * value for weight, value in zip(inverse_time_column, score)) ** 2
        for score in cluster_scores.values()
    )
    correction = clusters / (clusters - 1) * (observations - 1) / (observations - terms)
    slope_se = math.sqrt(max(0.0, correction * slope_variance))
    annual_change = coefficients[time_index] * 100
    annual_se = slope_se * 100
    p_value = (
        math.erfc(abs(annual_change / annual_se) / math.sqrt(2))
        if annual_se > 0
        else (0.0 if annual_change else 1.0)
    )
    return {
        "adjusted_annual_change_percentage_points": annual_change,
        "adjusted_annual_change_cluster_se": annual_se,
        "adjusted_cluster_ci95_lower": annual_change - 1.96 * annual_se,
        "adjusted_cluster_ci95_upper": annual_change + 1.96 * annual_se,
        "adjusted_cluster_p_value": p_value,
        "observations": observations,
        "respondent_clusters": clusters,
        "model_terms": terms,
        "dropped_collinear_terms": len(full_names) - terms,
    }


def adjusted_leader_sensitivity(
    path: Path, trends: list[dict[str, object]]
) -> list[dict[str, object]]:
    """Refit the two unadjusted leader tails with composition/calendar controls."""
    eligible = [row for row in trends if row["eligible"]]
    growing = sorted(
        eligible, key=lambda row: float(row["annual_change_percentage_points"]), reverse=True
    )[:LEADER_SENSITIVITY_PER_TAIL]
    shrinking = sorted(
        eligible, key=lambda row: float(row["annual_change_percentage_points"])
    )[:LEADER_SENSITIVITY_PER_TAIL]
    selections = [
        ("positive", rank, row) for rank, row in enumerate(growing, start=1)
    ] + [("negative", rank, row) for rank, row in enumerate(shrinking, start=1)]
    wanted = {str(row["signifier"]) for _, _, row in selections}
    observations: dict[str, list[dict[str, str]]] = {signifier: [] for signifier in wanted}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as source:
        for row in csv.DictReader(source):
            if row["signifier"] in observations:
                observations[row["signifier"]].append(row)

    results = []
    for tail, rank, trend in selections:
        signifier = str(trend["signifier"])
        fitted = fit_adjusted_trend(observations[signifier])
        unadjusted = float(trend["annual_change_percentage_points"])
        adjusted = float(fitted["adjusted_annual_change_percentage_points"])
        results.append(
            {
                "unadjusted_tail": tail,
                "unadjusted_tail_rank": rank,
                "signifier": signifier,
                "unadjusted_annual_change_percentage_points": unadjusted,
                "unadjusted_cluster_ci95_lower": trend["annual_change_cluster_ci95_lower"],
                "unadjusted_cluster_ci95_upper": trend["annual_change_cluster_ci95_upper"],
                **fitted,
                "adjustment_shift_percentage_points": adjusted - unadjusted,
                "same_direction": (adjusted >= 0) == (unadjusted >= 0),
            }
        )
    return results


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def svg_frame(title: str, description: str, body: str, width: int = 960, height: int = 540) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{html.escape(title)}</title>
  <desc id="desc">{html.escape(description)}</desc>
  <rect width="{width}" height="{height}" fill="#ffffff"/>
  <style>
    text {{ font-family: system-ui, -apple-system, sans-serif; fill: #243128; }}
    .title {{ font-size: 25px; font-weight: 700; }}
    .subtitle {{ font-size: 15px; fill: #4e5d51; }}
    .axis {{ stroke: #66736a; stroke-width: 1; }}
    .grid {{ stroke: #dde3d8; stroke-width: 1; }}
    .tick {{ font-size: 13px; fill: #4e5d51; }}
  </style>
{body}
</svg>
'''


def observation_growth_svg(audit: DatasetAudit) -> str:
    width, height = 960, 540
    left, right, top, bottom = 92, 35, 94, 70
    plot_w, plot_h = width - left - right, height - top - bottom
    dates = sorted(audit.daily)
    cumulative = []
    running = 0
    for date in dates:
        running += audit.daily[date]
        cumulative.append(running)
    x0, x1 = dates[0].toordinal(), dates[-1].toordinal()
    ymax = math.ceil(cumulative[-1] / 100000) * 100000

    def px(date: dt.date) -> float:
        return left + (date.toordinal() - x0) / max(1, x1 - x0) * plot_w

    def py(value: int) -> float:
        return top + plot_h - value / ymax * plot_h

    parts = [
        f'  <text class="title" x="{left}" y="38">Cumulative Ipseity Daily observations</text>',
        f'  <text class="subtitle" x="{left}" y="65">Canonical microdata through {dates[-1].isoformat()} · {cumulative[-1]:,} Yes/No responses</text>',
    ]
    for value in range(0, ymax + 1, 100000):
        y = py(value)
        parts.append(f'  <line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        parts.append(f'  <text class="tick" text-anchor="end" x="{left - 12}" y="{y + 5:.1f}">{value // 1000:,}k</text>')
    tick_indexes = sorted({round(index * (len(dates) - 1) / 4) for index in range(5)})
    for index in tick_indexes:
        x = px(dates[index])
        parts.append(f'  <line class="axis" x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 6}"/>')
        parts.append(f'  <text class="tick" text-anchor="middle" x="{x:.1f}" y="{top + plot_h + 27}">{dates[index].isoformat()}</text>')
    points = " ".join(f"{px(date):.2f},{py(value):.2f}" for date, value in zip(dates, cumulative))
    parts.extend(
        [
            f'  <line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/>',
            f'  <line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>',
            f'  <polyline points="{points}" fill="none" stroke="#4B6F44" stroke-width="4" stroke-linejoin="round"/>',
            f'  <circle cx="{px(dates[-1]):.2f}" cy="{py(cumulative[-1]):.2f}" r="5" fill="#243128"/>',
            f'  <text class="tick" transform="translate(24 {top + plot_h / 2:.1f}) rotate(-90)" text-anchor="middle">Cumulative observations</text>',
        ]
    )
    return svg_frame(
        "Cumulative Ipseity Daily observations",
        f"A line rises from {cumulative[0]:,} observations on {dates[0]} to {cumulative[-1]:,} on {dates[-1]}.",
        "\n".join(parts),
    )


def trend_histogram_svg(trends: list[dict[str, object]], latest: dt.date) -> str:
    width, height = 960, 540
    left, right, top, bottom = 92, 35, 100, 74
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [float(row["annual_change_percentage_points"]) for row in trends if row["eligible"]]
    bin_width = 2
    lower = math.floor(min(values) / bin_width) * bin_width
    upper = math.ceil(max(values) / bin_width) * bin_width
    bins = list(range(lower, upper + bin_width, bin_width))
    counts = [0] * (len(bins) - 1)
    for value in values:
        index = min(len(counts) - 1, int((value - lower) // bin_width))
        counts[index] += 1
    ymax = max(counts)

    def px(value: float) -> float:
        return left + (value - lower) / (upper - lower) * plot_w

    def py(value: int) -> float:
        return top + plot_h - value / ymax * plot_h

    parts = [
        f'  <text class="title" x="{left}" y="38">Estimated annual prevalence change across signifiers</text>',
        f'  <text class="subtitle" x="{left}" y="66">{len(values)} eligible signifiers · unweighted linear trends through {latest.isoformat()} · 2-point bins</text>',
    ]
    y_step = max(5, math.ceil(ymax / 5 / 5) * 5)
    for value in range(0, ymax + 1, y_step):
        y = py(value)
        parts.append(f'  <line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        parts.append(f'  <text class="tick" text-anchor="end" x="{left - 12}" y="{y + 5:.1f}">{value}</text>')
    for start, count in zip(bins[:-1], counts):
        x = px(start) + 1
        bar_width = px(start + bin_width) - px(start) - 2
        y = py(count)
        parts.append(f'  <rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{top + plot_h - y:.2f}" fill="#4B6F44"/>')
    first_tick = math.ceil(lower / 10) * 10
    for value in range(first_tick, upper + 1, 10):
        x = px(value)
        parts.append(f'  <line class="axis" x1="{x:.1f}" y1="{top + plot_h}" x2="{x:.1f}" y2="{top + plot_h + 6}"/>')
        parts.append(f'  <text class="tick" text-anchor="middle" x="{x:.1f}" y="{top + plot_h + 27}">{value:+d}</text>')
    if lower <= 0 <= upper:
        x = px(0)
        parts.append(f'  <line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_h}" stroke="#243128" stroke-width="2"/>')
    parts.extend(
        [
            f'  <line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/>',
            f'  <line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>',
            f'  <text class="tick" x="{left + plot_w / 2:.1f}" y="{height - 18}" text-anchor="middle">Estimated change (percentage points per year)</text>',
            f'  <text class="tick" transform="translate(24 {top + plot_h / 2:.1f}) rotate(-90)" text-anchor="middle">Signifiers</text>',
        ]
    )
    return svg_frame(
        "Estimated annual prevalence change across signifiers",
        f"Histogram of unweighted linear probability slopes for {len(values)} signifiers. Most estimates cluster near zero.",
        "\n".join(parts),
    )


def leader_sensitivity_svg(sensitivity: list[dict[str, object]]) -> str:
    """Compare unadjusted and adjusted slopes for the displayed leader set."""
    displayed = [row for row in sensitivity if int(row["unadjusted_tail_rank"]) <= 5]
    width, height = 960, 660
    left, right, top, bottom = 235, 38, 125, 66
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [
        float(row[field])
        for row in displayed
        for field in (
            "unadjusted_annual_change_percentage_points",
            "adjusted_cluster_ci95_lower",
            "adjusted_cluster_ci95_upper",
        )
    ]
    lower = math.floor(min(values) / 10) * 10
    upper = math.ceil(max(values) / 10) * 10

    def px(value: float) -> float:
        return left + (value - lower) / (upper - lower) * plot_w

    def py(index: int) -> float:
        return top + (index + 0.5) * plot_h / len(displayed)

    parts = [
        f'  <text class="title" x="{left}" y="38">Leader slopes before and after adjustment</text>',
        f'  <text class="subtitle" x="{left}" y="66">Selected unadjusted extremes · age, composition, weekday, and month sensitivity</text>',
        f'  <circle cx="{left}" cy="92" r="5" fill="#ffffff" stroke="#66736a" stroke-width="2"/>',
        f'  <text class="tick" x="{left + 12}" y="97">Unadjusted</text>',
        f'  <circle cx="{left + 112}" cy="92" r="5" fill="#4B6F44"/>',
        f'  <text class="tick" x="{left + 124}" y="97">Adjusted; line is clustered 95% interval</text>',
    ]
    for value in range(lower, upper + 1, 10):
        x = px(value)
        parts.append(
            f'  <line class="grid" x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + plot_h}"/>'
        )
        parts.append(
            f'  <text class="tick" text-anchor="middle" x="{x:.1f}" y="{top + plot_h + 26}">{value:+d}</text>'
        )
    zero_x = px(0)
    parts.append(
        f'  <line x1="{zero_x:.1f}" y1="{top}" x2="{zero_x:.1f}" y2="{top + plot_h}" stroke="#243128" stroke-width="2"/>'
    )
    for index, row in enumerate(displayed):
        y = py(index)
        unadjusted = float(row["unadjusted_annual_change_percentage_points"])
        adjusted = float(row["adjusted_annual_change_percentage_points"])
        ci_low = float(row["adjusted_cluster_ci95_lower"])
        ci_high = float(row["adjusted_cluster_ci95_upper"])
        parts.extend(
            [
                f'  <text class="tick" text-anchor="end" x="{left - 12}" y="{y + 5:.1f}">{html.escape(str(row["signifier"]))}</text>',
                f'  <line x1="{px(unadjusted):.1f}" y1="{y:.1f}" x2="{px(adjusted):.1f}" y2="{y:.1f}" stroke="#aeb9b0" stroke-width="3"/>',
                f'  <line x1="{px(ci_low):.1f}" y1="{y:.1f}" x2="{px(ci_high):.1f}" y2="{y:.1f}" stroke="#4B6F44" stroke-width="2"/>',
                f'  <circle cx="{px(unadjusted):.1f}" cy="{y:.1f}" r="5" fill="#ffffff" stroke="#66736a" stroke-width="2"/>',
                f'  <circle cx="{px(adjusted):.1f}" cy="{y:.1f}" r="5" fill="#4B6F44"/>',
            ]
        )
    parts.append(
        f'  <text class="tick" text-anchor="middle" x="{left + plot_w / 2:.1f}" y="{height - 16}">Estimated change (percentage points per year)</text>'
    )
    return svg_frame(
        "Leader slopes before and after adjustment",
        "Dumbbell plot comparing unadjusted and composition-and-calendar-adjusted annual prevalence slopes for the five most positive and five most negative unadjusted leaders. Adjusted estimates include clustered 95 percent intervals.",
        "\n".join(parts),
        width,
        height,
    )


def compact_trend(row: dict[str, object]) -> dict[str, object]:
    return {
        "signifier": row["signifier"],
        "annual_change_percentage_points": round(float(row["annual_change_percentage_points"]), 3),
        "cluster_ci95_lower": round(float(row["annual_change_cluster_ci95_lower"]), 3),
        "cluster_ci95_upper": round(float(row["annual_change_cluster_ci95_upper"]), 3),
        "benjamini_hochberg_q_value": round(float(row["benjamini_hochberg_q_value"]), 6),
        "bonferroni_adjusted_p_value": round(float(row["bonferroni_adjusted_p_value"]), 6),
        "observations": row["observations"],
        "respondent_clusters": row["respondent_clusters"],
        "prevalence_percent": round(float(row["prevalence_percent"]), 3),
    }


def compact_sensitivity(row: dict[str, object]) -> dict[str, object]:
    return {
        "unadjusted_tail": row["unadjusted_tail"],
        "unadjusted_tail_rank": row["unadjusted_tail_rank"],
        "signifier": row["signifier"],
        "unadjusted_annual_change_percentage_points": round(
            float(row["unadjusted_annual_change_percentage_points"]), 3
        ),
        "adjusted_annual_change_percentage_points": round(
            float(row["adjusted_annual_change_percentage_points"]), 3
        ),
        "adjusted_cluster_ci95_lower": round(float(row["adjusted_cluster_ci95_lower"]), 3),
        "adjusted_cluster_ci95_upper": round(float(row["adjusted_cluster_ci95_upper"]), 3),
        "adjustment_shift_percentage_points": round(
            float(row["adjustment_shift_percentage_points"]), 3
        ),
        "same_direction": row["same_direction"],
        "observations": row["observations"],
        "respondent_clusters": row["respondent_clusters"],
        "model_terms": row["model_terms"],
        "dropped_collinear_terms": row["dropped_collinear_terms"],
    }


def findings_markdown(
    audit: DatasetAudit,
    checked_at: dt.datetime,
    trends: list[dict[str, object]],
    sensitivity: list[dict[str, object]],
) -> str:
    eligible = [row for row in trends if row["eligible"]]
    estimates = sorted(float(row["annual_change_percentage_points"]) for row in eligible)
    quartiles = statistics.quantiles(estimates, n=4, method="inclusive")
    growing = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]), reverse=True)[:5]
    shrinking = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]))[:5]
    fdr_discoveries = sum(bool(row["fdr_05"]) for row in eligible)
    bonferroni_discoveries = sum(bool(row["bonferroni_05"]) for row in eligible)
    respondent_signifier_clusters = sum(len(stats.respondent_sums) for stats in audit.signifiers.values())
    max_cluster_size = max(
        cluster[0]
        for stats in audit.signifiers.values()
        for cluster in stats.respondent_sums.values()
    )
    same_direction = sum(bool(row["same_direction"]) for row in sensitivity)
    median_absolute_shift = statistics.median(
        abs(float(row["adjustment_shift_percentage_points"])) for row in sensitivity
    )
    largest_shift = max(
        sensitivity, key=lambda row: abs(float(row["adjustment_shift_percentage_points"]))
    )

    def probability(value: object) -> str:
        numeric = float(value)
        return "<0.001" if numeric < 0.001 else f"{numeric:.3f}"

    def table(rows: list[dict[str, object]]) -> str:
        lines = [
            "| Signifier | Annual change (pp) | Clustered 95% CI | BH q | Bonferroni p | Responses |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            lines.append(
                f"| {str(row['signifier']).replace('|', '&#124;')} | "
                f"{float(row['annual_change_percentage_points']):+.1f} | "
                f"[{float(row['annual_change_cluster_ci95_lower']):+.1f}, {float(row['annual_change_cluster_ci95_upper']):+.1f}] | "
                f"{probability(row['benjamini_hochberg_q_value'])} | "
                f"{probability(row['bonferroni_adjusted_p_value'])} | "
                f"{int(row['observations']):,} |"
            )
        return "\n".join(lines)

    def sensitivity_table(rows: list[dict[str, object]]) -> str:
        displayed = [
            row
            for row in rows
            if int(row["unadjusted_tail_rank"]) <= 5
        ]
        lines = [
            "| Signifier | Unadjusted (pp/year) | Adjusted (pp/year) | Adjusted clustered 95% CI |",
            "|---|---:|---:|---:|",
        ]
        for row in displayed:
            lines.append(
                f"| {str(row['signifier']).replace('|', '&#124;')} | "
                f"{float(row['unadjusted_annual_change_percentage_points']):+.1f} | "
                f"{float(row['adjusted_annual_change_percentage_points']):+.1f} | "
                f"[{float(row['adjusted_cluster_ci95_lower']):+.1f}, "
                f"{float(row['adjusted_cluster_ci95_upper']):+.1f}] |"
            )
        return "\n".join(lines)

    return f"""# Current monitoring and prevalence findings

Current through the monitoring check at **{iso_z(checked_at)}**. This file is
replaced when the analysis is refreshed; it is not an archive.

## Monitor

The Ipseity Daily homepage and canonical microdata both returned HTTP 200. The
gzip parsed as UTF-8 CSV with the documented schema and contained
**{audit.rows:,} observations** from **{audit.earliest}** through
**{audit.latest}**, spanning **{len(audit.respondents):,} hashed respondents**
and **{len(audit.signifiers):,} signifiers**. No malformed rows or duplicate
respondent/date/signifier keys were detected. The newest observation was
{(checked_at.date() - audit.latest).days} day behind the check date, and this
check records no anomaly.

![Cumulative observations over time](outputs/observation-growth.svg)

The cumulative series is derived from observation dates inside the current
microdata, while `data/monitoring-history.csv` preserves the separate sequence
of outside-in checks for longitudinal monitoring.

## Estimated signifier prevalence change

For each signifier, an unweighted linear probability model regresses its binary
endorsement response on observation date. The slope is annualized to percentage
points per year. The histogram includes **{len(eligible)} of
{len(trends)} signifiers** with at least {MIN_TREND_OBSERVATIONS} responses,
{MIN_TREND_DATES} distinct observation dates, and a {MIN_TREND_SPAN_DAYS}-day
span. These are descriptive sample trends, not population-weighted or causal
estimates. The median estimate is **{statistics.median(estimates):+.1f}
percentage points per year**; the middle half runs from {quartiles[0]:+.1f} to
{quartiles[2]:+.1f} points.

![Histogram of estimated annual prevalence growth](outputs/annual-prevalence-growth-histogram.svg)

Uncertainty now uses a respondent-clustered sandwich estimator, so repeat
answers by the same hashed respondent are not treated as independent. The file
contains **{respondent_signifier_clusters:,} respondent–signifier clusters**;
the largest has {max_cluster_size} responses. Across {len(eligible)} eligible
trend tests, **{fdr_discoveries}** have Benjamini–Hochberg q-values at or below
0.05, and **{bonferroni_discoveries}** meet the more conservative Bonferroni
0.05 threshold.

### Fastest estimated growth

{table(growing)}

### Fastest estimated shrinkage

{table(shrinking)}

The largest point estimate is **{growing[0]['signifier']}** at
{float(growing[0]['annual_change_percentage_points']):.1f} percentage points
per year; the most negative is **{shrinking[0]['signifier']}** at
{float(shrinking[0]['annual_change_percentage_points']):.1f} points per year.
The intervals account for dependence within hashed respondents but not changing
sample composition, calendar structure, or model misspecification. The
Benjamini–Hochberg screen follows the original independent-test procedure;
correlation among signifier tests makes the Bonferroni column an important
conservative sensitivity check. Point-estimate rankings selected from
{len(eligible)} tests remain monitoring leads, not evidence that the underlying
US adult population changed at those rates.

## Composition and calendar sensitivity

As a targeted robustness check, the ten most positive and ten most negative
unadjusted slopes were refit with respondent-clustered uncertainty after
adjusting for linear age, missing age, demographics availability, sex,
ethnicity, student status, employment, weekday, and month of year. **{same_direction}
of {len(sensitivity)}** leaders retained their original direction. The median
absolute slope shift was **{median_absolute_shift:.1f} percentage points per
year**. The largest shift was for **{largest_shift['signifier']}**, from
{float(largest_shift['unadjusted_annual_change_percentage_points']):+.1f} to
{float(largest_shift['adjusted_annual_change_percentage_points']):+.1f} points.

![Unadjusted and adjusted leader slopes](outputs/leader-adjustment-sensitivity.svg)

{sensitivity_table(sensitivity)}

This selected-leader sensitivity is diagnostic, not a new discovery screen.
It cannot correct unobserved composition, nonrepresentative recruitment,
functional-form error, or selection of extremes from the full set of tests.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; adjusted leader checks are in
`outputs/leader-adjusted-sensitivity.csv`; the daily and cumulative counts are
in `outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page]({MAIN_URL}download.html) at the check time;
SHA-256 `{audit.sha256}`.

Liang, K.-Y., & Zeger, S. L. (1986). Longitudinal data analysis using
generalized linear models. *Biometrika, 73*(1), 13–22.
[https://doi.org/10.1093/biomet/73.1.13](https://doi.org/10.1093/biomet/73.1.13).

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate: A
practical and powerful approach to multiple testing. *Journal of the Royal
Statistical Society: Series B (Methodological), 57*(1), 289–300.
[https://doi.org/10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
"""


def read_history(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != HISTORY_FIELDS:
            raise ValueError(f"monitoring history schema mismatch in {path}")
        return list(reader)


def anomaly_text(
    audit: DatasetAudit | None,
    main_ok: bool,
    dataset_ok: bool,
    retrieval_errors: list[str],
    previous: dict[str, str] | None,
) -> str:
    anomalies = list(retrieval_errors)
    if not main_ok:
        anomalies.append("main site unreachable")
    if not dataset_ok:
        anomalies.append("canonical dataset retrieval failed")
    if audit is not None:
        anomalies.extend(audit.errors)
        if audit.latest is not None:
            lag = (audit.checked_at.date() - audit.latest).days
            if lag > 4:
                anomalies.append(f"newest observation is {lag} days behind check date")
        if previous and audit.parsed_successfully:
            old_rows = previous.get("observations", "")
            old_latest = previous.get("most_recent_observation_date", "")
            if old_rows and audit.rows < int(old_rows):
                anomalies.append(f"observation count decreased from {old_rows} to {audit.rows}")
            if old_latest and audit.latest and audit.latest < dt.date.fromisoformat(old_latest):
                anomalies.append(f"latest observation date regressed from {old_latest} to {audit.latest}")
    return "; ".join(dict.fromkeys(anomalies)) if anomalies else "none"


def history_row(
    checked_at: dt.datetime,
    main_status: int | None,
    dataset_status: int | None,
    audit: DatasetAudit | None,
    anomaly: str,
) -> dict[str, object]:
    main_ok = main_status is not None and 200 <= main_status < 400
    dataset_ok = dataset_status is not None and 200 <= dataset_status < 400 and audit is not None
    parsed = audit is not None and audit.parsed_successfully
    lag = (checked_at.date() - audit.latest).days if audit and audit.latest else ""
    return {
        "checked_at_utc": iso_z(checked_at),
        "main_url": MAIN_URL,
        "main_http_status": "" if main_status is None else main_status,
        "main_site_reachable": str(main_ok).lower(),
        "canonical_url": DATASET_URL,
        "canonical_http_status": "" if dataset_status is None else dataset_status,
        "canonical_dataset_retrieved": str(dataset_ok).lower(),
        "parsed_successfully": str(parsed).lower(),
        "observations": audit.rows if audit else "",
        "earliest_observation_date": audit.earliest.isoformat() if audit and audit.earliest else "",
        "most_recent_observation_date": audit.latest.isoformat() if audit and audit.latest else "",
        "data_lag_days": lag,
        "unique_respondents": len(audit.respondents) if audit else "",
        "signifiers": len(audit.signifiers) if audit else "",
        "duplicate_keys": audit.duplicate_keys if audit else "",
        "validation_error_count": len(audit.errors) if audit else "",
        "dataset_bytes": audit.byte_count if audit else "",
        "dataset_sha256": audit.sha256 if audit else "",
        "anomaly": anomaly,
    }


def append_history(path: Path, row: dict[str, object], existing: list[dict[str, str]]) -> None:
    timestamp = str(row["checked_at_utc"])
    if any(old["checked_at_utc"] == timestamp for old in existing):
        raise ValueError(f"refusing duplicate monitoring timestamp {timestamp}")
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if path.exists() else "w"
    with path.open(mode, encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=HISTORY_FIELDS, lineterminator="\n")
        if mode == "w":
            writer.writeheader()
        writer.writerow(row)


def write_outputs(audit: DatasetAudit, checked_at: dt.datetime, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    daily_rows = []
    running = 0
    for date in sorted(audit.daily):
        running += audit.daily[date]
        daily_rows.append(
            {"observation_date": date.isoformat(), "daily_observations": audit.daily[date], "cumulative_observations": running}
        )
    write_csv(
        output_dir / "daily-observation-growth.csv",
        ["observation_date", "daily_observations", "cumulative_observations"],
        daily_rows,
    )
    trends = [trend_row(signifier, stats) for signifier, stats in sorted(audit.signifiers.items())]
    add_robust_inference(trends, audit.signifiers)
    write_csv(
        output_dir / "signifier-growth.csv",
        list(trends[0]),
        trends,
    )
    sensitivity = adjusted_leader_sensitivity(audit.path, trends)
    write_csv(
        output_dir / "leader-adjusted-sensitivity.csv",
        list(sensitivity[0]),
        sensitivity,
    )
    (output_dir / "leader-adjustment-sensitivity.svg").write_text(
        leader_sensitivity_svg(sensitivity), encoding="utf-8"
    )
    (output_dir / "observation-growth.svg").write_text(observation_growth_svg(audit), encoding="utf-8")
    (output_dir / "annual-prevalence-growth-histogram.svg").write_text(
        trend_histogram_svg(trends, audit.latest), encoding="utf-8"
    )
    eligible = [row for row in trends if row["eligible"]]
    growing = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]), reverse=True)[:10]
    shrinking = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]))[:10]
    summary = {
        "checked_at_utc": iso_z(checked_at),
        "source": {"url": DATASET_URL, "bytes": audit.byte_count, "sha256": audit.sha256},
        "validation": {
            "parsed_successfully": audit.parsed_successfully,
            "duplicate_keys": audit.duplicate_keys,
            "errors": audit.errors,
        },
        "dataset": {
            "observations": audit.rows,
            "earliest_observation_date": audit.earliest.isoformat(),
            "latest_observation_date": audit.latest.isoformat(),
            "unique_respondents": len(audit.respondents),
            "signifiers": len(audit.signifiers),
        },
        "trend_method": {
            "model": "unweighted OLS linear probability model: endorsed ~ observation_date",
            "uncertainty": "CR1 sandwich standard errors clustered by hashed respondent",
            "multiplicity": "Benjamini-Hochberg and Bonferroni adjustments across eligible signifiers",
            "annualization_days": DAYS_PER_YEAR,
            "minimum_observations": MIN_TREND_OBSERVATIONS,
            "minimum_span_days": MIN_TREND_SPAN_DAYS,
            "minimum_distinct_dates": MIN_TREND_DATES,
            "eligible_signifiers": len(eligible),
            "respondent_signifier_clusters": sum(
                len(stats.respondent_sums) for stats in audit.signifiers.values()
            ),
            "fdr_05_discoveries": sum(bool(row["fdr_05"]) for row in eligible),
            "bonferroni_05_discoveries": sum(bool(row["bonferroni_05"]) for row in eligible),
        },
        "fastest_growing": [compact_trend(row) for row in growing],
        "fastest_shrinking": [compact_trend(row) for row in shrinking],
        "leader_sensitivity": {
            "selection": (
                f"top {LEADER_SENSITIVITY_PER_TAIL} positive and top "
                f"{LEADER_SENSITIVITY_PER_TAIL} negative unadjusted slopes"
            ),
            "model": (
                "unweighted OLS linear probability trend adjusted for linear age, missing age, "
                "demographics status, sex, ethnicity, student status, employment, weekday, "
                "and month of year"
            ),
            "uncertainty": "CR1 sandwich standard errors clustered by hashed respondent",
            "selected_signifiers": len(sensitivity),
            "same_direction": sum(bool(row["same_direction"]) for row in sensitivity),
            "median_absolute_slope_shift_percentage_points": round(
                statistics.median(
                    abs(float(row["adjustment_shift_percentage_points"]))
                    for row in sensitivity
                ),
                3,
            ),
            "results": [compact_sensitivity(row) for row in sensitivity],
        },
    }
    (output_dir / "current-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (PROJECT / "CURRENT-FINDINGS.md").write_text(
        findings_markdown(audit, checked_at, trends, sensitivity), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="already downloaded canonical .csv.gz")
    parser.add_argument("--checked-at", help="UTC ISO timestamp; defaults to current time")
    parser.add_argument("--main-http-status", type=int, help="status observed when --input was retrieved")
    parser.add_argument("--dataset-http-status", type=int, help="status observed when --input was retrieved")
    parser.add_argument("--history", type=Path, default=PROJECT / "data/monitoring-history.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT / "outputs")
    parser.add_argument("--no-history", action="store_true", help="validate and render without appending history")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        checked_at = utc_timestamp(args.checked_at)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    retrieval_errors: list[str] = []
    temporary: tempfile.NamedTemporaryFile | None = None
    if args.input:
        if args.main_http_status is None or args.dataset_http_status is None:
            raise SystemExit("--input requires --main-http-status and --dataset-http-status")
        dataset_path = args.input
        main_status = args.main_http_status
        dataset_status = args.dataset_http_status
    else:
        main_status, main_error = retrieve(MAIN_URL)
        if main_error:
            retrieval_errors.append(f"main retrieval: {main_error}")
        temporary = tempfile.NamedTemporaryFile(prefix="ipseity-", suffix=".csv.gz", delete=False)
        temporary.close()
        dataset_path = Path(temporary.name)
        dataset_status, dataset_error = retrieve(DATASET_URL, dataset_path)
        if dataset_error:
            retrieval_errors.append(f"dataset retrieval: {dataset_error}")

    main_ok = main_status is not None and 200 <= main_status < 400
    dataset_ok = dataset_status is not None and 200 <= dataset_status < 400 and dataset_path.is_file()
    audit = audit_dataset(dataset_path, checked_at) if dataset_ok else None
    existing = read_history(args.history)
    previous = existing[-1] if existing else None
    anomaly = anomaly_text(audit, main_ok, dataset_ok, retrieval_errors, previous)
    row = history_row(checked_at, main_status, dataset_status, audit, anomaly)
    if not args.no_history:
        append_history(args.history, row, existing)
    if audit is not None and audit.parsed_successfully:
        write_outputs(audit, checked_at, args.output_dir)
    if temporary is not None:
        dataset_path.unlink(missing_ok=True)

    print(json.dumps(row, indent=2))
    if anomaly != "none":
        print(f"ALERT: {anomaly}")
        return 1
    print("PASS: site reachable, canonical dataset retrieved and validated, outputs refreshed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
