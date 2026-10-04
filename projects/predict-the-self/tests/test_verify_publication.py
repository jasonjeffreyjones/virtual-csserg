from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "analysis/verify_publication.py"
)
SPEC = importlib.util.spec_from_file_location("predict_verify_publication", MODULE_PATH)
assert SPEC and SPEC.loader
verify_publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_publication)


class ArtifactCopyTests(unittest.TestCase):
    def test_matching_canonical_and_alias_copies_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            for path in (source, canonical, alias):
                path.write_bytes(b"authoritative research artifact\n")

            verify_publication.validate_artifact_copy(source, canonical, alias)

    def test_stale_canonical_copy_fails_even_when_public_copies_match(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            source.write_bytes(b"current\n")
            canonical.write_bytes(b"stale\n")
            alias.write_bytes(b"stale\n")

            with self.assertRaisesRegex(
                AssertionError, "published artifact differs from Project source"
            ):
                verify_publication.validate_artifact_copy(source, canonical, alias)

    def test_stale_alias_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            canonical = root / "canonical.txt"
            alias = root / "alias.txt"
            source.write_bytes(b"current\n")
            canonical.write_bytes(b"current\n")
            alias.write_bytes(b"stale\n")

            with self.assertRaisesRegex(
                AssertionError,
                "published artifact alias differs from Project source",
            ):
                verify_publication.validate_artifact_copy(source, canonical, alias)


if __name__ == "__main__":
    unittest.main()
