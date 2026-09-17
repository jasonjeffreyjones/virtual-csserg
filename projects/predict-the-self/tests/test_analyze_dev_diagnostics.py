from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_dev_diagnostics as diagnostics  # noqa: E402


class FakeEvaluator:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.casefold().split()

    @staticmethod
    def f1(precision: float, recall: float) -> float:
        return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)

    @staticmethod
    def lcs_length(left: list[str], right: list[str]) -> int:
        previous = [0] * (len(right) + 1)
        for left_token in left:
            current = [0]
            for index, right_token in enumerate(right, start=1):
                current.append(
                    previous[index - 1] + 1
                    if left_token == right_token
                    else max(previous[index], current[-1])
                )
            previous = current
        return previous[-1]


class DevelopmentDiagnosticTests(unittest.TestCase):
    def test_percentile_uses_linear_interpolation(self) -> None:
        self.assertEqual(diagnostics.percentile([0.0, 10.0], 0.25), 2.5)

    def test_comparison_orients_lower_errors_so_positive_favors_stable(self) -> None:
        result = diagnostics.summarize_comparison(
            [1.0, 2.0, 3.0],
            [3.0, 2.0, 4.0],
            higher_is_better=False,
            resamples=100,
            rng=random.Random(1),
        )
        self.assertAlmostEqual(result["mean_effect_positive_favors_stable"], 1.0)
        self.assertEqual(result["stable_case_wins"], 2)
        self.assertEqual(result["case_ties"], 1)
        self.assertEqual(result["stable_case_losses"], 0)

    def test_extractive_diagnostics_identify_unavailable_future_tokens(self) -> None:
        result = diagnostics.extractive_diagnostics(
            ["old self old"], ["old new new"], FakeEvaluator
        )
        self.assertEqual(result["future_unique_token_novelty_fraction"], [0.5])
        self.assertAlmostEqual(
            result["future_token_occurrence_unavailable_fraction"][0], 2 / 3
        )
        self.assertEqual(result["source_unique_token_retention_fraction"], [0.5])
        self.assertEqual(result["oracle_unique_token_jaccard_ceiling"], [0.5])
        self.assertEqual(result["oracle_bag_of_words_f1_ceiling"], [0.5])
        self.assertEqual(
            result["oracle_source_order_subsequence_rouge_l_f1_ceiling"], [0.5]
        )


if __name__ == "__main__":
    unittest.main()
