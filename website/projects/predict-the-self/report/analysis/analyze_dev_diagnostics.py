#!/usr/bin/env python3
"""Diagnose paired development effects and limits of extractive prediction.

This analysis leaves the frozen prediction method unchanged. It imports the
pinned benchmark's authoritative evaluator, compares the stable-signifier
projection with repeat-2024 case by case, and quantifies lexical material in
the observed follow-up that no strictly extractive prediction can reproduce.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import random
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Callable


EXPECTED_DEV_SHA256 = (
    "afe74265475f1897161f54ac91395ded74d839e43236e8f4d189d91f9b40651a"
)
EXPECTED_EVALUATOR_SHA256 = (
    "1236dbcca70129f6200c2703dd67649dbfa760a2a7f74402fa1d3d956b97b2ae"
)
BOOTSTRAP_SEED = 20260917
BOOTSTRAP_RESAMPLES = 20_000
CONFIDENCE_LEVEL = 0.95


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_hash(path: Path, expected: str) -> None:
    observed = sha256(path)
    if observed != expected:
        raise ValueError(
            f"Unexpected SHA-256 for {path}: expected {expected}, observed {observed}"
        )


def load_evaluator(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("future_selves_evaluator", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load evaluator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def percentile(sorted_values: list[float], probability: float) -> float:
    """Return a linearly interpolated sample percentile (R type 7)."""
    if not sorted_values:
        raise ValueError("Cannot take a percentile of an empty sequence")
    position = (len(sorted_values) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return sorted_values[lower] + fraction * (
        sorted_values[upper] - sorted_values[lower]
    )


def bootstrap_mean_interval(
    values: list[float], resamples: int, rng: random.Random
) -> tuple[float, float]:
    if not values:
        raise ValueError("Cannot bootstrap an empty sequence")
    sample_size = len(values)
    means = sorted(
        sum(values[rng.randrange(sample_size)] for _ in range(sample_size))
        / sample_size
        for _ in range(resamples)
    )
    tail = (1 - CONFIDENCE_LEVEL) / 2
    return percentile(means, tail), percentile(means, 1 - tail)


def summarize_values(
    values: list[float], resamples: int, rng: random.Random
) -> dict[str, float]:
    low, high = bootstrap_mean_interval(values, resamples, rng)
    ordered = sorted(values)
    return {
        "mean": sum(values) / len(values),
        "median": percentile(ordered, 0.5),
        "case_bootstrap_95_ci_low": low,
        "case_bootstrap_95_ci_high": high,
        "minimum": ordered[0],
        "maximum": ordered[-1],
    }


def summarize_comparison(
    stable_values: list[float],
    repeat_values: list[float],
    higher_is_better: bool,
    resamples: int,
    rng: random.Random,
) -> dict[str, object]:
    if len(stable_values) != len(repeat_values) or not stable_values:
        raise ValueError("Paired metric vectors must have the same nonzero length")
    raw_differences = [
        stable - repeat
        for stable, repeat in zip(stable_values, repeat_values)
    ]
    utility_differences = (
        raw_differences
        if higher_is_better
        else [-difference for difference in raw_differences]
    )
    low, high = bootstrap_mean_interval(utility_differences, resamples, rng)
    tolerance = 1e-12
    return {
        "stable_mean": sum(stable_values) / len(stable_values),
        "repeat_2024_mean": sum(repeat_values) / len(repeat_values),
        "effect_definition": (
            "stable_minus_repeat_2024"
            if higher_is_better
            else "repeat_2024_error_minus_stable_error"
        ),
        "mean_effect_positive_favors_stable": sum(utility_differences)
        / len(utility_differences),
        "paired_case_bootstrap_95_ci_low": low,
        "paired_case_bootstrap_95_ci_high": high,
        "stable_case_wins": sum(value > tolerance for value in utility_differences),
        "case_ties": sum(abs(value) <= tolerance for value in utility_differences),
        "stable_case_losses": sum(value < -tolerance for value in utility_differences),
    }


def read_prediction_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        if reader.fieldnames != ["id", "predicted_tst_2025"]:
            raise ValueError(f"Unexpected prediction columns: {reader.fieldnames}")
        rows = list(reader)
    if any(None in row.values() for row in rows):
        raise ValueError("Prediction CSV has a missing field")
    return rows


def round_floats(value: object) -> object:
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, dict):
        return {key: round_floats(item) for key, item in value.items()}
    if isinstance(value, list):
        return [round_floats(item) for item in value]
    return value


def case_metric_vectors(
    sources: list[str],
    references: list[str],
    predictions: list[str],
    evaluator: ModuleType,
) -> dict[str, tuple[list[float], list[float], bool]]:
    agreement_functions: dict[str, Callable[[str, str], float]] = {
        "normalized_exact_match_rate": lambda prediction, reference: float(
            evaluator.normalize(prediction) == evaluator.normalize(reference)
        ),
        "normalized_edit_similarity": evaluator.normalized_edit_similarity,
        "token_jaccard_similarity": evaluator.token_jaccard_similarity,
        "token_overlap_f1": evaluator.token_overlap_f1,
        "rouge_l_f1": evaluator.rouge_l_f1,
        "character_ngram_f1": evaluator.character_ngram_f1,
    }
    vectors: dict[str, tuple[list[float], list[float], bool]] = {}
    for name, function in agreement_functions.items():
        vectors[name] = (
            [function(prediction, reference) for prediction, reference in zip(predictions, references)],
            [function(source, reference) for source, reference in zip(sources, references)],
            True,
        )

    vectors["word_count_mae"] = (
        [
            abs(len(evaluator.tokenize(prediction)) - len(evaluator.tokenize(reference)))
            for prediction, reference in zip(predictions, references)
        ],
        [
            abs(len(evaluator.tokenize(source)) - len(evaluator.tokenize(reference)))
            for source, reference in zip(sources, references)
        ],
        False,
    )
    vectors["line_count_mae"] = (
        [
            abs(evaluator.line_count(prediction) - evaluator.line_count(reference))
            for prediction, reference in zip(predictions, references)
        ],
        [
            abs(evaluator.line_count(source) - evaluator.line_count(reference))
            for source, reference in zip(sources, references)
        ],
        False,
    )
    observed_source_similarity = [
        evaluator.rouge_l_f1(reference, source)
        for reference, source in zip(references, sources)
    ]
    vectors["source_similarity_mae"] = (
        [
            abs(evaluator.rouge_l_f1(prediction, source) - observed)
            for prediction, source, observed in zip(
                predictions, sources, observed_source_similarity
            )
        ],
        [1 - observed for observed in observed_source_similarity],
        False,
    )
    return vectors


def extractive_diagnostics(
    sources: list[str], references: list[str], evaluator: ModuleType
) -> dict[str, list[float]]:
    diagnostics: dict[str, list[float]] = {
        "future_unique_token_novelty_fraction": [],
        "future_token_occurrence_unavailable_fraction": [],
        "source_unique_token_retention_fraction": [],
        "oracle_unique_token_jaccard_ceiling": [],
        "oracle_bag_of_words_f1_ceiling": [],
        "oracle_source_order_subsequence_rouge_l_f1_ceiling": [],
    }
    for source, reference in zip(sources, references):
        source_tokens = evaluator.tokenize(source)
        reference_tokens = evaluator.tokenize(reference)
        source_set = set(source_tokens)
        reference_set = set(reference_tokens)
        shared_types = source_set & reference_set
        diagnostics["future_unique_token_novelty_fraction"].append(
            1 - len(shared_types) / len(reference_set)
        )
        diagnostics["source_unique_token_retention_fraction"].append(
            len(shared_types) / len(source_set)
        )
        diagnostics["oracle_unique_token_jaccard_ceiling"].append(
            len(shared_types) / len(reference_set)
        )

        overlap_occurrences = sum(
            (Counter(source_tokens) & Counter(reference_tokens)).values()
        )
        occurrence_recall = overlap_occurrences / len(reference_tokens)
        diagnostics["future_token_occurrence_unavailable_fraction"].append(
            1 - occurrence_recall
        )
        diagnostics["oracle_bag_of_words_f1_ceiling"].append(
            evaluator.f1(1.0, occurrence_recall)
        )

        subsequence_recall = (
            evaluator.lcs_length(source_tokens, reference_tokens)
            / len(reference_tokens)
        )
        diagnostics["oracle_source_order_subsequence_rouge_l_f1_ceiling"].append(
            evaluator.f1(1.0, subsequence_recall)
        )
    return diagnostics


def analyze(
    benchmark_dir: Path,
    prediction_path: Path,
    resamples: int = BOOTSTRAP_RESAMPLES,
) -> dict[str, object]:
    development_path = benchmark_dir / "data/dev.csv"
    evaluator_path = benchmark_dir / "scripts/evaluate_predictions.py"
    require_hash(development_path, EXPECTED_DEV_SHA256)
    require_hash(evaluator_path, EXPECTED_EVALUATOR_SHA256)
    evaluator = load_evaluator(evaluator_path)

    _, development_rows = evaluator.read_csv(development_path)
    prediction_rows = read_prediction_rows(prediction_path)
    predictions_by_id = {row["id"]: row["predicted_tst_2025"] for row in prediction_rows}
    case_ids = [row["id"] for row in development_rows]
    if list(predictions_by_id) != case_ids:
        raise ValueError("Predictions must contain development IDs in reference order")

    sources = [row["tst_2024"] for row in development_rows]
    references = [row["tst_2025"] for row in development_rows]
    predictions = [predictions_by_id[case_id] for case_id in case_ids]
    rng = random.Random(BOOTSTRAP_SEED)

    comparisons = {
        name: summarize_comparison(stable, repeat, direction, resamples, rng)
        for name, (stable, repeat, direction) in case_metric_vectors(
            sources, references, predictions, evaluator
        ).items()
    }
    diagnostic_vectors = extractive_diagnostics(sources, references, evaluator)
    diagnostics = {
        name: summarize_values(values, resamples, rng)
        for name, values in diagnostic_vectors.items()
    }

    return round_floats(
        {
            "schema_version": 1,
            "analysis": "post_hoc_diagnostics_of_frozen_development_predictions",
            "cases": len(case_ids),
            "benchmark": {
                "commit": "9b6a766712583fec8d3182957260b1123fbfa146",
                "development_sha256": EXPECTED_DEV_SHA256,
                "evaluator_sha256": EXPECTED_EVALUATOR_SHA256,
                "prediction_sha256": sha256(prediction_path),
            },
            "bootstrap": {
                "unit": "paired development case",
                "resamples": resamples,
                "seed": BOOTSTRAP_SEED,
                "interval": "percentile",
                "confidence_level": CONFIDENCE_LEVEL,
                "interpretation": (
                    "Describes sensitivity to development-case composition; it is not "
                    "a population-generalization interval."
                ),
            },
            "paired_comparisons": comparisons,
            "extractive_limit_diagnostics": diagnostics,
            "oracle_warning": (
                "Oracle ceilings use observed follow-ups and are unattainable prospective "
                "diagnostics, not prediction results."
            ),
        }
    )


def parse_args() -> argparse.Namespace:
    project = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument(
        "--predictions",
        type=Path,
        default=project / "results/stable_signifier_dev_predictions.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project / "results/stable_signifier_dev_diagnostics.json",
    )
    parser.add_argument("--bootstrap-resamples", type=int, default=BOOTSTRAP_RESAMPLES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_resamples < 1:
        raise SystemExit("--bootstrap-resamples must be positive")
    try:
        result = analyze(args.benchmark_dir, args.predictions, args.bootstrap_resamples)
    except (OSError, csv.Error, ValueError, ImportError) as error:
        raise SystemExit(f"analyze_dev_diagnostics: {error}") from error
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote diagnostics for {result['cases']} cases to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
