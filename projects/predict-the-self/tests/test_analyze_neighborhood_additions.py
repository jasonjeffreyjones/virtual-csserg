from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

import analyze_neighborhood_additions as neighborhood  # noqa: E402


def row(case_id: str, text: str) -> dict[str, str]:
    result = {field: "" for field in neighborhood.retrieval.DEMOGRAPHIC_FIELDS}
    result.update({"id": case_id, "tst_2024": text, "tst_2025": ""})
    return result


class NeighborhoodAdditionTests(unittest.TestCase):
    def test_neighbor_selection_uses_similarity_then_fold_order(self) -> None:
        training = [
            row("first", "reader books"),
            row("second", "reader books"),
            row("other", "music guitar"),
        ]
        indices, similarities = neighborhood.select_neighbors(
            row("held", "reader books"), training, count=2
        )
        self.assertEqual(indices, [0, 1])
        self.assertAlmostEqual(similarities[0], similarities[1])

    def test_neighbor_weights_clip_and_sum_to_fixed_total(self) -> None:
        weights = neighborhood.normalized_neighbor_weights([0.5, -0.2, 1.0], 30)
        self.assertEqual(weights[1], 0.0)
        self.assertAlmostEqual(sum(weights), 30.0)
        self.assertAlmostEqual(weights[2], 2 * weights[0])

    def test_zero_similarities_receive_equal_weights(self) -> None:
        self.assertEqual(
            neighborhood.normalized_neighbor_weights([0.0, -1.0, 0.0], 30),
            [10.0, 10.0, 10.0],
        )

    def test_neighborhood_votes_can_promote_personalized_candidate(self) -> None:
        ranked = neighborhood.regularized_neighborhood_ranking(
            Counter({"common": 4, "personal": 2, "source": 5}),
            {"source"},
            [{"personal"}, {"personal"}, {"other"}],
            [10.0, 10.0, 10.0],
            fold_size=10,
            prior_weight=30.0,
        )
        self.assertEqual(ranked[0], "personal")
        self.assertNotIn("source", ranked)

    def test_bad_neighbor_arguments_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            neighborhood.normalized_neighbor_weights([])
        with self.assertRaises(ValueError):
            neighborhood.regularized_neighborhood_ranking(
                Counter({"x": 1}), set(), [{"x"}], [], fold_size=2
            )

    def test_paired_summary_orients_positive_toward_neighborhood(self) -> None:
        summary = neighborhood.paired_summary([0.5, 0.2], [0.1, 0.2], 100)
        self.assertAlmostEqual(
            summary["mean_effect_positive_favors_regularized_neighborhood"], 0.2
        )
        self.assertEqual(summary["regularized_neighborhood_case_wins"], 1)
        self.assertEqual(summary["case_ties"], 1)
        self.assertEqual(summary["regularized_neighborhood_case_losses"], 0)


if __name__ == "__main__":
    unittest.main()
