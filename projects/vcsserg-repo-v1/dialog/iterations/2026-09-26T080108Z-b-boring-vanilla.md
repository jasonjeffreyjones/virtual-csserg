---
started: 2026-09-26T08:01:08Z
finished: 2026-09-26T08:13:05Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Accessible names for every public data table

## Scope

Audit a deterministic prerequisite of the remaining rendered screen-reader
gate: whether each public data table has a programmatically associated name as
well as explicit header relationships. Repair the maintained publication
sources and add regression coverage without treating source markup as observed
assistive-technology behavior.

## Work completed

- Extended the standard-library page parser to collect table captions and
  explicit ARIA labels, require one nonempty accessible name per data table,
  and report missing or empty `aria-labelledby` targets.
- Added a focused fixture accepting a caption, `aria-label`, and resolved
  `aria-labelledby`, while rejecting unnamed tables and broken or empty label
  references. The routine v1 suite now contains 41 tests.
- Audited all 26 public data tables. Twenty-four had scoped headers but no
  table-level name; the other two archived-design tables already had captions.
  Added concise source-owned captions to the VCSSERG v1, Predict the Self, and
  NFL Team Fandom Identities Full Reports and visually hidden captions to the
  seven Predict the Self Executive Summary tables. All 26 now pass.
- Updated the audit, accessibility protocol, recommendations, build guide,
  state, homepage, Projects catalog, and all three v1 report forms. The Project
  remains Active because rendered keyboard and screen-reader review is open.
- Recorded the clean outgoing v1 report set under full commit
  `94c7ebbc5e99636ae0b9183af104d5be6d8b76e9` before materially revising the
  report narrative. Caption-only maintenance to the other two Projects remains
  recoverable through ordinary Git history.

## Evidence and validation

- Before editing, the credential-free production probe found all 182 expected
  website files byte-identical. Public HTTP still cannot discover extra
  remote-only paths.
- The pre-change baseline passed all 40 routine tests and all seven Version 1
  promise groups. The stronger rule initially failed on exactly 24 unnamed
  tables across four selected production pages; after source repair, all 41
  routine tests and all seven promise groups pass across 26 HTML pages, 26
  named data tables, 542 interactive or keyboard-focusable elements, and six
  first-party stylesheets.
- Quarto 1.10.18 rebuilt the four affected Full Report pages. Guarded publishers
  replaced the VCSSERG v1 and Predict the Self report trees, and the NFL report
  rebuilt in place with its existing output-path warning. A second normalizer
  pass changed zero pages.
- The VCSSERG v1, Predict the Self, and NFL publication verifiers pass. Their
  routine suites pass 41, 52, and 7 tests respectively. The regenerated v1
  short report remains a linked two-page, two-column PDF within the ten-page
  ceiling. Python compilation and repository whitespace validation pass.

## Limitations and decisions

W3C technique H39 describes a caption as a programmatically associated table
identifier, but techniques are examples rather than a conformance requirement.
The verifier deliberately accepts a nonempty caption or explicit ARIA naming
mechanism. It checks source associations, not computed accessibility trees,
announcement quality, row/column navigation, or caption visibility in a
rendered browser.

No graphical browser or supported screen-reader/browser pairing is installed,
so the 44-result review in `ACCESSIBILITY-REVIEW.md` remains incomplete and is
still the sole manual gate. No credential, `.env`, manual deployment, package
or replacement-runtime installation, PI-owned runner edit, charter edit,
earlier iteration edit, PI blockquote change, or parallel agent was used.
Normal host-managed automation must still commit, push, deploy, and perform
authenticated inventory for this revised release.

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, verify that all table captions and header
relationships are announced and navigable along with the other recorded
checks, repair and retest any failure, and only then assess the charter and PI
authority before changing lifecycle state.

Elapsed time: 11 minutes 57 seconds (717 seconds).
