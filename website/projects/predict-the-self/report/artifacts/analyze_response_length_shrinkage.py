#!/usr/bin/env python3
"""Test cross-fitted regression-to-the-mean response-length forecasts.

The locked analysis reads only the preceding 150-case count audit. It never
reads benchmark text, development rows, or private-test rows and never writes
a text prediction.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from pathlib import Path

import analyze_change_distributions as distributions
import analyze_dev_diagnostics as shared


EXPECTED_PLAN_SHA256 = (
    "ca69f562c3a78e34ed5cb9997a1ac6816492bf5273cda4686a3a92a8fb22fd92"
)
EXPECTED_PRECEDING_PLAN_SHA256 = (
    "8071914fd204beefeabd294fac7e3f1b00dceeba50c0372ffbd5498b2d136861"
)
EXPECTED_PRECEDING_IMPLEMENTATION_SHA256 = (
    "e8a055f2f0ca0be65bc898caeadcef3f901c57b84fca6d323f6cbe50f44bc98d"
)
EXPECTED_PRECEDING_AUDIT_SHA256 = (
    "b9dec6d552f116ecef9344b4ae8762dbbd1ac1b458bc2fb296aed5295ec0aa8d"
)
BOOTSTRAP_SEED = 20261003
BOOTSTRAP_RESAMPLES = 20_000
EXPECTED_CASES = 150
STORAGE_TOLERANCE = 5.1e-7

AUDIT_FIELDS = [
    "id",
    "source_word_count",
    "observed_word_count",
    "linear_slope_mean",
    "linear_slope_standard_deviation",
    "linear_slope_minimum",
    "linear_slope_maximum",
    "raw_marginal_prediction",
    "additive_persistence_prediction",
    "linear_persistence_prediction",
    "raw_marginal_absolute_error",
    "additive_persistence_absolute_error",
    "linear_persistence_absolute_error",
    "raw_marginal_minus_linear_absolute_error",
    "raw_marginal_crps",
    "additive_persistence_crps",
    "source_form_neighborhood_crps",
    "linear_persistence_crps",
    "raw_marginal_minus_linear_crps",
    "additive_persistence_minus_linear_crps",
    "source_form_minus_linear_crps",
    "raw_marginal_minus_source_form_crps",
    "raw_marginal_lower_80",
    "raw_marginal_upper_80",
    "raw_marginal_covered_80",
    "raw_marginal_width_80",
    "raw_marginal_interval_score_80",
    "linear_persistence_lower_80",
    "linear_persistence_upper_80",
    "linear_persistence_covered_80",
    "linear_persistence_width_80",
    "linear_persistence_interval_score_80",
    "raw_marginal_minus_linear_interval_score_80",
]


def ols_slope(source_counts: list[float], followup_counts: list[float]) -> float:
    """Return the ordinary least-squares slope with an implicit intercept."""
    if len(source_counts) != len(followup_counts) or len(source_counts) < 2:
        raise ValueError("OLS vectors must have equal length of at least two")
    if any(
        not math.isfinite(value) for value in source_counts + followup_counts
    ):
        raise ValueError("OLS vectors must be finite")
    source_mean = sum(source_counts) / len(source_counts)
    followup_mean = sum(followup_counts) / len(followup_counts)
    denominator = sum((value - source_mean) ** 2 for value in source_counts)
    if denominator == 0:
        return 0.0
    numerator = sum(
        (source - source_mean) * (followup - followup_mean)
        for source, followup in zip(source_counts, followup_counts)
    )
    return numerator / denominator


def cross_fitted_linear_support(
    held_out_index: int,
    source_counts: list[float],
    followup_counts: list[float],
) -> tuple[list[float], list[float]]:
    """Transport each support follow-up with a slope fit without i or j."""
    if len(source_counts) != len(followup_counts) or len(source_counts) < 4:
        raise ValueError("Count vectors must have equal length of at least four")
    if held_out_index < 0 or held_out_index >= len(source_counts):
        raise ValueError("Held-out index is outside the count vectors")
    held_out_source = source_counts[held_out_index]
    support: list[float] = []
    slopes: list[float] = []
    for support_index, (source, followup) in enumerate(
        zip(source_counts, followup_counts)
    ):
        if support_index == held_out_index:
            continue
        fit_indices = [
            index
            for index in range(len(source_counts))
            if index not in (held_out_index, support_index)
        ]
        slope = ols_slope(
            [source_counts[index] for index in fit_indices],
            [followup_counts[index] for index in fit_indices],
        )
        slopes.append(slope)
        support.append(max(0.0, followup + slope * (held_out_source - source)))
    return support, slopes


def parse_count(value: str, field: str, case_id: str) -> float:
    """Parse one stored count and require an exact nonnegative integer."""
    try:
        parsed = float(value)
    except ValueError as error:
        raise ValueError(f"Invalid {field} for {case_id}") from error
    if not math.isfinite(parsed) or parsed < 0 or not parsed.is_integer():
        raise ValueError(f"{field} must be a finite nonnegative integer for {case_id}")
    return parsed


def read_preceding_audit(path: Path) -> list[dict[str, str]]:
    """Read and validate the hash-guarded preceding 150-case audit."""
    shared.require_hash(path, EXPECTED_PRECEDING_AUDIT_SHA256)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        required = {
            "id",
            "source_word_count",
            "observed_word_count",
            "raw_marginal_crps",
            "additive_persistence_crps",
            "source_form_neighborhood_crps",
        }
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("Preceding audit is missing required columns")
        rows = list(reader)
    if len(rows) != EXPECTED_CASES:
        raise ValueError(f"Expected {EXPECTED_CASES} audit rows, found {len(rows)}")
    ids = [row["id"] for row in rows]
    if any(not case_id for case_id in ids) or len(set(ids)) != len(ids):
        raise ValueError("Audit IDs must be nonempty and unique")
    for row in rows:
        case_id = row["id"]
        parse_count(row["source_word_count"], "source_word_count", case_id)
        parse_count(row["observed_word_count"], "observed_word_count", case_id)
        for field in (
            "raw_marginal_crps",
            "additive_persistence_crps",
            "source_form_neighborhood_crps",
        ):
            try:
                value = float(row[field])
            except ValueError as error:
                raise ValueError(f"Invalid {field} for {case_id}") from error
            if not math.isfinite(value) or value < 0:
                raise ValueError(f"{field} must be finite and nonnegative for {case_id}")
    return rows


def require_stored_score(
    calculated: float, stored: str, field: str, case_id: str
) -> None:
    """Require reproduction within six-decimal storage precision."""
    if not math.isclose(
        calculated, float(stored), rel_tol=0.0, abs_tol=STORAGE_TOLERANCE
    ):
        raise ValueError(f"Preceding audit did not reproduce {field} for {case_id}")


def leave_one_out_scores(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[float]]:
    """Score raw, additive, source-form, and cross-fitted linear forecasts."""
    source_counts = [
        parse_count(row["source_word_count"], "source_word_count", row["id"])
        for row in rows
    ]
    followup_counts = [
        parse_count(row["observed_word_count"], "observed_word_count", row["id"])
        for row in rows
    ]
    audits: list[dict[str, object]] = []
    all_slopes: list[float] = []

    for held_out_index, row in enumerate(rows):
        source = source_counts[held_out_index]
        observed = followup_counts[held_out_index]
        fold_indices = [
            index for index in range(len(rows)) if index != held_out_index
        ]
        raw = [followup_counts[index] for index in fold_indices]
        additive = [
            max(
                0.0,
                followup_counts[index] + source - source_counts[index],
            )
            for index in fold_indices
        ]
        linear, slopes = cross_fitted_linear_support(
            held_out_index, source_counts, followup_counts
        )
        all_slopes.extend(slopes)
        weights = [1.0] * len(raw)
        raw_diagnostics = distributions.distribution_diagnostics(
            raw, weights, observed
        )
        additive_diagnostics = distributions.distribution_diagnostics(
            additive, weights, observed
        )
        linear_diagnostics = distributions.distribution_diagnostics(
            linear, weights, observed
        )
        require_stored_score(
            float(raw_diagnostics["crps"]),
            row["raw_marginal_crps"],
            "raw_marginal_crps",
            row["id"],
        )
        require_stored_score(
            float(additive_diagnostics["crps"]),
            row["additive_persistence_crps"],
            "additive_persistence_crps",
            row["id"],
        )
        source_form_crps = float(row["source_form_neighborhood_crps"])
        raw_prediction = distributions.weighted_quantile(raw, weights, 0.5)
        additive_prediction = distributions.weighted_quantile(
            additive, weights, 0.5
        )
        linear_prediction = distributions.weighted_quantile(linear, weights, 0.5)
        raw_error = abs(observed - raw_prediction)
        additive_error = abs(observed - additive_prediction)
        linear_error = abs(observed - linear_prediction)

        audit: dict[str, object] = {
            "id": row["id"],
            "source_word_count": source,
            "observed_word_count": observed,
            "linear_slope_mean": sum(slopes) / len(slopes),
            "linear_slope_standard_deviation": statistics.pstdev(slopes),
            "linear_slope_minimum": min(slopes),
            "linear_slope_maximum": max(slopes),
            "raw_marginal_prediction": raw_prediction,
            "additive_persistence_prediction": additive_prediction,
            "linear_persistence_prediction": linear_prediction,
            "raw_marginal_absolute_error": raw_error,
            "additive_persistence_absolute_error": additive_error,
            "linear_persistence_absolute_error": linear_error,
            "raw_marginal_minus_linear_absolute_error": raw_error - linear_error,
            "raw_marginal_crps": raw_diagnostics["crps"],
            "additive_persistence_crps": additive_diagnostics["crps"],
            "source_form_neighborhood_crps": source_form_crps,
            "linear_persistence_crps": linear_diagnostics["crps"],
            "raw_marginal_minus_linear_crps": (
                float(raw_diagnostics["crps"])
                - float(linear_diagnostics["crps"])
            ),
            "additive_persistence_minus_linear_crps": (
                float(additive_diagnostics["crps"])
                - float(linear_diagnostics["crps"])
            ),
            "source_form_minus_linear_crps": (
                source_form_crps - float(linear_diagnostics["crps"])
            ),
            "raw_marginal_minus_source_form_crps": (
                float(raw_diagnostics["crps"]) - source_form_crps
            ),
        }
        for name, value in raw_diagnostics.items():
            if name != "crps":
                audit[f"raw_marginal_{name}"] = value
        for name, value in linear_diagnostics.items():
            if name != "crps":
                audit[f"linear_persistence_{name}"] = value
        audit["raw_marginal_minus_linear_interval_score_80"] = (
            float(raw_diagnostics["interval_score_80"])
            - float(linear_diagnostics["interval_score_80"])
        )
        audits.append(audit)
    return audits, all_slopes


def paired_summary(
    differences: list[float], effect_definition: str, favored_method: str
) -> dict[str, object]:
    """Summarize a paired first-minus-second effect; positive favors second."""
    if not differences or any(not math.isfinite(value) for value in differences):
        raise ValueError("Paired differences must be nonempty and finite")
    low, high = shared.bootstrap_mean_interval(
        differences, BOOTSTRAP_RESAMPLES, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": effect_definition,
        "positive_favors": favored_method,
        "mean_effect": sum(differences) / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "favored_method_case_wins": sum(value > tolerance for value in differences),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        "favored_method_case_losses": sum(
            value < -tolerance for value in differences
        ),
    }


def summarize_distribution(
    audits: list[dict[str, object]], prefix: str
) -> dict[str, float]:
    """Summarize one predictive distribution's proper and interval scores."""
    def mean(field: str) -> float:
        return sum(float(row[field]) for row in audits) / len(audits)

    return {
        "mean_crps": mean(f"{prefix}_crps"),
        "central_80_interval_coverage": mean(f"{prefix}_covered_80"),
        "mean_central_80_interval_width": mean(f"{prefix}_width_80"),
        "mean_central_80_interval_score": mean(f"{prefix}_interval_score_80"),
    }


def describe_slopes(values: list[float]) -> dict[str, float | int]:
    """Return the prespecified complete support-slope description."""
    if not values or any(not math.isfinite(value) for value in values):
        raise ValueError("Slopes must be nonempty and finite")
    weights = [1.0] * len(values)
    return {
        "count": len(values),
        "mean": sum(values) / len(values),
        "standard_deviation": statistics.pstdev(values),
        "minimum": min(values),
        "first_quartile": distributions.weighted_quantile(values, weights, 0.25),
        "median": distributions.weighted_quantile(values, weights, 0.5),
        "third_quartile": distributions.weighted_quantile(values, weights, 0.75),
        "maximum": max(values),
    }


def analyze(
    plan_path: Path,
    preceding_plan_path: Path,
    preceding_implementation_path: Path,
    preceding_audit_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the locked, hash-guarded response-length shrinkage analysis."""
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(preceding_plan_path, EXPECTED_PRECEDING_PLAN_SHA256)
    shared.require_hash(
        preceding_implementation_path, EXPECTED_PRECEDING_IMPLEMENTATION_SHA256
    )
    rows = read_preceding_audit(preceding_audit_path)
    audits, slopes = leave_one_out_scores(rows)
    if len(slopes) != EXPECTED_CASES * (EXPECTED_CASES - 1):
        raise ValueError("Unexpected number of cross-fitted support slopes")

    primary = paired_summary(
        [float(row["raw_marginal_minus_linear_crps"]) for row in audits],
        "raw_marginal_crps_minus_linear_persistence_crps",
        "linear_persistence",
    )
    primary_low = float(primary["paired_case_bootstrap_95_ci_low"])
    primary_high = float(primary["paired_case_bootstrap_95_ci_high"])
    if primary_low > 0:
        decision = "linear_persistence_improves_beyond_raw_marginal"
    elif primary_high < 0:
        decision = "raw_marginal_outperforms_linear_persistence"
    else:
        decision = "primary_comparison_does_not_separate_methods"

    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_response_length_shrinkage",
        "cases": len(audits),
        "provenance": {
            "benchmark_commit_inherited": "9b6a766712583fec8d3182957260b1123fbfa146",
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "preceding_plan_sha256": EXPECTED_PRECEDING_PLAN_SHA256,
            "preceding_implementation_sha256": (
                EXPECTED_PRECEDING_IMPLEMENTATION_SHA256
            ),
            "preceding_audit_sha256": EXPECTED_PRECEDING_AUDIT_SHA256,
        },
        "design": {
            "training_cases_per_outer_fold": EXPECTED_CASES - 1,
            "slope_fit_cases_per_support_value": EXPECTED_CASES - 2,
            "linear_distribution": (
                "max(0, support follow-up + OLS slope fit without outer or support "
                "case * (held-out source - support source)), equally weighted"
            ),
            "raw_marginal_distribution": (
                "each outer-fold support follow-up count, equally weighted"
            ),
            "additive_distribution": (
                "max(0, support follow-up + held-out source - support source), "
                "equally weighted"
            ),
            "point_forecast": "left-continuous empirical median",
            "probabilistic_score": "empirical CRPS",
            "primary_contrast": (
                "raw follow-up marginal CRPS minus linear-persistence CRPS"
            ),
            "future_information_used_for_focal_prediction": "none",
        },
        "preceding_raw_and_additive_scores_reproduced": True,
        "support_specific_slope_distribution": describe_slopes(slopes),
        "mean_absolute_error": {
            method: sum(float(row[f"{method}_absolute_error"]) for row in audits)
            / len(audits)
            for method in (
                "raw_marginal",
                "additive_persistence",
                "linear_persistence",
            )
        },
        "predictive_distributions": {
            "raw_marginal": summarize_distribution(audits, "raw_marginal"),
            "additive_persistence": {
                "mean_crps": sum(
                    float(row["additive_persistence_crps"]) for row in audits
                )
                / len(audits),
            },
            "source_form_neighborhood": {
                "mean_crps": sum(
                    float(row["source_form_neighborhood_crps"]) for row in audits
                )
                / len(audits),
                "provenance": "inherited preceding case audit",
            },
            "linear_persistence": summarize_distribution(
                audits, "linear_persistence"
            ),
        },
        "primary_comparison": primary,
        "primary_decision": decision,
        "secondary_comparisons": {
            "additive_vs_linear_crps": paired_summary(
                [
                    float(row["additive_persistence_minus_linear_crps"])
                    for row in audits
                ],
                "additive_persistence_crps_minus_linear_persistence_crps",
                "linear_persistence",
            ),
            "source_form_vs_linear_crps": paired_summary(
                [float(row["source_form_minus_linear_crps"]) for row in audits],
                "source_form_neighborhood_crps_minus_linear_persistence_crps",
                "linear_persistence",
            ),
            "raw_marginal_vs_source_form_crps": paired_summary(
                [
                    float(row["raw_marginal_minus_source_form_crps"])
                    for row in audits
                ],
                "raw_marginal_crps_minus_source_form_neighborhood_crps",
                "source_form_neighborhood",
            ),
            "raw_marginal_vs_linear_absolute_error": paired_summary(
                [
                    float(row["raw_marginal_minus_linear_absolute_error"])
                    for row in audits
                ],
                "raw_marginal_absolute_error_minus_linear_persistence_absolute_error",
                "linear_persistence",
            ),
            "raw_marginal_vs_linear_interval_score": paired_summary(
                [
                    float(row["raw_marginal_minus_linear_interval_score_80"])
                    for row in audits
                ],
                "raw_marginal_interval_score_minus_linear_persistence_interval_score",
                "linear_persistence",
            ),
        },
        "bootstrap": {
            "unit": "paired outer training case",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed_restarted_for_each_comparison": BOOTSTRAP_SEED,
            "interval": "percentile",
            "confidence_level": shared.CONFIDENCE_LEVEL,
            "multiplicity_adjustment": "none; one primary contrast",
        },
        "claim_boundary": (
            "This dependent training-cohort diagnostic concerns response length, "
            "not correct future identity content. It is not untouched confirmation, "
            "population evidence, development performance, or private-test "
            "performance."
        ),
    }
    return shared.round_floats(result), audits


def write_audit(path: Path, rows: list[dict[str, object]]) -> None:
    """Write the complete 150-case audit with stable numeric formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: f"{row[key]:.6f}" if isinstance(row[key], float) else row[key]
                    for key in AUDIT_FIELDS
                }
            )


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md",
    )
    parser.add_argument(
        "--preceding-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md",
    )
    parser.add_argument(
        "--preceding-implementation",
        type=Path,
        default=project / "analysis/analyze_response_length_persistence.py",
    )
    parser.add_argument(
        "--preceding-audit",
        type=Path,
        default=project / "results/response_length_persistence_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/response_length_shrinkage_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/response_length_shrinkage_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result, audit = analyze(
            args.analysis_plan,
            args.preceding_plan,
            args.preceding_implementation,
            args.preceding_audit,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError) as error:
        raise SystemExit(f"analyze_response_length_shrinkage: {error}") from error
    print(
        f"Wrote response-length shrinkage analysis for {result['cases']} cases "
        f"to {args.output}"
    )
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
