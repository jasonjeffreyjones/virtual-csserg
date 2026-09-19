from __future__ import annotations

import random
import sys
import unittest
from collections import Counter
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_novelty_prior as novelty  # noqa: E402


class FakeEvaluator:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.casefold().split()

    @staticmethod
    def f1(precision: float, recall: float) -> float:
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)


class NoveltyPriorTests(unittest.TestCase):
    def test_training_additions_count_cases_not_occurrences(self) -> None:
        rows = [
            {"tst_2024": "old", "tst_2025": "old new new"},
            {"tst_2024": "old", "tst_2025": "other new"},
        ]
        self.assertEqual(
            novelty.training_addition_counts(rows, FakeEvaluator),
            Counter({"new": 2, "other": 1}),
        )

    def test_marginal_prediction_obeys_budget_and_excludes_source(self) -> None:
        prediction = novelty.marginal_prediction(
            ["common", "source", "next", "last"], {"source"}, 2
        )
        self.assertEqual(prediction, {"common", "next"})

    def test_recovery_scores_use_novel_type_sets(self) -> None:
        precision, recall, f1 = novelty.recovery_scores(
            {"right", "wrong"}, {"right", "missed"}, FakeEvaluator
        )
        self.assertEqual((precision, recall, f1), (0.5, 0.5, 0.5))

    def test_pair_summary_orients_positive_toward_marginal_prior(self) -> None:
        result = novelty.summarize_pair(
            [0.5, 0.2], [0.1, 0.2], random.Random(1), 100
        )
        self.assertAlmostEqual(
            result["mean_effect_positive_favors_marginal_prior"], 0.2
        )
        self.assertEqual(result["marginal_prior_case_wins"], 1)
        self.assertEqual(result["case_ties"], 1)
        self.assertEqual(result["marginal_prior_case_losses"], 0)


if __name__ == "__main__":
    unittest.main()
