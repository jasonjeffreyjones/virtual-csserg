import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "projects/vcsserg-repo-v1/verify_v1.py"
SPEC = importlib.util.spec_from_file_location("verify_v1_publication_test", MODULE_PATH)
verify = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verify
SPEC.loader.exec_module(verify)


class PublicationStateTests(unittest.TestCase):
    def test_active_unpublished_project_does_not_require_public_reports(self):
        original = verify.read_state_metadata

        def active_unpublished(project):
            metadata = original(project)
            if project.name == "ipseity-daily-pulse":
                metadata = dict(
                    metadata,
                    status="Active",
                    publication="Unpublished",
                    updated="2026-09-16T16:00:00Z",
                )
            return metadata

        with patch.object(verify, "read_state_metadata", side_effect=active_unpublished):
            catalog = verify.check_public_catalogs()
            reports = verify.check_report_formats()
        self.assertTrue(catalog.passed, catalog.detail)
        self.assertTrue(reports.passed, reports.detail)


if __name__ == "__main__":
    unittest.main()
