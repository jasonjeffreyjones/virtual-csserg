import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python" / "create_project.py"
SPEC = importlib.util.spec_from_file_location("create_project", MODULE_PATH)
create_project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(create_project)


class CreateProjectTests(unittest.TestCase):
    def test_creates_personalized_complete_scaffold(self):
        with tempfile.TemporaryDirectory() as temporary:
            projects_root = Path(temporary) / "projects"
            destination = create_project.create_project(
                "collective-memory-online", "Collective Memory: Online", projects_root
            )
            self.assertEqual(destination, projects_root / "collective-memory-online")
            self.assertEqual(
                {path.name for path in destination.iterdir()},
                {
                    path.name
                    for path in (
                        create_project.DEFAULT_PROJECTS_ROOT / "_template"
                    ).iterdir()
                },
            )
            self.assertIn(
                "# Collective Memory: Online",
                (destination / "PROJECT.md").read_text(encoding="utf-8"),
            )
            state = (destination / "STATE.md").read_text(encoding="utf-8")
            self.assertIn('title: "Collective Memory: Online"', state)
            self.assertIn("status: Proposed", state)
            self.assertIn("updated: null", state)

    def test_refuses_overwrite_without_changing_existing_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            projects_root = Path(temporary) / "projects"
            destination = create_project.create_project(
                "test-project", "First", projects_root
            )
            before = {
                path.name: path.read_bytes() for path in destination.iterdir() if path.is_file()
            }
            with self.assertRaises(create_project.ScaffoldError):
                create_project.create_project("test-project", "Second", projects_root)
            after = {
                path.name: path.read_bytes() for path in destination.iterdir() if path.is_file()
            }
            self.assertEqual(before, after)

    def test_rejects_unsafe_or_unstable_slugs(self):
        for slug in ("Uppercase", "two_words", "two--words", "../outside", "-leading"):
            with self.subTest(slug=slug), self.assertRaises(
                create_project.ScaffoldError
            ):
                create_project.validate_slug(slug)

    def test_rejects_multiline_and_blank_titles(self):
        for title in ("", "   ", "First\nSecond"):
            with self.subTest(title=title), self.assertRaises(
                create_project.ScaffoldError
            ):
                create_project.validate_title(title)


if __name__ == "__main__":
    unittest.main()
