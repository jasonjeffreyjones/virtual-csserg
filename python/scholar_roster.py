#!/usr/bin/env python3
"""Validate and query Virtual CSSERG's Scholar identity roster."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER_PATH = REPOSITORY_ROOT / "scholars.json"
DEFAULT_BIOGRAPHIES_ROOT = REPOSITORY_ROOT / "scholars"
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MONOGRAM_PATTERN = re.compile(r"[A-Z0-9]{1,8}\Z")
RECORD_FIELDS = {"name", "slug", "monogram"}


class RosterError(ValueError):
    """Raised when the roster or its biography sources are malformed."""


@dataclass(frozen=True)
class ScholarRecord:
    name: str
    slug: str
    monogram: str


def validate_name(value: object, field: str = "name") -> str:
    if not isinstance(value, str):
        raise RosterError(f"{field} must be a string")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > 160 or any(ord(char) < 32 for char in value):
        raise RosterError(f"{field} must be 1-160 printable characters")
    return normalized


def validate_slug(value: object, field: str = "slug") -> str:
    if not isinstance(value, str) or not SLUG_PATTERN.fullmatch(value):
        raise RosterError(f"{field} must be a lowercase hyphenated slug")
    if len(value) > 80:
        raise RosterError(f"{field} must be at most 80 characters")
    return value


def validate_monogram(value: object, field: str = "monogram") -> str:
    if not isinstance(value, str) or not MONOGRAM_PATTERN.fullmatch(value):
        raise RosterError(f"{field} must be 1-8 A-Z/0-9 characters")
    return value


def load_biography(path: Path) -> str:
    try:
        biography = path.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise RosterError(f"cannot read biography {path}: {error}") from error
    if not biography:
        raise RosterError(f"biography is empty: {path}")
    if "\x00" in biography:
        raise RosterError(f"biography contains a null byte: {path}")
    return biography


def load_roster(
    roster_path: Path = DEFAULT_ROSTER_PATH,
    biographies_root: Path = DEFAULT_BIOGRAPHIES_ROOT,
) -> list[ScholarRecord]:
    """Load and validate identity data and canonical biographies read-only."""
    roster_path = Path(roster_path)
    biographies_root = Path(biographies_root)
    try:
        payload = json.loads(roster_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RosterError(f"cannot read {roster_path}: {error}") from error

    if not isinstance(payload, dict) or set(payload) != {"schema_version", "scholars"}:
        raise RosterError("roster must contain only schema_version and scholars")
    if payload["schema_version"] != 2:
        raise RosterError("unsupported roster schema_version")
    if not isinstance(payload["scholars"], list) or not payload["scholars"]:
        raise RosterError("scholars must be a nonempty list")

    records = []
    for number, raw_record in enumerate(payload["scholars"], start=1):
        if not isinstance(raw_record, dict) or set(raw_record) != RECORD_FIELDS:
            raise RosterError(
                f"scholar {number} must contain exactly {', '.join(sorted(RECORD_FIELDS))}"
            )
        name = validate_name(raw_record["name"], f"scholar {number} name")
        slug = validate_slug(raw_record["slug"], f"scholar {number} slug")
        monogram = validate_monogram(
            raw_record["monogram"], f"scholar {number} monogram"
        )
        load_biography(biographies_root / slug / "BIOGRAPHY.md")
        records.append(ScholarRecord(name, slug, monogram))

    for field in ("name", "slug", "monogram"):
        values = [getattr(record, field) for record in records]
        if len(values) != len(set(values)):
            raise RosterError(f"duplicate Scholar {field}")
    return records


def scholar_by_slug(
    slug: str,
    roster_path: Path = DEFAULT_ROSTER_PATH,
    biographies_root: Path = DEFAULT_BIOGRAPHIES_ROOT,
) -> ScholarRecord:
    slug = validate_slug(slug, "Scholar slug")
    for record in load_roster(roster_path, biographies_root):
        if record.slug == slug:
            return record
    raise RosterError(f"unknown Scholar slug {slug!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--name-for",
        metavar="SCHOLAR_SLUG",
        help="print the display name for one validated Scholar",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.name_for:
        try:
            print(scholar_by_slug(args.name_for).name)
        except RosterError as error:
            raise SystemExit(f"scholar_roster: {error}") from error
        return 0

    try:
        records = load_roster()
    except RosterError as error:
        raise SystemExit(f"scholar_roster: {error}") from error
    print(f"Roster valid: {len(records)} Scholars with canonical biographies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
