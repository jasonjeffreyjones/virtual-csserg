#!/usr/bin/env python3
"""Generate a deterministic matched-trajectory development baseline.

The method represents 2024 text and field-qualified 2024 demographics with
TF-IDF features, retrieves the most similar public training input, and uses
that training case's observed follow-up as the prediction. It is intentionally
limited to development cases and never writes a private-test submission.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import re
from collections import Counter
from pathlib import Path


EXPECTED_TRAIN_SHA256 = (
    "720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48"
)
EXPECTED_DEV_SHA256 = (
    "afe74265475f1897161f54ac91395ded74d839e43236e8f4d189d91f9b40651a"
)
TOKEN_RE = re.compile(r"\w+(?:['\N{RIGHT SINGLE QUOTATION MARK}]\w+)*", re.UNICODE)
PREDICTION_FIELDS = ["id", "predicted_tst_2025"]
AUDIT_FIELDS = ["id", "matched_train_id", "cosine_similarity"]
DEMOGRAPHIC_FIELDS = [
    "age_2024",
    "sex_2024",
    "ethnicity_simplified_2024",
    "country_of_birth_2024",
    "country_of_residence_2024",
    "nationality_2024",
    "language_2024",
    "student_status_2024",
    "employment_status_2024",
    "fluent_languages_2024",
]


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


def tokenize(text: str) -> list[str]:
    """Match the benchmark evaluator's case-folded Unicode word tokens."""
    return TOKEN_RE.findall(" ".join(text.casefold().split()))


def normalized_metadata(value: str) -> str:
    return " ".join(value.casefold().split())


def feature_counts(row: dict[str, str]) -> Counter[str]:
    """Return text counts plus collision-resistant categorical features."""
    counts: Counter[str] = Counter(tokenize(row["tst_2024"]))
    for field in DEMOGRAPHIC_FIELDS:
        value = normalized_metadata(row.get(field, ""))
        if value:
            counts[f"metadata::{field}::{value}"] += 1
    return counts


def fit_idf(training_counts: list[Counter[str]]) -> dict[str, float]:
    document_frequency: Counter[str] = Counter()
    for counts in training_counts:
        document_frequency.update(counts.keys())
    document_count = len(training_counts)
    return {
        feature: math.log((document_count + 1) / (frequency + 1)) + 1
        for feature, frequency in document_frequency.items()
    }


def vectorize(
    counts: Counter[str], idf: dict[str, float]
) -> tuple[dict[str, float], float]:
    vector = {
        feature: (1 + math.log(frequency)) * idf[feature]
        for feature, frequency in counts.items()
        if feature in idf
    }
    norm = math.sqrt(sum(weight * weight for weight in vector.values()))
    return vector, norm


def cosine_similarity(
    left: dict[str, float],
    left_norm: float,
    right: dict[str, float],
    right_norm: float,
) -> float:
    if left_norm == 0 or right_norm == 0:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    numerator = sum(weight * right.get(feature, 0.0) for feature, weight in left.items())
    return numerator / (left_norm * right_norm)


def make_predictions(
    input_rows: list[dict[str, str]], training_rows: list[dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    if not training_rows:
        raise ValueError("Training data must contain at least one row")
    training_counts = [feature_counts(row) for row in training_rows]
    idf = fit_idf(training_counts)
    training_vectors = [vectorize(counts, idf) for counts in training_counts]

    predictions: list[dict[str, str]] = []
    audit_rows: list[dict[str, str]] = []
    for input_row in input_rows:
        query_vector, query_norm = vectorize(feature_counts(input_row), idf)
        similarities = [
            cosine_similarity(query_vector, query_norm, vector, norm)
            for vector, norm in training_vectors
        ]
        neighbor_index = max(
            range(len(training_rows)),
            key=lambda index: (similarities[index], -index),
        )
        neighbor = training_rows[neighbor_index]
        prediction = neighbor.get("tst_2025", "")
        if not prediction.strip():
            raise ValueError(f"Matched training row {neighbor.get('id', '')!r} is unlabeled")
        predictions.append(
            {"id": input_row["id"], "predicted_tst_2025": prediction}
        )
        audit_rows.append(
            {
                "id": input_row["id"],
                "matched_train_id": neighbor["id"],
                "cosine_similarity": f"{similarities[neighbor_index]:.12f}",
            }
        )
    return predictions, audit_rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, strict=True))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark-dir", required=True, type=Path)
    parser.add_argument("--dev-output", required=True, type=Path)
    parser.add_argument("--audit-output", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    training_path = args.benchmark_dir / "data/train.csv"
    development_path = args.benchmark_dir / "data/dev.csv"
    try:
        require_hash(training_path, EXPECTED_TRAIN_SHA256)
        require_hash(development_path, EXPECTED_DEV_SHA256)
        training_rows = read_csv(training_path)
        development_rows = read_csv(development_path)
        predictions, audit_rows = make_predictions(development_rows, training_rows)
    except (OSError, csv.Error, KeyError, ValueError) as error:
        raise SystemExit(f"trajectory_retrieval: {error}") from error
    write_csv(args.dev_output, predictions, PREDICTION_FIELDS)
    write_csv(args.audit_output, audit_rows, AUDIT_FIELDS)
    print(f"Wrote {len(predictions)} development predictions to {args.dev_output}")
    print(f"Wrote {len(audit_rows)} retrieval audit rows to {args.audit_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
