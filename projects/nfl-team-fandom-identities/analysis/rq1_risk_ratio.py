#!/usr/bin/env python3
"""Estimate the RQ1 happy prevalence ratio from Ipseity Daily microdata.

The unit of analysis is a respondent-day. A respondent-day enters the risk set
only when the respondent explicitly answered both the fandom and outcome items.
Responses are inner-joined to demographics on (hashed_respondent_id, obs_date)
without retaining or reporting demographic attributes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import NormalDist
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple


Key = Tuple[str, str]
Record = Tuple[str, str, bool, bool]
CellCounts = Tuple[int, int, int, int]


class AnalysisError(ValueError):
    """Raised when input data cannot support a trustworthy analysis."""


def require_columns(fieldnames: Optional[Sequence[str]], required: Iterable[str], source: Path) -> None:
    if fieldnames is None:
        raise AnalysisError(f"{source} is empty or has no CSV header")
    missing = sorted(set(required) - set(fieldnames))
    if missing:
        found = ", ".join(fieldnames)
        raise AnalysisError(
            f"{source} is missing required column(s): {', '.join(missing)}. "
            f"Found: {found}"
        )


def nonempty_key(row: Mapping[str, str], id_column: str, date_column: str, source: Path, row_number: int) -> Key:
    respondent_id = (row.get(id_column) or "").strip()
    obs_date = (row.get(date_column) or "").strip()
    if not respondent_id or not obs_date:
        raise AnalysisError(
            f"{source} row {row_number} has a blank {id_column!r} or {date_column!r}"
        )
    return respondent_id, obs_date


def read_demographic_keys(
    path: Path,
    id_column: str,
    date_column: str,
) -> Tuple[Set[Key], int, int, int]:
    keys: Set[Key] = set()
    all_keys: Set[Key] = set()
    row_count = 0
    consent_revoked_rows = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader.fieldnames, (id_column, date_column), path)
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            key = nonempty_key(row, id_column, date_column, path, row_number)
            if key in all_keys:
                raise AnalysisError(
                    f"{path} has duplicate join key {key!r} at row {row_number}; "
                    "an inner join would duplicate response rows"
                )
            all_keys.add(key)
            if any(
                (value or "").strip().casefold() == "consent_revoked"
                for value in row.values()
            ):
                consent_revoked_rows += 1
                continue
            keys.add(key)
    return keys, row_count, len(all_keys), consent_revoked_rows


def normalize_binary(value: str, source: Path, row_number: int, column: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"1", "yes"}:
        return True
    if normalized in {"0", "no"}:
        return False
    raise AnalysisError(
        f"{source} row {row_number} has unexpected {column!r} value {value!r}; "
        "expected 1/0 or Yes/No"
    )


def load_records(
    responses_path: Path,
    demographics_path: Path,
    fandom_signifier: str,
    outcome_signifier: str,
    id_column: str = "hashed_respondent_id",
    date_column: str = "obs_date",
    signifier_column: str = "signifier",
    response_column: str = "response",
) -> Tuple[List[Record], Dict[str, object]]:
    (
        demographic_keys,
        demographic_rows,
        unique_demographic_keys,
        consent_revoked_rows,
    ) = read_demographic_keys(demographics_path, id_column, date_column)

    answers_by_key: MutableMapping[Key, Dict[str, bool]] = defaultdict(dict)
    response_keys: Set[Key] = set()
    joined_response_keys: Set[Key] = set()
    response_rows = 0
    joined_response_rows = 0
    unmatched_response_rows = 0
    relevant_joined_rows = 0
    identical_duplicate_rows = 0
    conflicting_relevant_rows = 0
    conflicting_keys: Set[Key] = set()
    relevant = {fandom_signifier, outcome_signifier}

    with responses_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        require_columns(
            reader.fieldnames,
            (id_column, date_column, signifier_column, response_column),
            responses_path,
        )
        for row_number, row in enumerate(reader, start=2):
            response_rows += 1
            key = nonempty_key(row, id_column, date_column, responses_path, row_number)
            response_keys.add(key)
            if key not in demographic_keys:
                unmatched_response_rows += 1
                continue
            joined_response_keys.add(key)
            joined_response_rows += 1
            signifier = (row.get(signifier_column) or "").strip()
            if signifier not in relevant:
                continue
            relevant_joined_rows += 1
            answer = normalize_binary(
                row.get(response_column) or "", responses_path, row_number, response_column
            )
            previous = answers_by_key[key].get(signifier)
            if previous is not None:
                if previous != answer:
                    conflicting_relevant_rows += 1
                    conflicting_keys.add(key)
                else:
                    identical_duplicate_rows += 1
                continue
            answers_by_key[key][signifier] = answer

    records: List[Record] = []
    for (respondent_id, obs_date), answers in answers_by_key.items():
        if (
            (respondent_id, obs_date) not in conflicting_keys
            and fandom_signifier in answers
            and outcome_signifier in answers
        ):
            records.append(
                (
                    respondent_id,
                    obs_date,
                    answers[fandom_signifier],
                    answers[outcome_signifier],
                )
            )

    if not records:
        raise AnalysisError(
            "No respondent-days explicitly answered both target signifiers after the demographics join"
        )

    records.sort(key=lambda record: (record[1], record[0]))
    unique_respondents = {record[0] for record in records}
    respondent_day_counts: Dict[str, int] = defaultdict(int)
    for respondent_id, _obs_date, _fandom, _outcome in records:
        respondent_day_counts[respondent_id] += 1

    audit: Dict[str, object] = {
        "demographic_rows": demographic_rows,
        "unique_demographic_join_keys": unique_demographic_keys,
        "consent_revoked_demographic_rows_excluded": consent_revoked_rows,
        "analysis_eligible_demographic_join_keys": len(demographic_keys),
        "response_rows": response_rows,
        "unique_response_join_keys": len(response_keys),
        "joined_response_keys": len(joined_response_keys),
        "joined_response_rows": joined_response_rows,
        "unmatched_response_rows_excluded": unmatched_response_rows,
        "demographic_join_keys_without_responses": len(
            demographic_keys - response_keys
        ),
        "relevant_joined_response_rows": relevant_joined_rows,
        "identical_duplicate_relevant_rows_collapsed": identical_duplicate_rows,
        "conflicting_relevant_rows": conflicting_relevant_rows,
        "conflicting_target_respondent_days_excluded": len(conflicting_keys),
        "eligible_respondent_days": len(records),
        "eligible_unique_respondents": len(unique_respondents),
        "eligible_repeated_respondents": sum(
            count > 1 for count in respondent_day_counts.values()
        ),
        "maximum_eligible_days_per_respondent": max(respondent_day_counts.values()),
        "earliest_eligible_obs_date": min(record[1] for record in records),
        "latest_eligible_obs_date": max(record[1] for record in records),
    }
    return records, audit


def cell_counts(records: Iterable[Record]) -> CellCounts:
    # a: exposed/outcome yes; b: exposed/outcome no;
    # c: reference/outcome yes; d: reference/outcome no.
    a = b = c = d = 0
    for _respondent_id, _obs_date, fandom_yes, outcome_yes in records:
        if fandom_yes and outcome_yes:
            a += 1
        elif fandom_yes and not outcome_yes:
            b += 1
        elif not fandom_yes and outcome_yes:
            c += 1
        else:
            d += 1
    return a, b, c, d


def quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise AnalysisError("Cannot calculate a quantile from no values")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def bootstrap_clustered(
    records: Sequence[Record], reps: int, seed: int, ci_level: float
) -> Optional[Dict[str, object]]:
    if reps == 0:
        return None

    counts_by_respondent: MutableMapping[str, List[int]] = defaultdict(
        lambda: [0, 0, 0, 0]
    )
    for respondent_id, _obs_date, fandom_yes, outcome_yes in records:
        if fandom_yes and outcome_yes:
            cell = 0
        elif fandom_yes and not outcome_yes:
            cell = 1
        elif not fandom_yes and outcome_yes:
            cell = 2
        else:
            cell = 3
        counts_by_respondent[respondent_id][cell] += 1

    clusters = list(counts_by_respondent.values())
    rng = random.Random(seed)
    prevalence_ratio_values: List[float] = []
    prevalence_difference_values: List[float] = []
    for _ in range(reps):
        a = b = c = d = 0
        for _draw in range(len(clusters)):
            draw = clusters[rng.randrange(len(clusters))]
            a += draw[0]
            b += draw[1]
            c += draw[2]
            d += draw[3]
        exposed_n = a + b
        reference_n = c + d
        if not exposed_n or not reference_n:
            continue
        exposed_prevalence = a / exposed_n
        reference_prevalence = c / reference_n
        prevalence_difference_values.append(exposed_prevalence - reference_prevalence)
        if reference_prevalence > 0:
            prevalence_ratio_values.append(exposed_prevalence / reference_prevalence)

    alpha = 1 - ci_level
    lower_probability = alpha / 2
    upper_probability = 1 - alpha / 2
    return {
        "method": "respondent-cluster percentile bootstrap",
        "requested_replicates": reps,
        "prevalence_ratio_successful_replicates": len(prevalence_ratio_values),
        "prevalence_difference_successful_replicates": len(
            prevalence_difference_values
        ),
        "seed": seed,
        "ci_level": ci_level,
        "prevalence_ratio_ci": (
            [
                quantile(prevalence_ratio_values, lower_probability),
                quantile(prevalence_ratio_values, upper_probability),
            ]
            if prevalence_ratio_values
            else None
        ),
        "prevalence_difference_ci": (
            [
                quantile(prevalence_difference_values, lower_probability),
                quantile(prevalence_difference_values, upper_probability),
            ]
            if prevalence_difference_values
            else None
        ),
    }


def descriptive_estimate(records: Iterable[Record]) -> Dict[str, object]:
    a, b, c, d = cell_counts(records)
    exposed_n = a + b
    reference_n = c + d
    exposed_prevalence = a / exposed_n if exposed_n else None
    reference_prevalence = c / reference_n if reference_n else None
    prevalence_ratio = None
    prevalence_difference = None
    if exposed_prevalence is not None and reference_prevalence is not None:
        prevalence_difference = exposed_prevalence - reference_prevalence
        if reference_prevalence > 0:
            prevalence_ratio = exposed_prevalence / reference_prevalence
    return {
        "eligible_respondent_days": exposed_n + reference_n,
        "fandom_yes_n": exposed_n,
        "fandom_no_n": reference_n,
        "happy_prevalence_fandom_yes": exposed_prevalence,
        "happy_prevalence_fandom_no": reference_prevalence,
        "prevalence_ratio": prevalence_ratio,
        "prevalence_difference": prevalence_difference,
    }


def temporal_sensitivity(records: Sequence[Record]) -> Dict[str, object]:
    by_date: MutableMapping[str, List[Record]] = defaultdict(list)
    by_month: MutableMapping[str, List[Record]] = defaultdict(list)
    for record in records:
        by_date[record[1]].append(record)
        by_month[record[1][:7]].append(record)
    eligible_per_date = [len(date_records) for date_records in by_date.values()]
    return {
        "eligible_dates": len(by_date),
        "minimum_eligible_respondent_days_per_date": min(eligible_per_date),
        "median_eligible_respondent_days_per_date": quantile(
            [float(value) for value in eligible_per_date], 0.5
        ),
        "maximum_eligible_respondent_days_per_date": max(eligible_per_date),
        "dates_with_both_fandom_groups": sum(
            descriptive_estimate(date_records)["fandom_yes_n"] > 0
            and descriptive_estimate(date_records)["fandom_no_n"] > 0
            for date_records in by_date.values()
        ),
        "by_month": [
            {"month": month, **descriptive_estimate(by_month[month])}
            for month in sorted(by_month)
        ],
    }


def estimate(records: Sequence[Record], ci_level: float, bootstrap_reps: int, seed: int) -> Dict[str, object]:
    a, b, c, d = cell_counts(records)
    exposed_n = a + b
    reference_n = c + d
    if not exposed_n or not reference_n:
        raise AnalysisError(
            "Both Cleveland Browns fan Yes and explicit No groups must contain eligible respondent-days"
        )

    exposed_prevalence = a / exposed_n
    reference_prevalence = c / reference_n
    prevalence_ratio = (
        exposed_prevalence / reference_prevalence
        if reference_prevalence > 0
        else math.inf
    )
    prevalence_difference = exposed_prevalence - reference_prevalence
    z = NormalDist().inv_cdf(0.5 + ci_level / 2)

    prevalence_ratio_ci = None
    if a > 0 and c > 0 and math.isfinite(prevalence_ratio):
        log_standard_error = math.sqrt(
            (1 / a) - (1 / exposed_n) + (1 / c) - (1 / reference_n)
        )
        prevalence_ratio_ci = [
            math.exp(math.log(prevalence_ratio) - z * log_standard_error),
            math.exp(math.log(prevalence_ratio) + z * log_standard_error),
        ]

    difference_standard_error = math.sqrt(
        exposed_prevalence * (1 - exposed_prevalence) / exposed_n
        + reference_prevalence * (1 - reference_prevalence) / reference_n
    )
    prevalence_difference_ci = [
        prevalence_difference - z * difference_standard_error,
        prevalence_difference + z * difference_standard_error,
    ]

    return {
        "two_by_two": {
            "fandom_yes_happy_yes": a,
            "fandom_yes_happy_no": b,
            "fandom_no_happy_yes": c,
            "fandom_no_happy_no": d,
        },
        "fandom_yes_n": exposed_n,
        "fandom_no_n": reference_n,
        "happy_prevalence_fandom_yes": exposed_prevalence,
        "happy_prevalence_fandom_no": reference_prevalence,
        "prevalence_ratio": (
            prevalence_ratio if math.isfinite(prevalence_ratio) else None
        ),
        "prevalence_ratio_ci": prevalence_ratio_ci,
        "prevalence_ratio_ci_method": "Katz log interval (respondent-days treated as independent)",
        "prevalence_difference": prevalence_difference,
        "prevalence_difference_ci": prevalence_difference_ci,
        "prevalence_difference_ci_method": "unpooled Wald interval (respondent-days treated as independent)",
        "ci_level": ci_level,
        "cluster_bootstrap": bootstrap_clustered(records, bootstrap_reps, seed, ci_level),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def analyze(args: argparse.Namespace) -> Dict[str, object]:
    records, audit = load_records(
        args.responses_csv,
        args.demographics_csv,
        args.fandom_signifier,
        args.outcome_signifier,
        args.id_column,
        args.date_column,
        args.signifier_column,
        args.response_column,
    )
    return {
        "analysis": "NFL Team Fandom Identities RQ1",
        "unit": "respondent-day with explicit answers to both target signifiers",
        "fandom_signifier": args.fandom_signifier,
        "outcome_signifier": args.outcome_signifier,
        "reference_group": f"explicit No to {args.fandom_signifier}",
        "inputs": {
            "responses_file": args.responses_csv.name,
            "responses_sha256": sha256(args.responses_csv),
            "demographics_file": args.demographics_csv.name,
            "demographics_sha256": sha256(args.demographics_csv),
        },
        "join_audit": audit,
        "estimates": estimate(records, args.ci_level, args.bootstrap_reps, args.seed),
        "temporal_sensitivity": temporal_sensitivity(records),
    }


def print_summary(result: Mapping[str, object]) -> None:
    estimates = result["estimates"]
    audit = result["join_audit"]
    assert isinstance(estimates, Mapping)
    assert isinstance(audit, Mapping)
    prevalence_ratio = estimates["prevalence_ratio"]
    ratio_text = (
        "undefined"
        if prevalence_ratio is None
        else f"{float(prevalence_ratio):.4f}"
    )
    print("NFL Team Fandom Identities — RQ1")
    print(f"Eligible respondent-days: {audit['eligible_respondent_days']}")
    print(
        "Happy prevalence, Cleveland Browns fan Yes: "
        f"{100 * float(estimates['happy_prevalence_fandom_yes']):.2f}% "
        f"(n={estimates['fandom_yes_n']})"
    )
    print(
        "Happy prevalence, Cleveland Browns fan No:  "
        f"{100 * float(estimates['happy_prevalence_fandom_no']):.2f}% "
        f"(n={estimates['fandom_no_n']})"
    )
    print(f"Prevalence ratio: {ratio_text}")
    print(
        "Prevalence difference: "
        f"{100 * float(estimates['prevalence_difference']):+.2f} percentage points"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses_csv", type=Path)
    parser.add_argument("demographics_csv", type=Path)
    parser.add_argument("--output", type=Path, help="Write the complete result as JSON")
    parser.add_argument("--fandom-signifier", default="Cleveland Browns fan")
    parser.add_argument("--outcome-signifier", default="happy")
    parser.add_argument("--id-column", default="hashed_respondent_id")
    parser.add_argument("--date-column", default="obs_date")
    parser.add_argument("--signifier-column", default="signifier")
    parser.add_argument("--response-column", default="endorsed")
    parser.add_argument("--ci-level", type=float, default=0.95)
    parser.add_argument("--bootstrap-reps", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260828)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not 0 < args.ci_level < 1:
        parser.error("--ci-level must be between 0 and 1")
    if args.bootstrap_reps < 0:
        parser.error("--bootstrap-reps must be nonnegative")
    for path in (args.responses_csv, args.demographics_csv):
        if not path.is_file():
            parser.error(f"file not found: {path}")
    try:
        result = analyze(args)
    except AnalysisError as error:
        parser.error(str(error))
    print_summary(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
