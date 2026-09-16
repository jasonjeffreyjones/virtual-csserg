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
DAYS_PER_YEAR = 365.2425
TREND_EPOCH_ORDINAL = dt.date(2020, 1, 1).toordinal()


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

    def add(self, date: dt.date, endorsed: int) -> None:
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
                audit.signifiers.setdefault(signifier, SignifierStats()).add(observation_date, endorsed)
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
        "eligible": eligible,
        "exclusion_reason": "; ".join(reasons),
        "annual_change_percentage_points": annual_pp if eligible else None,
        "annual_change_ci95_lower": ci_low if eligible else None,
        "annual_change_ci95_upper": ci_high if eligible else None,
    }


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


def compact_trend(row: dict[str, object]) -> dict[str, object]:
    return {
        "signifier": row["signifier"],
        "annual_change_percentage_points": round(float(row["annual_change_percentage_points"]), 3),
        "ci95_lower": round(float(row["annual_change_ci95_lower"]), 3),
        "ci95_upper": round(float(row["annual_change_ci95_upper"]), 3),
        "observations": row["observations"],
        "prevalence_percent": round(float(row["prevalence_percent"]), 3),
    }


def findings_markdown(audit: DatasetAudit, checked_at: dt.datetime, trends: list[dict[str, object]]) -> str:
    eligible = [row for row in trends if row["eligible"]]
    estimates = sorted(float(row["annual_change_percentage_points"]) for row in eligible)
    quartiles = statistics.quantiles(estimates, n=4, method="inclusive")
    growing = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]), reverse=True)[:5]
    shrinking = sorted(eligible, key=lambda row: float(row["annual_change_percentage_points"]))[:5]

    def table(rows: list[dict[str, object]]) -> str:
        lines = [
            "| Signifier | Annual change (pp) | Approx. 95% CI | Responses | Overall yes |",
            "|---|---:|---:|---:|---:|",
        ]
        for row in rows:
            lines.append(
                f"| {str(row['signifier']).replace('|', '&#124;')} | "
                f"{float(row['annual_change_percentage_points']):+.1f} | "
                f"[{float(row['annual_change_ci95_lower']):+.1f}, {float(row['annual_change_ci95_upper']):+.1f}] | "
                f"{int(row['observations']):,} | {float(row['prevalence_percent']):.1f}% |"
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
{(checked_at.date() - audit.latest).days} day behind the check date, so this
first check records no anomaly.

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

### Fastest estimated growth

{table(growing)}

### Fastest estimated shrinkage

{table(shrinking)}

The largest point estimate is **{growing[0]['signifier']}** at
{float(growing[0]['annual_change_percentage_points']):.1f} percentage points
per year; the most negative is **{shrinking[0]['signifier']}** at
{float(shrinking[0]['annual_change_percentage_points']):.1f} points per year.
The intervals are ordinary model-based intervals. They do not adjust for
repeated respondents, changing sample composition, or selecting extremes from
{len(eligible)} simultaneous estimates. The rankings are therefore leads for
continued monitoring, not evidence that the underlying US adult population
changed at those rates.

Full machine-readable estimates, eligibility flags, and interval bounds are in
`outputs/signifier-growth.csv`; the daily and cumulative counts are in
`outputs/daily-observation-growth.csv`.

## Source

Jones, J. (2026). *Ipseity Daily Data* [Data set]. Zenodo.
[https://doi.org/10.5281/zenodo.22636514](https://doi.org/10.5281/zenodo.22636514).
The analysis used the newer canonical file served directly by the
[Ipseity Daily download page]({MAIN_URL}download.html) at the check time;
SHA-256 `{audit.sha256}`.
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
    write_csv(
        output_dir / "signifier-growth.csv",
        list(trends[0]),
        trends,
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
            "annualization_days": DAYS_PER_YEAR,
            "minimum_observations": MIN_TREND_OBSERVATIONS,
            "minimum_span_days": MIN_TREND_SPAN_DAYS,
            "minimum_distinct_dates": MIN_TREND_DATES,
            "eligible_signifiers": len(eligible),
        },
        "fastest_growing": [compact_trend(row) for row in growing],
        "fastest_shrinking": [compact_trend(row) for row in shrinking],
    }
    (output_dir / "current-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (PROJECT / "CURRENT-FINDINGS.md").write_text(findings_markdown(audit, checked_at, trends), encoding="utf-8")


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
