#!/usr/bin/env python3
"""Evaluate regularized neighborhood Add rankings in training leave-one-out.

Each held-out training source retrieves 30 similar sources. Their Add events
are similarity-weighted and shrunk equally toward fold-wide marginal Add rates.
Both the personalized ranking and its marginal comparator receive the held-out
case's observed novel-token budget, so this diagnoses ranking information and
is not a prospective full-text forecast.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path

import analyze_dev_diagnostics as shared
import analyze_source_conditioned_additions as source_conditioned
import trajectory_retrieval as retrieval


EXPECTED_TRAIN_SHA256 = source_conditioned.EXPECTED_TRAIN_SHA256
EXPECTED_PLAN_SHA256 = (
    "c7a494327dd1dd7fc83911540a6a9095fcc8d684172a7388bd610206ac4ca13d"
)
NEIGHBOR_COUNT = 30
NEIGHBOR_EFFECTIVE_WEIGHT = 30.0
PRIOR_WEIGHT = 30.0
BOOTSTRAP_SEED = 20260921
BOOTSTRAP_RESAMPLES = 20_000
AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "observed_addition_budget",
    "reachable_observed_additions",
    "reachable_fraction",
    "mean_neighbor_cosine_similarity",
    "marginal_hits",
    "marginal_recovered_fraction",
    "neighborhood_hits",
    "neighborhood_recovered_fraction",
    "neighborhood_minus_marginal",
    "top_set_overlap_fraction",
]


def select_neighbors(
    query: dict[str, str],
    training_rows: list[dict[str, str]],
    count: int = NEIGHBOR_COUNT,
) -> tuple[list[int], list[float]]:
    """Return fold-local indices and cosine similarities for nearest sources."""
    if count < 1 or count > len(training_rows):
        raise ValueError("Neighbor count must be within the training-fold size")
    training_counts = [retrieval.feature_counts(row) for row in training_rows]
    idf = retrieval.fit_idf(training_counts)
    training_vectors = [retrieval.vectorize(features, idf) for features in training_counts]
    query_vector, query_norm = retrieval.vectorize(retrieval.feature_counts(query), idf)
    similarities = [
        retrieval.cosine_similarity(query_vector, query_norm, vector, norm)
        for vector, norm in training_vectors
    ]
    indices = sorted(
        range(len(training_rows)), key=lambda index: (-similarities[index], index)
    )[:count]
    return indices, [similarities[index] for index in indices]


def normalized_neighbor_weights(
    similarities: list[float],
    effective_weight: float = NEIGHBOR_EFFECTIVE_WEIGHT,
) -> list[float]:
    """Clip similarities at zero and rescale to a fixed effective total."""
    if not similarities:
        raise ValueError("At least one neighbor similarity is required")
    if effective_weight <= 0:
        raise ValueError("Effective neighbor weight must be positive")
    clipped = [max(0.0, similarity) for similarity in similarities]
    total = sum(clipped)
    if total == 0:
        return [effective_weight / len(clipped)] * len(clipped)
    return [similarity * effective_weight / total for similarity in clipped]


def regularized_neighborhood_ranking(
    fold_counts: Counter[str],
    held_out_source: set[str],
    neighbor_additions: list[set[str]],
    neighbor_weights: list[float],
    fold_size: int,
    prior_weight: float = PRIOR_WEIGHT,
) -> list[str]:
    """Rank eligible additions by shrunk similarity-weighted neighbor rates."""
    if len(neighbor_additions) != len(neighbor_weights) or not neighbor_additions:
        raise ValueError("Neighbor additions and weights must have equal nonzero length")
    if fold_size < 1 or prior_weight <= 0:
        raise ValueError("Fold size and prior weight must be positive")
    effective_weight = sum(neighbor_weights)
    if effective_weight <= 0:
        raise ValueError("Neighbor weights must sum to a positive value")
    weighted_counts: Counter[str] = Counter()
    for additions, weight in zip(neighbor_additions, neighbor_weights):
        for token in additions:
            weighted_counts[token] += weight
    scored = []
    for token in source_conditioned.eligible_candidates(fold_counts, held_out_source):
        marginal_rate = fold_counts[token] / fold_size
        score = (
            weighted_counts[token] + prior_weight * marginal_rate
        ) / (effective_weight + prior_weight)
        scored.append((score, fold_counts[token], token))
    return [
        token
        for _, _, token in sorted(
            scored, key=lambda item: (-item[0], -item[1], item[2])
        )
    ]


def paired_summary(
    neighborhood: list[float], marginal: list[float], resamples: int
) -> dict[str, object]:
    if len(neighborhood) != len(marginal) or not neighborhood:
        raise ValueError("Paired vectors must have the same nonzero length")
    differences = [
        personalized - baseline
        for personalized, baseline in zip(neighborhood, marginal)
    ]
    low, high = shared.bootstrap_mean_interval(
        differences, resamples, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": "regularized_neighborhood_minus_marginal",
        "mean_effect_positive_favors_regularized_neighborhood": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "regularized_neighborhood_case_wins": sum(
            difference > tolerance for difference in differences
        ),
        "case_ties": sum(abs(difference) <= tolerance for difference in differences),
        "regularized_neighborhood_case_losses": sum(
            difference < -tolerance for difference in differences
        ),
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)

    rows = source_conditioned.read_rows(training_path)
    sources, additions = source_conditioned.token_sets(rows, evaluator)
    _, addition_counts, _ = source_conditioned.build_counts(sources, additions)
    fold_size = len(rows) - 1
    if fold_size < NEIGHBOR_COUNT:
        raise ValueError(
            f"Leave-one-out fold needs at least {NEIGHBOR_COUNT} training cases"
        )

    audit: list[dict[str, object]] = []
    budgets: list[int] = []
    reachable_fractions: list[float] = []
    neighbor_similarities: list[float] = []
    marginal_scores: list[float] = []
    neighborhood_scores: list[float] = []
    overlap_fractions: list[float] = []

    for held_out_index, (row, source, observed) in enumerate(
        zip(rows, sources, additions)
    ):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1 :]
        fold_additions = additions[:held_out_index] + additions[held_out_index + 1 :]
        fold_counts = source_conditioned.fold_addition_counts(
            addition_counts, observed
        )
        neighbor_indices, similarities = select_neighbors(row, fold_rows)
        weights = normalized_neighbor_weights(similarities)
        marginal = source_conditioned.marginal_ranking(fold_counts, source)
        neighborhood = regularized_neighborhood_ranking(
            fold_counts,
            source,
            [fold_additions[index] for index in neighbor_indices],
            weights,
            fold_size,
        )

        budget = len(observed)
        reachable = len(observed & set(fold_counts))
        marginal_top = source_conditioned.top_set(marginal, budget)
        neighborhood_top = source_conditioned.top_set(neighborhood, budget)
        marginal_hits = len(marginal_top & observed)
        neighborhood_hits = len(neighborhood_top & observed)
        mean_similarity = sum(similarities) / len(similarities)
        budgets.append(budget)
        neighbor_similarities.append(mean_similarity)

        if budget:
            reachable_fraction = reachable / budget
            marginal_score = marginal_hits / budget
            neighborhood_score = neighborhood_hits / budget
            overlap_fraction = len(marginal_top & neighborhood_top) / budget
            reachable_fractions.append(reachable_fraction)
            marginal_scores.append(marginal_score)
            neighborhood_scores.append(neighborhood_score)
            overlap_fractions.append(overlap_fraction)
            difference = neighborhood_score - marginal_score
        else:
            reachable_fraction = marginal_score = neighborhood_score = 0.0
            overlap_fraction = difference = 0.0

        audit.append(
            {
                "id": row["id"],
                "source_unique_tokens": len(source),
                "observed_addition_budget": budget,
                "reachable_observed_additions": reachable,
                "reachable_fraction": f"{reachable_fraction:.6f}",
                "mean_neighbor_cosine_similarity": f"{mean_similarity:.6f}",
                "marginal_hits": marginal_hits,
                "marginal_recovered_fraction": f"{marginal_score:.6f}",
                "neighborhood_hits": neighborhood_hits,
                "neighborhood_recovered_fraction": f"{neighborhood_score:.6f}",
                "neighborhood_minus_marginal": f"{difference:.6f}",
                "top_set_overlap_fraction": f"{overlap_fraction:.6f}",
            }
        )

    scored_cases = len(marginal_scores)
    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "training_leave_one_out_regularized_neighborhood_additions",
            "cases": len(rows),
            "scored_cases_with_positive_budget": scored_cases,
            "zero_budget_cases": len(rows) - scored_cases,
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": EXPECTED_TRAIN_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            },
            "design": {
                "training_cases_per_fold": fold_size,
                "neighbor_count": NEIGHBOR_COUNT,
                "neighbor_effective_weight": NEIGHBOR_EFFECTIVE_WEIGHT,
                "marginal_prior_weight": PRIOR_WEIGHT,
                "source_representation": (
                    "text and field-qualified 2024 demographics with fold-fit TF-IDF"
                ),
                "budget": "observed held-out novel-token-type count",
                "warning": (
                    "The oracle budget uses each held-out follow-up and isolates "
                    "ranking quality; neither method is a standalone forecast."
                ),
                "score_identity": (
                    "Predicted and observed sets have equal size, so case-level "
                    "novel-type precision, recall, and F1 are identical."
                ),
            },
            "observed_addition_budget": source_conditioned.descriptive(
                [float(value) for value in budgets]
            ),
            "candidate_vocabulary_reachable_fraction": (
                source_conditioned.descriptive(reachable_fractions)
            ),
            "mean_selected_neighbor_cosine_similarity": (
                source_conditioned.descriptive(neighbor_similarities)
            ),
            "top_set_overlap_fraction": source_conditioned.descriptive(
                overlap_fractions
            ),
            "novel_type_recovered_fraction": {
                "marginal_addition": source_conditioned.descriptive(
                    marginal_scores
                ),
                "regularized_neighborhood": source_conditioned.descriptive(
                    neighborhood_scores
                ),
            },
            "paired_comparison": paired_summary(
                neighborhood_scores, marginal_scores, resamples
            ),
            "bootstrap": {
                "unit": "paired scored training case",
                "resamples": resamples,
                "seed": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": shared.CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to training-case composition; it is "
                    "not a population-generalization interval."
                ),
            },
            "interpretation_limits": (
                "This training-only leave-one-out diagnostic uses an oracle token "
                "budget. Demographics are coarse observed attributes, and lexical "
                "tokens include function words that need not be semantic identity "
                "signifiers. It is not development or private-test performance."
            ),
        }
    )
    return result, audit


def write_audit(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/neighborhood_additions_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/neighborhood_additions_train_audit.csv",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, audit = analyze(
            args.benchmark_dir, args.analysis_plan, args.bootstrap_resamples
        )
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_neighborhood_additions: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_audit(args.audit_output, audit)
    print(
        "Wrote regularized-neighborhood Add analysis for "
        f"{result['cases']} cases to {args.output}"
    )
    print(f"Wrote {len(audit)} case audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
