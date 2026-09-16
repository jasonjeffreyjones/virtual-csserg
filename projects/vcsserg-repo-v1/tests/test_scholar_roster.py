import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python/scholar_roster.py"
SPEC = importlib.util.spec_from_file_location("scholar_roster", MODULE_PATH)
roster = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = roster
SPEC.loader.exec_module(roster)


class ScholarRosterTests(unittest.TestCase):
    def write_fixture(self, temporary, scholars):
        root = Path(temporary)
        biographies = root / "scholars"
        for scholar in scholars:
            biography = biographies / scholar["slug"] / "BIOGRAPHY.md"
            biography.parent.mkdir(parents=True, exist_ok=True)
            biography.write_text("PI-authored biography.\n", encoding="utf-8")
        roster_path = root / "scholars.json"
        roster_path.write_text(
            json.dumps({"schema_version": 2, "scholars": scholars}),
            encoding="utf-8",
        )
        return roster_path, biographies

    def record(self, **changes):
        base = {
            "name": "Test Scholar",
            "slug": "test-scholar",
            "monogram": "TS",
        }
        base.update(changes)
        return base

    def test_repository_roster_and_biographies_are_valid(self):
        records = roster.load_roster()
        names = {record.name for record in records}
        self.assertTrue(
            {"Aleph Initial Alpha", "Bee Boring Vanilla", "Ceetown"}.issubset(names)
        )
        self.assertEqual(len(records), len({record.slug for record in records}))

    def test_lookup_uses_permanent_slug(self):
        self.assertEqual(
            "Bee Boring Vanilla", roster.scholar_by_slug("b-boring-vanilla").name
        )
        with self.assertRaisesRegex(roster.RosterError, "unknown Scholar"):
            roster.scholar_by_slug("missing-scholar")

    def test_duplicate_slug_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            records = [
                self.record(),
                self.record(name="Second Scholar", slug="test-scholar", monogram="SS"),
            ]
            roster_path, biographies = self.write_fixture(temporary, records)
            with self.assertRaisesRegex(roster.RosterError, "duplicate Scholar slug"):
                roster.load_roster(roster_path, biographies)

    def test_missing_biography_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            roster_path = root / "scholars.json"
            roster_path.write_text(
                json.dumps({"schema_version": 2, "scholars": [self.record()]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(roster.RosterError, "cannot read biography"):
                roster.load_roster(roster_path, root / "scholars")

    def test_assignment_field_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            record = self.record(current_project="known-project")
            roster_path, biographies = self.write_fixture(temporary, [record])
            with self.assertRaisesRegex(roster.RosterError, "exactly"):
                roster.load_roster(roster_path, biographies)


if __name__ == "__main__":
    unittest.main()
