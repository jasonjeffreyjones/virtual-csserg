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
