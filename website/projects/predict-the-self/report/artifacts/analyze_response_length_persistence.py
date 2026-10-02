#!/usr/bin/env python3
"""Test a one-count additive persistence forecast in training leave-one-out.

The locked diagnostic compares a person's prior word count plus the fold
distribution of word-count changes with the inherited three-count source-form
neighborhood. It never reads or writes development or private-test rows.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from types import ModuleType

import analyze_change_distributions as distributions
import analyze_change_volume as volume
import analyze_dev_diagnostics as shared


EXPECTED_PLAN_SHA256 = (
    "8071914fd204beefeabd294fac7e3f1b00dceeba50c0372ffbd5498b2d136861"
)
EXPECTED_INITIAL_PLAN_SHA256 = (
    "13e8737f02b1546d08e8d51998b115a5500ac5621910204c97f0f13258685ebb"
)
EXPECTED_SOURCE_FORM_IMPLEMENTATION_SHA256 = (
    "721815303644b0da611732496207609f26cd421ae28f9f00d1563d3fe473195f"
)
EXPECTED_SOURCE_FORM_AUDIT_SHA256 = (
    "b2de65f50f20584c866a113b84cf98b40aa4ed0e972e9db36494753dbcee0c0e"
)
BOOTSTRAP_SEED = 20261002
BOOTSTRAP_RESAMPLES = 20_000

AUDIT_FIELDS = [
    "id",
    "source_word_count",
    "observed_word_count",
    "observed_word_count_change",
    "raw_marginal_prediction",
    "additive_persistence_prediction",
    "unchanged_source_prediction",
    "raw_marginal_absolute_error",
    "additive_persistence_absolute_error",
    "unchanged_source_absolute_error",
    "raw_marginal_minus_additive_absolute_error",
    "unchanged_source_minus_additive_absolute_error",
    "raw_marginal_crps",
    "additive_persistence_crps",
    "source_form_neighborhood_crps",
    "additive_minus_source_form_crps",
    "raw_marginal_minus_additive_crps",
    "raw_marginal_lower_80",
    "raw_marginal_upper_80",
    "raw_marginal_covered_80",
    "raw_marginal_width_80",
    "raw_marginal_interval_score_80",
    "additive_persistence_lower_80",
    "additive_persistence_upper_80",
    "additive_persistence_covered_80",
    "additive_persistence_width_80",
    "additive_persistence_interval_score_80",
    "raw_marginal_minus_additive_interval_score_80",
]


def additive_support(
    source_word_count: float, fold_changes: list[float]
) -> list[float]:
    """Shift fold word-count changes by the held-out source count."""
    if not math.isfinite(source_word_count) or source_word_count < 0:
        raise ValueError("Source word count must be finite and nonnegative")
    if not fold_changes or any(not math.isfinite(value) for value in fold_changes):
        raise ValueError("Fold changes must be nonempty and finite")
    return [max(0.0, source_word_count + change) for change in fold_changes]


def leave_one_out_scores(
    rows: list[dict[str, str]], evaluator: ModuleType
) -> list[dict[str, object]]:
    """Score raw-marginal and additive forecasts without held-out futures."""
    volume.validate_rows(rows, neighbor_count=1)
    quantities = [volume.case_quantities(row, evaluator) for row in rows]
    audits: list[dict[str, object]] = []

    for held_out_index, (row, held_out) in enumerate(zip(rows, quantities)):
        fold = quantities[:held_out_index] + quantities[held_out_index + 1 :]
        source_count = float(held_out["source_word_count"])
        observed = float(held_out["observed"]["word_count"])
        fold_followups = [float(case["observed"]["word_count"]) for case in fold]
        fold_changes = [float(case["modeled"]["word_count"]) for case in fold]
        additive = additive_support(source_count, fold_changes)
        weights = [1.0] * len(fold)

        raw_marginal_diagnostics = distributions.distribution_diagnostics(
            fold_followups, weights, observed
        )
        additive_diagnostics = distributions.distribution_diagnostics(
            additive, weights, observed
        )
        raw_marginal_prediction = distributions.weighted_quantile(
            fold_followups, weights, 0.5
        )
        additive_prediction = distributions.weighted_quantile(additive, weights, 0.5)
        raw_marginal_error = abs(observed - raw_marginal_prediction)
        additive_error = abs(observed - additive_prediction)
        unchanged_error = abs(observed - source_count)

        audit: dict[str, object] = {
            "id": row["id"],
            "source_word_count": source_count,
            "observed_word_count": observed,
            "observed_word_count_change": observed - source_count,
            "raw_marginal_prediction": raw_marginal_prediction,
            "additive_persistence_prediction": additive_prediction,
            "unchanged_source_prediction": source_count,
            "raw_marginal_absolute_error": raw_marginal_error,
            "additive_persistence_absolute_error": additive_error,
            "unchanged_source_absolute_error": unchanged_error,
            "raw_marginal_minus_additive_absolute_error": (
                raw_marginal_error - additive_error
            ),
            "unchanged_source_minus_additive_absolute_error": (
                unchanged_error - additive_error
            ),
            "raw_marginal_crps": raw_marginal_diagnostics["crps"],
            "additive_persistence_crps": additive_diagnostics["crps"],
            "raw_marginal_minus_additive_crps": (
                float(raw_marginal_diagnostics["crps"])
                - float(additive_diagnostics["crps"])
            ),
        }
        for name, value in raw_marginal_diagnostics.items():
            if name != "crps":
                audit[f"raw_marginal_{name}"] = value
        for name, value in additive_diagnostics.items():
            if name != "crps":
                audit[f"additive_persistence_{name}"] = value
        audit["raw_marginal_minus_additive_interval_score_80"] = (
            float(raw_marginal_diagnostics["interval_score_80"])
            - float(additive_diagnostics["interval_score_80"])
        )
        audits.append(audit)
    return audits


def attach_and_verify_source_form_scores(
    audits: list[dict[str, object]], existing_audit_path: Path
) -> None:
    """Verify inherited case quantities and attach locked source-form CRPS."""
    shared.require_hash(existing_audit_path, EXPECTED_SOURCE_FORM_AUDIT_SHA256)
    with existing_audit_path.open("r", encoding="utf-8", newline="") as handle:
        existing = list(csv.DictReader(handle, strict=True))
    if len(existing) != len(audits):
        raise ValueError("Existing source-form audit has a different row count")
    for current, prior in zip(audits, existing):
        if current["id"] != prior["id"]:
            raise ValueError("Existing source-form audit case order differs")
        comparisons = {
            "source_word_count": "source_word_count",
            "observed_word_count": "word_count_observed",
            "additive_persistence_crps": "word_count_marginal_crps",
        }
        for current_field, prior_field in comparisons.items():
            if not math.isclose(
                float(current[current_field]),
                float(prior[prior_field]),
                rel_tol=0.0,
                abs_tol=5e-7,
            ):
                raise ValueError(
                    f"Existing source-form audit did not reproduce {current_field} "
                    f"for {current['id']}"
                )
        source_form_crps = float(prior["word_count_source_form_only_crps"])
        current["source_form_neighborhood_crps"] = source_form_crps
        current["additive_minus_source_form_crps"] = (
            float(current["additive_persistence_crps"]) - source_form_crps
        )


def paired_summary(
    differences: list[float],
    effect_definition: str,
    favored_method: str,
) -> dict[str, object]:
    """Summarize a paired score or error reduction; positive favors method."""
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
        "favored_method_case_losses": sum(value < -tolerance for value in differences),
    }


def pearson_correlation(left: list[float], right: list[float]) -> float:
    """Return the ordinary finite-sample Pearson correlation."""
    if len(left) != len(right) or len(left) < 2:
        raise ValueError("Correlation vectors must have equal length of at least two")
    if any(not math.isfinite(value) for value in left + right):
        raise ValueError("Correlation vectors must be finite")
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    numerator = sum(
        (x - left_mean) * (y - right_mean) for x, y in zip(left, right)
    )
    left_ss = sum((x - left_mean) ** 2 for x in left)
    right_ss = sum((y - right_mean) ** 2 for y in right)
    if left_ss == 0 or right_ss == 0:
        raise ValueError("Correlation is undefined for a constant vector")
    return numerator / math.sqrt(left_ss * right_ss)


def summarize_method(audits: list[dict[str, object]], prefix: str) -> dict[str, float]:
    """Summarize one predictive distribution's proper and interval scores."""
    def mean(field: str) -> float:
        return sum(float(row[field]) for row in audits) / len(audits)

    return {
        "mean_crps": mean(f"{prefix}_crps"),
        "central_80_interval_coverage": mean(f"{prefix}_covered_80"),
        "mean_central_80_interval_width": mean(f"{prefix}_width_80"),
        "mean_central_80_interval_score": mean(f"{prefix}_interval_score_80"),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    initial_plan_path: Path,
    source_form_implementation_path: Path,
    source_form_audit_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the locked hash-guarded response-length persistence analysis."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, volume.EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(initial_plan_path, EXPECTED_INITIAL_PLAN_SHA256)
    shared.require_hash(
        source_form_implementation_path, EXPECTED_SOURCE_FORM_IMPLEMENTATION_SHA256
    )
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    audits = leave_one_out_scores(rows, evaluator)
    attach_and_verify_source_form_scores(audits, source_form_audit_path)

    sources = [float(row["source_word_count"]) for row in audits]
    followups = [float(row["observed_word_count"]) for row in audits]
    changes = [float(row["observed_word_count_change"]) for row in audits]
    primary = paired_summary(
        [float(row["raw_marginal_minus_additive_crps"]) for row in audits],
        "raw_marginal_crps_minus_additive_persistence_crps",
        "additive_persistence",
    )
    primary_low = float(primary["paired_case_bootstrap_95_ci_low"])
    primary_high = float(primary["paired_case_bootstrap_95_ci_high"])
    if primary_low > 0:
        decision = "additive_persistence_improves_beyond_raw_marginal"
    elif primary_high < 0:
        decision = "raw_marginal_outperforms_additive_persistence"
    else:
        decision = "primary_comparison_does_not_separate_methods"

    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_response_length_persistence",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": volume.EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "superseded_initial_plan_sha256": EXPECTED_INITIAL_PLAN_SHA256,
            "source_form_implementation_sha256": (
                EXPECTED_SOURCE_FORM_IMPLEMENTATION_SHA256
            ),
            "source_form_audit_sha256": EXPECTED_SOURCE_FORM_AUDIT_SHA256,
        },
        "design": {
            "training_cases_per_fold": len(rows) - 1,
            "additive_distribution": (
                "max(0, held-out source word count + each fold follow-up-minus-"
                "source word-count change), equally weighted"
            ),
            "raw_marginal_distribution": (
                "each fold follow-up word count, equally weighted"
            ),
            "point_forecast": "left-continuous empirical median",
            "probabilistic_score": "empirical CRPS",
            "central_interval": {
                "nominal_coverage": 1 - distributions.INTERVAL_ALPHA,
                "quantiles": [
                    distributions.INTERVAL_LOW,
                    distributions.INTERVAL_HIGH,
                ],
            },
            "primary_contrast": (
                "raw follow-up marginal CRPS minus additive persistence CRPS"
            ),
            "future_information_used_for_prediction": "none",
        },
        "inherited_source_form_audit_reproduced": True,
        "descriptive": {
            "source_word_count": volume.descriptive(sources),
            "followup_word_count": volume.descriptive(followups),
            "followup_minus_source_word_count": volume.descriptive(changes),
            "source_followup_word_count_pearson_correlation": pearson_correlation(
                sources, followups
            ),
        },
        "mean_absolute_error": {
            "raw_marginal_median": sum(
                float(row["raw_marginal_absolute_error"]) for row in audits
            )
            / len(audits),
            "additive_persistence_median": sum(
                float(row["additive_persistence_absolute_error"]) for row in audits
            )
            / len(audits),
            "unchanged_source": sum(
                float(row["unchanged_source_absolute_error"]) for row in audits
            )
            / len(audits),
        },
        "predictive_distributions": {
            "raw_marginal": summarize_method(audits, "raw_marginal"),
            "additive_persistence": summarize_method(
                audits, "additive_persistence"
            ),
            "source_form_neighborhood": {
                "mean_crps": sum(
                    float(row["source_form_neighborhood_crps"]) for row in audits
                )
                / len(audits),
                "provenance": "inherited locked source-form case audit",
            },
        },
        "primary_comparison": primary,
        "primary_decision": decision,
        "secondary_comparisons": {
            "additive_vs_source_form_crps_reproduction": paired_summary(
                [float(row["additive_minus_source_form_crps"]) for row in audits],
                "additive_persistence_crps_minus_source_form_neighborhood_crps",
                "source_form_neighborhood",
            ),
            "raw_marginal_vs_additive_absolute_error": paired_summary(
                [
                    float(row["raw_marginal_minus_additive_absolute_error"])
                    for row in audits
                ],
                "raw_marginal_absolute_error_minus_additive_persistence_absolute_error",
                "additive_persistence",
            ),
            "unchanged_source_vs_additive_absolute_error": paired_summary(
                [
                    float(row["unchanged_source_minus_additive_absolute_error"])
                    for row in audits
                ],
                "unchanged_source_absolute_error_minus_additive_persistence_absolute_error",
                "additive_persistence",
            ),
            "raw_marginal_vs_additive_interval_score": paired_summary(
                [
                    float(row["raw_marginal_minus_additive_interval_score_80"])
                    for row in audits
                ],
                "raw_marginal_interval_score_minus_additive_persistence_interval_score",
                "additive_persistence",
            ),
        },
        "bootstrap": {
            "unit": "paired training case",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed_restarted_for_each_comparison": BOOTSTRAP_SEED,
            "interval": "percentile",
            "confidence_level": shared.CONFIDENCE_LEVEL,
            "multiplicity_adjustment": "none; one primary contrast",
        },
        "claim_boundary": (
            "This dependent, locked training-cohort diagnostic concerns response "
            "length, not correct future identity content. It is not untouched "
            "confirmation, population evidence, development performance, or "
            "private-test performance."
        ),
    }
    return shared.round_floats(result), audits


def write_audit(path: Path, rows: list[dict[str, object]]) -> None:
    """Write the complete case audit with stable numeric formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: f"{value:.6f}" if isinstance(value, float) else value
                    for key, value in row.items()
                }
            )


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md",
    )
    parser.add_argument(
        "--initial-analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md",
    )
    parser.add_argument(
        "--source-form-implementation",
        type=Path,
        default=project / "analysis/analyze_source_form_ablation.py",
    )
    parser.add_argument(
        "--source-form-audit",
        type=Path,
        default=project / "results/source_form_ablation_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/response_length_persistence_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/response_length_persistence_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            args.initial_analysis_plan,
            args.source_form_implementation,
            args.source_form_audit,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_response_length_persistence: {error}") from error
    print(
        f"Wrote response-length persistence analysis for {result['cases']} cases "
        f"to {args.output}"
    )
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
