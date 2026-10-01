#!/usr/bin/env python3
"""Evaluate GloVe-semantic Add rankings in training leave-one-out.

Each held-out source retrieves 30 sources by cosine similarity between
IDF-weighted centroids of pretrained word vectors. Their Add events are
similarity-weighted and shrunk equally toward fold-wide marginal rates. The
oracle held-out Add budget isolates ranking quality; this script never reads a
development or private-test row and never writes a prediction artifact.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import math
import random
from collections import Counter
from pathlib import Path

import analyze_dev_diagnostics as shared
import analyze_neighborhood_additions as neighborhood
import analyze_source_conditioned_additions as source_conditioned


EXPECTED_TRAIN_SHA256 = source_conditioned.EXPECTED_TRAIN_SHA256
EXPECTED_PLAN_SHA256 = (
    "6a6a536a11c552b0e75f40ce6d79100902727958fa908cb57a662ac85df5fdcf"
)
EXPECTED_EMBEDDINGS_SHA256 = (
    "63877d71151688baf6f31d5437374f637f737a5e100e12150a5bd61a9f273c3f"
)
EXPECTED_NEIGHBORHOOD_SHA256 = (
    "bdcfbf9bc2c72fc9e4e45e7fa8bb317d5ecf88efb8959d77222816c5154c8b4a"
)
EXPECTED_INHERITED_AUDIT_SHA256 = (
    "dbd03631a34829311715885caf49455c71e06bf4fd22ee3484a0e8afd184f0bc"
)
EXPECTED_VECTOR_COUNT = 1_193_514
VECTOR_DIMENSION = 25
NEIGHBOR_COUNT = 30
NEIGHBOR_EFFECTIVE_WEIGHT = 30.0
PRIOR_WEIGHT = 30.0
BOOTSTRAP_SEED = 20261001
BOOTSTRAP_RESAMPLES = 20_000
AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "source_in_vocabulary_tokens",
    "source_vector_coverage_fraction",
    "observed_addition_budget",
    "reachable_observed_additions",
    "reachable_fraction",
    "mean_semantic_neighbor_cosine_similarity",
    "marginal_hits",
    "marginal_recovered_fraction",
    "surface_neighborhood_hits",
    "surface_neighborhood_recovered_fraction",
    "semantic_neighborhood_hits",
    "semantic_neighborhood_recovered_fraction",
    "semantic_minus_marginal",
    "semantic_minus_surface_neighborhood",
    "semantic_marginal_top_set_overlap_fraction",
    "semantic_surface_top_set_overlap_fraction",
]


def load_embeddings(
    path: Path, vocabulary: set[str], expected_count: int = EXPECTED_VECTOR_COUNT,
    dimension: int = VECTOR_DIMENSION,
) -> dict[str, tuple[float, ...]]:
    """Stream a word2vec-format gzip and retain only requested vectors."""
    if expected_count < 1 or dimension < 1:
        raise ValueError("Expected vector count and dimension must be positive")
    retained: dict[str, tuple[float, ...]] = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        header = handle.readline().split()
        if header != [str(expected_count), str(dimension)]:
            raise ValueError(
                "Unexpected embedding header: "
                f"expected {expected_count} {dimension}, observed {' '.join(header)}"
            )
        observed_count = 0
        for observed_count, line in enumerate(handle, start=1):
            row = line.rstrip("\r\n")
            try:
                token, coordinate_text = row.split(" ", 1)
            except ValueError as error:
                raise ValueError(
                    f"Embedding row {observed_count} has no coordinate separator"
                ) from error
            coordinates = coordinate_text.split(" ")
            if len(coordinates) != dimension:
                raise ValueError(
                    f"Embedding row {observed_count} has {len(coordinates)} "
                    f"coordinates rather than {dimension}"
                )
            if token not in vocabulary:
                continue
            if token in retained:
                raise ValueError(f"Duplicate retained embedding token: {token!r}")
            try:
                vector = tuple(float(value) for value in coordinates)
            except ValueError as error:
                raise ValueError(
                    f"Embedding row {observed_count} contains a nonnumeric coordinate"
                ) from error
            if any(not math.isfinite(value) for value in vector):
                raise ValueError(
                    f"Embedding row {observed_count} contains a nonfinite coordinate"
                )
            retained[token] = vector
    if observed_count != expected_count:
        raise ValueError(
            f"Expected {expected_count} embedding rows, observed {observed_count}"
        )
    return retained


def fit_idf(source_token_sets: list[set[str]]) -> dict[str, float]:
    """Fit smooth document-frequency weights within one source-only fold."""
    if not source_token_sets:
        raise ValueError("At least one source document is required")
    frequencies: Counter[str] = Counter()
    for tokens in source_token_sets:
        frequencies.update(tokens)
    document_count = len(source_token_sets)
    return {
        token: math.log((document_count + 1) / (frequency + 1)) + 1
        for token, frequency in frequencies.items()
    }


def centroid(
    tokens: set[str],
    embeddings: dict[str, tuple[float, ...]],
    idf: dict[str, float],
    dimension: int = VECTOR_DIMENSION,
) -> tuple[tuple[float, ...], float]:
    """Return an IDF-weighted distinct-token centroid and its Euclidean norm."""
    sums = [0.0] * dimension
    total_weight = 0.0
    for token in sorted(tokens):
        vector = embeddings.get(token)
        if vector is None:
            continue
        if len(vector) != dimension:
            raise ValueError(f"Embedding for {token!r} has the wrong dimension")
        weight = idf.get(token)
        if weight is None:
            continue
        total_weight += weight
        for index, value in enumerate(vector):
            sums[index] += weight * value
    if total_weight == 0:
        values = tuple(sums)
        return values, 0.0
    values = tuple(value / total_weight for value in sums)
    norm = math.sqrt(sum(value * value for value in values))
    return values, norm


def dense_cosine(
    left: tuple[float, ...], left_norm: float,
    right: tuple[float, ...], right_norm: float,
) -> float:
    """Return cosine similarity, using zero for either zero-norm vector."""
    if len(left) != len(right):
        raise ValueError("Cosine vectors must have equal dimensions")
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return sum(a * b for a, b in zip(left, right)) / (left_norm * right_norm)


def select_semantic_neighbors(
    query_tokens: set[str],
    fold_source_tokens: list[set[str]],
    embeddings: dict[str, tuple[float, ...]],
    count: int = NEIGHBOR_COUNT,
    dimension: int = VECTOR_DIMENSION,
) -> tuple[list[int], list[float]]:
    """Select source-only semantic neighbors with fold order breaking ties."""
    if count < 1 or count > len(fold_source_tokens):
        raise ValueError("Neighbor count must be within the training-fold size")
    idf = fit_idf(fold_source_tokens)
    query_vector, query_norm = centroid(query_tokens, embeddings, idf, dimension)
    fold_vectors = [centroid(tokens, embeddings, idf, dimension)
                    for tokens in fold_source_tokens]
    similarities = [
        dense_cosine(query_vector, query_norm, vector, norm)
        for vector, norm in fold_vectors
    ]
    indices = sorted(
        range(len(fold_source_tokens)),
        key=lambda index: (-similarities[index], index),
    )[:count]
    return indices, [similarities[index] for index in indices]


def paired_summary(
    first: list[float], second: list[float], first_name: str, second_name: str,
    resamples: int,
) -> dict[str, object]:
    """Summarize a paired recovered-fraction contrast."""
    if len(first) != len(second) or not first:
        raise ValueError("Paired vectors must have equal nonzero length")
    differences = [left - right for left, right in zip(first, second)]
    low, high = shared.bootstrap_mean_interval(
        differences, resamples, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": f"{first_name}_minus_{second_name}",
        f"mean_effect_positive_favors_{first_name}": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        f"{first_name}_case_wins": sum(value > tolerance for value in differences),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        f"{first_name}_case_losses": sum(value < -tolerance for value in differences),
    }


def read_inherited_audit(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def require_inherited_reproduction(
    inherited: dict[str, str], case_id: str, source_count: int, budget: int,
    marginal_hits: int, surface_hits: int,
) -> None:
    """Require exact inherited case identifiers, counts, and hit totals."""
    expected = {
        "id": case_id,
        "source_unique_tokens": str(source_count),
        "observed_addition_budget": str(budget),
        "marginal_hits": str(marginal_hits),
        "neighborhood_hits": str(surface_hits),
    }
    observed = {key: inherited.get(key, "") for key in expected}
    if observed != expected:
        raise ValueError(
            f"Inherited neighborhood audit did not reproduce for {case_id}: "
            f"expected {expected}, observed {observed}"
        )


def analyze(
    benchmark_dir: Path,
    embeddings_path: Path,
    plan_path: Path,
    neighborhood_path: Path,
    inherited_audit_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the locked semantic-neighborhood analysis."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(embeddings_path, EXPECTED_EMBEDDINGS_SHA256)
    shared.require_hash(neighborhood_path, EXPECTED_NEIGHBORHOOD_SHA256)
    shared.require_hash(inherited_audit_path, EXPECTED_INHERITED_AUDIT_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)

    rows = source_conditioned.read_rows(training_path)
    sources, additions = source_conditioned.token_sets(rows, evaluator)
    if len(rows) <= NEIGHBOR_COUNT:
        raise ValueError("Training data has too few cases for the fixed neighborhood")
    vocabulary = set().union(*sources)
    embeddings = load_embeddings(embeddings_path, vocabulary)
    _, addition_counts, _ = source_conditioned.build_counts(sources, additions)
    inherited_audit = read_inherited_audit(inherited_audit_path)
    if len(inherited_audit) != len(rows):
        raise ValueError("Inherited neighborhood audit has the wrong row count")

    audits: list[dict[str, object]] = []
    budgets: list[int] = []
    coverage: list[float] = []
    reachable_fractions: list[float] = []
    semantic_similarities: list[float] = []
    marginal_scores: list[float] = []
    surface_scores: list[float] = []
    semantic_scores: list[float] = []
    semantic_marginal_overlaps: list[float] = []
    semantic_surface_overlaps: list[float] = []
    fold_size = len(rows) - 1

    for held_out_index, (row, source, observed, inherited) in enumerate(
        zip(rows, sources, additions, inherited_audit)
    ):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1:]
        fold_sources = sources[:held_out_index] + sources[held_out_index + 1:]
        fold_additions = additions[:held_out_index] + additions[held_out_index + 1:]
        fold_counts = source_conditioned.fold_addition_counts(
            addition_counts, observed
        )

        semantic_indices, similarities = select_semantic_neighbors(
            source, fold_sources, embeddings
        )
        semantic_weights = neighborhood.normalized_neighbor_weights(
            similarities, NEIGHBOR_EFFECTIVE_WEIGHT
        )
        semantic_ranking = neighborhood.regularized_neighborhood_ranking(
            fold_counts,
            source,
            [fold_additions[index] for index in semantic_indices],
            semantic_weights,
            fold_size,
            PRIOR_WEIGHT,
        )

        surface_indices, surface_similarities = neighborhood.select_neighbors(
            row, fold_rows, NEIGHBOR_COUNT
        )
        surface_weights = neighborhood.normalized_neighbor_weights(
            surface_similarities, NEIGHBOR_EFFECTIVE_WEIGHT
        )
        surface_ranking = neighborhood.regularized_neighborhood_ranking(
            fold_counts,
            source,
            [fold_additions[index] for index in surface_indices],
            surface_weights,
            fold_size,
            PRIOR_WEIGHT,
        )
        marginal_ranking = source_conditioned.marginal_ranking(fold_counts, source)

        budget = len(observed)
        marginal_top = source_conditioned.top_set(marginal_ranking, budget)
        surface_top = source_conditioned.top_set(surface_ranking, budget)
        semantic_top = source_conditioned.top_set(semantic_ranking, budget)
        marginal_hits = len(marginal_top & observed)
        surface_hits = len(surface_top & observed)
        semantic_hits = len(semantic_top & observed)
        require_inherited_reproduction(
            inherited, row["id"], len(source), budget, marginal_hits, surface_hits
        )

        retained_tokens = len(source & embeddings.keys())
        case_coverage = retained_tokens / len(source) if source else 0.0
        reachable = len(observed & set(fold_counts))
        mean_similarity = sum(similarities) / len(similarities)
        budgets.append(budget)
        coverage.append(case_coverage)
        semantic_similarities.append(mean_similarity)

        if budget:
            reachable_fraction = reachable / budget
            marginal_score = marginal_hits / budget
            surface_score = surface_hits / budget
            semantic_score = semantic_hits / budget
            marginal_overlap = len(semantic_top & marginal_top) / budget
            surface_overlap = len(semantic_top & surface_top) / budget
            reachable_fractions.append(reachable_fraction)
            marginal_scores.append(marginal_score)
            surface_scores.append(surface_score)
            semantic_scores.append(semantic_score)
            semantic_marginal_overlaps.append(marginal_overlap)
            semantic_surface_overlaps.append(surface_overlap)
        else:
            reachable_fraction = marginal_score = surface_score = semantic_score = 0.0
            marginal_overlap = surface_overlap = 0.0

        audits.append(
            {
                "id": row["id"],
                "source_unique_tokens": len(source),
                "source_in_vocabulary_tokens": retained_tokens,
                "source_vector_coverage_fraction": f"{case_coverage:.6f}",
                "observed_addition_budget": budget,
                "reachable_observed_additions": reachable,
                "reachable_fraction": f"{reachable_fraction:.6f}",
                "mean_semantic_neighbor_cosine_similarity": f"{mean_similarity:.6f}",
                "marginal_hits": marginal_hits,
                "marginal_recovered_fraction": f"{marginal_score:.6f}",
                "surface_neighborhood_hits": surface_hits,
                "surface_neighborhood_recovered_fraction": f"{surface_score:.6f}",
                "semantic_neighborhood_hits": semantic_hits,
                "semantic_neighborhood_recovered_fraction": f"{semantic_score:.6f}",
                "semantic_minus_marginal": f"{semantic_score - marginal_score:.6f}",
                "semantic_minus_surface_neighborhood": (
                    f"{semantic_score - surface_score:.6f}"
                ),
                "semantic_marginal_top_set_overlap_fraction": f"{marginal_overlap:.6f}",
                "semantic_surface_top_set_overlap_fraction": f"{surface_overlap:.6f}",
            }
        )

    primary = paired_summary(
        semantic_scores,
        marginal_scores,
        "semantic_neighborhood",
        "marginal_addition",
        resamples,
    )
    secondary = paired_summary(
        semantic_scores,
        surface_scores,
        "semantic_neighborhood",
        "surface_neighborhood",
        resamples,
    )
    primary_mean = float(
        primary["mean_effect_positive_favors_semantic_neighborhood"]
    )
    primary_low = float(primary["paired_case_bootstrap_95_ci_low"])
    gate_passed = primary_mean > 0 and primary_low > 0

    scored_cases = len(semantic_scores)
    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "training_leave_one_out_semantic_neighborhood_additions",
            "cases": len(rows),
            "scored_cases_with_positive_budget": scored_cases,
            "zero_budget_cases": len(rows) - scored_cases,
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": EXPECTED_TRAIN_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
                "inherited_neighborhood_implementation_sha256": (
                    EXPECTED_NEIGHBORHOOD_SHA256
                ),
                "inherited_neighborhood_audit_sha256": (
                    EXPECTED_INHERITED_AUDIT_SHA256
                ),
            },
            "external_representation": {
                "name": "GloVe Twitter 25-dimensional vectors",
                "artifact_sha256": EXPECTED_EMBEDDINGS_SHA256,
                "vectors": EXPECTED_VECTOR_COUNT,
                "dimensions": VECTOR_DIMENSION,
                "source": (
                    "Twitter: 2 billion tweets and 27 billion tokens; "
                    "Gensim-data word2vec-format conversion"
                ),
                "license": "Open Data Commons PDDL 1.0",
                "project_source_vocabulary_types": len(vocabulary),
                "in_vocabulary_source_types": len(embeddings),
                "source_type_coverage_fraction": len(embeddings) / len(vocabulary),
            },
            "design": {
                "training_cases_per_fold": fold_size,
                "neighbor_count": NEIGHBOR_COUNT,
                "neighbor_effective_weight": NEIGHBOR_EFFECTIVE_WEIGHT,
                "marginal_prior_weight": PRIOR_WEIGHT,
                "source_representation": (
                    "fold-IDF-weighted centroid of distinct source-token "
                    "GloVe Twitter vectors"
                ),
                "comparators": [
                    "fold marginal Add frequency",
                    "inherited text-and-demographic surface-TF-IDF neighborhood",
                ],
                "budget": "observed held-out novel-token-type count",
                "warning": (
                    "The oracle budget uses each held-out follow-up and isolates "
                    "ranking quality; no method is a standalone forecast."
                ),
                "score_identity": (
                    "Predicted and observed sets have equal size, so case-level "
                    "novel-type precision, recall, and F1 are identical."
                ),
            },
            "source_vector_case_coverage_fraction": (
                source_conditioned.descriptive(coverage)
            ),
            "cases_with_zero_source_vector_coverage": sum(
                value == 0 for value in coverage
            ),
            "observed_addition_budget": source_conditioned.descriptive(
                [float(value) for value in budgets]
            ),
            "candidate_vocabulary_reachable_fraction": (
                source_conditioned.descriptive(reachable_fractions)
            ),
            "mean_selected_semantic_neighbor_cosine_similarity": (
                source_conditioned.descriptive(semantic_similarities)
            ),
            "top_set_overlap_fraction": {
                "semantic_with_marginal": source_conditioned.descriptive(
                    semantic_marginal_overlaps
                ),
                "semantic_with_surface_neighborhood": (
                    source_conditioned.descriptive(semantic_surface_overlaps)
                ),
            },
            "novel_type_recovered_fraction": {
                "marginal_addition": source_conditioned.descriptive(marginal_scores),
                "surface_neighborhood": source_conditioned.descriptive(surface_scores),
                "semantic_neighborhood": source_conditioned.descriptive(semantic_scores),
            },
            "paired_comparisons": {
                "primary_semantic_vs_marginal": primary,
                "secondary_semantic_vs_surface_neighborhood": secondary,
            },
            "primary_gate": {
                "rule": (
                    "semantic-minus-marginal mean must be positive and its "
                    "pointwise 95% interval must exclude zero positively"
                ),
                "passed": gate_passed,
                "development_evaluation_permitted_this_iteration": False,
                "next_step_if_passed": (
                    "A later locked prospective method must still forecast "
                    "volume, preserve response form, beat simple source counts, "
                    "and pass a full-text training gate."
                ),
            },
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
                "GloVe proximity is distributional rather than an ipseological "
                "identity measure. The centroid discards order and polysemy, "
                "Twitter vectors can encode bias and domain mismatch, and the "
                "oracle budget prevents a prospective forecasting claim. This "
                "is not development or private-test performance."
            ),
        }
    )
    return result, audits


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
    parser.add_argument("--embeddings", required=True, type=Path)
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md",
    )
    parser.add_argument(
        "--neighborhood-implementation",
        type=Path,
        default=project / "analysis/analyze_neighborhood_additions.py",
    )
    parser.add_argument(
        "--inherited-audit",
        type=Path,
        default=project / "results/neighborhood_additions_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/semantic_neighborhood_additions_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/semantic_neighborhood_additions_train_audit.csv",
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
            args.embeddings,
            args.analysis_plan,
            args.neighborhood_implementation,
            args.inherited_audit,
            args.bootstrap_resamples,
        )
    except (OSError, csv.Error, gzip.BadGzipFile, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_semantic_neighborhood_additions: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_audit(args.audit_output, audit)
    print(
        "Wrote semantic-neighborhood Add analysis for "
        f"{result['cases']} cases to {args.output}"
    )
    print(f"Wrote {len(audit)} case audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
