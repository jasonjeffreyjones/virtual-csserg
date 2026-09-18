from __future__ import annotations

import sys
import unittest
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_trajectory_retrieval as analysis  # noqa: E402
import trajectory_retrieval as model  # noqa: E402


def row(case_id: str, text: str, target: str = "") -> dict[str, str]:
    result = {field: "" for field in model.DEMOGRAPHIC_FIELDS}
    result.update({"id": case_id, "tst_2024": text, "tst_2025": target})
    return result


class FakeEvaluator:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.casefold().split()

    @staticmethod
    def f1(precision: float, recall: float) -> float:
        return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


class TrajectoryRetrievalTests(unittest.TestCase):
    def test_metadata_features_are_field_qualified_and_normalized(self) -> None:
        example = row("a", "I am HERE")
        example["nationality_2024"] = "  United   Kingdom "
        features = model.feature_counts(example)
        self.assertEqual(features["i"], 1)
        self.assertEqual(
            features["metadata::nationality_2024::united kingdom"], 1
        )

    def test_prediction_uses_closest_training_trajectory(self) -> None:
        first = row("train_1", "gardener soil flowers", "future garden")
        second = row("train_2", "music guitar songs", "future concert")
        query = row("dev_1", "guitar music")
        predictions, audit = model.make_predictions([query], [first, second])
        self.assertEqual(predictions[0]["predicted_tst_2025"], "future concert")
        self.assertEqual(audit[0]["matched_train_id"], "train_2")

    def test_exact_similarity_tie_uses_training_order(self) -> None:
        first = row("train_1", "reader", "first future")
        second = row("train_2", "reader", "second future")
        prediction, audit = model.make_predictions(
            [row("dev_1", "reader")], [first, second]
        )
        self.assertEqual(prediction[0]["predicted_tst_2025"], "first future")
        self.assertEqual(audit[0]["matched_train_id"], "train_1")

    def test_novel_type_recovery_separates_precision_and_recall(self) -> None:
        precision, recall, f1 = analysis.novel_type_recovery(
            "old guessed extra", "old", "old guessed missed", FakeEvaluator
        )
        self.assertEqual(precision, 0.5)
        self.assertEqual(recall, 0.5)
        self.assertEqual(f1, 0.5)


if __name__ == "__main__":
    unittest.main()
