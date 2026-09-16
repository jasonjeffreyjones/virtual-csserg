"""Manual integration tests for run-scholar.sh.

The filename deliberately does not match unittest's default ``test*.py``
discovery pattern. A live Scholar runner holds the repository-wide iteration
lock, so recursively launching runner fixtures from its routine post-iteration
suite would create a false lock failure. Run this module explicitly when the
runner or its publication boundary changes.
"""

import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]


class RunnerTests(unittest.TestCase):
    def executable(self, path: Path, source: str) -> None:
        path.write_text(source, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)

    def fixture(
        self,
        temporary,
        codex_status=0,
        validation_failure=False,
        dirty=False,
        status_failure=False,
        runner_modified=False,
    ):
        root = Path(temporary) / "repo"
        fakebin = Path(temporary) / "bin"
        fake_home = Path(temporary) / "home"
        (root / "scripts").mkdir(parents=True)
        fakebin.mkdir()
        fake_home.mkdir()
        shutil.copy2(ROOT / "run-scholar.sh", root / "run-scholar.sh")
        shutil.copy2(ROOT / "scripts/preflight.sh", root / "scripts/preflight.sh")
        (root / "run-scholar.sh").chmod(0o755)
        (root / "scripts/preflight.sh").chmod(0o755)
        calls = Path(temporary) / "calls.log"

        self.executable(
            fakebin / "git",
            '''#!/usr/bin/env bash
echo "git $*" >> "$VCSSERG_TEST_CALLS"
if [[ "$1" == "status" ]]; then
  if [[ "${VCSSERG_TEST_STATUS_FAILURE:-0}" == "1" ]]; then exit 9; fi
  if [[ "${VCSSERG_TEST_DIRTY:-0}" == "1" ]]; then echo " M existing.txt"; fi
  exit 0
fi
if [[ "$*" == "diff --quiet HEAD -- run-scholar.sh" ]]; then
  if [[ "${VCSSERG_TEST_RUNNER_MODIFIED:-0}" == "1" ]]; then exit 8; fi
  exit 0
fi
if [[ "$1 $2 $3" == "diff --cached --quiet" ]]; then exit 1; fi
exit 0
''',
        )
        self.executable(
            fakebin / "codex",
            '''#!/usr/bin/env bash
echo "codex $*" >> "$VCSSERG_TEST_CALLS"
touch "$VCSSERG_TEST_REPO/partial-change.txt"
exit "$VCSSERG_TEST_CODEX_STATUS"
''',
        )
        self.executable(
            fakebin / "python3",
            '''#!/usr/bin/env bash
echo "python3 $*" >> "$VCSSERG_TEST_CALLS"
case "$*" in
  *"scholar_roster.py --name-for"*) echo "Test Scholar" ;;
  *"project_registry.py --active-title"*) echo "Test Project" ;;
  *"verify_v1.py"*)
    if [[ "${VCSSERG_TEST_VALIDATION_FAILURE:-0}" == "1" ]]; then exit 7; fi ;;
esac
exit 0
''',
        )
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(fake_home),
                "PATH": f"{fakebin}:/usr/bin:/bin",
                "VCSSERG_TEST_CALLS": str(calls),
                "VCSSERG_TEST_REPO": str(root),
                "VCSSERG_TEST_CODEX_STATUS": str(codex_status),
                "VCSSERG_TEST_VALIDATION_FAILURE": "1" if validation_failure else "0",
                "VCSSERG_TEST_DIRTY": "1" if dirty else "0",
                "VCSSERG_TEST_STATUS_FAILURE": "1" if status_failure else "0",
                "VCSSERG_TEST_RUNNER_MODIFIED": "1" if runner_modified else "0",
            }
        )
        return root, calls, environment

    def run_fixture(self, root, environment):
        return subprocess.run(
            [str(root / "run-scholar.sh"), "test-scholar", "test-project"],
            cwd=root,
            env=environment,
            capture_output=True,
            text=True,
        )

    def assert_no_publication_operations(self, calls):
        source = calls.read_text(encoding="utf-8")
        self.assertNotIn("git add", source)
        self.assertNotIn("git commit", source)
        self.assertNotIn("git push", source)
        self.assertNotIn("vcsserg_deploy.py", source)

    def test_dirty_tree_refuses_to_start_scholar(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(temporary, dirty=True)
            result = self.run_fixture(root, environment)
            self.assertEqual(3, result.returncode)
            self.assertIn("working tree is not clean", result.stderr)
            source = calls.read_text(encoding="utf-8")
            self.assertNotIn("codex ", source)
            self.assertNotIn("git pull", source)
            self.assert_no_publication_operations(calls)

    def test_status_failure_refuses_to_start_scholar(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(temporary, status_failure=True)
            result = self.run_fixture(root, environment)
            self.assertEqual(3, result.returncode)
            self.assertIn("could not inspect", result.stderr)
            source = calls.read_text(encoding="utf-8")
            self.assertNotIn("codex ", source)
            self.assertNotIn("git pull", source)
            self.assert_no_publication_operations(calls)

    def test_runner_edit_fails_validation_before_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(
                temporary, runner_modified=True
            )
            result = self.run_fixture(root, environment)
            self.assertEqual(8, result.returncode)
            self.assert_no_publication_operations(calls)
            log = (root / "logs/test-scholar_test-project.log").read_text()
            self.assertIn("Independent post-iteration validation failed", log)

    def test_scholar_failure_preserves_changes_without_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(temporary, codex_status=42)
            result = self.run_fixture(root, environment)
            self.assertEqual(42, result.returncode)
            self.assertTrue((root / "partial-change.txt").is_file())
            self.assert_no_publication_operations(calls)
            log = (root / "logs/test-scholar_test-project.log").read_text()
            self.assertIn("ITERATION ABORTED", log)
            self.assertNotIn("ITERATION COMPLETE", log)

    def test_validation_failure_preserves_changes_without_publication(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(
                temporary, validation_failure=True
            )
            result = self.run_fixture(root, environment)
            self.assertEqual(7, result.returncode)
            self.assert_no_publication_operations(calls)
            log = (root / "logs/test-scholar_test-project.log").read_text()
            self.assertIn("Independent post-iteration validation failed", log)

    def test_success_commits_pushes_deploys_then_completes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root, calls, environment = self.fixture(temporary)
            result = self.run_fixture(root, environment)
            self.assertEqual(0, result.returncode, result.stderr)
            source = calls.read_text(encoding="utf-8")
            for expected in ("git add -A", "git commit -m", "git push origin main", "vcsserg_deploy.py"):
                self.assertIn(expected, source)
            log = (root / "logs/test-scholar_test-project.log").read_text()
            self.assertIn("ITERATION COMPLETE", log)


if __name__ == "__main__":
    unittest.main()
