import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python/project_registry.py"
SPEC = importlib.util.spec_from_file_location("project_registry", MODULE_PATH)
registry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = registry
SPEC.loader.exec_module(registry)


class ProjectRegistryTests(unittest.TestCase):
    def write_project(self, root, status="Active", publication="Unpublished"):
        project = Path(root) / "example-project"
        project.mkdir(parents=True)
        (project / "STATE.md").write_text(
            "---\n"
            'title: "Example Project"\n'
            f"status: {status}\n"
            f"publication: {publication}\n"
            "updated: 2026-09-16\n"
            "---\n",
            encoding="utf-8",
        )
        return project

    def test_active_unpublished_project_is_valid_for_iterations(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.write_project(temporary)
            self.assertEqual(
                "Example Project",
                registry.active_project_title("example-project", Path(temporary)),
            )

    def test_non_active_project_is_rejected_for_iterations(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.write_project(temporary, status="Paused", publication="Published")
            with self.assertRaisesRegex(registry.ProjectError, "require Active"):
                registry.active_project_title("example-project", Path(temporary))

    def test_proposed_published_combination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            self.write_project(temporary, status="Proposed", publication="Published")
            with self.assertRaisesRegex(registry.ProjectError, "cannot be Proposed"):
                registry.load_project("example-project", Path(temporary))


if __name__ == "__main__":
    unittest.main()
