---
started: 2026-09-21T08:01:16Z
finished: 2026-09-21T08:12:07Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Atomic first-anchor bypass validation

## Scope

Audit one deterministic claim supporting the remaining rendered-accessibility
gate: that every public page's first anchor is itself a valid bypass targeting
the page's `main` region. Repair any false-positive path without claiming
browser, keyboard, or assistive-technology evidence this host cannot produce.

## Work completed

- Reproduced a conjunction error in `page_accessibility_problems`: an invalid
  first skip-styled anchor plus a later valid bypass satisfied the separately
  evaluated first-anchor and valid-target conditions.
- Extended `PageParser` to retain the first anchor's own `href` and changed the
  check to require that exact reference among the main-targeting bypasses.
- Added a focused regression fixture that failed before the repair and now
  rejects the misleading two-anchor document. All 26 current public HTML pages
  continue to pass.
- Updated the accessibility protocol, audit, current state, homepage notebook,
  and metadata-derived Projects directory. The Project remains Active because
  the rendered keyboard and screen-reader review is still open.

## Evidence and validation

- Before editing, the credential-free production probe found all 142 expected
  website files byte-identical. This describes the incoming release; public
  HTTP still cannot discover extra remote-only paths.
- The pre-change baseline passed all 32 routine tests and all seven Version 1
  promise groups. The new fixture then reproduced the false positive as one
  expected test failure before the code repair.
- After repair, all 33 routine v1 tests pass. The v1 publication verifier
  passes one summary figure, reciprocal links, the required phrase, and the
  linked two-page, two-column PDF. Roster and Project-registry validation report
  four Scholars, four Projects, and three Published Projects.
- All seven Version 1 groups pass across 26 HTML pages and six first-party
  stylesheets. Python compilation and repository whitespace validation pass.

## Limitations and decisions

No graphical browser or supported screen-reader/browser pairing is installed,
so this iteration strengthens only the deterministic source check. It does not
perform the 44-result review in `ACCESSIBILITY-REVIEW.md`, and the sole manual
gate remains open.

The publication verifier initially failed because base Python lacks `pypdf`;
rerunning it with the documented existing build-only dependency path passed. No
package, credential, `.env`, manual deployment, replacement runtime, PI-owned
runner edit, charter edit, earlier iteration edit, PI blockquote change, or
parallel agent was used. The report forms did not change, so no material report
supersession was recorded. Normal host-managed automation must still commit,
push, deploy, and perform authenticated inventory for this revised release.

## Questions and next steps

No blocking PI question. Execute `ACCESSIBILITY-REVIEW.md` on a
browser/screen-reader-equipped host, record the environment and all 44 results,
repair and retest any failure, and only then assess the charter and PI authority
before changing the Project lifecycle state.

Elapsed time: 10 minutes 51 seconds (651 seconds).
