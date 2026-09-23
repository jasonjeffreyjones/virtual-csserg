#!/usr/bin/env python3
"""Forecast response form and revision volume in training leave-one-out.

The analysis compares source-calibrated fold medians with a regularized
30-neighbor weighted median. It uses no future-derived prediction budget and
writes only training-cohort diagnostics, never development or test forecasts.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from pathlib import Path
from types import ModuleType

import analyze_dev_diagnostics as shared
import trajectory_retrieval as retrieval


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_PLAN_SHA256 = (
    "53c974fcd37f443ea846e88328a125169265fb41ac1cc7877529bdbf9a09638f"
)
EXPECTED_RETRIEVAL_SHA256 = (
    "05f64bb95440dcea8125358441878612e71ba19b898a791a0d3a200511a5077e"
)
NEIGHBOR_COUNT = 30
NEIGHBOR_EFFECTIVE_WEIGHT = 30.0
PRIOR_WEIGHT = 30.0
BOOTSTRAP_SEED = 20260923
BOOTSTRAP_RESAMPLES = 20_000
REQUIRED_FIELDS = {"id", "tst_2024", "tst_2025"}
OUTCOMES = (
    "add_count",
    "delete_count",
    "word_count",
    "line_count",
    "source_similarity",
)
BASE_AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "source_word_count",
    "source_line_count",
    "mean_neighbor_cosine_similarity",
]
AUDIT_FIELDS = BASE_AUDIT_FIELDS + [
    f"{outcome}_{suffix}"
    for outcome in OUTCOMES
    for suffix in (
        "observed",
        "marginal_prediction",
        "neighborhood_prediction",
        "marginal_absolute_error",
        "neighborhood_absolute_error",
        "marginal_minus_neighborhood_absolute_error",
    )
]


def validate_rows(rows: list[dict[str, str]], neighbor_count: int) -> None:
    """Require unique paired cases and enough fold rows for the neighborhood."""
    if len(rows) <= neighbor_count:
        raise ValueError("Training data has too few rows for leave-one-out neighbors")
    missing = REQUIRED_FIELDS - set(rows[0]) if rows else REQUIRED_FIELDS
    if missing:
        raise ValueError(f"Training data is missing fields: {sorted(missing)}")
    case_ids = [row["id"] for row in rows]
    if any(not case_id for case_id in case_ids):
        raise ValueError("Training data contains a blank ID")
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("Training data contains duplicate IDs")
    if any(not row["tst_2024"].strip() or not row["tst_2025"].strip() for row in rows):
        raise ValueError("Training source and follow-up responses must be nonblank")


def weighted_median(values: list[float], weights: list[float]) -> float:
    """Return a deterministic weighted median, averaging an exact half split."""
    if len(values) != len(weights) or not values:
        raise ValueError("Values and weights must have equal nonzero length")
    if any(not math.isfinite(value) for value in values):
        raise ValueError("Weighted-median values must be finite")
    if any(not math.isfinite(weight) or weight < 0 for weight in weights):
        raise ValueError("Weighted-median weights must be finite and nonnegative")
    total = sum(weights)
    if total <= 0:
        raise ValueError("Weighted-median weights must have positive total")
    ordered = sorted(zip(values, weights), key=lambda pair: pair[0])
    half = total / 2
    cumulative = 0.0
    for index, (value, weight) in enumerate(ordered):
        cumulative += weight
        if math.isclose(cumulative, half, rel_tol=0.0, abs_tol=1e-12):
            next_values = [candidate for candidate, _ in ordered[index + 1 :]]
            return (value + next_values[0]) / 2 if next_values else value
        if cumulative > half:
            return value
    return ordered[-1][0]


def select_neighbors(
    query: dict[str, str],
    training_rows: list[dict[str, str]],
    count: int,
) -> tuple[list[int], list[float]]:
    """Select nearest fold sources with fold order as the exact-tie rule."""
    if count < 1 or count > len(training_rows):
        raise ValueError("Neighbor count must be within the training-fold size")
    counts = [retrieval.feature_counts(row) for row in training_rows]
    idf = retrieval.fit_idf(counts)
    vectors = [retrieval.vectorize(features, idf) for features in counts]
    query_vector, query_norm = retrieval.vectorize(retrieval.feature_counts(query), idf)
    similarities = [
        retrieval.cosine_similarity(query_vector, query_norm, vector, norm)
        for vector, norm in vectors
    ]
    indices = sorted(
        range(len(training_rows)), key=lambda index: (-similarities[index], index)
    )[:count]
    return indices, [similarities[index] for index in indices]


def normalized_neighbor_weights(
    similarities: list[float], effective_weight: float = NEIGHBOR_EFFECTIVE_WEIGHT
) -> list[float]:
    """Clip cosine similarities at zero and give neighbors fixed total mass."""
    if not similarities or effective_weight <= 0:
        raise ValueError("Similarities and effective weight must be positive")
    clipped = [max(0.0, similarity) for similarity in similarities]
    total = sum(clipped)
    if total == 0:
        return [effective_weight / len(clipped)] * len(clipped)
    return [similarity * effective_weight / total for similarity in clipped]


def case_quantities(
    row: dict[str, str], evaluator: ModuleType
) -> dict[str, object]:
    """Calculate observed outcomes and their source-calibrated model scales."""
    source = row["tst_2024"]
    follow_up = row["tst_2025"]
    source_tokens = evaluator.tokenize(source)
    follow_up_tokens = evaluator.tokenize(follow_up)
    source_set = set(source_tokens)
    follow_up_set = set(follow_up_tokens)
    source_lines = evaluator.line_count(source)
    follow_up_lines = evaluator.line_count(follow_up)
    if not source_tokens or not follow_up_tokens or source_lines < 1 or follow_up_lines < 1:
        raise ValueError(f"Case {row.get('id', '')!r} has an empty token or line count")

    observed = {
        "add_count": float(len(follow_up_set - source_set)),
        "delete_count": float(len(source_set - follow_up_set)),
        "word_count": float(len(follow_up_tokens)),
        "line_count": float(follow_up_lines),
        "source_similarity": evaluator.rouge_l_f1(follow_up, source),
    }
    modeled = {
        "add_count": observed["add_count"],
        "delete_count": observed["delete_count"] / len(source_set),
        "word_count": observed["word_count"] - len(source_tokens),
        "line_count": observed["line_count"] - source_lines,
        "source_similarity": observed["source_similarity"],
    }
    return {
        "source_unique_tokens": len(source_set),
        "source_word_count": len(source_tokens),
        "source_line_count": source_lines,
        "observed": observed,
        "modeled": modeled,
    }


def outcome_scale(
    outcome: str, modeled_value: float, quantities: dict[str, object]
) -> float:
    """Transform one modeled quantity back to its reported outcome scale."""
    if outcome == "add_count":
        return modeled_value
    if outcome == "delete_count":
        source_unique = float(quantities["source_unique_tokens"])
        return min(source_unique, max(0.0, modeled_value * source_unique))
    if outcome == "word_count":
        return max(0.0, float(quantities["source_word_count"]) + modeled_value)
    if outcome == "line_count":
        return max(1.0, float(quantities["source_line_count"]) + modeled_value)
    if outcome == "source_similarity":
        return min(1.0, max(0.0, modeled_value))
    raise ValueError(f"Unknown outcome: {outcome}")


def leave_one_out_forecasts(
    rows: list[dict[str, str]],
    evaluator: ModuleType,
    neighbor_count: int = NEIGHBOR_COUNT,
    neighbor_effective_weight: float = NEIGHBOR_EFFECTIVE_WEIGHT,
    prior_weight: float = PRIOR_WEIGHT,
) -> list[dict[str, object]]:
    """Forecast all outcomes without using each held-out case's follow-up."""
    validate_rows(rows, neighbor_count)
    quantities = [case_quantities(row, evaluator) for row in rows]
    audits: list[dict[str, object]] = []

    for held_out_index, (row, held_out) in enumerate(zip(rows, quantities)):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1 :]
        fold_quantities = quantities[:held_out_index] + quantities[held_out_index + 1 :]
        neighbor_indices, similarities = select_neighbors(
            row, fold_rows, neighbor_count
        )
        neighbor_weights = normalized_neighbor_weights(
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
            marginal_modeled = statistics.median(fold_values)
            neighborhood_modeled = weighted_median(
                fold_values + [fold_values[index] for index in neighbor_indices],
                [prior_case_weight] * len(fold_values) + neighbor_weights,
            )
            observed = float(held_out["observed"][outcome])
            marginal = outcome_scale(outcome, marginal_modeled, held_out)
            neighborhood = outcome_scale(outcome, neighborhood_modeled, held_out)
            marginal_error = abs(observed - marginal)
            neighborhood_error = abs(observed - neighborhood)
            audit.update(
                {
                    f"{outcome}_observed": observed,
                    f"{outcome}_marginal_prediction": marginal,
                    f"{outcome}_neighborhood_prediction": neighborhood,
                    f"{outcome}_marginal_absolute_error": marginal_error,
                    f"{outcome}_neighborhood_absolute_error": neighborhood_error,
                    f"{outcome}_marginal_minus_neighborhood_absolute_error": (
                        marginal_error - neighborhood_error
                    ),
                }
            )
        audits.append(audit)
    return audits


def descriptive(values: list[float]) -> dict[str, float]:
    """Summarize one complete vector without concealing its center."""
    if not values:
        raise ValueError("Cannot summarize an empty vector")
    return {
        "mean": sum(values) / len(values),
        "median": statistics.median(values),
    }


def paired_summary(differences: list[float], resamples: int) -> dict[str, object]:
    """Summarize paired absolute-error reductions; positive favors neighbors."""
    low, high = shared.bootstrap_mean_interval(
        differences, resamples, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": "marginal_mae_minus_neighborhood_mae",
        "mean_effect_positive_favors_neighborhood": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "neighborhood_case_wins": sum(value > tolerance for value in differences),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        "neighborhood_case_losses": sum(value < -tolerance for value in differences),
    }


def summarize_outcome(
    audits: list[dict[str, object]], outcome: str, resamples: int
) -> dict[str, object]:
    """Return calibration, error, and paired evidence for one outcome."""
    observed = [float(row[f"{outcome}_observed"]) for row in audits]
    marginal = [float(row[f"{outcome}_marginal_prediction"]) for row in audits]
    neighborhood = [
        float(row[f"{outcome}_neighborhood_prediction"]) for row in audits
    ]
    differences = [
        float(row[f"{outcome}_marginal_minus_neighborhood_absolute_error"])
        for row in audits
    ]

    def errors(predictions: list[float]) -> dict[str, float]:
        residuals = [prediction - truth for prediction, truth in zip(predictions, observed)]
        return {
            "mean_absolute_error": sum(abs(value) for value in residuals)
            / len(residuals),
            "root_mean_squared_error": math.sqrt(
                sum(value * value for value in residuals) / len(residuals)
            ),
        }

    return {
        "observed": descriptive(observed),
        "source_calibrated_marginal_prediction": descriptive(marginal),
        "regularized_neighborhood_prediction": descriptive(neighborhood),
        "source_calibrated_marginal_error": errors(marginal),
        "regularized_neighborhood_error": errors(neighborhood),
        "paired_absolute_error_comparison": paired_summary(differences, resamples),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    retrieval_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the hash-guarded locked analysis and return result plus case audit."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(retrieval_path, EXPECTED_RETRIEVAL_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    audits = leave_one_out_forecasts(rows, evaluator)
    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_change_volume_forecasting",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "retrieval_feature_implementation_sha256": EXPECTED_RETRIEVAL_SHA256,
        },
        "design": {
            "training_cases_per_fold": len(rows) - 1,
            "neighbor_count": NEIGHBOR_COUNT,
            "neighbor_effective_weight": NEIGHBOR_EFFECTIVE_WEIGHT,
            "fold_prior_effective_weight": PRIOR_WEIGHT,
            "estimator": "weighted median",
            "source_representation": (
                "text and field-qualified 2024 demographics with fold-fit TF-IDF"
            ),
            "future_information_used_for_prediction": "none",
            "warning": (
                "This forecasts revision volume and response form, not correct "
                "future lexical content."
            ),
        },
        "mean_selected_neighbor_cosine_similarity": descriptive(
            [float(row["mean_neighbor_cosine_similarity"]) for row in audits]
        ),
        "outcomes": {
            outcome: summarize_outcome(audits, outcome, resamples)
            for outcome in OUTCOMES
        },
        "bootstrap": {
            "unit": "paired training case",
            "resamples": resamples,
            "seed_restarted_for_each_outcome": BOOTSTRAP_SEED,
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
        default=project / "ANALYSIS_PLAN_CHANGE_VOLUME.md",
    )
    parser.add_argument(
        "--retrieval-implementation",
        type=Path,
        default=project / "analysis/trajectory_retrieval.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/change_volume_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/change_volume_train_audit.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            args.retrieval_implementation,
            args.bootstrap_resamples,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_change_volume: {error}") from error
    print(f"Wrote change-volume analysis for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
