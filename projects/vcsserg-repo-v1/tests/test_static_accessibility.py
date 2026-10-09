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
    def test_autofocus_is_rejected(self):
        valid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<label for="query">Search</label><input id="query"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "stable.html"), []
        )

        automatic = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<input aria-label="Search" autofocus>'
            '<button autofocus="false">Menu</button></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(automatic, "focus.html"),
            ["focus.html: contains 2 autofocus attribute(s)"],
        )

    def test_automatic_meta_refresh_or_redirect_is_rejected(self):
        valid = parse(
            '<meta http-equiv="content-type" content="text/html; charset=utf-8">'
            '<a class="skip" href="#main">Skip</a><main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "stable.html"), []
        )

        automatic = parse(
            '<meta http-equiv="refresh" content="30">'
            '<meta HTTP-EQUIV="Refresh" content="0; url=elsewhere.html">'
            '<a class="skip" href="#main">Skip</a><main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(automatic, "timed.html"),
            [
                "timed.html: contains 2 automatic meta refresh or redirect "
                "declaration(s)"
            ],
        )

    def test_viewport_is_responsive_and_does_not_restrict_zoom(self):
        valid = parse(
            '<meta name="viewport" '
            'content="width=device-width, initial-scale=1, user-scalable=yes">'
        )
        self.assertEqual(VERIFY.page_viewport_problems(valid, "page.html"), [])

        valid_at_two_hundred_percent = parse(
            '<meta name="viewport" '
            'content="width=device-width, maximum-scale=2">'
        )
        self.assertEqual(
            VERIFY.page_viewport_problems(
                valid_at_two_hundred_percent, "page.html"
            ),
            [],
        )

        missing = parse("<html><body></body></html>")
        self.assertEqual(
            VERIFY.page_viewport_problems(missing, "missing.html"),
            ["missing.html: expected one viewport meta declaration, found 0"],
        )

        duplicate = parse(
            '<meta name="viewport" content="width=device-width">'
            '<meta name="viewport" content="width=device-width">'
        )
        self.assertEqual(
            VERIFY.page_viewport_problems(duplicate, "duplicate.html"),
            ["duplicate.html: expected one viewport meta declaration, found 2"],
        )

        restrictive = parse(
            '<meta name="viewport" content="width=980, user-scalable=no, '
            'maximum-scale=1.5">'
        )
        self.assertEqual(
            VERIFY.page_viewport_problems(restrictive, "restricted.html"),
            [
                "restricted.html: viewport does not use width=device-width",
                "restricted.html: viewport disables user scaling",
                "restricted.html: viewport maximum-scale is below 2",
            ],
        )

        ambiguous = parse(
            '<meta name="viewport" content="width=device-width, maximum-scale=yes">'
        )
        self.assertEqual(
            VERIFY.page_viewport_problems(ambiguous, "ambiguous.html"),
            ["ambiguous.html: viewport has invalid maximum-scale 'yes'"],
        )

    def test_page_frame_has_one_top_level_banner_main_and_contentinfo(self):
        valid = parse(
            "<html><body><header>Site identity</header><main>"
            "<article><header>Article title</header><footer>Article notes</footer>"
            "</article></main><footer>Site information</footer></body></html>"
        )
        self.assertEqual(valid.banner_count, 1)
        self.assertEqual(valid.contentinfo_count, 1)
        self.assertEqual(VERIFY.page_landmark_problems(valid, "frame.html"), [])

        missing = parse(
            "<html><body><main><header>Section title</header>"
            "<footer>Section notes</footer></main></body></html>"
        )
        self.assertEqual(
            VERIFY.page_landmark_problems(missing, "frame.html"),
            [
                "frame.html: expected one banner landmark, found 0",
                "frame.html: expected one contentinfo landmark, found 0",
            ],
        )

        invalid = parse(
            '<html><body><header>First</header><div role="banner">Second</div>'
            '<main><footer>Nested notes</footer></main><div role="main"></div>'
            '<footer>First</footer><div role="contentinfo">Second</div>'
            "</body></html>"
        )
        self.assertEqual(
            VERIFY.page_landmark_problems(invalid, "frame.html"),
            [
                "frame.html: expected one banner landmark, found 2",
                "frame.html: expected one main landmark, found 2",
                "frame.html: expected one contentinfo landmark, found 2",
            ],
        )

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

    def test_aria_images_need_resolvable_accessible_names(self):
        invalid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<div role="img"></div>'
            '<div role="img" aria-labelledby="missing"></div>'
            '<span id="empty"></span>'
            '<div role="img" aria-labelledby="empty"></div>'
            '<div role="img" aria-hidden="true"></div></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(invalid, "graphics.html"),
            [
                "graphics.html: ARIA image 1 has no accessible name",
                "graphics.html: ARIA image 2 references missing label ids: missing",
                "graphics.html: ARIA image 2 has no accessible name",
                "graphics.html: ARIA image 3 references labels without text",
                "graphics.html: ARIA image 3 has no accessible name",
            ],
        )

        valid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<div role="img" aria-label="Seven promise groups pass"></div>'
            '<p id="trend-name">Annual prevalence trend</p>'
            '<div role="img" aria-labelledby="trend-name"></div></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "graphics.html"), []
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
                "navigation.html: navigation landmark 2 has no accessible name",
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

    def test_navigation_landmark_label_references_need_text(self):
        empty_label = parse(
            '<a class="skip" href="#main">Skip</a>'
            '<nav aria-label="Primary"><a href="/">Home</a></nav>'
            '<main id="main"><span id="empty"></span>'
            '<nav aria-labelledby="empty"></nav></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(empty_label, "navigation.html"),
            [
                "navigation.html: navigation landmark 2 references labels without text",
                "navigation.html: navigation landmark 2 has no accessible name",
            ],
        )

    def test_duplicate_navigation_names_require_identical_link_sets(self):
        different_links = parse(
            '<a class="skip" href="#main">Skip</a>'
            '<nav aria-label="Sections"><a href="#one">One</a></nav>'
            '<main id="main"><nav aria-label="Sections">'
            '<a href="#two">Two</a></nav></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(
                different_links, "navigation.html"
            ),
            [
                "navigation.html: navigation landmarks 1, 2 share accessible "
                "name 'Sections' but contain different links"
            ],
        )

        identical_links = parse(
            '<a class="skip" href="#main">Skip</a>'
            '<nav aria-label="Results"><a href="#previous">Previous</a>'
            '<a href="#next">Next</a></nav><main id="main">'
            '<nav aria-label="Results"><a href="#next">Next</a>'
            '<a href="#previous">Previous</a></nav></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(
                identical_links, "navigation.html"
            ),
            [],
        )

    def test_headings_need_text_and_must_not_skip_forward(self):
        invalid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<h1>Report</h1><h3>Skipped subsection</h3><h2></h2>'
            '<h4>Another skipped subsection</h4></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(invalid, "headings.html"),
            [
                "headings.html: heading 3 (h2) has no text",
                "headings.html: heading 2 skips forward from h1 to h3",
                "headings.html: heading 4 skips forward from h2 to h4",
            ],
        )

        valid = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<h1>Report</h1><h2>Finding</h2><h3>Evidence</h3>'
            '<h2>Limitations</h2></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(valid, "headings.html"), []
        )

    def test_table_headers_need_valid_scope(self):
        unscoped = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<table aria-label="Results"><thead><tr><th>Result</th>'
            "</tr></thead></table></main>"
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unscoped, "table.html"),
            ["table.html: table header cell 1 has no valid scope"],
        )

        scoped = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<table><caption>Results</caption><thead><tr>'
            '<th scope="col">Result</th></tr></thead>'
            '<tbody><tr><th scope="row">Project</th></tr></tbody></table></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(scoped, "table.html"), []
        )

    def test_data_tables_need_accessible_names(self):
        unnamed = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<table><thead><tr><th scope="col">Result</th></tr></thead>'
            '<tbody><tr><td>Pass</td></tr></tbody></table>'
            '<h2 id="empty"></h2><table aria-labelledby="empty">'
            '<tr><th scope="row">Result</th><td>Pass</td></tr></table>'
            '<table aria-labelledby="missing"><tr>'
            '<th scope="row">Result</th><td>Pass</td></tr></table></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(unnamed, "tables.html"),
            [
                "tables.html: heading 1 (h2) has no text",
                "tables.html: table 1 has no accessible name",
                "tables.html: table 2 references labels without text",
                "tables.html: table 2 has no accessible name",
                "tables.html: table 3 references missing label ids: missing",
                "tables.html: table 3 has no accessible name",
            ],
        )

        named = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<table><caption>Promise-group results</caption><tr>'
            '<th scope="row">Static site</th><td>Pass</td></tr></table>'
            '<table aria-label="Development scorecard"><tr>'
            '<th scope="row">Edit similarity</th><td>0.30</td></tr></table>'
            '<h2 id="comparison">Forecast comparison</h2>'
            '<table aria-labelledby="comparison"><tr>'
            '<th scope="row">Word count</th><td>53</td></tr></table></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(named, "tables.html"), []
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

    def test_positive_tabindex_is_rejected(self):
        custom_order = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<button tabindex="2">Second</button>'
            '<a href="first" tabindex="1">First</a></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(custom_order, "focus.html"),
            [
                "focus.html: interactive element 2 (button) uses positive tabindex 2",
                "focus.html: interactive element 3 (a) uses positive tabindex 1",
            ],
        )

        source_order = parse(
            '<a class="skip" href="#main">Skip</a><main id="main">'
            '<button>First</button>'
            '<div tabindex="0" aria-label="Scrollable results"></div>'
            '<div tabindex="-1"></div></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(source_order, "focus.html"), []
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
