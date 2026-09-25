import csv
import datetime as dt
import gzip
import importlib.util
import json
import statistics
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

    def test_early_late_contrast_recovers_constructed_shift(self):
        rows = []
        start = dt.date(2025, 1, 1)
        midpoint = start + dt.timedelta(days=99)
        for day_index in range(200):
            date = start + dt.timedelta(days=day_index)
            for respondent_index in range(5):
                endorsed = (
                    respondent_index == 0
                    if day_index < 100
                    else respondent_index < 4
                )
                rows.append(
                    row(
                        "two-period",
                        date,
                        f"{respondent_index:012x}",
                        int(endorsed),
                    )
                )
        contrast = monitor.fit_early_late_contrast(rows, midpoint)
        self.assertEqual(contrast["early_observations"], 500)
        self.assertEqual(contrast["late_observations"], 500)
        self.assertEqual(contrast["respondent_clusters"], 5)
        self.assertAlmostEqual(contrast["early_prevalence_percent"], 20.0)
        self.assertAlmostEqual(contrast["late_prevalence_percent"], 80.0)
        self.assertAlmostEqual(
            contrast["late_minus_early_percentage_points"], 60.0
        )
        self.assertGreater(contrast["late_minus_early_cluster_se"], 0)

    def test_adjusted_early_late_contrast_removes_constructed_sex_mix_shift(self):
        rows = []
        start = dt.date(2025, 1, 1)
        midpoint = start + dt.timedelta(days=99)
        for day_index in range(200):
            date = start + dt.timedelta(days=day_index)
            male_slots = 2 if day_index < 100 else 8
            for slot in range(10):
                male = slot < male_slots
                record = row(
                    "period-composition",
                    date,
                    f"{day_index * 10 + slot:012x}",
                    int(male),
                )
                record.update({"age": "35", "sex": "Male" if male else "Female"})
                rows.append(record)
        unadjusted = monitor.fit_early_late_contrast(rows, midpoint)
        adjusted = monitor.fit_adjusted_early_late_contrast(rows, midpoint)
        self.assertAlmostEqual(
            unadjusted["late_minus_early_percentage_points"], 60.0
        )
        self.assertAlmostEqual(
            adjusted["adjusted_late_minus_early_percentage_points"],
            0.0,
            places=7,
        )

    def test_four_period_trajectory_tracks_reversal_and_concentration(self):
        rows = []
        start = dt.date(2025, 1, 1)
        prevalence_counts = (2, 4, 8, 7)
        for period, endorsed_count in enumerate(prevalence_counts):
            for day_in_period in range(10):
                date = start + dt.timedelta(days=period * 10 + day_in_period)
                for slot in range(10):
                    rows.append(
                        row(
                            "trajectory",
                            date,
                            f"{period * 100 + day_in_period * 10 + slot:012x}",
                            int(slot < endorsed_count),
                        )
                    )
        fitted = monitor.fit_period_trajectory(
            rows, start, start + dt.timedelta(days=39)
        )
        self.assertEqual(fitted["period_1_start"], "2025-01-01")
        self.assertEqual(fitted["period_4_end"], "2025-02-09")
        self.assertEqual(fitted["period_1_observations"], 100)
        self.assertAlmostEqual(fitted["period_1_prevalence_percent"], 20.0)
        self.assertAlmostEqual(fitted["period_4_prevalence_percent"], 70.0)
        self.assertAlmostEqual(
            fitted["period_1_to_2_change_percentage_points"], 20.0
        )
        self.assertAlmostEqual(
            fitted["period_2_to_3_change_percentage_points"], 40.0
        )
        self.assertAlmostEqual(
            fitted["period_3_to_4_change_percentage_points"], -10.0
        )
        self.assertAlmostEqual(
            fitted["total_absolute_adjacent_change_percentage_points"], 70.0
        )
        self.assertEqual(fitted["largest_transition"], "period_2_to_3")
        self.assertAlmostEqual(
            fitted["largest_transition_share_of_absolute_path"], 4 / 7
        )

    def test_adjusted_four_period_trajectory_removes_constructed_mix_lurch(self):
        rows = []
        start = dt.date(2025, 7, 8)
        male_slots_by_period = (2, 2, 8, 8)
        for period, male_slots in enumerate(male_slots_by_period):
            for day_in_period in range(111):
                day_index = period * 111 + day_in_period
                date = start + dt.timedelta(days=day_index)
                for slot in range(10):
                    male = slot < male_slots
                    record = row(
                        "adjusted-trajectory",
                        date,
                        f"{day_index * 10 + slot:012x}",
                        int(male),
                    )
                    record.update(
                        {"age": "35", "sex": "Male" if male else "Female"}
                    )
                    rows.append(record)
        end = start + dt.timedelta(days=443)
        raw = monitor.fit_period_trajectory(rows, start, end)
        adjusted = monitor.fit_adjusted_period_trajectory(rows, start, end)
        self.assertAlmostEqual(
            raw["period_2_to_3_change_percentage_points"], 60.0
        )
        for period in range(1, monitor.TRAJECTORY_PERIODS + 1):
            self.assertAlmostEqual(
                adjusted[f"adjusted_period_{period}_prevalence_percent"],
                50.0,
                places=6,
            )
        self.assertAlmostEqual(
            adjusted["adjusted_total_absolute_adjacent_change_percentage_points"],
            0.0,
            places=6,
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
        for singleton_index in range(40):
            stats.add(
                start + dt.timedelta(days=210 + singleton_index),
                0,
                f"{100 + singleton_index:012x}",
            )
        pooled = monitor.trend_row("turnover", stats)
        repeat_pooled = monitor.fit_repeat_respondent_pooled_trend(stats)
        within = monitor.fit_within_respondent_trend(stats)
        self.assertGreater(pooled["annual_change_percentage_points"], 0)
        self.assertGreater(
            repeat_pooled["repeat_pooled_annual_change_percentage_points"],
            pooled["annual_change_percentage_points"],
        )
        self.assertEqual(repeat_pooled["repeat_pooled_respondents"], 4)
        self.assertEqual(repeat_pooled["repeat_pooled_observations"], 300)
        self.assertAlmostEqual(within["within_annual_change_percentage_points"], 0.0)
        self.assertEqual(within["repeat_respondents"], 4)
        self.assertEqual(within["within_observations"], 300)
        self.assertEqual(within["within_residual_degrees_of_freedom"], 295)
        self.assertEqual(within["endorsement_switchers"], 0)
        self.assertTrue(within["zero_within_outcome_variation"])
        self.assertEqual(within["single_observation_respondents_excluded"], 40)

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

    def test_monitoring_history_summary_and_svg(self):
        history = []
        for index, observations in enumerate((100, 125, 160)):
            item = {field: "" for field in monitor.HISTORY_FIELDS}
            item.update(
                {
                    "checked_at_utc": f"2026-09-{16 + index:02d}T10:00:00Z",
                    "main_site_reachable": "true",
                    "canonical_dataset_retrieved": "true",
                    "parsed_successfully": "true",
                    "observations": str(observations),
                    "data_lag_days": "1",
                    "anomaly": "none",
                }
            )
            history.append(item)
        history[1]["main_site_reachable"] = "false"
        history[1]["anomaly"] = "main site unreachable"
        summary = monitor.monitoring_history_summary(history)
        self.assertEqual(summary["checks"], 3)
        self.assertEqual(summary["fully_healthy_checks"], 2)
        self.assertEqual(summary["maximum_data_lag_days"], 1)
        self.assertEqual(summary["observation_growth_across_checks"], 60)
        root = ET.fromstring(monitor.monitoring_history_svg(history))
        self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertIn(
            "Across 3 checks", root.find("{http://www.w3.org/2000/svg}desc").text
        )
        self.assertIn("×", ET.tostring(root, encoding="unicode"))

    def test_committed_outputs_are_internally_consistent(self):
        project = Path(__file__).resolve().parents[1]
        history = monitor.read_history(project / "data/monitoring-history.csv")
        summary = json.loads((project / "outputs/current-summary.json").read_text())
        self.assertEqual(history[-1]["checked_at_utc"], summary["checked_at_utc"])
        self.assertEqual(int(history[-1]["observations"]), summary["dataset"]["observations"])
        self.assertEqual(history[-1]["dataset_sha256"], summary["source"]["sha256"])
        self.assertEqual(len(history), summary["monitoring_history"]["checks"])
        healthy = sum(
            item["main_site_reachable"] == "true"
            and item["canonical_dataset_retrieved"] == "true"
            and item["parsed_successfully"] == "true"
            and item["anomaly"] == "none"
            for item in history
        )
        self.assertEqual(
            healthy, summary["monitoring_history"]["fully_healthy_checks"]
        )
        self.assertEqual(
            max(int(item["data_lag_days"]) for item in history if item["data_lag_days"]),
            summary["monitoring_history"]["maximum_data_lag_days"],
        )
        self.assertEqual(
            int(history[-1]["observations"]) - int(history[0]["observations"]),
            summary["monitoring_history"]["observation_growth_across_checks"],
        )

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
        with (project / "outputs/leader-early-late-sensitivity.csv").open(
            newline=""
        ) as source:
            early_late_sensitivity = list(csv.DictReader(source))
        self.assertEqual(
            len(early_late_sensitivity),
            summary["early_late_sensitivity"]["selected_signifiers"],
        )
        self.assertEqual(
            sum(item["same_direction"] == "True" for item in early_late_sensitivity),
            summary["early_late_sensitivity"]["same_direction"],
        )
        self.assertEqual(
            sum(
                item["adjusted_same_direction"] == "True"
                for item in early_late_sensitivity
            ),
            summary["early_late_sensitivity"]["adjusted_same_direction"],
        )
        self.assertEqual(
            sum(
                item["adjusted_same_direction_as_unadjusted_contrast"] == "True"
                for item in early_late_sensitivity
            ),
            summary["early_late_sensitivity"][
                "adjusted_same_direction_as_unadjusted_contrast"
            ],
        )
        self.assertEqual(
            early_late_sensitivity[0]["midpoint_date"],
            summary["early_late_sensitivity"]["midpoint_date"],
        )
        self.assertEqual(
            early_late_sensitivity[0]["signifier"],
            summary["early_late_sensitivity"]["results"][0]["signifier"],
        )
        self.assertEqual(
            (
                dt.date.fromisoformat(
                    summary["early_late_sensitivity"]["early_period_end"]
                )
                + dt.timedelta(days=1)
            ).isoformat(),
            summary["early_late_sensitivity"]["late_period_start"],
        )
        for item in early_late_sensitivity:
            self.assertAlmostEqual(
                float(item["late_prevalence_percent"])
                - float(item["early_prevalence_percent"]),
                float(item["late_minus_early_percentage_points"]),
            )
            self.assertEqual(
                (float(item["late_minus_early_percentage_points"]) >= 0)
                == (float(item["unadjusted_annual_change_percentage_points"]) >= 0),
                item["same_direction"] == "True",
            )
            self.assertAlmostEqual(
                float(item["late_minus_early_percentage_points"])
                + float(item["early_late_adjustment_shift_percentage_points"]),
                float(item["adjusted_late_minus_early_percentage_points"]),
            )
            self.assertEqual(
                (float(item["adjusted_late_minus_early_percentage_points"]) >= 0)
                == (float(item["unadjusted_annual_change_percentage_points"]) >= 0),
                item["adjusted_same_direction"] == "True",
            )
        self.assertEqual(
            round(
                statistics.median(
                    abs(float(item["late_minus_early_percentage_points"]))
                    for item in early_late_sensitivity
                ),
                3,
            ),
            summary["early_late_sensitivity"][
                "median_absolute_prevalence_difference_percentage_points"
            ],
        )
        self.assertEqual(
            round(
                statistics.median(
                    abs(float(item["early_late_adjustment_shift_percentage_points"]))
                    for item in early_late_sensitivity
                ),
                3,
            ),
            summary["early_late_sensitivity"][
                "median_absolute_adjustment_shift_percentage_points"
            ],
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
            sum(
                item["repeat_pooled_same_direction"] == "True"
                for item in within_sensitivity
            ),
            summary["within_respondent_sensitivity"][
                "repeat_pooled_same_direction_as_all_responses"
            ],
        )
        self.assertEqual(
            sum(
                item["within_same_direction_as_repeat"] == "True"
                for item in within_sensitivity
            ),
            summary["within_respondent_sensitivity"][
                "within_same_direction_as_repeat_pooled"
            ],
        )
        self.assertEqual(
            within_sensitivity[0]["signifier"],
            summary["within_respondent_sensitivity"]["results"][0]["signifier"],
        )
        for item in within_sensitivity:
            self.assertEqual(
                int(item["repeat_pooled_observations"]),
                int(item["within_observations"]),
            )
            self.assertEqual(
                int(item["repeat_pooled_respondents"]),
                int(item["repeat_respondents"]),
            )
            self.assertAlmostEqual(
                float(item["repeat_sample_shift_percentage_points"])
                + float(item["within_vs_repeat_shift_percentage_points"]),
                float(item["within_shift_percentage_points"]),
            )
        with (project / "outputs/leader-period-trajectory.csv").open(
            newline=""
        ) as source:
            period_trajectories = list(csv.DictReader(source))
        period_summary = summary["period_trajectory_sensitivity"]
        self.assertEqual(
            len(period_trajectories), period_summary["selected_signifiers"]
        )
        self.assertEqual(
            sum(
                item["first_to_last_same_direction"] == "True"
                for item in period_trajectories
            ),
            period_summary["first_to_last_same_direction"],
        )
        self.assertEqual(
            sum(
                item["all_adjacent_transitions_aligned"] == "True"
                for item in period_trajectories
            ),
            period_summary["all_adjacent_transitions_aligned"],
        )
        self.assertEqual(
            sum(
                int(item["aligned_adjacent_transitions"]) >= 2
                for item in period_trajectories
            ),
            period_summary["at_least_two_adjacent_transitions_aligned"],
        )
        for item in period_trajectories:
            prevalence = [
                float(item[f"period_{period}_prevalence_percent"])
                for period in range(1, monitor.TRAJECTORY_PERIODS + 1)
            ]
            changes = [
                float(
                    item[
                        f"period_{period}_to_{period + 1}_change_percentage_points"
                    ]
                )
                for period in range(1, monitor.TRAJECTORY_PERIODS)
            ]
            for period, change in enumerate(changes):
                self.assertAlmostEqual(prevalence[period + 1] - prevalence[period], change)
            self.assertAlmostEqual(
                sum(abs(change) for change in changes),
                float(item["total_absolute_adjacent_change_percentage_points"]),
            )
        self.assertEqual(
            round(
                statistics.median(
                    float(item["largest_transition_share_of_absolute_path"])
                    for item in period_trajectories
                ),
                6,
            ),
            period_summary["median_largest_transition_share_of_absolute_path"],
        )
        self.assertEqual(
            sum(
                item["adjusted_first_to_last_same_direction"] == "True"
                for item in period_trajectories
            ),
            period_summary["adjusted_first_to_last_same_direction"],
        )
        self.assertEqual(
            sum(
                item["adjusted_all_adjacent_transitions_aligned"] == "True"
                for item in period_trajectories
            ),
            period_summary["adjusted_all_adjacent_transitions_aligned"],
        )
        self.assertEqual(
            sum(
                int(item["adjusted_aligned_adjacent_transitions"]) >= 2
                for item in period_trajectories
            ),
            period_summary[
                "adjusted_at_least_two_adjacent_transitions_aligned"
            ],
        )
        self.assertEqual(
            sum(
                item["same_largest_transition_after_adjustment"] == "True"
                for item in period_trajectories
            ),
            period_summary["same_largest_transition_after_adjustment"],
        )
        for item in period_trajectories:
            adjusted_prevalence = [
                float(item[f"adjusted_period_{period}_prevalence_percent"])
                for period in range(1, monitor.TRAJECTORY_PERIODS + 1)
            ]
            adjusted_changes = [
                float(
                    item[
                        f"adjusted_period_{period}_to_{period + 1}_change_percentage_points"
                    ]
                )
                for period in range(1, monitor.TRAJECTORY_PERIODS)
            ]
            for period, change in enumerate(adjusted_changes):
                self.assertAlmostEqual(
                    adjusted_prevalence[period + 1]
                    - adjusted_prevalence[period],
                    change,
                )
            self.assertAlmostEqual(
                sum(abs(change) for change in adjusted_changes),
                float(
                    item[
                        "adjusted_total_absolute_adjacent_change_percentage_points"
                    ]
                ),
            )
        self.assertEqual(
            round(
                statistics.median(
                    float(
                        item[
                            "adjusted_largest_transition_share_of_absolute_path"
                        ]
                    )
                    for item in period_trajectories
                ),
                6,
            ),
            period_summary[
                "adjusted_median_largest_transition_share_of_absolute_path"
            ],
        )
        for name in (
            "observation-growth.svg",
            "monitoring-history.svg",
            "annual-prevalence-growth-histogram.svg",
            "leader-adjustment-sensitivity.svg",
            "leader-early-late-sensitivity.svg",
            "leader-period-trajectory.svg",
            "leader-period-adjustment-sensitivity.svg",
            "leader-within-respondent-sensitivity.svg",
        ):
            root = ET.parse(project / "outputs" / name).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")


if __name__ == "__main__":
    unittest.main()
