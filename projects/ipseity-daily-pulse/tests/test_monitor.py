import csv
import datetime as dt
import gzip
import importlib.util
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "analysis/monitor.py"
SPEC = importlib.util.spec_from_file_location("ipseity_monitor", MODULE_PATH)
monitor = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = monitor
SPEC.loader.exec_module(monitor)


def row(signifier, date, respondent, endorsed):
    values = {name: "NA" for name in monitor.EXPECTED_COLUMNS}
    values.update(
        {
            "endorsed": str(endorsed),
            "signifier": signifier,
            "observation_date": date.isoformat(),
            "hashed_respondent_id": respondent,
            "demographics_status": "available",
        }
    )
    return values


class MonitorTests(unittest.TestCase):
    def make_gzip(self, path, duplicate=False):
        with gzip.open(path, "wt", encoding="utf-8", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=monitor.EXPECTED_COLUMNS, lineterminator="\n")
            writer.writeheader()
            start = dt.date(2025, 1, 1)
            for index in range(300):
                date = start + dt.timedelta(days=index)
                respondent = f"{index % 30:012x}"
                writer.writerow(row("rising", date, respondent, int(index >= 150)))
                writer.writerow(row("falling", date, respondent, int(index < 150)))
            if duplicate:
                writer.writerow(row("rising", start, "000000000000", 0))

    def test_valid_dataset_and_opposite_trends(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.csv.gz"
            self.make_gzip(path)
            audit = monitor.audit_dataset(
                path, dt.datetime(2025, 11, 1, tzinfo=dt.timezone.utc)
            )
            self.assertTrue(audit.parsed_successfully, audit.errors)
            self.assertEqual(audit.rows, 600)
            self.assertEqual(audit.duplicate_keys, 0)
            rising = monitor.trend_row("rising", audit.signifiers["rising"])
            falling = monitor.trend_row("falling", audit.signifiers["falling"])
            self.assertTrue(rising["eligible"])
            self.assertGreater(rising["annual_change_percentage_points"], 0)
            self.assertLess(falling["annual_change_percentage_points"], 0)
            trends = [rising, falling]
            monitor.add_robust_inference(trends, audit.signifiers)
            self.assertEqual(rising["respondent_clusters"], 30)
            self.assertEqual(rising["max_responses_per_respondent"], 10)
            self.assertGreater(rising["annual_change_cluster_se"], 0)
            self.assertLessEqual(rising["benjamini_hochberg_q_value"], 1)
            self.assertLessEqual(rising["bonferroni_adjusted_p_value"], 1)

    def test_benjamini_hochberg_is_monotone_in_rank(self):
        adjusted = monitor.benjamini_hochberg([0.01, 0.04, 0.03])
        self.assertEqual([round(value, 3) for value in adjusted], [0.03, 0.04, 0.04])

    def test_composition_adjustment_removes_constructed_sex_mix_trend(self):
        rows = []
        stats = monitor.SignifierStats()
        start = dt.date(2025, 1, 1)
        for day_index in range(200):
            date = start + dt.timedelta(days=day_index)
            male_slots = min(9, day_index // 20)
            for slot in range(10):
                male = slot < male_slots
                respondent = f"{day_index * 10 + slot:012x}"
                record = row("composition", date, respondent, int(male))
                record.update({"age": "35", "sex": "Male" if male else "Female"})
                rows.append(record)
                stats.add(date, int(male), respondent)
        unadjusted = monitor.trend_row("composition", stats)
        adjusted = monitor.fit_adjusted_trend(rows)
        self.assertGreater(unadjusted["annual_change_percentage_points"], 0)
        self.assertAlmostEqual(
            adjusted["adjusted_annual_change_percentage_points"], 0.0, places=7
        )

    def test_within_respondent_trend_removes_turnover_only_change(self):
        stats = monitor.SignifierStats()
        start = dt.date(2025, 1, 1)
        for respondent_index, (offset, endorsed) in enumerate(
            ((0, 0), (2, 0), (200, 1), (202, 1))
        ):
            respondent = f"{respondent_index:012x}"
            for day in range(75):
                stats.add(start + dt.timedelta(days=offset + day), endorsed, respondent)
        pooled = monitor.trend_row("turnover", stats)
        within = monitor.fit_within_respondent_trend(stats)
        self.assertGreater(pooled["annual_change_percentage_points"], 0)
        self.assertAlmostEqual(within["within_annual_change_percentage_points"], 0.0)
        self.assertEqual(within["repeat_respondents"], 4)
        self.assertEqual(within["within_observations"], 300)
        self.assertEqual(within["within_residual_degrees_of_freedom"], 295)
        self.assertEqual(within["endorsement_switchers"], 0)
        self.assertTrue(within["zero_within_outcome_variation"])

    def test_duplicate_key_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.csv.gz"
            self.make_gzip(path, duplicate=True)
            audit = monitor.audit_dataset(
                path, dt.datetime(2025, 11, 1, tzinfo=dt.timezone.utc)
            )
            self.assertFalse(audit.parsed_successfully)
            self.assertEqual(audit.duplicate_keys, 1)

    def test_history_refuses_duplicate_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "history.csv"
            template = {field: "" for field in monitor.HISTORY_FIELDS}
            template["checked_at_utc"] = "2026-09-16T20:47:07Z"
            monitor.append_history(path, template, [])
            existing = monitor.read_history(path)
            with self.assertRaisesRegex(ValueError, "refusing duplicate"):
                monitor.append_history(path, template, existing)

    def test_committed_outputs_are_internally_consistent(self):
        project = Path(__file__).resolve().parents[1]
        history = monitor.read_history(project / "data/monitoring-history.csv")
        summary = json.loads((project / "outputs/current-summary.json").read_text())
        self.assertEqual(history[-1]["checked_at_utc"], summary["checked_at_utc"])
        self.assertEqual(int(history[-1]["observations"]), summary["dataset"]["observations"])
        self.assertEqual(history[-1]["dataset_sha256"], summary["source"]["sha256"])

        with (project / "outputs/daily-observation-growth.csv").open(newline="") as source:
            daily = list(csv.DictReader(source))
        self.assertEqual(
            sum(int(item["daily_observations"]) for item in daily),
            summary["dataset"]["observations"],
        )
        self.assertEqual(
            int(daily[-1]["cumulative_observations"]), summary["dataset"]["observations"]
        )
        self.assertEqual(daily[0]["observation_date"], summary["dataset"]["earliest_observation_date"])
        self.assertEqual(daily[-1]["observation_date"], summary["dataset"]["latest_observation_date"])

        with (project / "outputs/signifier-growth.csv").open(newline="") as source:
            trends = list(csv.DictReader(source))
        eligible = [item for item in trends if item["eligible"] == "True"]
        self.assertEqual(len(trends), summary["dataset"]["signifiers"])
        self.assertEqual(len(eligible), summary["trend_method"]["eligible_signifiers"])
        self.assertEqual(
            sum(int(item["respondent_clusters"]) for item in trends),
            summary["trend_method"]["respondent_signifier_clusters"],
        )
        self.assertEqual(
            sum(item["fdr_05"] == "True" for item in eligible),
            summary["trend_method"]["fdr_05_discoveries"],
        )
        self.assertEqual(
            sum(item["bonferroni_05"] == "True" for item in eligible),
            summary["trend_method"]["bonferroni_05_discoveries"],
        )
        self.assertEqual(
            max(eligible, key=lambda item: float(item["annual_change_percentage_points"]))["signifier"],
            summary["fastest_growing"][0]["signifier"],
        )
        self.assertEqual(
            min(eligible, key=lambda item: float(item["annual_change_percentage_points"]))["signifier"],
            summary["fastest_shrinking"][0]["signifier"],
        )
        growth_row = next(
            item
            for item in eligible
            if item["signifier"] == summary["fastest_growing"][0]["signifier"]
        )
        self.assertEqual(
            round(float(growth_row["benjamini_hochberg_q_value"]), 6),
            summary["fastest_growing"][0]["benjamini_hochberg_q_value"],
        )
        with (project / "outputs/leader-adjusted-sensitivity.csv").open(newline="") as source:
            sensitivity = list(csv.DictReader(source))
        self.assertEqual(len(sensitivity), summary["leader_sensitivity"]["selected_signifiers"])
        self.assertEqual(
            sum(item["same_direction"] == "True" for item in sensitivity),
            summary["leader_sensitivity"]["same_direction"],
        )
        self.assertEqual(
            sensitivity[0]["signifier"],
            summary["leader_sensitivity"]["results"][0]["signifier"],
        )
        with (project / "outputs/leader-within-respondent-sensitivity.csv").open(
            newline=""
        ) as source:
            within_sensitivity = list(csv.DictReader(source))
        self.assertEqual(
            len(within_sensitivity),
            summary["within_respondent_sensitivity"]["selected_signifiers"],
        )
        self.assertEqual(
            sum(item["same_direction"] == "True" for item in within_sensitivity),
            summary["within_respondent_sensitivity"]["same_direction"],
        )
        self.assertEqual(
            within_sensitivity[0]["signifier"],
            summary["within_respondent_sensitivity"]["results"][0]["signifier"],
        )
        for name in (
            "observation-growth.svg",
            "annual-prevalence-growth-histogram.svg",
            "leader-adjustment-sensitivity.svg",
            "leader-within-respondent-sensitivity.svg",
        ):
            root = ET.parse(project / "outputs" / name).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
