#!/usr/bin/env python3
"""Compare lexical and count-only source neighborhoods for volume forecasts.

This locked training-only diagnostic asks whether text-only word-count CRPS
skill exceeds matching on the observable form of the earlier response. It
never reads or writes development or private-test predictions.
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

import analyze_change_distributions as distributions
import analyze_change_volume as volume
import analyze_dev_diagnostics as shared
import analyze_feature_ablation as feature_ablation


EXPECTED_PLAN_SHA256 = (
    "5ffaf6b8289a360926da3ae3b1398a336949e698c6157f8ba94ef316ec63c5ad"
)
EXPECTED_FEATURE_ABLATION_SHA256 = (
    "5d745bad7af9e1498e494e841a9bceb08945a068789de8410dfcdbf899e0d3d3"
)
EXPECTED_FEATURE_AUDIT_SHA256 = (
    "423582b332c74841347c763f2638aed1a22e4a9036b0f30175b7b74348aa6987"
)
BOOTSTRAP_SEED = 20260926
BOOTSTRAP_RESAMPLES = 20_000
METHODS = ("marginal", "source_form_only", "text_only")
COMPARISONS = (
    (
        "marginal_minus_source_form_only",
        "marginal",
        "source_form_only",
    ),
    ("marginal_minus_text_only", "marginal", "text_only"),
    (
        "source_form_only_minus_text_only",
        "source_form_only",
        "text_only",
    ),
)
OUTCOMES = volume.OUTCOMES
PRIMARY_OUTCOME = "word_count"
PRIMARY_COMPARISON = "source_form_only_minus_text_only"
FORM_FEATURES = ("log_word_count", "log_unique_token_count", "log_line_count")
BASE_AUDIT_FIELDS = [
    "id",
    "source_unique_tokens",
    "source_word_count",
    "source_line_count",
    "mean_source_form_neighbor_similarity",
    "mean_text_only_neighbor_cosine_similarity",
]
AUDIT_FIELDS = BASE_AUDIT_FIELDS + [
    field
    for outcome in OUTCOMES
    for field in (
        f"{outcome}_observed",
        *(f"{outcome}_{method}_crps" for method in METHODS),
    )
]


def source_form_features(
    row: dict[str, str], evaluator: ModuleType
) -> tuple[float, float, float]:
    """Return log-scaled counts from the source response and nothing else."""
    tokens = evaluator.tokenize(row["tst_2024"])
    line_count = evaluator.line_count(row["tst_2024"])
    if not tokens or line_count < 1:
        raise ValueError("Source response must contain a token and a nonblank line")
    return (
        math.log1p(len(tokens)),
        math.log1p(len(set(tokens))),
        math.log1p(line_count),
    )


def feature_scales(
    vectors: list[tuple[float, float, float]],
) -> tuple[float, float, float]:
    """Fit fold-only population standard deviations with a safe fallback."""
    if not vectors:
        raise ValueError("Cannot scale an empty source-form fold")
    scales = []
    for index in range(len(FORM_FEATURES)):
        scale = statistics.pstdev(vector[index] for vector in vectors)
        scales.append(scale if scale > 0 else 1.0)
    return tuple(scales)  # type: ignore[return-value]


def select_source_form_neighbors(
    query: dict[str, str],
    training_rows: list[dict[str, str]],
    count: int,
    evaluator: ModuleType,
) -> tuple[list[int], list[float]]:
    """Select the fixed count-only response-form neighborhood."""
    if count < 1 or count > len(training_rows):
        raise ValueError("Neighbor count must be within the training-fold size")
    vectors = [source_form_features(row, evaluator) for row in training_rows]
    query_vector = source_form_features(query, evaluator)
    scales = feature_scales(vectors)
    similarities = []
    for vector in vectors:
        distance = math.sqrt(
            sum(
                ((query_value - candidate_value) / scale) ** 2
                for query_value, candidate_value, scale in zip(
                    query_vector, vector, scales
                )
            )
        )
        similarities.append(1.0 / (1.0 + distance))
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
    """Score marginal, source-form, and lexical predictive distributions."""
    volume.validate_rows(rows, neighbor_count)
    quantities = [volume.case_quantities(row, evaluator) for row in rows]
    audits: list[dict[str, object]] = []

    for held_out_index, (row, held_out) in enumerate(zip(rows, quantities)):
        fold_rows = rows[:held_out_index] + rows[held_out_index + 1 :]
        fold_quantities = quantities[:held_out_index] + quantities[held_out_index + 1 :]
        form_indices, form_similarities = select_source_form_neighbors(
            row, fold_rows, neighbor_count, evaluator
        )
        text_indices, text_similarities = feature_ablation.select_neighbors(
            row, fold_rows, neighbor_count, "text_only"
        )
        method_neighbors = {
            "source_form_only": (form_indices, form_similarities),
            "text_only": (text_indices, text_similarities),
        }
        audit: dict[str, object] = {
            "id": row["id"],
            "source_unique_tokens": held_out["source_unique_tokens"],
            "source_word_count": held_out["source_word_count"],
            "source_line_count": held_out["source_line_count"],
            "mean_source_form_neighbor_similarity": (
                sum(form_similarities) / len(form_similarities)
            ),
            "mean_text_only_neighbor_cosine_similarity": (
                sum(text_similarities) / len(text_similarities)
            ),
        }
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

            for method, (indices, similarities) in method_neighbors.items():
                neighbor_weights = volume.normalized_neighbor_weights(
                    similarities, neighbor_effective_weight
                )
                support, weights = distributions.normalize_distribution(
                    transformed + [transformed[index] for index in indices],
                    [prior_case_weight] * len(transformed) + neighbor_weights,
                )
                audit[f"{outcome}_{method}_crps"] = distributions.empirical_crps(
                    support, weights, observed
                )
        audits.append(audit)
    return audits


def require_feature_ablation_replication(
    audits: list[dict[str, object]], existing_audit_path: Path
) -> None:
    """Require marginal and text-only scores to reproduce the preceding lock."""
    shared.require_hash(existing_audit_path, EXPECTED_FEATURE_AUDIT_SHA256)
    with existing_audit_path.open("r", encoding="utf-8", newline="") as handle:
        existing = list(csv.DictReader(handle, strict=True))
    if len(existing) != len(audits):
        raise ValueError("Existing feature-ablation audit has a different row count")
    for current, prior in zip(audits, existing):
        if current["id"] != prior["id"]:
            raise ValueError("Existing feature-ablation audit case order differs")
        for field in (
            "source_unique_tokens",
            "source_word_count",
            "source_line_count",
            "mean_text_only_neighbor_cosine_similarity",
        ):
            if not math.isclose(
                float(current[field]), float(prior[field]), rel_tol=0.0, abs_tol=5e-7
            ):
                raise ValueError(
                    f"Existing feature-ablation audit did not reproduce {field} "
                    f"for {current['id']}"
                )
        for outcome in OUTCOMES:
            for method in ("marginal", "text_only"):
                field = f"{outcome}_{method}_crps"
                if not math.isclose(
                    float(current[field]),
                    float(prior[field]),
                    rel_tol=0.0,
                    abs_tol=5e-7,
                ):
                    raise ValueError(
                        "Existing feature-ablation audit did not reproduce "
                        f"{field} for {current['id']}"
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
    """Return mean CRPS and all three locked paired comparisons."""
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
    feature_ablation_path: Path,
    existing_audit_path: Path,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Run the hash-guarded source-form comparison."""
    training_path = benchmark_dir / "data/train.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, volume.EXPECTED_TRAIN_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    shared.require_hash(feature_ablation_path, EXPECTED_FEATURE_ABLATION_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)
    _, rows = evaluator.read_csv(training_path)
    audits = leave_one_out_scores(rows, evaluator)
    require_feature_ablation_replication(audits, existing_audit_path)
    result = {
        "schema_version": 1,
        "analysis": "training_leave_one_out_source_form_ablation",
        "cases": len(rows),
        "benchmark": {
            "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
            "training_sha256": volume.EXPECTED_TRAIN_SHA256,
            "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
            "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            "feature_ablation_implementation_sha256": (
                EXPECTED_FEATURE_ABLATION_SHA256
            ),
            "feature_ablation_audit_sha256": EXPECTED_FEATURE_AUDIT_SHA256,
        },
        "design": {
            "primary_outcome": PRIMARY_OUTCOME,
            "primary_comparison": PRIMARY_COMPARISON,
            "secondary_outcomes": [
                outcome for outcome in OUTCOMES if outcome != PRIMARY_OUTCOME
            ],
            "source_form_features": list(FORM_FEATURES),
            "source_form_scaling": "fold-fit population standard deviation",
            "source_form_similarity": "1 / (1 + standardized Euclidean distance)",
            "text_representation": "case-folded word-token TF-IDF from tst_2024",
            "training_cases_per_fold": len(rows) - 1,
            "neighbor_count": volume.NEIGHBOR_COUNT,
            "neighbor_effective_weight": volume.NEIGHBOR_EFFECTIVE_WEIGHT,
            "fold_prior_effective_weight": volume.PRIOR_WEIGHT,
            "probabilistic_score": "weighted empirical CRPS",
            "future_information_used_for_prediction": "none",
        },
        "mean_selected_neighbor_similarity": {
            "source_form_only": volume.descriptive(
                [
                    float(row["mean_source_form_neighbor_similarity"])
                    for row in audits
                ]
            ),
            "text_only_cosine": volume.descriptive(
                [
                    float(row["mean_text_only_neighbor_cosine_similarity"])
                    for row in audits
                ]
            ),
        },
        "existing_marginal_and_text_only_audit_reproduced": True,
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
            "This dependent, locked training-cohort diagnostic compares one "
            "lexical neighborhood with one count-only source-form neighborhood. "
            "It is not untouched confirmation, evidence of a semantic or causal "
            "mechanism, population evidence, development performance, private-test "
            "performance, or a forecast of correct future content."
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
        default=project / "ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md",
    )
    parser.add_argument(
        "--feature-ablation-implementation",
        type=Path,
        default=project / "analysis/analyze_feature_ablation.py",
    )
    parser.add_argument(
        "--existing-feature-audit",
        type=Path,
        default=project / "results/feature_ablation_train_audit.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/source_form_ablation_train_analysis.json",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=project / "results/source_form_ablation_train_audit.csv",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result, audit = analyze(
            args.benchmark_dir,
            args.analysis_plan,
            args.feature_ablation_implementation,
            args.existing_feature_audit,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        write_audit(args.audit_output, audit)
    except (OSError, csv.Error, KeyError, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_source_form_ablation: {error}") from error
    print(f"Wrote source-form ablation for {result['cases']} cases to {args.output}")
    print(f"Wrote {len(audit)} audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
