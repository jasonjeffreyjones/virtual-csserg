#!/usr/bin/env python3
"""Apply one simultaneous-interval stress test to 16 inherited contrasts.

The locked audit uses only four existing training-case score files. It never
reads benchmark rows, development data, or private-test data and never creates
a prediction.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
import sys
from pathlib import Path


EXPECTED_PLAN_SHA256 = (
    "d3c31e1bd77df8da0d5b7017438f2b9ff04ba5f39c4dfcb803c1c38f294fb9ac"
)
EXPECTED_INPUT_SHA256 = {
    "change_volume": (
        "0c400f1a060d5d390f22ccf8691c6e6266705846c48d50307d7d1a619570db6e"
    ),
    "change_distributions": (
        "0c257335a92538e2e0eb223c39c10c49d3f8204888e77590a0bcf7e23a8edff7"
    ),
    "feature_ablation": (
        "423582b332c74841347c763f2638aed1a22e4a9036b0f30175b7b74348aa6987"
    ),
    "source_form_ablation": (
        "b2de65f50f20584c866a113b84cf98b40aa4ed0e972e9db36494753dbcee0c0e"
    ),
}
EXPECTED_CASES = 150
BOOTSTRAP_SEED = 20260929
BOOTSTRAP_RESAMPLES = 20_000
CONFIDENCE_LEVEL = 0.95
OUTCOMES = (
    "add_count",
    "delete_count",
    "word_count",
    "line_count",
    "source_similarity",
)

# The expected six-decimal means come from the locked constituent analyses.
# Requiring them protects the family from silent changes to inherited scores.
EXPECTED_MEANS = {
    "point_mae_add_count": 1.213333,
    "point_mae_delete_count": 0.278660,
    "point_mae_word_count": 3.140000,
    "point_mae_line_count": 0.000000,
    "point_mae_source_similarity": 0.002867,
    "distribution_crps_add_count": 0.212518,
    "distribution_crps_delete_count": 0.072801,
    "distribution_crps_word_count": 2.515843,
    "distribution_crps_line_count": -0.011761,
    "distribution_crps_source_similarity": 0.002486,
    "word_crps_marginal_minus_text_only": 2.298139,
    "word_crps_marginal_minus_demographics_only": 0.200711,
    "word_crps_text_only_minus_combined": 0.217704,
    "word_crps_demographics_only_minus_combined": 2.315132,
    "word_crps_marginal_minus_source_form": 3.245309,
    "word_crps_source_form_minus_text_only": -0.947170,
}

CONTRAST_METADATA = {
    "point_mae_add_count": (
        "point_forecast",
        "add_count",
        "marginal absolute error minus neighborhood absolute error",
        "positive favors neighborhood",
    ),
    "point_mae_delete_count": (
        "point_forecast",
        "delete_count",
        "marginal absolute error minus neighborhood absolute error",
        "positive favors neighborhood",
    ),
    "point_mae_word_count": (
        "point_forecast",
        "word_count",
        "marginal absolute error minus neighborhood absolute error",
        "positive favors neighborhood",
    ),
    "point_mae_line_count": (
        "point_forecast",
        "line_count",
        "marginal absolute error minus neighborhood absolute error",
        "positive favors neighborhood",
    ),
    "point_mae_source_similarity": (
        "point_forecast",
        "source_similarity",
        "marginal absolute error minus neighborhood absolute error",
        "positive favors neighborhood",
    ),
    "distribution_crps_add_count": (
        "distribution_forecast",
        "add_count",
        "marginal CRPS minus neighborhood CRPS",
        "positive favors neighborhood",
    ),
    "distribution_crps_delete_count": (
        "distribution_forecast",
        "delete_count",
        "marginal CRPS minus neighborhood CRPS",
        "positive favors neighborhood",
    ),
    "distribution_crps_word_count": (
        "distribution_forecast",
        "word_count",
        "marginal CRPS minus neighborhood CRPS",
        "positive favors neighborhood",
    ),
    "distribution_crps_line_count": (
        "distribution_forecast",
        "line_count",
        "marginal CRPS minus neighborhood CRPS",
        "positive favors neighborhood",
    ),
    "distribution_crps_source_similarity": (
        "distribution_forecast",
        "source_similarity",
        "marginal CRPS minus neighborhood CRPS",
        "positive favors neighborhood",
    ),
    "word_crps_marginal_minus_text_only": (
        "word_count_ablation",
        "word_count",
        "marginal CRPS minus text-only CRPS",
        "positive favors text only",
    ),
    "word_crps_marginal_minus_demographics_only": (
        "word_count_ablation",
        "word_count",
        "marginal CRPS minus demographics-only CRPS",
        "positive favors demographics only",
    ),
    "word_crps_text_only_minus_combined": (
        "word_count_ablation",
        "word_count",
        "text-only CRPS minus combined CRPS",
        "positive favors combined",
    ),
    "word_crps_demographics_only_minus_combined": (
        "word_count_ablation",
        "word_count",
        "demographics-only CRPS minus combined CRPS",
        "positive favors combined",
    ),
    "word_crps_marginal_minus_source_form": (
        "word_count_ablation",
        "word_count",
        "marginal CRPS minus source-form CRPS",
        "positive favors source form",
    ),
    "word_crps_source_form_minus_text_only": (
        "word_count_ablation",
        "word_count",
        "source-form CRPS minus text-only CRPS",
        "positive favors text only",
    ),
}

AUDIT_FIELDS = [
    "contrast",
    "family_group",
    "outcome",
    "effect_definition",
    "direction",
    "mean_effect",
    "standard_error",
    "simultaneous_95_ci_low",
    "simultaneous_95_ci_high",
    "simultaneous_status",
]


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_hash(path: Path, expected: str) -> None:
    """Refuse changed plans or inherited case scores."""
    observed = sha256(path)
    if observed != expected:
        raise ValueError(
            f"SHA-256 mismatch for {path}: expected {expected}, observed {observed}"
        )


def read_audit(path: Path) -> list[dict[str, str]]:
    """Read one strict, complete inherited case audit."""
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, strict=True))
    if len(rows) != EXPECTED_CASES:
        raise ValueError(f"Expected {EXPECTED_CASES} rows in {path}, found {len(rows)}")
    ids = [row.get("id", "") for row in rows]
    if any(not case_id for case_id in ids) or len(ids) != len(set(ids)):
        raise ValueError(f"Missing or duplicate case ID in {path}")
    return rows


def finite_float(row: dict[str, str], field: str) -> float:
    """Parse and validate one required numeric field."""
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"Missing or invalid numeric field {field}") from error
    if not math.isfinite(value):
        raise ValueError(f"Nonfinite value in {field}")
    return value


def require_same_ids(audits: dict[str, list[dict[str, str]]]) -> list[str]:
    """Require every inherited audit to describe the same ordered cases."""
    reference_name = next(iter(audits))
    reference = [row["id"] for row in audits[reference_name]]
    for name, rows in audits.items():
        if [row["id"] for row in rows] != reference:
            raise ValueError(
                f"Case IDs or order in {name} differ from {reference_name}"
            )
    return reference


def require_algebraic_difference(
    row: dict[str, str], direct_field: str, first_field: str, second_field: str
) -> float:
    """Validate an inherited rounded paired difference against its scores."""
    direct = finite_float(row, direct_field)
    calculated = finite_float(row, first_field) - finite_float(row, second_field)
    if not math.isclose(direct, calculated, rel_tol=0.0, abs_tol=1.1e-6):
        raise ValueError(
            f"{direct_field} does not reproduce {first_field} minus {second_field}"
        )
    return direct


def extract_contrasts(
    audits: dict[str, list[dict[str, str]]]
) -> dict[str, list[float]]:
    """Extract the locked 16-contrast family and verify inherited arithmetic."""
    require_same_ids(audits)
    contrasts: dict[str, list[float]] = {}

    volume_rows = audits["change_volume"]
    for outcome in OUTCOMES:
        contrasts[f"point_mae_{outcome}"] = [
            require_algebraic_difference(
                row,
                f"{outcome}_marginal_minus_neighborhood_absolute_error",
                f"{outcome}_marginal_absolute_error",
                f"{outcome}_neighborhood_absolute_error",
            )
            for row in volume_rows
        ]

    distribution_rows = audits["change_distributions"]
    for outcome in OUTCOMES:
        contrasts[f"distribution_crps_{outcome}"] = [
            require_algebraic_difference(
                row,
                f"{outcome}_marginal_minus_neighborhood_crps",
                f"{outcome}_marginal_crps",
                f"{outcome}_neighborhood_crps",
            )
            for row in distribution_rows
        ]

    feature_rows = audits["feature_ablation"]
    feature_pairs = {
        "word_crps_marginal_minus_text_only": ("marginal", "text_only"),
        "word_crps_marginal_minus_demographics_only": (
            "marginal",
            "demographics_only",
        ),
        "word_crps_text_only_minus_combined": ("text_only", "combined"),
        "word_crps_demographics_only_minus_combined": (
            "demographics_only",
            "combined",
        ),
    }
    for name, (first, second) in feature_pairs.items():
        contrasts[name] = [
            finite_float(row, f"word_count_{first}_crps")
            - finite_float(row, f"word_count_{second}_crps")
            for row in feature_rows
        ]

    form_rows = audits["source_form_ablation"]
    form_pairs = {
        "word_crps_marginal_minus_source_form": (
            "marginal",
            "source_form_only",
        ),
        "word_crps_source_form_minus_text_only": (
            "source_form_only",
            "text_only",
        ),
    }
    for name, (first, second) in form_pairs.items():
        contrasts[name] = [
            finite_float(row, f"word_count_{first}_crps")
            - finite_float(row, f"word_count_{second}_crps")
            for row in form_rows
        ]

    if list(contrasts) != list(CONTRAST_METADATA):
        raise ValueError("Extracted contrast family differs from the locked family")
    for name, values in contrasts.items():
        mean = statistics.fmean(values)
        if round(mean, 6) != EXPECTED_MEANS[name]:
            raise ValueError(
                f"Inherited mean for {name} changed: {mean:.9f} versus "
                f"{EXPECTED_MEANS[name]:.6f}"
            )
    return contrasts


def nearest_rank(values: list[float], probability: float) -> float:
    """Return a fixed nearest-rank empirical quantile."""
    if not values or not 0 < probability <= 1:
        raise ValueError("Nearest-rank quantile requires values and 0 < p <= 1")
    ordered = sorted(values)
    return ordered[math.ceil(probability * len(ordered)) - 1]


def simultaneous_summary(
    contrasts: dict[str, list[float]],
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[float, dict[str, dict[str, float | str]]]:
    """Calculate synchronized studentized max-|t| bootstrap intervals."""
    if resamples < 1:
        raise ValueError("At least one bootstrap resample is required")
    lengths = {len(values) for values in contrasts.values()}
    if len(lengths) != 1 or next(iter(lengths), 0) < 2:
        raise ValueError("Every contrast must contain the same two or more cases")
    n = next(iter(lengths))
    means = {name: statistics.fmean(values) for name, values in contrasts.items()}
    standard_errors = {
        name: statistics.stdev(values) / math.sqrt(n)
        for name, values in contrasts.items()
    }
    active = [name for name, standard_error in standard_errors.items() if standard_error]
    if not active:
        critical_value = 0.0
    else:
        rng = random.Random(seed)
        maxima: list[float] = []
        for _ in range(resamples):
            indices = [rng.randrange(n) for _ in range(n)]
            maximum = 0.0
            for name in active:
                values = contrasts[name]
                total = sum(values[index] for index in indices)
                total_squares = sum(values[index] ** 2 for index in indices)
                bootstrap_mean = total / n
                variance = max(
                    0.0, (total_squares - total * total / n) / (n - 1)
                )
                bootstrap_standard_error = math.sqrt(variance / n)
                if bootstrap_standard_error == 0:
                    studentized = (
                        0.0
                        if bootstrap_mean == means[name]
                        else float("inf")
                    )
                else:
                    studentized = abs(
                        (bootstrap_mean - means[name]) / bootstrap_standard_error
                    )
                maximum = max(maximum, studentized)
            maxima.append(maximum)
        critical_value = nearest_rank(maxima, CONFIDENCE_LEVEL)
        if not math.isfinite(critical_value):
            raise ValueError("Nonfinite simultaneous critical value")

    summaries: dict[str, dict[str, float | str]] = {}
    for name in contrasts:
        mean = means[name]
        standard_error = standard_errors[name]
        low = mean - critical_value * standard_error
        high = mean + critical_value * standard_error
        if standard_error == 0 and mean == 0:
            status = "exact_zero"
        elif low > 0:
            status = "positive"
        elif high < 0:
            status = "negative"
        else:
            status = "includes_zero"
        summaries[name] = {
            "mean_effect": mean,
            "standard_error": standard_error,
            "simultaneous_95_ci_low": low,
            "simultaneous_95_ci_high": high,
            "simultaneous_status": status,
        }
    return critical_value, summaries


def round_floats(value: object) -> object:
    """Round stored results without changing booleans or integers."""
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, dict):
        return {key: round_floats(item) for key, item in value.items()}
    if isinstance(value, list):
        return [round_floats(item) for item in value]
    return value


def analyze(
    plan_path: Path,
    input_paths: dict[str, Path],
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = BOOTSTRAP_SEED,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the hash-guarded cross-analysis stress test."""
    require_hash(plan_path, EXPECTED_PLAN_SHA256)
    for name, path in input_paths.items():
        require_hash(path, EXPECTED_INPUT_SHA256[name])
    audits = {name: read_audit(path) for name, path in input_paths.items()}
    contrasts = extract_contrasts(audits)
    critical_value, summaries = simultaneous_summary(contrasts, resamples, seed)

    rows: list[dict[str, object]] = []
    for name, summary in summaries.items():
        family_group, outcome, definition, direction = CONTRAST_METADATA[name]
        rows.append(
            {
                "contrast": name,
                "family_group": family_group,
                "outcome": outcome,
                "effect_definition": definition,
                "direction": direction,
                **summary,
            }
        )
    stable = [
        row["contrast"]
        for row in rows
        if row["simultaneous_status"] in {"positive", "negative"}
    ]
    result: dict[str, object] = {
        "schema_version": 1,
        "analysis": "training_cross_analysis_multiplicity_stress_test",
        "cases": EXPECTED_CASES,
        "contrast_count": len(rows),
        "inputs": {
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "case_audit_sha256": EXPECTED_INPUT_SHA256,
        },
        "family": {
            "point_forecast_outcomes": list(OUTCOMES),
            "distribution_forecast_outcomes": list(OUTCOMES),
            "unique_word_count_ablation_comparisons": 6,
            "excluded": (
                "central-interval scores, secondary ablation outcomes, "
                "oracle-budget rankings, full-text scorecards, development "
                "analyses, and duplicate inherited contrasts"
            ),
        },
        "resampling": {
            "unit": "paired derived leave-one-out training case",
            "resamples": resamples,
            "seed": seed,
            "synchronization": "one shared index resample across all contrasts",
            "statistic": "maximum absolute studentized mean deviation",
            "confidence_level": CONFIDENCE_LEVEL,
            "critical_quantile": "nearest-rank",
            "common_critical_value": critical_value,
        },
        "contrasts": {row["contrast"]: row for row in rows},
        "simultaneously_stable_contrast_count": len(stable),
        "simultaneously_stable_contrasts": stable,
        "claim_boundary": (
            "This dependent post hoc robustness audit describes simultaneous "
            "sensitivity to case composition for one fixed 16-contrast family "
            "within the selected cohort. It is not retroactive preregistration, "
            "population-generalization evidence, development performance, or "
            "private-test performance; overlapping fitted folds are not refit."
        ),
    }
    return round_floats(result), [round_floats(row) for row in rows]


def write_json(path: Path, result: dict[str, object]) -> None:
    """Write stable, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_audit(path: Path, rows: list[dict[str, object]]) -> None:
    """Write the flat 16-row contrast audit."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: f"{row[field]:.6f}"
                    if isinstance(row[field], float)
                    else row[field]
                    for field in AUDIT_FIELDS
                }
            )


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md",
    )
    parser.add_argument(
        "--change-volume-audit",
        type=Path,
        default=project / "results/change_volume_train_audit.csv",
    )
    parser.add_argument(
        "--change-distributions-audit",
        type=Path,
        default=project / "results/change_distributions_train_audit.csv",
    )
    parser.add_argument(
        "--feature-ablation-audit",
        type=Path,
        default=project / "results/feature_ablation_train_audit.csv",
    )
    parser.add_argument(
        "--source-form-ablation-audit",
        type=Path,
        default=project / "results/source_form_ablation_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/multiplicity_stress_test_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/multiplicity_stress_test_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_paths = {
        "change_volume": args.change_volume_audit,
        "change_distributions": args.change_distributions_audit,
        "feature_ablation": args.feature_ablation_audit,
        "source_form_ablation": args.source_form_ablation_audit,
    }
    try:
        result, audit = analyze(args.analysis_plan, input_paths)
        write_json(args.output, result)
        write_audit(args.audit_output, audit)
    except (OSError, ValueError, csv.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    print(f"Wrote {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
