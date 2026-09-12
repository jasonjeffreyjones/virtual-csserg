#!/usr/bin/env python3
"""Replace the public Full Report with the complete local Quarto build."""

from pathlib import Path
import shutil
import tempfile
import uuid


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
SOURCE = PROJECT / "_book"
PUBLIC = ROOT / "website/projects/vcsserg-repo-v1/report"


class PublicationError(ValueError):
    """Raised when the completed local report cannot be safely published."""


def publish(source: Path = SOURCE, public: Path = PUBLIC) -> None:
    source = Path(source).resolve()
    public = Path(public).resolve()
    for required in (source / "index.html", source / "report.css"):
        if not required.is_file():
            raise PublicationError(f"missing build artifact {required}")

    public.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".v1-report-stage-", dir=public.parent))
    backup = public.parent / f".v1-report-backup-{uuid.uuid4().hex}"
    moved_existing = False
    try:
        shutil.copytree(source, staging, dirs_exist_ok=True)
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
