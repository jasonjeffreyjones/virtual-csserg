from __future__ import annotations

import importlib.util
import math
import sys
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_source_form_ablation.py"
SPEC = importlib.util.spec_from_file_location("source_form_ablation", MODULE_PATH)
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


def row(case_id: str, source: str, future: str) -> dict[str, str]:
    return {"id": case_id, "tst_2024": source, "tst_2025": future}


class SourceFormAblationTests(unittest.TestCase):
    def test_source_form_features_use_only_source_counts(self) -> None:
        first = row("a", "One two two\nthree", "short future")
        second = row("b", "One two two\nthree", "a very different future response")
        expected = (math.log1p(4), math.log1p(3), math.log1p(2))
        self.assertEqual(analysis.source_form_features(first, FakeEvaluator), expected)
        self.assertEqual(
            analysis.source_form_features(second, FakeEvaluator), expected
        )

    def test_zero_variance_feature_scale_falls_back_to_one(self) -> None:
        self.assertEqual(
            analysis.feature_scales([(1.0, 2.0, 3.0), (1.0, 4.0, 3.0)]),
            (1.0, 1.0, 1.0),
        )

    def test_source_form_neighbors_use_similarity_then_original_order(self) -> None:
        rows = [
            row("a", "one two", "later"),
            row("b", "alpha beta", "later"),
            row("c", "one two three four", "later"),
        ]
        indices, similarities = analysis.select_source_form_neighbors(
            row("q", "query terms", "future"), rows, 2, FakeEvaluator
        )
        self.assertEqual(indices, [0, 1])
        self.assertEqual(similarities, [1.0, 1.0])

    def test_scores_include_every_method_and_outcome(self) -> None:
        rows = [
            row("a", "alpha source", "alpha later"),
            row("b", "beta source words", "beta later words"),
            row("c", "gamma source", "gamma later words"),
            row("d", "delta source words", "delta later"),
        ]
        audit = analysis.leave_one_out_scores(rows, FakeEvaluator, neighbor_count=2)
        self.assertEqual(len(audit), 4)
        for outcome in analysis.OUTCOMES:
            for method in analysis.METHODS:
                self.assertIn(f"{outcome}_{method}_crps", audit[0])

    def test_paired_effect_sign_favors_second_method(self) -> None:
        audits = [
            {
                "word_count_source_form_only_crps": 2.0,
                "word_count_text_only_crps": 1.0,
            },
            {
                "word_count_source_form_only_crps": 1.0,
                "word_count_text_only_crps": 1.5,
            },
        ]
        original_resamples = analysis.BOOTSTRAP_RESAMPLES
        analysis.BOOTSTRAP_RESAMPLES = 100
        try:
            summary = analysis.paired_summary(
                audits, "word_count", "source_form_only", "text_only"
            )
        finally:
            analysis.BOOTSTRAP_RESAMPLES = original_resamples
        self.assertGreater(
            summary["mean_effect_positive_favors_second_method"], 0
        )
        self.assertEqual(summary["second_method_case_wins"], 1)
        self.assertEqual(summary["second_method_case_losses"], 1)

    def test_locked_plan_and_preceding_artifacts_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        self.assertEqual(
            analysis.shared.sha256(
                project / "ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md"
            ),
            analysis.EXPECTED_PLAN_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(project / "analysis/analyze_feature_ablation.py"),
            analysis.EXPECTED_FEATURE_ABLATION_SHA256,
        )
        self.assertEqual(
            analysis.shared.sha256(project / "results/feature_ablation_train_audit.csv"),
            analysis.EXPECTED_FEATURE_AUDIT_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
