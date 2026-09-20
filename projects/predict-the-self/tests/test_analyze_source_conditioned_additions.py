from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_source_conditioned_additions as conditioned  # noqa: E402


class SourceConditionedAdditionTests(unittest.TestCase):
    def test_build_counts_uses_document_level_sets(self) -> None:
        source_counts, addition_counts, coadd_counts = conditioned.build_counts(
            [{"a", "common"}, {"b", "common"}],
            [{"x"}, {"x", "y"}],
        )
        self.assertEqual(source_counts, Counter({"common": 2, "a": 1, "b": 1}))
        self.assertEqual(addition_counts, Counter({"x": 2, "y": 1}))
        self.assertEqual(coadd_counts["common"], Counter({"x": 2, "y": 1}))
        self.assertEqual(coadd_counts["a"], Counter({"x": 1}))

    def test_fold_counts_remove_held_out_only_candidates(self) -> None:
        fold = conditioned.fold_addition_counts(
            Counter({"common": 3, "held": 1, "other": 1}), {"held", "common"}
        )
        self.assertEqual(fold, Counter({"common": 2, "other": 1}))

    def test_marginal_ranking_excludes_source_and_breaks_ties(self) -> None:
        ranked = conditioned.marginal_ranking(
            Counter({"source": 5, "z": 2, "a": 2, "m": 1}), {"source"}
        )
        self.assertEqual(ranked, ["a", "z", "m"])

    def test_conditioning_can_promote_source_linked_candidate(self) -> None:
        source_counts = Counter({"cue": 4, "other": 4})
        coadds = {
            "cue": Counter({"linked": 3}),
            "other": Counter({"common": 3, "linked": 1}),
        }
        ranked = conditioned.source_conditioned_ranking(
            Counter({"common": 3, "linked": 2}),
            {"cue"},
            set(),
            source_counts,
            coadds,
            fold_size=5,
        )
        self.assertEqual(ranked[0], "linked")

    def test_top_set_enforces_budget(self) -> None:
        self.assertEqual(conditioned.top_set(["a", "b", "c"], 2), {"a", "b"})
        with self.assertRaises(ValueError):
            conditioned.top_set(["a"], 2)

    def test_paired_summary_orients_positive_toward_conditioning(self) -> None:
        summary = conditioned.paired_summary([0.5, 0.2], [0.1, 0.2], 100)
        self.assertAlmostEqual(
            summary["mean_effect_positive_favors_source_conditioned"], 0.2
        )
        self.assertEqual(summary["source_conditioned_case_wins"], 1)
        self.assertEqual(summary["case_ties"], 1)
        self.assertEqual(summary["source_conditioned_case_losses"], 0)


if __name__ == "__main__":
    unittest.main()
