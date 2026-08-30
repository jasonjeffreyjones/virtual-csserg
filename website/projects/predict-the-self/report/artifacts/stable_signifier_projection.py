#!/usr/bin/env python3
"""Generate a deterministic stable-signifier Future Selves submission.

The model learns document-level token retention rates from the public training
pairs. It ranks source response units by their tokens' smoothed retention
rates, predicts follow-up word count with a training-only ordinary least
squares regression, and retains the highest-ranked units up to that target.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path


TOKEN_RE = re.compile(r"\w+(?:['\N{RIGHT SINGLE QUOTATION MARK}]\w+)*", re.UNICODE)
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")
COMMA_BOUNDARY_RE = re.compile(r"\s*,\s*")
STOP_TOKENS = {
    "a",
    "am",
    "an",
    "and",
    "i",
    "in",
    "is",
    "my",
    "of",
    "person",
    "someone",
    "the",
    "to",
    "who",
}
PREDICTION_FIELDS = ["id", "predicted_tst_2025"]


def tokenize(text: str) -> list[str]:
    """Match the shared evaluator's case-folded Unicode word tokens."""
    return TOKEN_RE.findall(" ".join(text.casefold().split()))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def write_predictions(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PREDICTION_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def response_units(text: str) -> list[str]:
    """Split a response at its strongest available repeated boundary."""
    lines = [unit.strip() for unit in text.splitlines() if unit.strip()]
    if len(lines) >= 3:
        return lines
    sentences = [unit.strip() for unit in SENTENCE_BOUNDARY_RE.split(text) if unit.strip()]
    if len(sentences) >= 3:
        return sentences
    comma_phrases = [unit.strip() for unit in COMMA_BOUNDARY_RE.split(text) if unit.strip()]
    if len(comma_phrases) >= 3:
        return comma_phrases
    return [text.strip()]


def fit_token_retention(
    training_rows: list[dict[str, str]], prior_strength: float
) -> tuple[dict[str, float], float]:
    """Estimate smoothed P(token appears later | token appears earlier)."""
    counts: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    source_token_count = 0
    retained_token_count = 0
    for row in training_rows:
        source_tokens = set(tokenize(row["tst_2024"]))
        target_tokens = set(tokenize(row["tst_2025"]))
        source_token_count += len(source_tokens)
        retained_token_count += len(source_tokens & target_tokens)
        for token in source_tokens:
            counts[token][1] += 1
            counts[token][0] += int(token in target_tokens)

    prior = retained_token_count / source_token_count
    probabilities = {
        token: (retained + prior_strength * prior) / (observed + prior_strength)
        for token, (retained, observed) in counts.items()
    }
    return probabilities, prior


def fit_length_regression(training_rows: list[dict[str, str]]) -> tuple[float, float]:
    """Fit target_words = intercept + slope * source_words with OLS."""
    source_lengths = [len(tokenize(row["tst_2024"])) for row in training_rows]
    target_lengths = [len(tokenize(row["tst_2025"])) for row in training_rows]
    source_mean = sum(source_lengths) / len(source_lengths)
    target_mean = sum(target_lengths) / len(target_lengths)
    denominator = sum((value - source_mean) ** 2 for value in source_lengths)
    slope = (
        sum(
            (source - source_mean) * (target - target_mean)
            for source, target in zip(source_lengths, target_lengths)
        )
        / denominator
        if denominator
        else 0.0
    )
    return target_mean - slope * source_mean, slope


def unit_score(
    unit: str, probabilities: dict[str, float], prior: float
) -> float:
    content_tokens = {
        token
        for token in tokenize(unit)
        if len(token) > 1 and token not in STOP_TOKENS
    }
    if not content_tokens:
        return prior
    return sum(probabilities.get(token, prior) for token in content_tokens) / len(
        content_tokens
    )


def predict_response(
    source: str,
    probabilities: dict[str, float],
    prior: float,
    length_intercept: float,
    length_slope: float,
) -> str:
    units = response_units(source)
    unit_lengths = [len(tokenize(unit)) for unit in units]
    source_length = sum(unit_lengths)
    target_length = max(1, round(length_intercept + length_slope * source_length))
    ranked_indices = sorted(
        range(len(units)),
        key=lambda index: (unit_score(units[index], probabilities, prior), -index),
        reverse=True,
    )

    chosen: list[int] = []
    chosen_length = 0
    for index in ranked_indices:
        candidate_length = chosen_length + unit_lengths[index]
        if not chosen or abs(candidate_length - target_length) <= abs(
            chosen_length - target_length
        ):
            chosen.append(index)
            chosen_length = candidate_length
    return "\n".join(units[index] for index in sorted(chosen))


def make_predictions(
    input_rows: list[dict[str, str]],
    training_rows: list[dict[str, str]],
    prior_strength: float,
) -> list[dict[str, str]]:
    probabilities, prior = fit_token_retention(training_rows, prior_strength)
    intercept, slope = fit_length_regression(training_rows)
    return [
        {
            "id": row["id"],
            "predicted_tst_2025": predict_response(
                row["tst_2024"], probabilities, prior, intercept, slope
            ),
        }
        for row in input_rows
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark-dir",
        required=True,
        type=Path,
        help="Checkout of jasonjeffreyjones/predict-future-selves",
    )
    parser.add_argument("--dev-output", required=True, type=Path)
    parser.add_argument("--test-output", required=True, type=Path)
    parser.add_argument(
        "--prior-strength",
        type=float,
        default=10.0,
        help="Equivalent prior observations for token-retention smoothing",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    training_rows = read_csv(args.benchmark_dir / "data" / "train.csv")
    development_rows = read_csv(args.benchmark_dir / "data" / "dev.csv")
    test_rows = read_csv(args.benchmark_dir / "data" / "test_input.csv")
    write_predictions(
        args.dev_output,
        make_predictions(development_rows, training_rows, args.prior_strength),
    )
    write_predictions(
        args.test_output,
        make_predictions(test_rows, training_rows, args.prior_strength),
    )
    print(f"Wrote {len(development_rows)} development predictions to {args.dev_output}")
    print(f"Wrote {len(test_rows)} test predictions to {args.test_output}")


if __name__ == "__main__":
    main()
