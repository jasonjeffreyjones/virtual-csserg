#!/usr/bin/env python3
"""Age-by-sex weighting sensitivity analysis for NFL fandom RQ1.

The unweighted prevalence ratio remains primary. This appendix analysis uses
2024 ACS 1-year table B01001 adult population counts in eight age-by-sex cells.
It does not assume that Browns fans have the overall U.S. age-sex distribution.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional, Sequence, Tuple

from rq1_risk_ratio import AnalysisError, Key, Record, load_records, require_columns


Cell = Tuple[str, str]

ACS_SOURCE = (
    "https://www2.census.gov/programs-surveys/acs/summary_file/2024/"
    "table-based-SF/data/1YRData/acsdt1y2024-b01001.dat"
)
ACS_TARGET_COUNTS: Dict[Cell, int] = {
    ("Male", "18-29"): 27_315_663,
    ("Male", "30-44"): 35_213_414,
    ("Male", "45-64"): 40_726_327,
    ("Male", "65+"): 27_683_311,
    ("Female", "18-29"): 26_279_247,
    ("Female", "30-44"): 34_617_925,
    ("Female", "45-64"): 41_783_819,
    ("Female", "65+"): 33_561_972,
}
ACS_VARIABLES: Dict[str, Sequence[str]] = {
    "Male 18-29": tuple(f"B01001_{number:03d}E" for number in range(7, 12)),
    "Male 30-44": tuple(f"B01001_{number:03d}E" for number in range(12, 15)),
    "Male 45-64": tuple(f"B01001_{number:03d}E" for number in range(15, 20)),
    "Male 65+": tuple(f"B01001_{number:03d}E" for number in range(20, 26)),
    "Female 18-29": tuple(f"B01001_{number:03d}E" for number in range(31, 36)),
    "Female 30-44": tuple(f"B01001_{number:03d}E" for number in range(36, 39)),
    "Female 45-64": tuple(f"B01001_{number:03d}E" for number in range(39, 44)),
    "Female 65+": tuple(f"B01001_{number:03d}E" for number in range(44, 50)),
}


def age_group(value: str) -> Optional[str]:
    try:
        age = int(value.strip())
    except ValueError:
        return None
    if 18 <= age <= 29:
        return "18-29"
    if 30 <= age <= 44:
        return "30-44"
    if 45 <= age <= 64:
        return "45-64"
    if age >= 65:
        return "65+"
    return None


def read_age_sex(
    path: Path,
    id_column: str,
    date_column: str,
    age_column: str,
    sex_column: str,
) -> Dict[Key, Optional[Cell]]:
    cells: Dict[Key, Optional[Cell]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        require_columns(
            reader.fieldnames,
            (id_column, date_column, age_column, sex_column),
            path,
        )
        for row in reader:
            key = ((row[id_column] or "").strip(), (row[date_column] or "").strip())
            if any(
                (value or "").strip().casefold() == "consent_revoked"
                for value in row.values()
            ):
                continue
            sex = (row[sex_column] or "").strip()
            grouped_age = age_group(row[age_column] or "")
            cell = (sex, grouped_age) if grouped_age and sex in {"Male", "Female"} else None
            cells[key] = cell
    return cells


def weighted_summary(
    records: Iterable[Tuple[Record, Cell]], weights: Mapping[Cell, float]
) -> Dict[str, object]:
    totals = defaultdict(float)
    happy = defaultdict(float)
    for record, cell in records:
        fandom = "yes" if record[2] else "no"
        weight = weights[cell]
        totals[fandom] += weight
        if record[3]:
            happy[fandom] += weight
    prevalence_yes = happy["yes"] / totals["yes"]
    prevalence_no = happy["no"] / totals["no"]
    return {
        "happy_prevalence_fandom_yes": prevalence_yes,
        "happy_prevalence_fandom_no": prevalence_no,
        "prevalence_ratio": prevalence_yes / prevalence_no,
        "prevalence_difference": prevalence_yes - prevalence_no,
        "weighted_denominator_fandom_yes": totals["yes"],
        "weighted_denominator_fandom_no": totals["no"],
    }


def direct_standardization(
    records: Sequence[Tuple[Record, Cell]], target_proportions: Mapping[Cell, float]
) -> Dict[str, object]:
    totals = Counter((record[2], cell) for record, cell in records)
    happy = Counter((record[2], cell) for record, cell in records if record[3])
    missing = [
        f"{'Yes' if fandom else 'No'} / {cell[0]} {cell[1]}"
        for fandom in (True, False)
        for cell in target_proportions
        if totals[(fandom, cell)] == 0
    ]
    if missing:
        return {
            "available": False,
            "reason": "One or more fandom-by-age-by-sex cells are empty",
            "empty_cells": missing,
        }
    standardized = {}
    for fandom in (True, False):
        standardized[fandom] = sum(
            target_proportions[cell]
            * happy[(fandom, cell)]
            / totals[(fandom, cell)]
            for cell in target_proportions
        )
    return {
        "available": True,
        "happy_prevalence_fandom_yes": standardized[True],
        "happy_prevalence_fandom_no": standardized[False],
        "prevalence_ratio": standardized[True] / standardized[False],
        "prevalence_difference": standardized[True] - standardized[False],
    }


def analyze(args: argparse.Namespace) -> Dict[str, object]:
    records, primary_audit = load_records(
        args.responses_csv,
        args.demographics_csv,
        args.fandom_signifier,
        args.outcome_signifier,
        args.id_column,
        args.date_column,
        args.signifier_column,
        args.response_column,
    )
    age_sex = read_age_sex(
        args.demographics_csv,
        args.id_column,
        args.date_column,
        args.age_column,
        args.sex_column,
    )
    complete = [
        (record, age_sex[(record[0], record[1])])
        for record in records
        if age_sex.get((record[0], record[1])) is not None
    ]
    typed_complete = [(record, cell) for record, cell in complete if cell is not None]
    sample_counts = Counter(cell for _record, cell in typed_complete)
    target_total = sum(ACS_TARGET_COUNTS.values())
    complete_n = len(typed_complete)
    target_proportions = {
        cell: count / target_total for cell, count in ACS_TARGET_COUNTS.items()
    }
    pooled_weights = {
        cell: target_proportions[cell] / (sample_counts[cell] / complete_n)
        for cell in ACS_TARGET_COUNTS
    }
    cell_diagnostics = [
        {
            "sex": cell[0],
            "age_group": cell[1],
            "acs_adult_count": ACS_TARGET_COUNTS[cell],
            "acs_adult_proportion": target_proportions[cell],
            "eligible_complete_records": sample_counts[cell],
            "pooled_poststratification_weight": pooled_weights[cell],
            "fandom_yes_records": sum(
                record[2] for record, record_cell in typed_complete if record_cell == cell
            ),
            "fandom_no_records": sum(
                not record[2] for record, record_cell in typed_complete if record_cell == cell
            ),
        }
        for cell in ACS_TARGET_COUNTS
    ]
    return {
        "analysis": "NFL Team Fandom Identities RQ1 age-by-sex weighting sensitivity",
        "status": "appendix sensitivity; unweighted descriptive estimate is primary",
        "target": {
            "source": "U.S. Census Bureau, 2024 ACS 1-year table B01001",
            "source_url": ACS_SOURCE,
            "universe": "U.S. resident population age 18 and older",
            "adult_population_count": target_total,
            "variable_groups": ACS_VARIABLES,
        },
        "audit": {
            "primary_eligible_respondent_days": primary_audit[
                "eligible_respondent_days"
            ],
            "complete_age_sex_respondent_days": complete_n,
            "excluded_missing_or_nonbinary_age_sex": len(records) - complete_n,
        },
        "cell_diagnostics": cell_diagnostics,
        "pooled_sample_poststratification": weighted_summary(
            typed_complete, pooled_weights
        ),
        "direct_standardization_to_common_us_age_sex_distribution": (
            direct_standardization(typed_complete, target_proportions)
        ),
        "interpretation_warning": (
            "The true age-sex distribution of Cleveland Browns fans is unknown. "
            "Pooled calibration assumes selection differences are captured by these "
            "eight cells; direct standardization describes a hypothetical common "
            "age-sex distribution, not the observed fandom populations."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses_csv", type=Path)
    parser.add_argument("demographics_csv", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fandom-signifier", default="Cleveland Browns fan")
    parser.add_argument("--outcome-signifier", default="happy")
    parser.add_argument("--id-column", default="hashed_respondent_id")
    parser.add_argument("--date-column", default="obs_date")
    parser.add_argument("--signifier-column", default="signifier")
    parser.add_argument("--response-column", default="endorsed")
    parser.add_argument("--age-column", default="age")
    parser.add_argument("--sex-column", default="sex")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    for path in (args.responses_csv, args.demographics_csv):
        if not path.is_file():
            raise SystemExit(f"file not found: {path}")
    try:
        result = analyze(args)
    except AnalysisError as error:
        raise SystemExit(str(error)) from error
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
