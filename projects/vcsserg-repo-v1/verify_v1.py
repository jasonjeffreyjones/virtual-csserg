#!/usr/bin/env python3
"""Run non-destructive checks for documented VCSSERG Version 1.0 promises."""

from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from html.parser import HTMLParser
import importlib.util
import io
import os
from pathlib import Path
import re
import subprocess
import sys
from unittest.mock import patch
from urllib.parse import unquote, urlsplit


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEBSITE_ROOT = PROJECT_ROOT / "website"
MEMORY_FILES = {"PROJECT.md", "STATE.md", "DIALOG.md"}
SCHOLAR_SLUG_OVERRIDES = {"Bee Boring Vanilla": "b-boring-vanilla"}


@dataclass
class Result:
    label: str
    passed: bool
    detail: str


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = ""
        self.footer_depth = 0
        self.footer_references = []
        self.figure_count = 0
        self.h1_count = 0
        self.html_lang = ""
        self.ids = []
        self.in_title = False
        self.main_count = 0
        self.project_updates = []
        self.references = []
        self.text_parts = []
        self.title_parts = []

    @property
    def title(self):
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "footer":
            self.footer_depth += 1
        if attributes.get("data-project"):
            self.project_updates.append(
                (attributes["data-project"], attributes.get("data-updated", ""))
            )
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)
        if tag == "html":
            self.html_lang = attributes.get("lang", "")
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "figure":
            self.figure_count += 1
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and attributes.get("name", "").lower() == "description":
            self.description = attributes.get("content", "").strip()

        for attribute in ("href", "src"):
            reference = attributes.get(attribute)
            if reference:
                self.references.append(reference)
                if self.footer_depth:
                    self.footer_references.append(reference)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "footer":
            self.footer_depth = max(0, self.footer_depth - 1)

    def handle_data(self, data):
        self.text_parts.append(data)
        if self.in_title:
            self.title_parts.append(data)

    @property
    def text(self):
        return " ".join(" ".join(self.text_parts).split())


def parse_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def resolve_local_reference(page, reference):
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:")):
        return None, parsed.fragment

    relative_path = unquote(parsed.path)
    if relative_path.startswith("/"):
        target = WEBSITE_ROOT / relative_path.lstrip("/")
    elif relative_path:
        target = page.parent / relative_path
    else:
        target = page

    target = target.resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment


def check_repository_documents():
    required = {"AGENTS.md", "README.md", "RESEARCHER-ORIENTATION.md"}
    missing = sorted(name for name in required if not (PROJECT_ROOT / name).is_file())
    return Result(
        "Repository guidance",
        not missing,
        "all required guidance files exist" if not missing else f"missing: {', '.join(missing)}",
    )


def check_project_memory():
    problems = []
    project_directories = sorted(
        path for path in (PROJECT_ROOT / "projects").iterdir()
        if path.is_dir()
    )
    for project in project_directories:
        missing = sorted(name for name in MEMORY_FILES if not (project / name).is_file())
        if missing:
            problems.append(f"{project.name} missing {', '.join(missing)}")
    return Result(
        "Project memory layout",
        not problems,
        f"{len(project_directories)} project directories (including _template) have all three memory files"
        if not problems else "; ".join(problems),
    )


def check_html_and_css():
    html_pages = sorted(WEBSITE_ROOT.rglob("*.html"))
    css_files = sorted(WEBSITE_ROOT.rglob("*.css"))
    parsed_pages = {page: parse_page(page) for page in html_pages}
    problems = []
    titles = {}
    logo_path = (WEBSITE_ROOT / "images" / "csserg-transparent-logo.png").resolve()
    required_footer_references = {
        "https://github.com/jasonjeffreyjones/virtual-csserg/",
        "https://jasonjones.ninja/",
        "https://jasonjones.ninja/csserg/",
        "https://creativecommons.org/licenses/by/4.0/",
        "https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png",
    }
    bootstrap_prefix = "https://cdn.jsdelivr.net/npm/bootstrap@"

    for page, parsed in parsed_pages.items():
        relative = page.relative_to(PROJECT_ROOT)
        if parsed.html_lang != "en":
            problems.append(f"{relative}: expected html lang=en")
        if not parsed.title:
            problems.append(f"{relative}: missing title")
        else:
            titles.setdefault(parsed.title, []).append(relative)
        if parsed.main_count != 1:
            problems.append(f"{relative}: expected one main element")
        if parsed.h1_count < 1:
            problems.append(f"{relative}: expected at least one h1")
        duplicate_ids = sorted({item for item in parsed.ids if parsed.ids.count(item) > 1})
        if duplicate_ids:
            problems.append(f"{relative}: duplicate ids {', '.join(duplicate_ids)}")
        if not any(reference.startswith(bootstrap_prefix) for reference in parsed.references):
            problems.append(f"{relative}: missing Bootstrap from the official CDN")

        missing_footer_references = sorted(
            required_footer_references - set(parsed.footer_references)
        )
        if missing_footer_references:
            problems.append(
                f"{relative}: footer missing brand/license references "
                f"{', '.join(missing_footer_references)}"
            )

        local_targets = set()
        for reference in parsed.references:
            target, fragment = resolve_local_reference(page, reference)
            if target is None:
                continue
            local_targets.add(target)
            try:
                target.relative_to(WEBSITE_ROOT.resolve())
            except ValueError:
                problems.append(f"{relative}: reference leaves website tree: {reference}")
                continue
            if not target.is_file():
                problems.append(f"{relative}: missing local target {reference}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsed_pages.get(target) or parse_page(target)
                if fragment not in target_parser.ids:
                    problems.append(f"{relative}: missing fragment target {reference}")

        if logo_path not in local_targets:
            problems.append(f"{relative}: missing CSSERG logo")

    for title, pages in titles.items():
        if len(pages) > 1:
            problems.append(f"duplicate title {title!r}: {', '.join(map(str, pages))}")

    first_party_css = [path for path in css_files if "site_libs" not in path.parts]
    if not first_party_css:
        problems.append("no CSS files found")
    for css_file in first_party_css:
        css = css_file.read_text(encoding="utf-8")
        relative = css_file.relative_to(PROJECT_ROOT)
        if css.count("{") != css.count("}"):
            problems.append(f"{relative}: unbalanced braces")
        for color, name in (("#4b6f44", "Artichoke Green"), ("#dde3d8", "Laurel Green")):
            if color not in css.lower():
                problems.append(f"{relative}: missing {name} brand color {color}")

    interface_styles = [
        path for path in first_party_css
        if path.name in {"styles.css", "previews.css", "review.css"}
    ]
    for css_file in interface_styles:
        css = css_file.read_text(encoding="utf-8")
        relative = css_file.relative_to(PROJECT_ROOT)
        if "@media" not in css:
            problems.append(f"{relative}: no responsive media query")
        if "prefers-reduced-motion" not in css:
            problems.append(f"{relative}: no reduced-motion treatment")

    return Result(
        "Static HTML/CSS site",
        not problems,
        f"{len(html_pages)} HTML page(s) and {len(first_party_css)} first-party stylesheet(s) passed structural and local-link checks"
        if not problems else "; ".join(problems),
    )


def check_public_catalogs():
    index_path = WEBSITE_ROOT / "index.html"
    index = parse_page(index_path)
    linked_targets = set()
    for reference in index.references:
        target, _ = resolve_local_reference(index_path, reference)
        if target is not None:
            linked_targets.add(target)

    expected_projects = {
        path.name: WEBSITE_ROOT / "projects" / path.name / "index.html"
        for path in (PROJECT_ROOT / "projects").iterdir()
        if path.is_dir() and path.name != "_template"
    }
    problems = []
    project_index_path = WEBSITE_ROOT / "projects" / "index.html"
    project_index_targets = set()
    if not project_index_path.is_file():
        problems.append("website/projects/index.html does not exist")
    else:
        project_index = parse_page(project_index_path)
        for reference in project_index.references:
            target, _ = resolve_local_reference(project_index_path, reference)
            if target is not None:
                project_index_targets.add(target)
        listed_projects = [name for name, _ in project_index.project_updates]
        if (
            len(listed_projects) != len(expected_projects)
            or set(listed_projects) != set(expected_projects)
        ):
            problems.append("website/projects/index.html update metadata does not cover every project exactly once")
        listed_updates = [updated for _, updated in project_index.project_updates]
        if not all(listed_updates) or listed_updates != sorted(listed_updates, reverse=True):
            problems.append("website/projects/index.html is not ordered by descending project update time")

    for name, page in expected_projects.items():
        if not page.is_file():
            problems.append(f"project {name} has no public index")
        elif page.resolve() not in linked_targets:
            problems.append(f"project {name} is not linked from website/index.html")
        elif page.resolve() not in project_index_targets:
            problems.append(f"project {name} is not linked from website/projects/index.html")

    charter = (PROJECT_ROOT / "projects" / "vcsserg-repo-v1" / "PROJECT.md").read_text(
        encoding="utf-8"
    )
    roster_match = re.search(
        r"^## Initial Scholars\s*$([\s\S]*?)(?=^##\s|\Z)",
        charter,
        flags=re.MULTILINE,
    )
    scholar_names = (
        re.findall(r"^###\s+(.+?)\s*$", roster_match.group(1), flags=re.MULTILINE)
        if roster_match else []
    )
    if not scholar_names:
        problems.append("PROJECT.md has no parseable Initial Scholars roster")

    scholar_index_path = WEBSITE_ROOT / "scholars" / "index.html"
    if not scholar_index_path.is_file():
        problems.append("website/scholars/index.html does not exist")
        scholar_index_targets = set()
    else:
        scholar_index = parse_page(scholar_index_path)
        scholar_index_targets = set()
        for reference in scholar_index.references:
            target, _ = resolve_local_reference(scholar_index_path, reference)
            if target is not None:
                scholar_index_targets.add(target)

    for name in scholar_names:
        slug = SCHOLAR_SLUG_OVERRIDES.get(name, re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"))
        page = WEBSITE_ROOT / "scholars" / slug / "index.html"
        if not page.is_file():
            problems.append(f"initial Scholar {name} has no public profile")
        elif page.resolve() not in linked_targets:
            problems.append(f"initial Scholar {name} is not linked from website/index.html")
        elif page.resolve() not in scholar_index_targets:
            problems.append(f"initial Scholar {name} is not linked from the Scholar index")

        bio_match = re.search(
            rf"^###\s+{re.escape(name)}\s*$([\s\S]*?)(?=^###\s|\Z)",
            roster_match.group(1) if roster_match else "",
            flags=re.MULTILINE,
        )
        if page.is_file() and bio_match:
            expected_bio = " ".join(bio_match.group(1).split())
            page_text = parse_page(page).text
            def normalize_bio(value):
                value = value.replace("’", "'").replace(" ", " ")
                return re.sub(r"\s+([,.;:!?])", r"\1", value)

            if normalize_bio(expected_bio) not in normalize_bio(page_text):
                problems.append(f"initial Scholar {name} profile omits or alters the charter biography")

    return Result(
        "Public project and Scholar catalogs",
        not problems,
        "all documented projects and initial Scholars are published and linked"
        if not problems else "; ".join(problems),
    )


def check_report_formats():
    """Check automatable parts of the three-format publication contract."""
    problems = []
    projects = sorted(
        path for path in (PROJECT_ROOT / "projects").iterdir()
        if path.is_dir() and path.name != "_template"
    )

    for project in projects:
        slug = project.name
        public = WEBSITE_ROOT / "projects" / slug
        summary = public / "index.html"
        full_report = public / "report" / "index.html"
        short_report = public / "short-report.pdf"

        if not summary.is_file():
            problems.append(f"{slug}: missing Executive Summary")
        if not full_report.is_file():
            problems.append(f"{slug}: missing Full Report")
        if not short_report.is_file():
            problems.append(f"{slug}: missing short-report.pdf")
        elif not short_report.read_bytes().startswith(b"%PDF"):
            problems.append(f"{slug}: short-report.pdf has no PDF signature")

        if summary.is_file():
            parsed_summary = parse_page(summary)
            if parsed_summary.figure_count != 1:
                problems.append(
                    f"{slug}: Executive Summary has {parsed_summary.figure_count} figures; expected exactly one"
                )
            targets = {
                resolve_local_reference(summary, reference)[0]
                for reference in parsed_summary.references
            }
            if full_report.is_file() and full_report.resolve() not in targets:
                problems.append(f"{slug}: Executive Summary does not link the Full Report")
            if short_report.is_file() and short_report.resolve() not in targets:
                problems.append(f"{slug}: Executive Summary does not link the short report")

        if full_report.is_file():
            report_source = full_report.read_text(encoding="utf-8")
            phrase_count = report_source.lower().count("far beyond")
            if phrase_count != 1:
                problems.append(
                    f"{slug}: Full Report contains 'far beyond' {phrase_count} times; expected exactly once"
                )
            parsed_report = parse_page(full_report)
            targets = {
                resolve_local_reference(full_report, reference)[0]
                for reference in parsed_report.references
            }
            if summary.is_file() and summary.resolve() not in targets:
                problems.append(f"{slug}: Full Report does not link the Executive Summary")
            if short_report.is_file() and short_report.resolve() not in targets:
                problems.append(f"{slug}: Full Report does not link the short report")

        if not (project / "_quarto.yml").is_file():
            problems.append(f"{slug}: missing Quarto book configuration")
        if not list(project.glob("*.qmd")):
            problems.append(f"{slug}: missing Quarto source")

    return Result(
        "Three-format project reports",
        not problems,
        f"{len(projects)} projects have linked Executive Summaries, Quarto Full Reports, and short PDFs"
        if not problems else "; ".join(problems),
    )


def check_runner():
    runner = PROJECT_ROOT / "run-scholar.sh"
    syntax = subprocess.run(
        ["bash", "-n", str(runner)], capture_output=True, text=True, check=False
    )
    problems = []
    if syntax.returncode != 0:
        problems.append("shell syntax check failed")

    source = runner.read_text(encoding="utf-8")
    for command in ("flock -n", "git pull --ff-only", "git commit", "git push"):
        if command not in source:
            problems.append(f"missing workflow command: {command}")

    deploy_matches = re.findall(r"^\s*python3\s+([^\s]+)\s*$", source, flags=re.MULTILINE)
    if len(deploy_matches) != 1:
        problems.append("expected one literal python3 deployment command")
    else:
        deployment_path = (PROJECT_ROOT / deploy_matches[0].strip("'\"")).resolve()
        if not deployment_path.is_file():
            problems.append(
                f"deployment command resolves to missing {deployment_path.relative_to(PROJECT_ROOT)}"
            )

    log_file_reference = re.search(r"\$(?:LOG_FILE\b|\{LOG_FILE(?:[^}]*)\})", source)
    log_file_assignment = re.search(r"^\s*LOG_FILE=", source, flags=re.MULTILINE)
    if log_file_reference and not log_file_assignment:
        problems.append("LOG_FILE is referenced but never assigned under set -u")

    return Result(
        "Automated Scholar runner",
        not problems,
        "runner syntax and pull/lock/commit/push/deploy wiring passed"
        if not problems else "; ".join(problems),
    )


def load_deployment_module():
    path = PROJECT_ROOT / "python" / "vcsserg_deploy.py"
    spec = importlib.util.spec_from_file_location("vcsserg_deploy_for_check", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_deployment_component():
    deployment = load_deployment_module()
    fake_environment = {
        "VCSSERG_DEPLOY_SSH_PORT": "22",
        "VCSSERG_DEPLOY_SSH_USER": "check-user",
        "VCSSERG_DEPLOY_SSH_HOST": "check-host",
        "VCSSERG_DEPLOY_REMOTE_PATH": "/check/virtual-csserg/",
    }
    problems = []

    with patch.dict(os.environ, fake_environment, clear=False):
        with patch.object(deployment.subprocess, "run") as mocked_run:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                deployment.deploy()
            command = mocked_run.call_args.args[0]
            options = mocked_run.call_args.kwargs
            if not isinstance(command, list) or options.get("shell") is True:
                problems.append("rsync is not invoked as a shell-free argument list")
            if options.get("check") is not True:
                problems.append("rsync subprocess failures are not checked")
            if not any(part.startswith("--delete") for part in command):
                problems.append("rsync does not delete stale remote website files")

        failure = subprocess.CalledProcessError(23, ["rsync"])
        with patch.object(deployment.subprocess, "run", side_effect=failure):
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    deployment.deploy()
            except SystemExit as error:
                if error.code in {None, 0}:
                    problems.append("rsync failure produced a successful exit status")
            except subprocess.CalledProcessError:
                pass
            else:
                problems.append("rsync failure did not reach the caller")

        with patch.object(deployment.subprocess, "run", side_effect=FileNotFoundError):
            try:
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    deployment.deploy()
            except SystemExit as error:
                if error.code != 127:
                    problems.append("missing rsync did not produce exit status 127")
            else:
                problems.append("missing rsync did not reach the caller")

        with patch.dict(
            os.environ, {"VCSSERG_DEPLOY_SSH_PORT": "not-a-port"}, clear=False
        ):
            with patch.object(deployment.subprocess, "run") as mocked_run:
                try:
                    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                        deployment.deploy()
                except ValueError:
                    pass
                else:
                    problems.append("invalid SSH port was accepted")
                if mocked_run.called:
                    problems.append("rsync ran with an invalid SSH port")

        with patch.dict(
            os.environ, {"VCSSERG_DEPLOY_REMOTE_PATH": "/"}, clear=False
        ):
            with patch.object(deployment.subprocess, "run") as mocked_run:
                try:
                    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                        deployment.deploy()
                except ValueError:
                    pass
                else:
                    problems.append("an unsafe remote deployment path was accepted")
                if mocked_run.called:
                    problems.append("rsync ran with an unsafe remote deployment path")

    return Result(
        "Deployment component",
        not problems,
        "guarded exact-mirror rsync and nonzero failure propagation passed"
        if not problems else "; ".join(problems),
    )


def main():
    checks = [
        check_repository_documents(),
        check_project_memory(),
        check_html_and_css(),
        check_public_catalogs(),
        check_report_formats(),
        check_runner(),
        check_deployment_component(),
    ]
    for result in checks:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.label}: {result.detail}")

    passed = sum(result.passed for result in checks)
    print(f"\n{passed}/{len(checks)} checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
