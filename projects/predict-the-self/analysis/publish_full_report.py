#!/usr/bin/env python3
"""Replace the public Full Report with the complete local Quarto build."""

import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import uuid


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
SOURCE = PROJECT / "_book"
PUBLIC = ROOT / "website/projects/predict-the-self/report"
MANIFEST = PROJECT / "PUBLICATION_ARTIFACTS.json"


class PublicationError(ValueError):
    """Raised when the completed local report cannot be safely published."""


def load_artifact_manifest(path: Path = MANIFEST) -> dict[str, str]:
    """Load one safe, duplicate-free source-to-alias artifact inventory."""
    try:
        pairs = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=lambda items: items
        )
    except (OSError, json.JSONDecodeError) as error:
        raise PublicationError(f"cannot read artifact manifest {path}: {error}") from error
    if not isinstance(pairs, list) or not pairs:
        raise PublicationError("artifact manifest must be a nonempty JSON object")

    artifacts = {}
    aliases = set()
    for entry in pairs:
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise PublicationError("artifact manifest must be a JSON object")
        source, alias = entry
        if not isinstance(source, str) or not isinstance(alias, str):
            raise PublicationError("artifact manifest paths must be strings")
        if source in artifacts:
            raise PublicationError(f"duplicate artifact source {source}")
        if alias in aliases:
            raise PublicationError(f"duplicate artifact alias {alias}")
        for label, value in (("source", source), ("alias", alias)):
            relative = PurePosixPath(value)
            if (
                not relative.parts
                or relative.is_absolute()
                or ".." in relative.parts
                or "\\" in value
            ):
                raise PublicationError(f"unsafe artifact {label} path {value}")
        if PurePosixPath(alias).parts[0] != "artifacts":
            raise PublicationError(f"artifact alias is outside artifacts/: {alias}")
        if source == alias:
            raise PublicationError(f"artifact source and alias are identical: {source}")
        artifacts[source] = alias
        aliases.add(alias)
    return artifacts


def normalize_generated_html(tree: Path) -> None:
    """Remove generator-introduced line-end whitespace from public HTML."""
    for path in tree.rglob("*.html"):
        source = path.read_text(encoding="utf-8")
        normalized = "\n".join(line.rstrip() for line in source.splitlines())
        if source.endswith(("\n", "\r")):
            normalized += "\n"
        path.write_text(normalized, encoding="utf-8")


def validate_authoritative_artifacts(
    source: Path, project: Path, artifacts: dict[str, str]
) -> None:
    """Require every built canonical artifact to equal its Project source."""
    for relative in artifacts:
        built = (source / relative).resolve()
        authoritative = (project / relative).resolve()
        if not built.is_relative_to(source):
            raise PublicationError(f"build artifact escapes report tree: {relative}")
        if not authoritative.is_relative_to(project):
            raise PublicationError(f"Project artifact escapes Project tree: {relative}")
        if not authoritative.is_file():
            raise PublicationError(f"missing authoritative Project artifact {relative}")
        if built.read_bytes() != authoritative.read_bytes():
            raise PublicationError(
                f"built artifact differs from authoritative Project source: {relative}"
            )


def publish(
    source: Path = SOURCE,
    public: Path = PUBLIC,
    project: Path = PROJECT,
    manifest: Path = MANIFEST,
) -> None:
    source = Path(source).resolve()
    public = Path(public).resolve()
    project = Path(project).resolve()
    artifacts = load_artifact_manifest(manifest)
    required = (source / "index.html", source / "report.html", source / "report.css")
    required += tuple(source / path for path in artifacts)
    for artifact in required:
        if not artifact.is_file():
            raise PublicationError(f"missing build artifact {artifact}")
    validate_authoritative_artifacts(source, project, artifacts)

    public.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".predict-report-stage-", dir=public.parent))
    backup = public.parent / f".predict-report-backup-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True)
        for current, legacy in artifacts.items():
            alias = staging / legacy
            alias.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(staging / current, alias)
        normalize_generated_html(staging)
        if public.exists():
            public.rename(backup)
            moved_existing = True
        staging.rename(public)
    except Exception:
        if not public.exists() and moved_existing and backup.exists():
            backup.rename(public)
        if staging.exists():
            shutil.rmtree(staging)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


def main() -> int:
    try:
        publish()
    except PublicationError as error:
        raise SystemExit(f"publish_full_report: {error}") from error
    print(f"Published {SOURCE.relative_to(ROOT)} to {PUBLIC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
