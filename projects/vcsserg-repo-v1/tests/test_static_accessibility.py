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

        relocated = parse(
            '<a href="/">Home</a>'
            '<a class="report-skip" href="#main">Skip</a>'
            '<script>document.body.prepend('
            'document.currentScript.previousElementSibling)</script>'
            '<main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(relocated, "relocated.html"), []
        )

        wrong_target = parse(
            '<a class="skip" href="#navigation">Skip</a>'
            '<nav id="navigation"></nav><main id="main"></main>'
        )
        self.assertEqual(
            VERIFY.page_accessibility_problems(wrong_target, "wrong.html"),
            ["wrong.html: missing bypass link"],
        )


if __name__ == "__main__":
    unittest.main()
