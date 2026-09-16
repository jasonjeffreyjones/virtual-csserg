import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
PYTHON_ROOT = ROOT / "python"
sys.path.insert(0, str(PYTHON_ROOT))
MODULE_PATH = PYTHON_ROOT / "create_scholar.py"
SPEC = importlib.util.spec_from_file_location("create_scholar", MODULE_PATH)
create_scholar = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(create_scholar)


class CreateScholarTests(unittest.TestCase):
    def fixture(self, temporary):
        root = Path(temporary)
        (root / "scholars/existing-scholar").mkdir(parents=True)
        (root / "scholars/existing-scholar/BIOGRAPHY.md").write_text(
            "Existing biography.\n", encoding="utf-8"
        )
        (root / "scholars.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "scholars": [
                        {
                            "name": "Existing Scholar",
                            "slug": "existing-scholar",
                            "monogram": "ES",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        (root / "website/scholars/existing-scholar").mkdir(parents=True)
        (root / "website/scholars/existing-scholar/index.html").write_text(
            "existing", encoding="utf-8"
        )
        (root / "website/index.html").write_text(
            "before"
            + create_scholar.HOME_START
            + '<ul class="people"><li>Existing</li></ul>'
            + create_scholar.HOME_END
            + "after",
            encoding="utf-8",
        )
        (root / "website/scholars/index.html").write_text(
            "existing directory", encoding="utf-8"
        )
        biography = root / "new-biography.md"
        biography.write_text("First paragraph.\n\nSecond & final paragraph.\n", encoding="utf-8")
        return root, biography

    def test_creates_identity_biography_and_public_pages(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, biography = self.fixture(temporary)
            destination = create_scholar.create_scholar(
                "new-scholar", "New Scholar", "NS", biography, root
            )
            self.assertEqual(root / "scholars/new-scholar", destination)
            roster = json.loads((root / "scholars.json").read_text(encoding="utf-8"))
            self.assertEqual(2, roster["schema_version"])
            self.assertEqual(
                {"name": "New Scholar", "slug": "new-scholar", "monogram": "NS"},
                roster["scholars"][-1],
            )
            profile = (root / "website/scholars/new-scholar/index.html").read_text(
                encoding="utf-8"
            )
            self.assertIn("First paragraph.", profile)
            self.assertIn("Second &amp; final paragraph.", profile)
            self.assertNotIn("assignment", profile.lower())
            self.assertIn("scholars/new-scholar/", (root / "website/index.html").read_text())
            self.assertIn("New Scholar", (root / "website/scholars/index.html").read_text())

    def test_refuses_overwrite_and_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, biography = self.fixture(temporary)
            create_scholar.create_scholar("new-scholar", "New Scholar", "NS", biography, root)
            before = (root / "scholars.json").read_bytes()
            with self.assertRaises(create_scholar.ScholarCreationError):
                create_scholar.create_scholar(
                    "new-scholar", "Replacement", "RR", biography, root
                )
            self.assertEqual(before, (root / "scholars.json").read_bytes())

    def test_rejects_duplicate_identity_fields(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, biography = self.fixture(temporary)
            for name, slug, monogram in (
                ("Existing Scholar", "different", "DI"),
                ("Different", "different", "ES"),
            ):
                with self.subTest(name=name, monogram=monogram), self.assertRaises(
                    create_scholar.ScholarCreationError
                ):
                    create_scholar.create_scholar(
                        slug, name, monogram, biography, root
                    )

    def test_rolls_back_files_when_installation_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, biography = self.fixture(temporary)
            watched = [
                root / "scholars.json",
                root / "website/index.html",
                root / "website/scholars/index.html",
            ]
            before = {path: path.read_bytes() for path in watched}
            real_load = create_scholar.scholar_roster.load_roster
            calls = 0

            def fail_after_writes(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise RuntimeError("injected final validation failure")
                return real_load(*args, **kwargs)

            with patch.object(
                create_scholar.scholar_roster,
                "load_roster",
                side_effect=fail_after_writes,
            ), self.assertRaisesRegex(RuntimeError, "injected"):
                create_scholar.create_scholar(
                    "new-scholar", "New Scholar", "NS", biography, root
                )

            self.assertEqual(before, {path: path.read_bytes() for path in watched})
            self.assertFalse((root / "scholars/new-scholar").exists())
            self.assertFalse((root / "website/scholars/new-scholar").exists())


if __name__ == "__main__":
    unittest.main()
