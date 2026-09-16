#!/usr/bin/env python3
"""Validate and query Virtual CSSERG Project lifecycle/publication metadata."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS_ROOT = REPOSITORY_ROOT / "projects"
SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
PROJECT_STATES = {"Proposed", "Active", "Blocked", "Paused", "Completed", "Archived"}
PUBLICATION_STATES = {"Unpublished", "Published"}


class ProjectError(ValueError):
    """Raised when Project metadata is missing, malformed, or ineligible."""


@dataclass(frozen=True)
class ProjectRecord:
    slug: str
    title: str
    status: str
    publication: str
    updated: str | None


def validate_slug(slug: str) -> str:
    if not SLUG_PATTERN.fullmatch(slug) or len(slug) > 80:
        raise ProjectError("Project slug must be 1-80 lowercase letters/digits with hyphens")
    return slug


def read_state_metadata(path: Path) -> dict[str, str | None]:
    source = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", source, flags=re.DOTALL)
    if not match:
        raise ProjectError(f"missing YAML front matter in {path}")
    metadata: dict[str, str | None] = {}
    for line in match.group(1).splitlines():
        key, separator, raw_value = line.partition(":")
        if not separator:
            raise ProjectError(f"invalid metadata line {line!r} in {path}")
        value = raw_value.strip()
        if value == "null":
            parsed = None
        elif value.startswith('"'):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError as error:
                raise ProjectError(f"invalid quoted metadata in {path}: {error}") from error
        else:
            parsed = value
        metadata[key.strip()] = parsed
    return metadata


def load_project(
    slug: str, projects_root: Path = DEFAULT_PROJECTS_ROOT
) -> ProjectRecord:
    slug = validate_slug(slug)
    project = Path(projects_root) / slug
    state = project / "STATE.md"
    if not project.is_dir() or not state.is_file():
        raise ProjectError(f"unknown Project slug {slug!r}")
    metadata = read_state_metadata(state)
    required = {"title", "status", "publication", "updated"}
    missing = sorted(required - set(metadata))
    if missing:
        raise ProjectError(f"{slug} metadata missing {', '.join(missing)}")
    title = metadata["title"]
    status = metadata["status"]
    publication = metadata["publication"]
    if not isinstance(title, str) or not title.strip():
        raise ProjectError(f"{slug} has no valid title")
    if status not in PROJECT_STATES:
        raise ProjectError(f"{slug} has invalid lifecycle state {status!r}")
    if publication not in PUBLICATION_STATES:
        raise ProjectError(f"{slug} has invalid publication state {publication!r}")
    if status == "Proposed" and publication == "Published":
        raise ProjectError(f"{slug} cannot be Proposed and Published")
    return ProjectRecord(slug, title, status, publication, metadata["updated"])


def active_project_title(slug: str, projects_root: Path = DEFAULT_PROJECTS_ROOT) -> str:
    record = load_project(slug, projects_root)
    if record.status != "Active":
        raise ProjectError(
            f"Project {slug!r} is {record.status}; Scholar iterations require Active"
        )
    return record.title


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--active-title",
        metavar="PROJECT_SLUG",
        help="validate an Active Project and print its title",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.active_title:
            print(active_project_title(args.active_title))
        else:
            records = [
                load_project(path.name)
                for path in sorted(DEFAULT_PROJECTS_ROOT.iterdir())
                if path.is_dir() and path.name != "_template"
            ]
            published = sum(record.publication == "Published" for record in records)
            print(f"Projects valid: {len(records)} total; {published} published.")
    except (OSError, ProjectError) as error:
        raise SystemExit(f"project_registry: {error}") from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
