#!/usr/bin/env python3
"""Migrate every Project from a shared dialog log to immutable iterations."""

from __future__ import annotations

import argparse
from datetime import date
import hashlib
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import NamedTuple


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECTS_ROOT = REPOSITORY_ROOT / "projects"
DATE_PATTERN = re.compile(r"20\d{2}-\d{2}-\d{2}\Z")
PROTOCOL_MARKER = "dialog_protocol: immutable-iterations-v1"


class MigrationError(ValueError):
    """Raised before migration when any Project cannot be migrated safely."""


class DialogPlan(NamedTuple):
    project: Path
    title: str
    legacy_bytes: bytes
    digest: str
    archive_name: str
    year: str


def validate_through_date(value: str) -> str:
    if not DATE_PATTERN.fullmatch(value):
        raise MigrationError("through date must use YYYY-MM-DD")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise MigrationError(f"invalid through date: {value}") from error
    return value


def state_title(project: Path) -> str:
    state = (project / "STATE.md").read_text(encoding="utf-8")
    match = re.search(r'^title:\s*"([^"\n]+)"\s*$', state, flags=re.MULTILINE)
    if not match:
        raise MigrationError(f"{project.name}: STATE.md has no quoted title")
    return match.group(1)


def build_plan(projects_root: Path, through_date: str) -> list[DialogPlan]:
    """Validate all Projects before returning a complete, mutation-free plan."""
    through_date = validate_through_date(through_date)
    projects_root = Path(projects_root).resolve()
    projects = sorted(path for path in projects_root.iterdir() if path.is_dir())
    if not projects:
        raise MigrationError(f"no Project directories found in {projects_root}")

    plans = []
    for project in projects:
        dialog = project / "DIALOG.md"
        if not dialog.is_file():
            raise MigrationError(f"{project.name}: missing DIALOG.md")
        if (project / "dialog").exists():
            raise MigrationError(
                f"{project.name}: refusing to overwrite existing dialog directory"
            )
        legacy_bytes = dialog.read_bytes()
        if PROTOCOL_MARKER.encode() in legacy_bytes:
            raise MigrationError(f"{project.name}: DIALOG.md is already migrated")
        plans.append(
            DialogPlan(
                project=project,
                title=state_title(project),
                legacy_bytes=legacy_bytes,
                digest=hashlib.sha256(legacy_bytes).hexdigest(),
                archive_name=f"DIALOG-through-{through_date}.md",
                year=through_date[:4],
            )
        )
    return plans


def landing_page(plan: DialogPlan) -> str:
    archive = f"dialog/legacy/{plan.archive_name}"
    active_guidance = (
        f"- [Review PI-authored guidance in the legacy archive]({archive}).\n"
        if any(line.startswith(b">") for line in plan.legacy_bytes.splitlines())
        else "None recorded.\n"
    )
    return f"""---
dialog_protocol: immutable-iterations-v1
legacy_archive: {archive}
legacy_sha256: {plan.digest}
---

# {plan.title} — Dialog

This is a bounded landing index. Scholar iteration records are immutable after
creation; Dr. Jones may append Markdown blockquotes to a specific record.

## Active PI guidance

{active_guidance}
## Unresolved questions

None recorded here. Consult `STATE.md` for the current handoff.

## Recent iteration records

Newest first; at most 20 records belong in this section.

No migrated-format iteration records yet.

## Yearly indexes

- [{plan.year}](dialog/indexes/{plan.year}.md)

## Legacy archive

- [{plan.archive_name}]({archive}) — pre-migration `DIALOG.md`, SHA-256
  `{plan.digest}`.
"""


def yearly_index(plan: DialogPlan) -> str:
    return f"""# {plan.title} — {plan.year} dialog index

Iteration records are listed newest first. No migrated-format records have been
created for this Project in {plan.year}.

## Pre-migration history

- [Legacy dialog through {plan.archive_name[15:-3]}](../legacy/{plan.archive_name})
  — SHA-256 `{plan.digest}`.
"""


def stage_plan(plan: DialogPlan, staging_root: Path) -> tuple[Path, Path]:
    project_stage = staging_root / plan.project.name
    dialog_stage = project_stage / "dialog"
    (dialog_stage / "iterations").mkdir(parents=True)
    (dialog_stage / "indexes").mkdir()
    (dialog_stage / "legacy").mkdir()
    (dialog_stage / "iterations" / ".gitkeep").write_text("", encoding="utf-8")
    (dialog_stage / "legacy" / plan.archive_name).write_bytes(plan.legacy_bytes)
    (dialog_stage / "indexes" / f"{plan.year}.md").write_text(
        yearly_index(plan), encoding="utf-8"
    )
    landing = project_stage / "DIALOG.md"
    landing.write_text(landing_page(plan), encoding="utf-8")

    if (dialog_stage / "legacy" / plan.archive_name).read_bytes() != plan.legacy_bytes:
        raise MigrationError(f"{plan.project.name}: staged archive changed bytes")
    return landing, dialog_stage


def migrate_all(
    projects_root: Path = DEFAULT_PROJECTS_ROOT,
    through_date: str | None = None,
    *,
    apply: bool = False,
) -> list[DialogPlan]:
    """Dry-run by default; apply only after every Project and output validates."""
    through_date = through_date or date.today().isoformat()
    plans = build_plan(projects_root, through_date)
    if not apply:
        return plans

    projects_root = Path(projects_root).resolve()
    original_dialogs = {plan.project: plan.legacy_bytes for plan in plans}
    installed_dialog_dirs: list[Path] = []
    replaced_landings: list[Path] = []
    with tempfile.TemporaryDirectory(prefix=".dialog-migration-", dir=projects_root) as temporary:
        staging_root = Path(temporary)
        staged = {plan.project: stage_plan(plan, staging_root) for plan in plans}
        try:
            for plan in plans:
                landing_stage, dialog_stage = staged[plan.project]
                dialog_target = plan.project / "dialog"
                os.replace(dialog_stage, dialog_target)
                installed_dialog_dirs.append(dialog_target)

                landing_target = plan.project / "DIALOG.md"
                os.replace(landing_stage, landing_target)
                replaced_landings.append(landing_target)
        except Exception:
            for landing in replaced_landings:
                rollback = landing.with_name(".DIALOG.md.rollback")
                rollback.write_bytes(original_dialogs[landing.parent])
                os.replace(rollback, landing)
            for dialog_dir in reversed(installed_dialog_dirs):
                shutil.rmtree(dialog_dir, ignore_errors=True)
            raise
    return plans


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan or apply the coordinated immutable-dialog migration."
    )
    parser.add_argument(
        "--through-date",
        default=date.today().isoformat(),
        help="last legacy-dialog date in YYYY-MM-DD form (default: today)",
    )
    parser.add_argument(
        "--projects-root",
        type=Path,
        default=DEFAULT_PROJECTS_ROOT,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the migration; omission is a read-only dry run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        plans = migrate_all(args.projects_root, args.through_date, apply=args.apply)
    except (MigrationError, OSError) as error:
        raise SystemExit(f"migrate_dialogs: {error}") from error

    action = "Migrated" if args.apply else "Would migrate"
    print(f"{action} {len(plans)} Project directories:")
    for plan in plans:
        print(f"- {plan.project.name}: {plan.digest}")
    if not args.apply:
        print("Dry run only; pass --apply to write the coordinated migration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
