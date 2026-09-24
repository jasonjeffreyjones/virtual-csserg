#!/usr/bin/env python3
"""Evaluate probabilistic revision-volume forecasts in training leave-one-out.

The analysis compares a source-calibrated fold distribution with the unchanged
regularized 30-neighbor mixture. It writes only training-cohort diagnostics and
never reads or writes development or private-test predictions.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path
from types import ModuleType

import analyze_change_volume as volume
import analyze_dev_diagnostics as shared


EXPECTED_PLAN_SHA256 = (
    "00d5e2805082986b00f2716808ee12d4cff70ec900a5e47636e893217368f020"
)
EXPECTED_CHANGE_VOLUME_SHA256 = (
    "59b1a48b9b4e7194bbe260b497c5463cb1e4ce984c544e58a404f913046d6c09"
)
BOOTSTRAP_SEED = 20260924
BOOTSTRAP_RESAMPLES = 20_000
INTERVAL_ALPHA = 0.20
INTERVAL_LOW = INTERVAL_ALPHA / 2
INTERVAL_HIGH = 1 - INTERVAL_LOW
OUTCOMES = volume.OUTCOMES

BASE_AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "source_word_count",
    "source_line_count",
    "mean_neighbor_cosine_similarity",
]
OUTCOME_AUDIT_SUFFIXES = (
    "observed",
    "marginal_crps",
    "neighborhood_crps",
    "marginal_minus_neighborhood_crps",
    "marginal_lower_80",
    "marginal_upper_80",
    "marginal_covered_80",
    "marginal_width_80",
    "marginal_interval_score_80",
    "neighborhood_lower_80",
    "neighborhood_upper_80",
    "neighborhood_covered_80",
    "neighborhood_width_80",
    "neighborhood_interval_score_80",
    "marginal_minus_neighborhood_interval_score_80",
)
AUDIT_FIELDS = BASE_AUDIT_FIELDS + [
    f"{outcome}_{suffix}"
    for outcome in OUTCOMES
    for suffix in OUTCOME_AUDIT_SUFFIXES
]


def normalize_distribution(
    support: list[float], weights: list[float]
) -> tuple[list[float], list[float]]:
    """Validate and normalize a finite weighted empirical distribution."""
    if len(support) != len(weights) or not support:
        raise ValueError("Support and weights must have equal nonzero length")
    if any(not math.isfinite(value) for value in support):
        raise ValueError("Distribution support must be finite")
    if any(not math.isfinite(weight) or weight < 0 for weight in weights):
        raise ValueError("Distribution weights must be finite and nonnegative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("Distribution weights must have positive total")
    return support, [weight / total for weight in weights]


def weighted_quantile(
    support: list[float], weights: list[float], probability: float
) -> float:
    """Return the left-continuous inverse weighted empirical CDF."""
    support, weights = normalize_distribution(support, weights)
    if probability < 0 or probability > 1:
        raise ValueError("Quantile probability must be within [0, 1]")
    ordered = sorted(zip(support, weights), key=lambda pair: pair[0])
    if probability == 0:
        return ordered[0][0]
    cumulative = 0.0
    for value, weight in ordered:
        cumulative += weight
        if cumulative + 1e-15 >= probability:
            return value
    return ordered[-1][0]


def empirical_crps(support: list[float], weights: list[float], truth: float) -> float:
    """Calculate CRPS for a weighted empirical distribution in O(n log n)."""
    support, weights = normalize_distribution(support, weights)
    if not math.isfinite(truth):
        raise ValueError("CRPS truth must be finite")
    first_term = sum(
        weight * abs(value - truth) for value, weight in zip(support, weights)
    )
    cumulative_weight = 0.0
    cumulative_weighted_value = 0.0
    half_pairwise_term = 0.0
    for value, weight in sorted(zip(support, weights), key=lambda pair: pair[0]):
        half_pairwise_term += weight * (
            value * cumulative_weight - cumulative_weighted_value
        )
        cumulative_weight += weight
        cumulative_weighted_value += weight * value
    score = first_term - half_pairwise_term
    return max(0.0, score) if abs(score) < 1e-12 else score


def interval_score(truth: float, lower: float, upper: float, alpha: float) -> float:
    """Return the central prediction-interval score; lower is better."""
    if not 0 < alpha < 1:
        raise ValueError("Interval alpha must be within (0, 1)")
    if lower > upper:
        raise ValueError("Interval lower bound cannot exceed upper bound")
    score = upper - lower
    if truth < lower:
        score += (2 / alpha) * (lower - truth)
    elif truth > upper:
        score += (2 / alpha) * (truth - upper)
    return score


def distribution_diagnostics(
    support: list[float], weights: list[float], truth: float
) -> dict[str, float | int]:
    """Score one distribution and its locked central 80% interval."""
    lower = weighted_quantile(support, weights, INTERVAL_LOW)
    upper = weighted_quantile(support, weights, INTERVAL_HIGH)
    return {
        "crps": empirical_crps(support, weights, truth),
        "lower_80": lower,
        "upper_80": upper,
        "covered_80": int(lower <= truth <= upper),
        "width_80": upper - lower,
        "interval_score_80": interval_score(truth, lower, upper, INTERVAL_ALPHA),
    }


def leave_one_out_distributions(
    rows: list[dict[str, str]],
    evaluator: ModuleType,
    neighbor_count: int = volume.NEIGHBOR_COUNT,
    neighbor_effective_weight: float = volume.NEIGHBOR_EFFECTIVE_WEIGHT,
    prior_weight: float = volume.PRIOR_WEIGHT,
) -> list[dict[str, object]]:
    """Score both predictive distributions without held-out future leakage."""
    volume.validate_rows(rows, neighbor_count)
    quantities = [volume.case_quantities(row, evaluator) for row in rows]
    audits: list[dict[str, object]] = []

    for held_out_index, (row, held_out) in enumerate(zip(rows, quantities)):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1 :]
        fold_quantities = quantities[:held_out_index] + quantities[held_out_index + 1 :]
        neighbor_indices, similarities = volume.select_neighbors(
            row, fold_rows, neighbor_count
        )
        neighbor_weights = volume.normalized_neighbor_weights(
            similarities, neighbor_effective_weight
        )
        prior_case_weight = prior_weight / len(fold_rows)
        audit: dict[str, object] = {
            "id": row["id"],
            "source_unique_tokens": held_out["source_unique_tokens"],
            "source_word_count": held_out["source_word_count"],
            "source_line_count": held_out["source_line_count"],
            "mean_neighbor_cosine_similarity": sum(similarities) / len(similarities),
        }

        for outcome in OUTCOMES:
            fold_values = [
                float(candidate["modeled"][outcome]) for candidate in fold_quantities
            ]
            transformed = [
                volume.outcome_scale(outcome, value, held_out) for value in fold_values
            ]
            marginal_support, marginal_weights = normalize_distribution(
                transformed, [1.0] * len(transformed)
            )
            neighborhood_support, neighborhood_distribution_weights = (
                normalize_distribution(
                    transformed + [transformed[index] for index in neighbor_indices],
                    [prior_case_weight] * len(transformed) + neighbor_weights,
                )
            )
            observed = float(held_out["observed"][outcome])
            marginal = distribution_diagnostics(
                marginal_support, marginal_weights, observed
            )
            neighborhood = distribution_diagnostics(
                neighborhood_support,
                neighborhood_distribution_weights,
                observed,
            )
            audit[f"{outcome}_observed"] = observed
            for name, value in marginal.items():
                audit[f"{outcome}_marginal_{name}"] = value
            for name, value in neighborhood.items():
                audit[f"{outcome}_neighborhood_{name}"] = value
            audit[f"{outcome}_marginal_minus_neighborhood_crps"] = (
                float(marginal["crps"]) - float(neighborhood["crps"])
            )
            audit[
                f"{outcome}_marginal_minus_neighborhood_interval_score_80"
            ] = float(marginal["interval_score_80"]) - float(
                neighborhood["interval_score_80"]
            )
        audits.append(audit)
    return audits


def paired_summary(differences: list[float], effect_definition: str) -> dict[str, object]:
    """Summarize paired score reductions; positive favors neighborhoods."""
    low, high = shared.bootstrap_mean_interval(
        differences, BOOTSTRAP_RESAMPLES, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": effect_definition,
        "mean_effect_positive_favors_neighborhood": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "neighborhood_case_wins": sum(value > tolerance for value in differences),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        "neighborhood_case_losses": sum(value < -tolerance for value in differences),
    }


def summarize_method(
    audits: list[dict[str, object]], outcome: str, method: str
) -> dict[str, float]:
    """Summarize proper scores, central-interval coverage, and sharpness."""
    def mean(suffix: str) -> float:
        values = [float(row[f"{outcome}_{method}_{suffix}"]) for row in audits]
        return sum(values) / len(values)

    return {
        "mean_crps": mean("crps"),
        "central_80_interval_coverage": mean("covered_80"),
        "mean_central_80_interval_width": mean("width_80"),
        "mean_central_80_interval_score": mean("interval_score_80"),
    }


def summarize_outcome(
    audits: list[dict[str, object]], outcome: str
) -> dict[str, object]:
    """Return distributional accuracy and paired evidence for one outcome."""
    crps_differences = [
        float(row[f"{outcome}_marginal_minus_neighborhood_crps"])
        for row in audits
    ]
    interval_differences = [
        float(row[f"{outcome}_marginal_minus_neighborhood_interval_score_80"])
        for row in audits
    ]
    return {
        "source_calibrated_marginal": summarize_method(
            audits, outcome, "marginal"
        ),
        "regularized_neighborhood": summarize_method(
            audits, outcome, "neighborhood"
        ),
        "paired_crps_comparison": paired_summary(
            crps_differences, "marginal_crps_minus_neighborhood_crps"
        ),
        "paired_central_80_interval_score_comparison": paired_summary(
            interval_differences,
            "marginal_interval_score_minus_neighborhood_interval_score",
        ),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    change_volume_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the hash-guarded locked analysis and return result plus case audit."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, volume.EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(change_volume_path, EXPECTED_CHANGE_VOLUME_SHA256)
    shared.require_hash(
        Path(volume.retrieval.__file__), volume.EXPECTED_RETRIEVAL_SHA256
    )
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    audits = leave_one_out_distributions(rows, evaluator)
    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_change_distribution_forecasting",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": volume.EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "change_volume_implementation_sha256": EXPECTED_CHANGE_VOLUME_SHA256,
            "retrieval_feature_implementation_sha256": (
                volume.EXPECTED_RETRIEVAL_SHA256
            ),
        },
        "design": {
            "training_cases_per_fold": len(rows) - 1,
            "neighbor_count": volume.NEIGHBOR_COUNT,
            "neighbor_effective_weight": volume.NEIGHBOR_EFFECTIVE_WEIGHT,
            "fold_prior_effective_weight": volume.PRIOR_WEIGHT,
            "source_representation": (
                "text and field-qualified 2024 demographics with fold-fit TF-IDF"
            ),
            "probabilistic_score": "weighted empirical CRPS",
            "central_interval": {
                "nominal_coverage": 1 - INTERVAL_ALPHA,
                "quantiles": [INTERVAL_LOW, INTERVAL_HIGH],
                "quantile_definition": "left-continuous inverse empirical CDF",
            },
            "future_information_used_for_prediction": "none",
            "warning": (
                "This forecasts distributions of revision volume and response "
                "form, not correct future lexical content."
            ),
        },
        "mean_selected_neighbor_cosine_similarity": volume.descriptive(
            [float(row["mean_neighbor_cosine_similarity"]) for row in audits]
        ),
        "outcomes": {
            outcome: summarize_outcome(audits, outcome) for outcome in OUTCOMES
        },
        "bootstrap": {
            "unit": "paired training case",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed_restarted_for_each_outcome_and_score": BOOTSTRAP_SEED,
            "interval": "percentile",
            "confidence_level": shared.CONFIDENCE_LEVEL,
            "interpretation": (
                "Describes sensitivity to training-case composition; it is not "
                "a population-generalization interval."
            ),
        },
        "claim_boundary": (
            "This is a locked training-cohort diagnostic using a previously "
            "selected representation and hyperparameters, not untouched "
            "confirmation, development performance, or private-test performance."
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
        default=project / "ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md",
    )
    parser.add_argument(
        "--change-volume-implementation",
        type=Path,
        default=project / "analysis/analyze_change_volume.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/change_distributions_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/change_distributions_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            args.change_volume_implementation,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_change_distributions: {error}") from error
    print(
        f"Wrote change-distribution analysis for {result['cases']} cases to "
        f"{args.output}"
    )
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
