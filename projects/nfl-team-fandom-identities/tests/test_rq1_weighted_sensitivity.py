import unittest
from pathlib import Path
import sys


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))

from rq1_weighted_sensitivity import age_group, direct_standardization  # noqa: E402


class RQ1WeightedSensitivityTests(unittest.TestCase):
    def test_age_group_boundaries(self):
        self.assertEqual(age_group("18"), "18-29")
        self.assertEqual(age_group("30"), "30-44")
        self.assertEqual(age_group("65"), "65+")
        self.assertIsNone(age_group("DATA_EXPIRED"))

    def test_direct_standardization_uses_common_target(self):
        records = [
            (("a", "2026-01-01", True, True), ("Male", "18-29")),
            (("b", "2026-01-01", True, False), ("Female", "65+")),
            (("c", "2026-01-01", False, False), ("Male", "18-29")),
            (("d", "2026-01-01", False, True), ("Female", "65+")),
        ]
        result = direct_standardization(
            records,
            {("Male", "18-29"): 0.25, ("Female", "65+"): 0.75},
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["happy_prevalence_fandom_yes"], 0.25)
        self.assertEqual(result["happy_prevalence_fandom_no"], 0.75)


if __name__ == "__main__":
    unittest.main()
