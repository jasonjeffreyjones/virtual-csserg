import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python/scholar_roster.py"
SPEC = importlib.util.spec_from_file_location("scholar_roster", MODULE_PATH)
roster = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roster)


class ScholarRosterTests(unittest.TestCase):
    def write_fixture(self, temporary, scholars):
        root = Path(temporary)
        projects = root / "projects"
        project = projects / "known-project"
        project.mkdir(parents=True)
        (project / "STATE.md").write_text("---\ntitle: Known\n---\n", encoding="utf-8")
        roster_path = root / "scholars.json"
        roster_path.write_text(
            json.dumps({"schema_version": 1, "scholars": scholars}),
            encoding="utf-8",
        )
        return roster_path, projects

    def record(self, **changes):
        base = {
            "name": "Test Scholar",
            "slug": "test-scholar",
            "monogram": "TS",
            "current_project": "known-project",
        }
        base.update(changes)
        return base

    def test_repository_roster_is_valid(self):
        records = roster.load_roster()
        self.assertEqual(4, len(records))
        self.assertEqual(
            "vcsserg-repo-v1",
            next(record for record in records if record.name == "Bee Boring Vanilla").current_project,
        )
        self.assertIsNone(
            next(
                record for record in records
                if record.name == "Disciple Dee Duplo"
            ).current_project
        )

    def test_duplicate_slug_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            roster_path, projects = self.write_fixture(
                temporary,
                [self.record(), self.record(name="Second Scholar", monogram="SS")],
            )
            with self.assertRaisesRegex(roster.RosterError, "duplicate Scholar slug"):
                roster.load_roster(roster_path, projects)

    def test_unknown_project_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            roster_path, projects = self.write_fixture(
                temporary, [self.record(current_project="missing-project")]
            )
            with self.assertRaisesRegex(roster.RosterError, "unknown Project"):
                roster.load_roster(roster_path, projects)

    def test_unexpected_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            roster_path, projects = self.write_fixture(
                temporary, [self.record(biography="Not roster data")]
            )
            with self.assertRaisesRegex(roster.RosterError, "exactly"):
                roster.load_roster(roster_path, projects)


if __name__ == "__main__":
    unittest.main()
