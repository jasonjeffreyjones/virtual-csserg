#!/usr/bin/env python3
"""Validate Virtual CSSERG's public Scholar roster and assignments."""

from dataclasses import dataclass
import json
from pathlib import Path
import re


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROSTER_PATH = REPOSITORY_ROOT / "scholars.json"
DEFAULT_PROJECTS_ROOT = REPOSITORY_ROOT / "projects"
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MONOGRAM_PATTERN = re.compile(r"[A-Z0-9]{1,8}\Z")
RECORD_FIELDS = {"name", "slug", "monogram", "current_project"}


class RosterError(ValueError):
    """Raised when the roster is malformed or refers to missing Projects."""


@dataclass(frozen=True)
class ScholarRecord:
    name: str
    slug: str
    monogram: str
    current_project: str | None


def _plain_name(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise RosterError(f"{field} must be a string")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > 160 or any(ord(char) < 32 for char in value):
        raise RosterError(f"{field} must be 1-160 printable characters")
    return normalized


def _slug(value: object, field: str) -> str:
    if not isinstance(value, str) or not SLUG_PATTERN.fullmatch(value):
        raise RosterError(f"{field} must be a lowercase hyphenated slug")
    if len(value) > 80:
        raise RosterError(f"{field} must be at most 80 characters")
    return value


def load_roster(
    roster_path: Path = DEFAULT_ROSTER_PATH,
    projects_root: Path = DEFAULT_PROJECTS_ROOT,
) -> list[ScholarRecord]:
    """Load and validate the versioned roster without changing repository files."""
    roster_path = Path(roster_path)
    projects_root = Path(projects_root)
    try:
        payload = json.loads(roster_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RosterError(f"cannot read {roster_path}: {error}") from error

    if not isinstance(payload, dict) or set(payload) != {"schema_version", "scholars"}:
        raise RosterError("roster must contain only schema_version and scholars")
    if payload["schema_version"] != 1:
        raise RosterError("unsupported roster schema_version")
    if not isinstance(payload["scholars"], list) or not payload["scholars"]:
        raise RosterError("scholars must be a nonempty list")

    records = []
    for number, raw_record in enumerate(payload["scholars"], start=1):
        if not isinstance(raw_record, dict) or set(raw_record) != RECORD_FIELDS:
            raise RosterError(
                f"scholar {number} must contain exactly {', '.join(sorted(RECORD_FIELDS))}"
            )
        name = _plain_name(raw_record["name"], f"scholar {number} name")
        slug = _slug(raw_record["slug"], f"scholar {number} slug")
        monogram = raw_record["monogram"]
        if not isinstance(monogram, str) or not MONOGRAM_PATTERN.fullmatch(monogram):
            raise RosterError(f"scholar {number} monogram must be 1-8 A-Z/0-9 characters")
        current_project = raw_record["current_project"]
        if current_project is not None:
            current_project = _slug(
                current_project, f"scholar {number} current_project"
            )
            project = projects_root / current_project
            if not project.is_dir() or not (project / "STATE.md").is_file():
                raise RosterError(
                    f"scholar {number} refers to unknown Project {current_project!r}"
                )
        records.append(ScholarRecord(name, slug, monogram, current_project))

    for field in ("name", "slug", "monogram"):
        values = [getattr(record, field) for record in records]
        if len(values) != len(set(values)):
            raise RosterError(f"duplicate Scholar {field}")
    return records


def main() -> int:
    records = load_roster()
    assigned = sum(record.current_project is not None for record in records)
    print(f"Roster valid: {len(records)} Scholars; {assigned} current assignments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
