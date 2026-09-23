import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "python/promote_report_skip_links.py"
SPEC = importlib.util.spec_from_file_location("promote_report_skip_links", MODULE_PATH)
PROMOTE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROMOTE)


def generated_page(skip_link=PROMOTE.SKIP_LINK):
    return (
        '<!doctype html><html><body class="nav-sidebar">\n'
        '<nav class="quarto-secondary-nav"><a href="index.html">Contents</a></nav>\n'
        '<nav class="sidebar-navigation"><a href="chapter.html">Chapter</a></nav>\n'
        '<nav class="toc-active"><a href="#section">On this page</a></nav>\n'
        '<nav class="page-navigation"><a href="next.html">Next</a></nav>\n'
        '<main id="quarto-document-content">\n'
        f"{skip_link}\n"
        '<h1>Report</h1><table><thead><tr><th>Result</th></tr></thead>'
        '<tbody><tr><td>Pass</td></tr></tbody></table>'
        '<section id="section"></section></main></body></html>\n'
    )


class PromoteReportSkipLinksTests(unittest.TestCase):
    def test_promotes_link_before_navigation_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            page = tree / "index.html"
            page.write_text(generated_page(), encoding="utf-8")

            self.assertEqual(PROMOTE.promote_tree(tree), (1, 1))
            promoted = page.read_text(encoding="utf-8")
            self.assertLess(promoted.index(PROMOTE.SKIP_LINK), promoted.index("<nav"))
            for accessible_name in PROMOTE.NAVIGATION_CLASS_LABELS.values():
                self.assertIn(f'aria-label="{accessible_name}"', promoted)
            self.assertIn('<th scope="col">Result</th>', promoted)
            self.assertEqual(PROMOTE.promote_tree(tree), (1, 0))
            self.assertEqual(page.read_text(encoding="utf-8"), promoted)

            button_first = generated_page().replace(
                '<nav class="quarto-secondary-nav"><a href="index.html">Contents</a></nav>',
                '<nav class="quarto-secondary-nav"><button type="button">Menu</button></nav>',
            )
            normalized, changed = PROMOTE.normalized_page(button_first, "button.html")
            self.assertTrue(changed)
            self.assertLess(normalized.index(PROMOTE.SKIP_LINK), normalized.index("<nav"))

    def test_preflight_refuses_duplicate_link_without_mutating_tree(self):
        with tempfile.TemporaryDirectory() as temporary:
            tree = Path(temporary)
            valid = tree / "index.html"
            invalid = tree / "report.html"
            valid_source = generated_page()
            invalid_source = generated_page(PROMOTE.SKIP_LINK * 2)
            valid.write_text(valid_source, encoding="utf-8")
            invalid.write_text(invalid_source, encoding="utf-8")

            with self.assertRaises(PROMOTE.PromotionError):
                PROMOTE.promote_tree(tree)

            self.assertEqual(valid.read_text(encoding="utf-8"), valid_source)
            self.assertEqual(invalid.read_text(encoding="utf-8"), invalid_source)

    def test_refuses_missing_main_target(self):
        source = generated_page().replace(
            'id="quarto-document-content"', 'id="different-main"'
        )
        with self.assertRaises(PROMOTE.PromotionError):
            PROMOTE.normalized_page(source, "missing-target.html")

    def test_refuses_unlabelled_unknown_navigation_landmark(self):
        source = generated_page().replace(
            "</main>", '<nav class="new-quarto-navigation"></nav></main>'
        )
        with self.assertRaisesRegex(
            PROMOTE.PromotionError, "navigation landmark has no accessible name"
        ):
            PROMOTE.normalized_page(source, "unknown-navigation.html")

    def test_refuses_unscoped_header_outside_table_head(self):
        source = generated_page().replace(
            "</tbody>", "<tr><th>Unexpected row header</th></tr></tbody>"
        )
        with self.assertRaisesRegex(
            PROMOTE.PromotionError, "table header cell 2 has no valid scope"
        ):
            PROMOTE.normalized_page(source, "unscoped-header.html")


if __name__ == "__main__":
    unittest.main()
