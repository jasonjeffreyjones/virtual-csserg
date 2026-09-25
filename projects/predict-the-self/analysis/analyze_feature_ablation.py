#!/usr/bin/env python3
"""Ablate source text and demographics in probabilistic volume forecasts.

The analysis reuses the locked leave-one-out distributions while separating
their source representation into text-only, demographics-only, and combined
features. It writes training-cohort diagnostics only.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import Counter
from pathlib import Path
from types import ModuleType

import analyze_change_distributions as distributions
import analyze_change_volume as volume
import analyze_dev_diagnostics as shared
import trajectory_retrieval as retrieval


EXPECTED_PLAN_SHA256 = (
    "ed9fa67b2cc1265f3710471f96d7ffbfd16986b8295ef5072da26c263d8b7da4"
)
EXPECTED_DISTRIBUTIONS_SHA256 = (
    "22b68061f875c789009918c4984f4fc36ce7cd172131688fdaccff4eda87d68a"
)
EXPECTED_EXISTING_AUDIT_SHA256 = (
    "0c257335a92538e2e0eb223c39c10c49d3f8204888e77590a0bcf7e23a8edff7"
)
BOOTSTRAP_SEED = 20260925
BOOTSTRAP_RESAMPLES = 20_000
REPRESENTATIONS = ("text_only", "demographics_only", "combined")
METHODS = ("marginal",) + REPRESENTATIONS
COMPARISONS = (
    ("marginal_minus_text_only", "marginal", "text_only"),
    (
        "marginal_minus_demographics_only",
        "marginal",
        "demographics_only",
    ),
    ("text_only_minus_combined", "text_only", "combined"),
    (
        "demographics_only_minus_combined",
        "demographics_only",
        "combined",
    ),
)
OUTCOMES = volume.OUTCOMES
PRIMARY_OUTCOME = "word_count"
BASE_AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "source_word_count",
    "source_line_count",
    *(f"mean_{representation}_neighbor_cosine_similarity" for representation in REPRESENTATIONS),
]
AUDIT_FIELDS = BASE_AUDIT_FIELDS + [
    field
    for outcome in OUTCOMES
    for field in (
        f"{outcome}_observed",
        *(f"{outcome}_{method}_crps" for method in METHODS),
    )
]


def feature_counts(row: dict[str, str], representation: str) -> Counter[str]:
    """Return one fixed ablation of the inherited feature representation."""
    if representation not in REPRESENTATIONS:
        raise ValueError(f"Unknown representation: {representation}")
    counts: Counter[str] = Counter()
    if representation in {"text_only", "combined"}:
        counts.update(retrieval.tokenize(row["tst_2024"]))
    if representation in {"demographics_only", "combined"}:
        for field in retrieval.DEMOGRAPHIC_FIELDS:
            value = retrieval.normalized_metadata(row.get(field, ""))
            if value:
                counts[f"metadata::{field}::{value}"] += 1
    return counts


def select_neighbors(
    query: dict[str, str],
    training_rows: list[dict[str, str]],
    count: int,
    representation: str,
) -> tuple[list[int], list[float]]:
    """Select fold neighbors under one fixed feature ablation."""
    if count < 1 or count > len(training_rows):
        raise ValueError("Neighbor count must be within the training-fold size")
    counts = [feature_counts(row, representation) for row in training_rows]
    idf = retrieval.fit_idf(counts)
    vectors = [retrieval.vectorize(features, idf) for features in counts]
    query_vector, query_norm = retrieval.vectorize(
        feature_counts(query, representation), idf
    )
    similarities = [
        retrieval.cosine_similarity(query_vector, query_norm, vector, norm)
        for vector, norm in vectors
    ]
    indices = sorted(
        range(len(training_rows)), key=lambda index: (-similarities[index], index)
    )[:count]
    return indices, [similarities[index] for index in indices]


def leave_one_out_scores(
    rows: list[dict[str, str]],
    evaluator: ModuleType,
    neighbor_count: int = volume.NEIGHBOR_COUNT,
    neighbor_effective_weight: float = volume.NEIGHBOR_EFFECTIVE_WEIGHT,
    prior_weight: float = volume.PRIOR_WEIGHT,
) -> list[dict[str, object]]:
    """Score every fixed representation without held-out future leakage."""
    volume.validate_rows(rows, neighbor_count)
    quantities = [volume.case_quantities(row, evaluator) for row in rows]
    audits: list[dict[str, object]] = []

    for held_out_index, (row, held_out) in enumerate(zip(rows, quantities)):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1 :]
        fold_quantities = quantities[:held_out_index] + quantities[held_out_index + 1 :]
        representation_neighbors: dict[str, tuple[list[int], list[float]]] = {}
        audit: dict[str, object] = {
            "id": row["id"],
            "source_unique_tokens": held_out["source_unique_tokens"],
            "source_word_count": held_out["source_word_count"],
            "source_line_count": held_out["source_line_count"],
        }
        for representation in REPRESENTATIONS:
            indices, similarities = select_neighbors(
                row, fold_rows, neighbor_count, representation
            )
            representation_neighbors[representation] = (indices, similarities)
            audit[f"mean_{representation}_neighbor_cosine_similarity"] = (
                sum(similarities) / len(similarities)
            )

        prior_case_weight = prior_weight / len(fold_rows)
        for outcome in OUTCOMES:
            fold_values = [
                float(candidate["modeled"][outcome]) for candidate in fold_quantities
            ]
            transformed = [
                volume.outcome_scale(outcome, value, held_out) for value in fold_values
            ]
            marginal_support, marginal_weights = distributions.normalize_distribution(
                transformed, [1.0] * len(transformed)
            )
            observed = float(held_out["observed"][outcome])
            audit[f"{outcome}_observed"] = observed
            audit[f"{outcome}_marginal_crps"] = distributions.empirical_crps(
                marginal_support, marginal_weights, observed
            )

            for representation, (indices, similarities) in (
                representation_neighbors.items()
            ):
                neighbor_weights = volume.normalized_neighbor_weights(
                    similarities, neighbor_effective_weight
                )
                support, weights = distributions.normalize_distribution(
                    transformed + [transformed[index] for index in indices],
                    [prior_case_weight] * len(transformed) + neighbor_weights,
                )
                audit[f"{outcome}_{representation}_crps"] = (
                    distributions.empirical_crps(support, weights, observed)
                )
        audits.append(audit)
    return audits


def require_existing_replication(
    audits: list[dict[str, object]], existing_audit_path: Path
) -> None:
    """Require the new marginal and combined scores to replicate the lock."""
    shared.require_hash(existing_audit_path, EXPECTED_EXISTING_AUDIT_SHA256)
    with existing_audit_path.open("r", encoding="utf-8", newline="") as handle:
        existing = list(csv.DictReader(handle, strict=True))
    if len(existing) != len(audits):
        raise ValueError("Existing distribution audit has a different row count")
    for current, prior in zip(audits, existing):
        if current["id"] != prior["id"]:
            raise ValueError("Existing distribution audit case order differs")
        for outcome in OUTCOMES:
            for current_method, prior_method in (
                ("marginal", "marginal"),
                ("combined", "neighborhood"),
            ):
                current_value = float(current[f"{outcome}_{current_method}_crps"])
                prior_value = float(prior[f"{outcome}_{prior_method}_crps"])
                if not math.isclose(
                    current_value, prior_value, rel_tol=0.0, abs_tol=5e-7
                ):
                    raise ValueError(
                        "Existing distribution audit did not reproduce for "
                        f"{current['id']} {outcome} {current_method}: "
                        f"{current_value} versus {prior_value}"
                    )


def paired_summary(
    audits: list[dict[str, object]], outcome: str, first: str, second: str
) -> dict[str, object]:
    """Summarize first-minus-second CRPS; positive favors the second method."""
    differences = [
        float(row[f"{outcome}_{first}_crps"])
        - float(row[f"{outcome}_{second}_crps"])
        for row in audits
    ]
    low, high = shared.bootstrap_mean_interval(
        differences, BOOTSTRAP_RESAMPLES, random.Random(BOOTSTRAP_SEED)
    )
    tolerance = 1e-12
    return {
        "effect_definition": f"{first}_crps_minus_{second}_crps",
        "mean_effect_positive_favors_second_method": sum(differences)
        / len(differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "second_method_case_wins": sum(value > tolerance for value in differences),
        "case_ties": sum(abs(value) <= tolerance for value in differences),
        "second_method_case_losses": sum(value < -tolerance for value in differences),
    }


def summarize_outcome(
    audits: list[dict[str, object]], outcome: str
) -> dict[str, object]:
    """Return mean CRPS and all four locked paired comparisons."""
    return {
        "role": "primary" if outcome == PRIMARY_OUTCOME else "secondary",
        "mean_crps": {
            method: sum(float(row[f"{outcome}_{method}_crps"]) for row in audits)
            / len(audits)
            for method in METHODS
        },
        "paired_comparisons": {
            name: paired_summary(audits, outcome, first, second)
            for name, first, second in COMPARISONS
        },
    }


def analyze(
    benchmark_dir: Path,
    plan_path: Path,
    distributions_path: Path,
    existing_audit_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the hash-guarded ablation and return result plus complete audit."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, volume.EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(distributions_path, EXPECTED_DISTRIBUTIONS_SHA256)
    shared.require_hash(
        Path(volume.__file__), distributions.EXPECTED_CHANGE_VOLUME_SHA256
    )
    shared.require_hash(Path(retrieval.__file__), volume.EXPECTED_RETRIEVAL_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    audits = leave_one_out_scores(rows, evaluator)
    require_existing_replication(audits, existing_audit_path)
    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_source_feature_ablation",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": volume.EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "change_distributions_implementation_sha256": (
                EXPECTED_DISTRIBUTIONS_SHA256
            ),
            "change_volume_implementation_sha256": (
                distributions.EXPECTED_CHANGE_VOLUME_SHA256
            ),
            "retrieval_feature_implementation_sha256": (
                volume.EXPECTED_RETRIEVAL_SHA256
            ),
            "existing_distribution_audit_sha256": EXPECTED_EXISTING_AUDIT_SHA256,
        },
        "design": {
            "primary_outcome": PRIMARY_OUTCOME,
            "secondary_outcomes": [
                outcome for outcome in OUTCOMES if outcome != PRIMARY_OUTCOME
            ],
            "representations": {
                "text_only": "case-folded word tokens from tst_2024",
                "demographics_only": (
                    "ten field-qualified normalized 2024 demographic values"
                ),
                "combined": "unchanged union of text and demographic features",
            },
            "training_cases_per_fold": len(rows) - 1,
            "neighbor_count": volume.NEIGHBOR_COUNT,
            "neighbor_effective_weight": volume.NEIGHBOR_EFFECTIVE_WEIGHT,
            "fold_prior_effective_weight": volume.PRIOR_WEIGHT,
            "probabilistic_score": "weighted empirical CRPS",
            "future_information_used_for_prediction": "none",
        },
        "mean_selected_neighbor_cosine_similarity": {
            representation: volume.descriptive(
                [
                    float(
                        row[
                            f"mean_{representation}_neighbor_cosine_similarity"
                        ]
                    )
                    for row in audits
                ]
            )
            for representation in REPRESENTATIONS
        },
        "existing_combined_and_marginal_audit_reproduced": True,
        "outcomes": {
            outcome: summarize_outcome(audits, outcome) for outcome in OUTCOMES
        },
        "bootstrap": {
            "unit": "paired training case",
            "resamples": BOOTSTRAP_RESAMPLES,
            "seed_restarted_for_each_outcome_and_comparison": BOOTSTRAP_SEED,
            "interval": "percentile",
            "confidence_level": shared.CONFIDENCE_LEVEL,
            "multiplicity_adjustment": "none; secondary outcomes are diagnostic",
        },
        "claim_boundary": (
            "This dependent, locked training-cohort diagnostic decomposes a "
            "previously observed revision-volume result. It is not untouched "
            "confirmation, population evidence, development performance, "
            "private-test performance, or a forecast of correct future content."
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
        default=project / "ANALYSIS_PLAN_FEATURE_ABLATION.md",
    )
    parser.add_argument(
        "--change-distributions-implementation",
        type=Path,
        default=project / "analysis/analyze_change_distributions.py",
    )
    parser.add_argument(
        "--existing-distribution-audit",
        type=Path,
        default=project / "results/change_distributions_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/feature_ablation_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/feature_ablation_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            args.change_distributions_implementation,
            args.existing_distribution_audit,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_feature_ablation: {error}") from error
    print(f"Wrote feature ablation for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
