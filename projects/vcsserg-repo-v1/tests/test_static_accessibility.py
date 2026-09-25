import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "projects/vcsserg-repo-v1/verify_v1.py"
SPEC = importlib.util.spec_from_file_location("verify_v1_accessibility", MODULE_PATH)
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def parse(source):
    parser = VERIFY.PageParser()
    parser.feed(source)
    return parser


def review_source(status, rows, field_value="Not recorded"):
    fields = "\n".join(
        f"{label}: {field_value}" for label in VERIFY.ACCESSIBILITY_RESULT_FIELDS
    )
    table = "\n".join(
        "| `" + path + "` | " + " | ".join(statuses) + " | note |"
        for path, statuses in rows
    )
    return (
        f"Status: **{status}**\n\n{fields}\n"
        f"{VERIFY.ACCESSIBILITY_RESULTS_START}\n{table}\n"
        f"{VERIFY.ACCESSIBILITY_RESULTS_END}\n"
    )


class StaticAccessibilityTests(unittest.TestCase):
    def test_accepts_first_bypass_link_and_explicit_image_alternatives(self):
        page = parse(
            '<a class="skip-link" href="#main">Skip to content</a>'
            '<main id="main"><img src="meaningful.png" alt="A chart">'
            '<img src="decoration.png" alt=""></main>'
        )
        self.assertEqual(VERIFY.page_accessibility_problems(page, "page.html"), [])

    def test_rejects_missing_or_late_bypass_link_and_missing_alt(self):
        missing = parse('<main><img src="chart.png"></main>')
        self.assertEqual(
            VERIFY.page_accessibility_problems(missing, "missing.html"),
            [
                "missing.html: missing bypass link",
                "missing.html: image has no alt attribute: chart.png",
            ],
        )

        late = parse(
            '<a href="/">Home</a><a class="skip" href="#main">Skip</a>'
            '<main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(late, "late.html"),
            ["late.html: bypass link is not the first link"],
        )

        runtime_relocated = parse(
            '<a href="/">Home</a>'
            '<a class="report-skip" href="#main">Skip</a>'
            '<script>document.body.prepend('
            'document.currentScript.previousElementSibling)</script>'
            '<main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(runtime_relocated, "relocated.html"),
            ["relocated.html: bypass link is not the first link"],
        )

        wrong_target = parse(
            '<a class="skip" href="#navigation">Skip</a>'
            '<nav id="navigation"></nav><main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(wrong_target, "wrong.html"),
            ["wrong.html: missing bypass link"],
        )

    def test_rejects_valid_bypass_after_misleading_first_skip_link(self):
        misleading_first_link = parse(
            '<a class="skip" href="#navigation">Skip to navigation</a>'
            '<nav id="navigation"></nav>'
            '<a class="skip" href="#main">Skip to content</a>'
            '<main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(
                misleading_first_link, "misleading.html"
            ),
            ["misleading.html: bypass link is not the first link"],
        )

    def test_repeated_navigation_landmarks_need_resolvable_names(self):
        unnamed = parse(
            '<a class="skip" href="#main">Skip</a>'
            '<nav><a href="/">Home</a></nav>'
            '<main id="main"><nav aria-labelledby="missing"></nav></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unnamed, "navigation.html"),
            [
                "navigation.html: navigation landmark 1 has no accessible name",
                "navigation.html: navigation landmark 2 references missing label ids: missing",
            ],
        )

        named = parse(
            '<a class="skip" href="#main">Skip</a>'
            '<nav aria-label="Primary"><a href="/">Home</a></nav>'
            '<main id="main"><h2 id="contents">Contents</h2>'
            '<nav aria-labelledby="contents"></nav></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(named, "navigation.html"), []
        )

    def test_table_headers_need_valid_scope(self):
        unscoped = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            "<table><thead><tr><th>Result</th></tr></thead></table></main>"
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unscoped, "table.html"),
            ["table.html: table header cell 1 has no valid scope"],
        )

        scoped = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<table><thead><tr><th scope="col">Result</th></tr></thead>'
            '<tbody><tr><th scope="row">Project</th></tr></tbody></table></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(scoped, "table.html"), []
        )

    def test_interactive_elements_need_accessible_names(self):
        unnamed = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<a href="elsewhere"><span aria-hidden="true">→</span></a>'
            '<button aria-labelledby="empty"></button>'
            '<span id="empty" aria-hidden="true">Menu</span></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unnamed, "controls.html"),
            [
                "controls.html: interactive element 2 (a) has no accessible name",
                "controls.html: interactive element 3 (button) references labels without text",
                "controls.html: interactive element 3 (button) has no accessible name",
            ],
        )

        hidden_code_anchor = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<span id="line"><a href="#line" aria-hidden="true" '
            'tabindex="-1"></a>Code</span></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(hidden_code_anchor, "code.html"), []
        )

    def test_names_native_form_disclosures_and_custom_focus_targets(self):
        valid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<details><summary><span aria-hidden="true">+</span>Code output</summary>'
            '<p>Result</p></details>'
            '<div tabindex="0" role="region" aria-label="Scrollable results"></div>'
            '<label for="query">Search reports</label>'
            '<input id="query" type="search" placeholder="Search">'
            '<label>Topic<textarea></textarea></label>'
            '<input type="submit" value="Run">'
            '<input type="hidden" value="internal">'
            '<map><area href="details" alt="Detailed results"></map></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "controls.html"), []
        )

        unnamed = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<details><summary><span aria-hidden="true">+</span></summary></details>'
            '<div tabindex="0"><span aria-hidden="true">Scrollable</span></div>'
            '<input type="search" placeholder="Search"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unnamed, "controls.html"),
            [
                "controls.html: interactive element 2 (summary) has no accessible name",
                "controls.html: interactive element 3 (div) has no accessible name",
                "controls.html: interactive element 4 (input) has no accessible name",
            ],
        )

    def test_interactive_aria_targets_and_states_must_resolve(self):
        broken = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<button aria-label="Menu" aria-controls="missing" '
            'aria-expanded="mixed"></button>'
            '<a href="elsewhere" aria-hidden="true">Hidden link</a></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(broken, "aria.html"),
            [
                "aria.html: interactive element 2 (button) references missing controlled ids: missing",
                "aria.html: interactive element 2 (button) has invalid aria-expanded",
                "aria.html: interactive element 3 (a) is hidden from assistive technology",
            ],
        )

        valid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<span id="menu-name">Sections <span>for</span> reports</span>'
            '<div id="menu"></div>'
            '<button aria-labelledby="menu-name" aria-controls="menu" '
            'aria-expanded="false"></button></main>'
        )
        self.assertEqual(valid.text_for_id("menu-name"), "Sections for reports")
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "aria.html"), []
        )

    def test_review_protocol_covers_current_manual_sample(self):
        expected = VERIFY.expected_accessibility_review_pages()
        source = (
            ROOT / "projects/vcsserg-repo-v1/ACCESSIBILITY-REVIEW.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(len(expected), 11)
        self.assertEqual(VERIFY.accessibility_review_problems(source, expected), [])

    def test_review_protocol_rejects_missing_duplicate_and_unknown_results(self):
        source = review_source(
            "Open",
            [
                ("website/a.html", ["Pass", "Pass", "Pass", "Pass"]),
                ("website/a.html", ["Maybe", "Pass", "Pass", "Pass"]),
            ],
        )
        problems = VERIFY.accessibility_review_problems(
            source, ["website/a.html", "website/b.html"]
        )
        self.assertTrue(any("invalid status 'Maybe'" in item for item in problems))
        self.assertIn(
            "accessibility review lists website/a.html more than once", problems
        )
        self.assertIn("accessibility review omits website/b.html", problems)

    def test_closed_review_requires_complete_passing_evidence(self):
        expected = ["website/a.html"]
        incomplete = review_source(
            "Closed",
            [("website/a.html", ["Pass", "Pass", "Not tested", "Pass"])],
        )
        problems = VERIFY.accessibility_review_problems(incomplete, expected)
        self.assertTrue(any("non-passing rows" in item for item in problems))
        self.assertTrue(any("placeholder fields" in item for item in problems))

        complete = review_source(
            "Closed",
            [("website/a.html", ["Pass", "Pass", "Pass", "Pass"])],
            field_value="Recorded",
        )
        complete = complete.replace("Commit: Recorded", "Commit: " + "a" * 40)
        complete = complete.replace(
            "Base URL: Recorded",
            "Base URL: https://jasonjones.ninja/virtual-csserg/",
        )
        complete = complete.replace("Date (UTC): Recorded", "Date (UTC): 2026-09-20")
        self.assertEqual(
            VERIFY.accessibility_review_problems(complete, expected), []
        )


if __name__ == "__main__":
    unittest.main()
