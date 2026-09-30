from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))
MODULE_PATH = ANALYSIS_DIR / "analyze_calibrated_synthesis.py"
SPEC = importlib.util.spec_from_file_location("calibrated_synthesis", MODULE_PATH)
assert SPEC and SPEC.loader
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class FakeEvaluator:
    @staticmethod
    def normalize(text: str) -> str:
        return " ".join(text.casefold().split())

    @staticmethod
    def tokenize(text: str) -> list[str]:
        return FakeEvaluator.normalize(text).split()

    @staticmethod
    def line_count(text: str) -> int:
        return sum(bool(line.strip()) for line in text.splitlines())

    @staticmethod
    def rouge_l_f1(left: str, right: str) -> float:
        left_tokens = FakeEvaluator.tokenize(left)
        right_tokens = FakeEvaluator.tokenize(right)
        overlap = len(set(left_tokens) & set(right_tokens))
        return 2 * overlap / (len(left_tokens) + len(right_tokens))


def row(case_id: str, source: str, future: str) -> dict[str, str]:
    return {"id": case_id, "tst_2024": source, "tst_2025": future}


class CalibratedSynthesisTests(unittest.TestCase):
    def test_common_units_count_once_per_case_and_require_recurrence(self) -> None:
        rows = [
            row("a", "old\ncalm\nready", "New\nnew\nother"),
            row("b", "steady\nkind\nopen", "new\nx\ny"),
        ]
        self.assertEqual(analysis.common_novel_units(rows), ["New"])

    def test_target_forecasts_ignore_query_follow_up(self) -> None:
        fold = [
            row("a", "one two", "one later longer"),
            row("b", "three four", "three"),
        ]
        first = row("q", "same source", "short")
        second = row("q", "same source", "a completely different held out future")
        with (
            patch.object(
                analysis.source_form,
                "select_source_form_neighbors",
                return_value=([0], [1.0]),
            ),
            patch.object(
                analysis.volume,
                "select_neighbors",
                return_value=([0], [1.0]),
            ),
        ):
            first_targets = analysis.forecast_targets(
                first, fold, FakeEvaluator, neighbor_count=1
            )
            second_targets = analysis.forecast_targets(
                second, fold, FakeEvaluator, neighbor_count=1
            )
        self.assertEqual(first_targets, second_targets)

    def test_synthesis_search_can_reserve_space_for_a_novel_unit(self) -> None:
        query = row("q", "I am old\nI am calm", "unused")
        with (
            patch.object(
                analysis,
                "ranked_source_units",
                return_value=(["I am old", "I am calm"], [0, 1]),
            ),
            patch.object(
                analysis,
                "common_novel_units",
                return_value=["I am new"],
            ),
        ):
            prediction, details = analysis.synthesize_response(
                query, [row("a", "source", "future")], FakeEvaluator, 6, 1
            )
        self.assertEqual(prediction, "I am old\nI am new")
        self.assertEqual(details["retained_source_unit_count"], 1)
        self.assertEqual(details["appended_unit_count"], 1)

    def test_zero_prediction_content_rule_is_explicit(self) -> None:
        self.assertEqual(analysis.content_scores(set(), {"new"}), (0.0, 0.0, 0.0))
        self.assertEqual(
            analysis.content_scores({"new", "self"}, {"new", "other"}),
            (0.5, 0.5, 0.5),
        )

    def test_paired_error_effect_positive_favors_first_method(self) -> None:
        summary = analysis.paired_metric_summary(
            [1.0, 3.0],
            [2.0, 4.0],
            False,
            "first",
            "second",
            100,
        )
        self.assertEqual(summary["mean_effect_positive_favors_first"], 1.0)
        self.assertEqual(summary["first_case_wins"], 2)

    def test_locked_plan_and_inherited_hashes_match(self) -> None:
        project = Path(__file__).resolve().parents[1]
        expected = (
            ("ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md", analysis.EXPECTED_PLAN_SHA256),
            (
                "analysis/stable_signifier_projection.py",
                analysis.EXPECTED_STABLE_SHA256,
            ),
            ("analysis/analyze_change_volume.py", analysis.EXPECTED_VOLUME_SHA256),
            (
                "analysis/analyze_source_form_ablation.py",
                analysis.EXPECTED_SOURCE_FORM_SHA256,
            ),
            (
                "analysis/analyze_source_conditioned_additions.py",
                analysis.EXPECTED_SOURCE_CONDITIONED_SHA256,
            ),
            ("analysis/trajectory_retrieval.py", analysis.EXPECTED_RETRIEVAL_SHA256),
        )
        for relative, digest in expected:
            self.assertEqual(analysis.shared.sha256(project / relative), digest)


if __name__ == "__main__":
    unittest.main()
