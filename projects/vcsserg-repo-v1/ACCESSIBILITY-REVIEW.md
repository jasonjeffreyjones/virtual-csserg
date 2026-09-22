# Rendered accessibility review protocol

Status: **Open**. Prepared by Bee Boring Vanilla on September 19, 2026;
structured evidence contract added September 20, 2026.

## Decision boundary

This protocol makes the sole remaining Version 1 manual gate reproducible. It
does not declare WCAG conformance. The gate closes only after a named reviewer
records the environment and page-by-page results below, fixes any blocking
defect, repeats the affected check, and links that evidence from `STATE.md`.
Change the status to **Closed** only after every result cell reads `Pass`.
`verify_v1.py` checks the sample against the current Published summaries and
Full Report pages and rejects a closed record with missing evidence; it does
not perform or replace the human review.

The protocol follows WCAG 2.2's testable requirements for reflow, keyboard
operation, bypass blocks, focus order, visible and unobscured focus, and
programmatic names and roles. It also follows W3C's practical advice to inspect
keyboard focus and a page's linearized structure. W3C explicitly describes its
easy checks as preliminary rather than definitive, so neither this protocol nor
the existing static verifier should be represented as a comprehensive
accessibility evaluation.

## What is already established

- `verify_v1.py` examines every public HTML page for one main region and
  requires the first anchor itself to be a bypass link targeting that main. A
  focused fixture rejects an invalid first skip-styled link followed by a valid
  bypass, preventing the two anchors from jointly satisfying that one-link
  requirement. The verifier also checks explicit image alternatives, page
  language and title, local references, and duplicate IDs.
- All four generated Quarto report pages now receive a source-controlled bypass
  link through a tested post-render normalizer. The public HTML contains that
  link first in body order; it no longer depends on JavaScript to move the link
  ahead of repeated navigation. The same normalizer now gives stable accessible
  names to Quarto's report, chapter, on-page, and previous/next navigation
  landmarks. The whole-site verifier rejects unnamed navigation landmarks when
  a page exposes more than one, and it rejects unresolved `aria-labelledby`
  references.
- On September 19, `w3m` 0.5.3 returned successfully for all 11 selected
  production pages at 40 and 120 columns. Each linearized view began with
  “Skip to content.” This is useful no-style text-order evidence, not graphical
  focus, responsive-layout, or screen-reader evidence.
- Before the September 19 protocol revision, the credential-free production
  probe found all 128 expected files byte-identical. Before the September 21
  verifier revision, the same probe found all 142 expected files
  byte-identical; before the September 22 navigation-landmark revision, all 150
  expected files were byte-identical. It cannot discover extra remote-only
  paths, and the latest result does not describe the not-yet-deployed changes
  in this iteration.

## Selected production pages

These 11 pages cover the live homepage, both catalogs, the shared Scholar
profile pattern, all three Executive Summaries, and every Full Report page.
The 15 dated design alternatives are decision archives, not selected layouts;
they retain whole-site static coverage but are outside this manual release
sample.

| Page | Layout or behavior represented |
|---|---|
| `website/index.html` | Editorial homepage and mixed-column notebook |
| `website/projects/index.html` | Project catalog and status metadata |
| `website/scholars/index.html` | Scholar-card catalog |
| `website/scholars/b-boring-vanilla/index.html` | Shared Scholar profile pattern |
| `website/projects/vcsserg-repo-v1/index.html` | Evidence brief and promise-map figure |
| `website/projects/predict-the-self/index.html` | Evidence brief with results table |
| `website/projects/nfl-team-fandom-identities/index.html` | Paused-project summary and citations |
| `website/projects/vcsserg-repo-v1/report/index.html` | One-chapter Quarto book |
| `website/projects/predict-the-self/report/index.html` | Multi-chapter Quarto book landing page |
| `website/projects/predict-the-self/report/report.html` | Quarto chapter with dense tables and code |
| `website/projects/nfl-team-fandom-identities/report/index.html` | Quarto report with figures, math, and tables |

## Test environment and result record

Test the deployed release, and record its full Git commit and base URL. Use a
current graphical browser at a desktop viewport (recommended 1440 by 900 CSS
pixels) and at 320 CSS pixels wide or an equivalent 400% zoom/reflow setting.
Use a screen reader/browser pairing whose exact names and versions are
recorded. A mobile screen reader is welcome additional evidence but is not a
substitute for the 320-pixel graphical reflow check.

Complete this record in place during the closing iteration. Use only `Pass`,
`Fail`, or `Not tested` in the four result columns. Record a failure until its
repair has been retested; summarize both the defect and retest under issues.

Commit: Not recorded

Base URL: Not recorded

Reviewer: Not recorded

Date (UTC): Not recorded

Operating system: Not recorded

Browser and version: Not recorded

Screen reader and version: Not recorded

Desktop viewport and zoom: Not recorded

Narrow viewport and zoom: Not recorded

Issues and retest evidence: Not recorded

<!-- accessibility-results:start -->
| Page | Desktop keyboard/focus | Narrow keyboard/focus | Narrow reflow and 200% text | Screen reader | Notes |
|---|---|---|---|---|---|
| `website/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/scholars/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/scholars/b-boring-vanilla/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/vcsserg-repo-v1/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/predict-the-self/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/nfl-team-fandom-identities/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/vcsserg-repo-v1/report/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/predict-the-self/report/index.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/predict-the-self/report/report.html` | Not tested | Not tested | Not tested | Not tested | — |
| `website/projects/nfl-team-fandom-identities/report/index.html` | Not tested | Not tested | Not tested | Not tested | — |
<!-- accessibility-results:end -->

## Checks on every selected page

### Keyboard and focus at both widths

1. Start at the address bar and put the pointing device aside.
2. Press Tab. “Skip to content” must be the first page control, visibly focused,
   and not hidden behind fixed content.
3. Activate the link. Focus or the next Tab stop must proceed at the main
   content rather than traversing the repeated site or book navigation.
4. Traverse forward and backward through every control. Order must preserve
   meaning, focus must remain visible and unobscured, and no control may trap
   focus.
5. Activate links, Quarto sidebar toggles, search, code disclosure controls,
   and any table-of-contents controls with the keyboard. No operation may
   require a pointer.

### Reflow and magnification

1. At 320 CSS pixels wide, inspect the page from beginning to end. Text and
   controls must not disappear, overlap, or be clipped.
2. The page must not require two-dimensional scrolling to read blocks of text.
   A wide data table, figure, or code block may have its own horizontal scroll
   region when its meaning requires two-dimensional layout.
3. Repeat at 200% text zoom. Navigation, report actions, figures, tables,
   citations, and footer links must remain readable and operable.

### Screen reader

1. Confirm that the page announces a descriptive title and English language,
   and exposes header/navigation, main, and footer landmarks without confusing
   duplication.
2. Navigate by headings and confirm that their order matches the visible
   document and that each section has an intelligible name.
3. Navigate by links and controls. Names must explain purpose; Quarto toggles,
   search, and code disclosures must announce role and state.
4. Confirm that meaningful figures announce the checked alternative text,
   decorative images are ignored, and visible captions are not needlessly
   repeated.
5. On report tables, verify that caption and header relationships support row
   and column navigation. Read equations, code, references, and footnotes that
   appear on the page and record any loss of meaning.

## Passing rule

Every selected page must pass the keyboard/focus and reflow checks at both
widths and the screen-reader checks in the recorded pairing. Every failure must
be fixed and retested. Set every result cell to `Pass`, complete every
environment field, and change the document status to **Closed**. The verifier
will reject omitted or duplicate sample pages, unknown result words,
placeholder environment fields, an invalid commit/base URL/date in a closed
record, and any non-passing cell.
Then rerun the Project checks, Version 1 verifier, public expected-file probe,
and host-managed authenticated deployment inventory.
Closing this Project remains a separate lifecycle judgment; passing this gate
does not validate other Projects' empirical claims or create a WCAG conformance
claim.

## References

World Wide Web Consortium. (2024, December 12). *Web Content Accessibility
Guidelines (WCAG) 2.2*. https://www.w3.org/TR/WCAG22/

World Wide Web Consortium Web Accessibility Initiative. (n.d.). *Easy checks:
A first review of web accessibility*. Retrieved September 19, 2026, from
https://www.w3.org/WAI/test-evaluate/preliminary/
