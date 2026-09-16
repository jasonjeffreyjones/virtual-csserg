import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python" / "migrate_dialogs.py"
SPEC = importlib.util.spec_from_file_location("migrate_dialogs", MODULE_PATH)
migrate_dialogs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migrate_dialogs)


class MigrateDialogsTests(unittest.TestCase):
    def write_project(self, root, slug, title, dialog):
        project = Path(root) / slug
        project.mkdir(parents=True)
        (project / "STATE.md").write_text(
            f'---\ntitle: "{title}"\nstatus: Active\nupdated: 2026-09-16\n---\n',
            encoding="utf-8",
        )
        (project / "DIALOG.md").write_bytes(dialog)
        return project

    def test_dry_run_is_read_only_for_every_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = self.write_project(temporary, "first", "First", b"first\n")
            second = self.write_project(temporary, "second", "Second", b"second\n")

            plans = migrate_dialogs.migrate_all(
                temporary, "2026-09-16", apply=False
            )

            self.assertEqual(["first", "second"], [plan.project.name for plan in plans])
            self.assertEqual(b"first\n", (first / "DIALOG.md").read_bytes())
            self.assertEqual(b"second\n", (second / "DIALOG.md").read_bytes())
            self.assertFalse((first / "dialog").exists())
            self.assertFalse((second / "dialog").exists())

    def test_apply_preserves_legacy_bytes_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            legacy = b"# A dialog\n\n> PI guidance\n"
            project = self.write_project(temporary, "alpha", "Alpha", legacy)

            migrate_dialogs.migrate_all(temporary, "2026-09-16", apply=True)

            archive = project / "dialog/legacy/DIALOG-through-2026-09-16.md"
            self.assertEqual(legacy, archive.read_bytes())
            digest = hashlib.sha256(legacy).hexdigest()
            landing = (project / "DIALOG.md").read_text(encoding="utf-8")
            self.assertIn(migrate_dialogs.PROTOCOL_MARKER, landing)
            self.assertIn(digest, landing)
            self.assertIn("Review PI-authored guidance", landing)
            self.assertTrue((project / "dialog/iterations").is_dir())
            self.assertTrue((project / "dialog/indexes/2026.md").is_file())
            with self.assertRaisesRegex(
                migrate_dialogs.MigrationError, "refusing to overwrite"
            ):
                migrate_dialogs.migrate_all(temporary, "2026-09-16", apply=True)

    def test_preflight_failure_leaves_every_project_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = self.write_project(temporary, "first", "First", b"first\n")
            second = self.write_project(temporary, "second", "Second", b"second\n")
            (second / "dialog").mkdir()

            with self.assertRaisesRegex(
                migrate_dialogs.MigrationError, "refusing to overwrite"
            ):
                migrate_dialogs.migrate_all(temporary, "2026-09-16", apply=True)

            self.assertEqual(b"first\n", (first / "DIALOG.md").read_bytes())
            self.assertEqual(b"second\n", (second / "DIALOG.md").read_bytes())
            self.assertFalse((first / "dialog").exists())


if __name__ == "__main__":
    unittest.main()
