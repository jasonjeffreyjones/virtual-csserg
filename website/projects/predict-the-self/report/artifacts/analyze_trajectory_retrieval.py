#!/usr/bin/env python3
"""Evaluate matched-trajectory retrieval under its locked analysis plan."""

from __future__ import annotations

import argparse
import concurrent.futures
import csv
import json
import random
from collections import Counter
from pathlib import Path
from types import ModuleType

import analyze_dev_diagnostics as shared


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_STABLE_PREDICTIONS_SHA256 = (
    "0b43ad574543cb128fa51470432467a34998c675b945665bb44141d6e04bca39"
)
EXPECTED_PLAN_SHA256 = (
    "86b2ddfe775773e1964beeefbac5479d88f6c46cd3385bf3a992fc7ae64e9c83"
)
BOOTSTRAP_SEED = 20260918
BOOTSTRAP_RESAMPLES = 20_000


def read_development(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def prediction_texts(path: Path, case_ids: list[str]) -> list[str]:
    rows = shared.read_prediction_rows(path)
    indexed = {row["id"]: row["predicted_tst_2025"] for row in rows}
    if list(indexed) != case_ids:
        raise ValueError(f"Predictions in {path} must follow development ID order")
    return [indexed[case_id] for case_id in case_ids]


def summarize_pair(
    focal_values: list[float],
    comparator_values: list[float],
    higher_is_better: bool,
    focal_name: str,
    comparator_name: str,
    rng: random.Random,
    resamples: int,
) -> dict[str, object]:
    raw = [focal - comparator for focal, comparator in zip(focal_values, comparator_values)]
    utility = raw if higher_is_better else [-value for value in raw]
    low, high = shared.bootstrap_mean_interval(utility, resamples, rng)
    tolerance = 1e-12
    return {
        f"{focal_name}_mean": sum(focal_values) / len(focal_values),
        f"{comparator_name}_mean": sum(comparator_values) / len(comparator_values),
        "effect_definition": (
            f"{focal_name}_minus_{comparator_name}"
            if higher_is_better
            else f"{comparator_name}_error_minus_{focal_name}_error"
        ),
        f"mean_effect_positive_favors_{focal_name}": sum(utility) / len(utility),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        f"{focal_name}_case_wins": sum(value > tolerance for value in utility),
        "case_ties": sum(abs(value) <= tolerance for value in utility),
        f"{focal_name}_case_losses": sum(value < -tolerance for value in utility),
    }


def unique_novelty(prediction: str, source: str, evaluator: ModuleType) -> float:
    predicted = set(evaluator.tokenize(prediction))
    if not predicted:
        return 0.0
    return len(predicted - set(evaluator.tokenize(source))) / len(predicted)


def occurrence_novelty(prediction: str, source: str, evaluator: ModuleType) -> float:
    predicted = Counter(evaluator.tokenize(prediction))
    if not predicted:
        return 0.0
    available = sum((predicted & Counter(evaluator.tokenize(source))).values())
    return 1 - available / sum(predicted.values())


def novel_type_recovery(
    prediction: str, source: str, reference: str, evaluator: ModuleType
) -> tuple[float, float, float]:
    source_types = set(evaluator.tokenize(source))
    predicted_novel = set(evaluator.tokenize(prediction)) - source_types
    observed_novel = set(evaluator.tokenize(reference)) - source_types
    overlap = len(predicted_novel & observed_novel)
    precision = overlap / len(predicted_novel) if predicted_novel else 0.0
    recall = overlap / len(observed_novel) if observed_novel else 0.0
    return precision, recall, evaluator.f1(precision, recall)


def method_metric_bundle(
    evaluator_path: Path,
    sources: list[str],
    references: list[str],
    predictions: list[str],
) -> dict[str, object]:
    """Calculate one method's authoritative per-case and descriptive metrics."""
    evaluator = shared.load_evaluator(evaluator_path)
    agreement_functions = {
        "normalized_exact_match_rate": lambda prediction, reference: float(
            evaluator.normalize(prediction) == evaluator.normalize(reference)
        ),
        "normalized_edit_similarity": evaluator.normalized_edit_similarity,
        "token_jaccard_similarity": evaluator.token_jaccard_similarity,
        "token_overlap_f1": evaluator.token_overlap_f1,
        "rouge_l_f1": evaluator.rouge_l_f1,
        "character_ngram_f1": evaluator.character_ngram_f1,
    }
    vectors = {
        name: [
            function(prediction, reference)
            for prediction, reference in zip(predictions, references)
        ]
        for name, function in agreement_functions.items()
    }
    vectors["word_count_mae"] = [
        abs(len(evaluator.tokenize(prediction)) - len(evaluator.tokenize(reference)))
        for prediction, reference in zip(predictions, references)
    ]
    vectors["line_count_mae"] = [
        abs(evaluator.line_count(prediction) - evaluator.line_count(reference))
        for prediction, reference in zip(predictions, references)
    ]
    prediction_source = [
        evaluator.rouge_l_f1(prediction, source)
        for prediction, source in zip(predictions, sources)
    ]
    observed_source = [
        evaluator.rouge_l_f1(reference, source)
        for reference, source in zip(references, sources)
    ]
    vectors["source_similarity_mae"] = [
        abs(predicted - observed)
        for predicted, observed in zip(prediction_source, observed_source)
    ]
    descriptive = {
        "prediction_word_count_mean": sum(
            len(evaluator.tokenize(text)) for text in predictions
        )
        / len(predictions),
        "reference_word_count_mean": sum(
            len(evaluator.tokenize(text)) for text in references
        )
        / len(references),
        "prediction_repeat_2024_rate": sum(
            evaluator.normalize(prediction) == evaluator.normalize(source)
            for prediction, source in zip(predictions, sources)
        )
        / len(predictions),
        "observed_repeat_2024_rate": sum(
            evaluator.normalize(reference) == evaluator.normalize(source)
            for reference, source in zip(references, sources)
        )
        / len(references),
        "prediction_source_similarity_mean": sum(prediction_source)
        / len(prediction_source),
        "observed_source_similarity_mean": sum(observed_source) / len(observed_source),
    }
    return {"vectors": vectors, "descriptive": descriptive}


def make_scorecard(
    retrieval_path: Path,
    development_path: Path,
    retrieval_bundle: dict[str, object],
    evaluator: ModuleType,
) -> dict[str, object]:
    vectors = retrieval_bundle["vectors"]
    descriptive = retrieval_bundle["descriptive"]
    values = {
        **{name: sum(items) / len(items) for name, items in vectors.items()},
        **descriptive,
    }
    return {
        "cases": len(next(iter(vectors.values()))),
        "predictions": str(retrieval_path),
        "references": str(development_path),
        "metrics": {
            name: {
                "value": round(values[name], 6),
                "group": evaluator.METRIC_INFO[name][0],
                "direction": evaluator.METRIC_INFO[name][1],
                "description": evaluator.METRIC_INFO[name][2],
            }
            for name in evaluator.METRIC_INFO
        },
    }


def analyze(
    benchmark_dir: Path,
    retrieval_path: Path,
    stable_path: Path,
    plan_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> tuple[dict[str, object], dict[str, object]]:
    training_path = benchmark_dir / "data/train.csv"
    development_path = benchmark_dir / "data/dev.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    shared.require_hash(training_path, EXPECTED_TRAIN_SHA256)
    shared.require_hash(development_path, shared.EXPECTED_DEV_SHA256)
    shared.require_hash(evaluator_path, shared.EXPECTED_EVALUATOR_SHA256)
    shared.require_hash(stable_path, EXPECTED_STABLE_PREDICTIONS_SHA256)
    shared.require_hash(plan_path, EXPECTED_PLAN_SHA256)
    evaluator = shared.load_evaluator(evaluator_path)

    development_rows = read_development(development_path)
    case_ids = [row["id"] for row in development_rows]
    sources = [row["tst_2024"] for row in development_rows]
    references = [row["tst_2025"] for row in development_rows]
    method_predictions = {
        "trajectory_retrieval": prediction_texts(retrieval_path, case_ids),
        "stable_projection": prediction_texts(stable_path, case_ids),
        "repeat_2024": sources,
    }

    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures = {
            method: executor.submit(
                method_metric_bundle,
                evaluator_path,
                sources,
                references,
                predictions,
            )
            for method, predictions in method_predictions.items()
        }
        metric_bundles = {method: future.result() for method, future in futures.items()}

    directional_vectors: dict[str, dict[str, list[float]]] = {}
    for method, bundle in metric_bundles.items():
        for metric, values in bundle["vectors"].items():
            directional_vectors.setdefault(metric, {})[method] = values
    directions = {
        metric: evaluator.METRIC_INFO[metric][1] == "higher"
        for metric in directional_vectors
    }

    rng = random.Random(BOOTSTRAP_SEED)
    comparisons: dict[str, object] = {}
    for comparator in ("stable_projection", "repeat_2024"):
        comparisons[f"trajectory_retrieval_vs_{comparator}"] = {
            metric: summarize_pair(
                method_values["trajectory_retrieval"],
                method_values[comparator],
                directions[metric],
                "trajectory_retrieval",
                comparator,
                rng,
                resamples,
            )
            for metric, method_values in directional_vectors.items()
        }

    observed_unique = [
        unique_novelty(reference, source, evaluator)
        for source, reference in zip(sources, references)
    ]
    observed_occurrence = [
        occurrence_novelty(reference, source, evaluator)
        for source, reference in zip(sources, references)
    ]
    novelty: dict[str, object] = {
        "observed_follow_up": {
            "unique_token_novelty": shared.summarize_values(
                observed_unique, resamples, rng
            ),
            "token_occurrence_novelty": shared.summarize_values(
                observed_occurrence, resamples, rng
            ),
        }
    }
    for method, predictions in method_predictions.items():
        unique_values = [
            unique_novelty(prediction, source, evaluator)
            for prediction, source in zip(predictions, sources)
        ]
        occurrence_values = [
            occurrence_novelty(prediction, source, evaluator)
            for prediction, source in zip(predictions, sources)
        ]
        recovery = [
            novel_type_recovery(prediction, source, reference, evaluator)
            for prediction, source, reference in zip(predictions, sources, references)
        ]
        novelty[method] = {
            "unique_token_novelty": shared.summarize_values(
                unique_values, resamples, rng
            ),
            "token_occurrence_novelty": shared.summarize_values(
                occurrence_values, resamples, rng
            ),
            "unique_token_novelty_mae": sum(
                abs(predicted - observed)
                for predicted, observed in zip(unique_values, observed_unique)
            )
            / len(unique_values),
            "novel_type_precision": shared.summarize_values(
                [item[0] for item in recovery], resamples, rng
            ),
            "novel_type_recall": shared.summarize_values(
                [item[1] for item in recovery], resamples, rng
            ),
            "novel_type_f1": shared.summarize_values(
                [item[2] for item in recovery], resamples, rng
            ),
        }

    scorecard = make_scorecard(
        retrieval_path,
        development_path,
        metric_bundles["trajectory_retrieval"],
        evaluator,
    )
    result = shared.round_floats(
        {
            "schema_version": 1,
            "analysis": "locked_exploratory_trajectory_retrieval_comparison",
            "cases": len(case_ids),
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "training_sha256": EXPECTED_TRAIN_SHA256,
                "development_sha256": shared.EXPECTED_DEV_SHA256,
                "evaluator_sha256": shared.EXPECTED_EVALUATOR_SHA256,
                "stable_prediction_sha256": EXPECTED_STABLE_PREDICTIONS_SHA256,
                "retrieval_prediction_sha256": shared.sha256(retrieval_path),
                "analysis_plan_sha256": EXPECTED_PLAN_SHA256,
            },
            "bootstrap": {
                "unit": "paired development case",
                "resamples": resamples,
                "seed": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": shared.CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to development-case composition; it is not "
                    "a population-generalization interval."
                ),
            },
            "trajectory_retrieval_scorecard": scorecard["metrics"],
            "paired_comparisons": comparisons,
            "novelty_diagnostics": novelty,
            "claim_boundary": (
                "Development labels were examined in prior iterations. This locked "
                "comparison is exploratory and is not a private-test result."
            ),
        }
    )
    return result, scorecard


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--retrieval-predictions",
        type=Path,
        default=project / "results/trajectory_retrieval_dev_predictions.csv",
    )
    parser.add_argument(
        "--stable-predictions",
        type=Path,
        default=project / "results/stable_signifier_dev_predictions.csv",
    )
    parser.add_argument(
        "--analysis-plan",
        type=Path,
        default=project / "ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/trajectory_retrieval_dev_analysis.json",
    )
    parser.add_argument(
        "--scorecard-output",
        type=Path,
        default=project / "results/trajectory_retrieval_dev_scorecard.json",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result, scorecard = analyze(
            args.benchmark_dir,
            args.retrieval_predictions,
            args.stable_predictions,
            args.analysis_plan,
            args.bootstrap_resamples,
        )
    except (OSError, csv.Error, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_trajectory_retrieval: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    args.scorecard_output.write_text(
        json.dumps(scorecard, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote locked analysis for {result['cases']} cases to {args.output}")
    print(f"Wrote complete official scorecard to {args.scorecard_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
