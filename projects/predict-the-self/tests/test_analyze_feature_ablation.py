from __future__ import annotations

import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_feature_ablation.py"
SPEC = importlib.util.spec_from_file_location("feature_ablation", MODULE_PATH)
assert SPEC and SPEC.loader
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class FakeEvaluator:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return text.casefold().split()

    @staticmethod
    def line_count(text: str) -> int:
        return sum(bool(line.strip()) for line in text.splitlines())

    @staticmethod
    def rouge_l_f1(left: str, right: str) -> float:
        left_tokens = left.casefold().split()
        right_tokens = right.casefold().split()
        overlap = len(set(left_tokens) & set(right_tokens))
        return 2 * overlap / (len(left_tokens) + len(right_tokens))


def row(
    case_id: str,
    source: str,
    future: str,
    sex: str = "",
) -> dict[str, str]:
    return {
        "id": case_id,
        "tst_2024": source,
        "tst_2025": future,
        "sex_2024": sex,
    }


class FeatureAblationTests(unittest.TestCase):
    def test_feature_families_are_separate_and_recombine_exactly(self) -> None:
        example = row("a", "Alpha alpha beta", "later", "Woman")
        text = analysis.feature_counts(example, "text_only")
        demographics = analysis.feature_counts(example, "demographics_only")
        combined = analysis.feature_counts(example, "combined")
        self.assertEqual(text, Counter({"alpha": 2, "beta": 1}))
        self.assertEqual(
            demographics, Counter({"metadata::sex_2024::woman": 1})
        )
        self.assertEqual(combined, text + demographics)

    def test_missing_demographics_produce_no_demographic_feature(self) -> None:
        self.assertEqual(
            analysis.feature_counts(row("a", "source", "future"), "demographics_only"),
            Counter(),
        )

    def test_zero_norm_demographics_use_original_order(self) -> None:
        rows = [
            row("a", "alpha", "later"),
            row("b", "beta", "later"),
            row("c", "gamma", "later"),
        ]
        indices, similarities = analysis.select_neighbors(
            row("q", "query", "future"), rows, 2, "demographics_only"
        )
        self.assertEqual(indices, [0, 1])
        self.assertEqual(similarities, [0.0, 0.0])

    def test_scores_include_every_method_and_outcome(self) -> None:
        rows = [
            row("a", "alpha source", "alpha later", "woman"),
            row("b", "beta source", "beta later words", "man"),
            row("c", "gamma source", "gamma later", "woman"),
            row("d", "delta source", "delta later words", "man"),
        ]
        audit = analysis.leave_one_out_scores(rows, FakeEvaluator, neighbor_count=2)
        self.assertEqual(len(audit), 4)
        for outcome in analysis.OUTCOMES:
            for method in analysis.METHODS:
                self.assertIn(f"{outcome}_{method}_crps", audit[0])

    def test_paired_effect_sign_favors_second_method(self) -> None:
        audits = [
            {"word_count_marginal_crps": 2.0, "word_count_text_only_crps": 1.0},
            {"word_count_marginal_crps": 1.0, "word_count_text_only_crps": 1.5},
        ]
        original_resamples = analysis.BOOTSTRAP_RESAMPLES
        analysis.BOOTSTRAP_RESAMPLES = 100
        try:
            summary = analysis.paired_summary(
                audits, "word_count", "marginal", "text_only"
            )
        finally:
            analysis.BOOTSTRAP_RESAMPLES = original_resamples
        self.assertGreater(
            summary["mean_effect_positive_favors_second_method"], 0
        )
        self.assertEqual(summary["second_method_case_wins"], 1)
        self.assertEqual(summary["second_method_case_losses"], 1)

    def test_locked_plan_and_implementations_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.shared.sha256(project / "ANALYSIS_PLAN_FEATURE_ABLATION.md"),
            analysis.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(
                project / "analysis/analyze_change_distributions.py"
            ),
            analysis.EXPECTED_DISTRIBUTIONS_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
