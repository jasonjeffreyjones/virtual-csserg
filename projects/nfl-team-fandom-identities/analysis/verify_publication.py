#!/usr/bin/env python3
"""Validate this frozen publication's arithmetic, artifacts, links, and PDF."""
import json
import math
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from pypdf import PdfReader

PROJECT = Path(__file__).resolve().parents[1]
PUBLIC = PROJECT.parents[1] / 'website/projects/nfl-team-fandom-identities'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids = [], set()
        self.figures = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attribute in ('href', 'src'):
            if attribute in attrs:
                self.links.append(attrs[attribute])
        if tag == 'figure':
            self.figures += 1


def main():
    primary = json.loads((PROJECT/'results/rq1_zenodo_20260911.json').read_text())
    e = primary['estimates']
    c = e['two_by_two']
    a, b, c0, d = (c[k] for k in ('fandom_yes_happy_yes', 'fandom_yes_happy_no',
                                   'fandom_no_happy_yes', 'fandom_no_happy_no'))
    assert (a, b, c0, d) == (263, 53, 6062, 1857)
    assert sum((a, b, c0, d)) == primary['join_audit']['eligible_respondent_days']
    assert math.isclose((a/(a+b))/(c0/(c0+d)), e['prevalence_ratio'])
    months = primary['temporal_sensitivity']['by_month']
    assert sum(m['fandom_yes_n'] for m in months) == a+b
    assert sum(m['fandom_no_n'] for m in months) == c0+d
    weighted = json.loads((PROJECT/'results/rq1_weighted_zenodo_20260911.json').read_text())
    assert weighted['inputs']['responses_sha256'] == primary['inputs']['responses_sha256']
    assert weighted['inputs']['demographics_sha256'] == primary['inputs']['demographics_sha256']
    assert weighted['complete_case_unweighted']['eligible_respondent_days'] == 8195
    for artifact in (PUBLIC/'report/artifacts').glob('*.json'):
        assert artifact.read_bytes() == (PROJECT/'results'/artifact.name).read_bytes()
    full = (PUBLIC/'report/index.html').read_text()
    assert full.count('far beyond') == 1
    summary = (PUBLIC/'index.html').read_text()
    assert Page(summary).figures == 1
    assert full.count('class="csl-entry"') == 5
    for path in (PUBLIC/'index.html', PUBLIC/'report/index.html'):
        for link in Page(path.read_text()).links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path and not url.fragment:
                continue
            target = (path.parent/unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= 'index.html'
            assert target.exists(), f'{path.name}: missing {link}'
            if url.fragment and target.suffix == '.html':
                assert unquote(url.fragment) in Page(target.read_text()).ids, f'Missing anchor: {link}'
    pdf = PdfReader(PUBLIC/'short-report.pdf')
    assert 1 <= len(pdf.pages) <= 10
    text = '\n'.join(page.extract_text() for page in pdf.pages)
    for number in ('83.23%', '76.55%', '1.087', '1.007', '1.160'):
        assert all(number in content for content in (full, summary, text)), number
    for page in pdf.pages:
        # ReportLab body origins should include both columns on every page.
        columns = set()
        def visit(text, cm, tm, font, size):
            if text.strip() and 9 <= size <= 20:
                x = cm[4] + tm[4]
                if 40 <= x <= 50:
                    columns.add('left')
                if 310 <= x <= 322:
                    columns.add('right')
        page.extract_text(visitor_text=visit)
        assert columns == {'left','right'}, columns
    print(f'PASS: arithmetic, snapshot consistency, artifact copies, local links/anchors, '
          f'one executive figure, APA bibliography, required phrase, '
          f'and {len(pdf.pages)}-page two-column PDF.')


if __name__ == '__main__':
    main()
