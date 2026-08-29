import csv
import math
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
import sys


ANALYSIS_DIR = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS_DIR))

from rq1_risk_ratio import AnalysisError, analyze, load_records  # noqa: E402


def write_csv(path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class RQ1RiskRatioTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.responses = root / "responses.csv"
        self.demographics = root / "demographics.csv"

        demographic_rows = [
            {"hashed_respondent_id": respondent, "obs_date": date, "age": "40"}
            for respondent, date in [
                ("r1", "2026-01-01"),
                ("r1", "2026-01-02"),
                ("r2", "2026-01-01"),
                ("r3", "2026-01-01"),
                ("r4", "2026-01-01"),
                ("r5", "2026-01-01"),
                ("r6", "2026-01-01"),
                ("r7", "2026-01-01"),
            ]
        ]
        write_csv(
            self.demographics,
            ["hashed_respondent_id", "obs_date", "age"],
            demographic_rows,
        )

        pairs = {
            ("r1", "2026-01-01"): ("Yes", "Yes"),
            ("r1", "2026-01-02"): ("Yes", "No"),
            ("r2", "2026-01-01"): ("Yes", "Yes"),
            ("r3", "2026-01-01"): ("No", "Yes"),
            ("r4", "2026-01-01"): ("No", "No"),
            ("r5", "2026-01-01"): ("No", "No"),
            # r6 was not presented happy and must not become an implicit No.
            ("r6", "2026-01-01"): ("Yes", None),
            # This respondent-day has no demographics match and must be excluded.
            ("outside", "2026-01-01"): ("Yes", "Yes"),
        }
        response_rows = []
        for (respondent, date), (fandom, happy) in pairs.items():
            response_rows.append(
                {
                    "hashed_respondent_id": respondent,
                    "obs_date": date,
                    "signifier": "Cleveland Browns fan",
                    "response": fandom,
                }
            )
            if happy is not None:
                response_rows.append(
                    {
                        "hashed_respondent_id": respondent,
                        "obs_date": date,
                        "signifier": "happy",
                        "response": happy,
                    }
                )
            response_rows.append(
                {
                    "hashed_respondent_id": respondent,
                    "obs_date": date,
                    "signifier": "unrelated",
                    "response": "Yes",
                }
            )
        write_csv(
            self.responses,
            ["hashed_respondent_id", "obs_date", "signifier", "response"],
            response_rows,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def args(self):
        return Namespace(
            responses_csv=self.responses,
            demographics_csv=self.demographics,
            fandom_signifier="Cleveland Browns fan",
            outcome_signifier="happy",
            id_column="hashed_respondent_id",
            date_column="obs_date",
            signifier_column="signifier",
            response_column="response",
            ci_level=0.95,
            bootstrap_reps=100,
            seed=7,
        )

    def test_co_presented_explicit_answers_and_inner_join_define_risk_set(self):
        result = analyze(self.args())
        audit = result["join_audit"]
        estimates = result["estimates"]

        self.assertEqual(audit["eligible_respondent_days"], 6)
        self.assertEqual(audit["eligible_unique_respondents"], 5)
        self.assertEqual(audit["eligible_repeated_respondents"], 1)
        self.assertEqual(audit["unmatched_response_rows_excluded"], 3)
        self.assertEqual(estimates["two_by_two"], {
            "fandom_yes_happy_yes": 2,
            "fandom_yes_happy_no": 1,
            "fandom_no_happy_yes": 1,
            "fandom_no_happy_no": 2,
        })
        self.assertTrue(math.isclose(estimates["prevalence_ratio"], 2.0))
        self.assertTrue(math.isclose(estimates["prevalence_difference"], 1 / 3))
        self.assertEqual(
            estimates["cluster_bootstrap"]["requested_replicates"], 100
        )
        self.assertEqual(result["temporal_sensitivity"]["eligible_dates"], 2)
        self.assertEqual(len(result["temporal_sensitivity"]["by_month"]), 1)

    def test_binary_one_zero_responses_are_supported(self):
        with self.responses.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        for row in rows:
            row["response"] = "1" if row["response"] == "Yes" else "0"
        write_csv(
            self.responses,
            ["hashed_respondent_id", "obs_date", "signifier", "response"],
            rows,
        )
        result = analyze(self.args())
        self.assertEqual(result["estimates"]["fandom_yes_n"], 3)
        self.assertEqual(result["estimates"]["fandom_no_n"], 3)

    def test_conflicting_duplicate_answer_excludes_respondent_day(self):
        with self.responses.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                ["r1", "2026-01-01", "Cleveland Browns fan", "No"]
            )
        records, audit = load_records(
            self.responses,
            self.demographics,
            "Cleveland Browns fan",
            "happy",
        )
        self.assertEqual(audit["conflicting_target_respondent_days_excluded"], 1)
        self.assertEqual(len(records), 5)

    def test_duplicate_demographics_join_key_fails_loudly(self):
        with self.demographics.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["r1", "2026-01-01", "40"])
        with self.assertRaisesRegex(AnalysisError, "duplicate join key"):
            load_records(
                self.responses,
                self.demographics,
                "Cleveland Browns fan",
                "happy",
            )

    def test_consent_revoked_respondent_day_is_excluded(self):
        with self.demographics.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
        rows[0]["age"] = "CONSENT_REVOKED"
        write_csv(
            self.demographics,
            ["hashed_respondent_id", "obs_date", "age"],
            rows,
        )
        result = analyze(self.args())
        self.assertEqual(
            result["join_audit"]["consent_revoked_demographic_rows_excluded"],
            1,
        )
        self.assertEqual(result["join_audit"]["eligible_respondent_days"], 5)


if __name__ == "__main__":
    unittest.main()
