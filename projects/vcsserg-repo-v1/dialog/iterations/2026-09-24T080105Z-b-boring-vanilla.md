---
started: 2026-09-24T08:01:05Z
finished: 2026-09-24T08:15:10Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Interactive control name and ARIA integrity

## Scope

Audit another deterministic prerequisite of the remaining rendered
accessibility gate: whether public links and buttons have accessible names and
internally valid label, control, expanded-state, and hidden-control markup. Add
regression coverage without treating source inspection as observed browser or
assistive-technology behavior.

## Work completed

- Extended the standard-library page parser to derive interactive names from
  exposed text, descendant image alternatives, ARIA labels, referenced label
  text, or title fallback while excluding `aria-hidden` descendant text.
- Added checks that `aria-labelledby` and `aria-controls` references resolve,
  `aria-expanded` is boolean, and a control hidden from assistive technology is
  explicitly removed from the tab order. Nested referenced-label text is
  retained correctly.
- Audited all 527 links and buttons across 26 public HTML pages. All 501
  assistive-technology-exposed elements are named with valid checked ARIA
  relationships; the other 26 are Quarto source-line anchors marked
  `aria-hidden="true"` and `tabindex="-1"`.
- Added two focused tests for unnamed icon-only links, empty/missing label
  targets, missing controlled targets, invalid expanded state, safe source-line
  anchors, focusable hidden controls, and nested referenced-label text.
- Updated the accessibility protocol, audit, recommendations, build guide,
  state, homepage, Projects catalog, and all three v1 report forms. The Project
  remains Active because rendered keyboard and screen-reader review is still
  open.
- Recorded the clean outgoing v1 report set under full commit
  `9d70a922dde140f958a757d75eaf1ce179f1ad0d` before materially updating the
  report narrative.

## Evidence and validation

- Before editing, the credential-free production probe found all 166 expected
  website files byte-identical. This describes the incoming release; public
  HTTP still cannot discover extra remote-only paths.
- The pre-change baseline passed all 37 routine v1 tests and all seven Version
  1 promise groups. The revised suite passes all 39 tests, including the two new
  interactive-element fixtures.
- All seven Version 1 groups pass across 26 HTML pages, 527 interactive
  elements, and six first-party stylesheets.
- Quarto 1.10.18 rebuilt the Full Report, the guarded publisher replaced its
  complete public tree, and the shared normalizer reported zero changes on a
  second pass. The v1 publication verifier passes one summary figure,
  reciprocal links, the required phrase, and the linked two-page, two-column
  PDF.
- Roster and Project registry checks report four Scholars, four Projects, and
  three Published Projects. Python compilation, archive-key artifact lookup,
  and repository whitespace validation pass.

## Limitations and decisions

The source contract intentionally covers only properties that can be inspected
deterministically. It allows Quarto's hidden source-line anchors only when they
are explicitly absent from sequential keyboard navigation. It accepts a
nonempty `title` as a fallback name but does not claim that this is the best
visible-label design.

No graphical browser or supported screen-reader/browser pairing is installed.
Static names, references, and state tokens do not establish the computed
accessibility tree, announcements, focus order, state changes, or control
operation. The 44-result review in `ACCESSIBILITY-REVIEW.md` remains incomplete
and is still the sole manual gate.

No credential, `.env`, manual deployment, package or replacement-runtime
installation, PI-owned runner edit, charter edit, earlier iteration edit, PI
blockquote change, or parallel agent was used. Normal host-managed automation
must still commit, push, deploy, and perform authenticated inventory for this
revised release.

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, confirm the computed names, roles, states,
focus behavior, and operation along with the other recorded checks, repair and
retest any failure, and only then assess the charter and PI authority before
changing lifecycle state.

Elapsed time: 14 minutes 5 seconds (845 seconds).
