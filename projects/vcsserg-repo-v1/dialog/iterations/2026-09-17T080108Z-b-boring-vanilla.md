---
started: 2026-09-17T08:01:08Z
finished: 2026-09-17T08:13:48Z
scholar: "Bee Boring Vanilla"
scholar_slug: b-boring-vanilla
project: vcsserg-repo-v1
---

# Static accessibility regression contract

## Scope

Close a deterministic portion of the remaining accessibility gate without
claiming browser or assistive-technology evidence that this host cannot
produce. Audit the public HTML for bypass mechanisms and image alternatives,
repair source rather than generated output, add negative regression fixtures,
and keep all affected report forms and Project records synchronized.

## Work completed

- Extended `verify_v1.py` to require every public HTML page to provide a
  bypass link targeting its `main` element and every image to carry an
  explicit `alt` attribute. Added two focused unit tests covering valid
  meaningful/decorative alternatives, missing and late bypass links, an
  incorrect bypass target, a generated-report relocation, and a missing image
  alternative.
- Added source-controlled skip-link fragments and visible-on-focus styles to
  all three Published Projects' Quarto sources. Quarto places
  `include-before-body` inside book navigation, so each fragment synchronously
  moves its link to the beginning of the live document and targets the report
  `main`. Regenerated all four Full Report pages.
- Corrected the two NFL Full Report figures with explicit Quarto `fig-alt`
  text while preserving their visible captions, then regenerated and checked
  the report. No empirical claim, estimate, data artifact, or analysis code
  changed.
- Updated the v1 audit, state, Full Report, two-page short PDF, Executive
  Summary, public homepage/Project catalog, and report-source dates. Recorded
  the clean outgoing material report set under full commit
  `026c1d4511fbd99789c8252c552e72f90a799b5a` in the append-only version
  ledger.

## Evidence and validation

- Before repair, the strengthened verifier failed only the four generated
  Quarto pages for absent bypass links and the two NFL figures for absent
  `alt` attributes. After source changes and rendering, all seven Version 1
  groups pass across 26 HTML pages and six first-party stylesheets.
- All 26 routine VCSSERG v1 unit tests pass. The v1 publication verifier passes
  one summary figure, reciprocal links, the required phrase, and a linked
  two-page, two-column PDF. Roster and Project-registry validators pass.
- Predict the Self's five tests and publication verifier pass. NFL Team Fandom
  Identities' seven tests and publication verifier pass, including arithmetic,
  snapshot consistency, local anchors, report structure, and its two-page PDF.
- Python compilation and `git diff --check` pass. Quarto 1.10.18 regenerated
  the v1, Predict the Self, and NFL Full Reports from their checked-in sources.
- The separately documented runner-integration suite was attempted, but all
  six fixtures were stopped by the live iteration's repository lock with
  `Another Scholar iteration is already running.` Its build guide explicitly
  excludes this nested invocation; neither the runner nor those fixtures
  changed. The routine runner inspection in the Version 1 verifier passes.

## Limitations and decisions

No installed Chromium, Chrome, or Firefox executable is available. The new
checks establish source structure, main-targeted bypass links, and explicit
image-alternative decisions; they do not establish rendered focus behavior,
keyboard order, screen-reader output, visual layout, or substantive report
validity. The synchronous relocation used by Quarto reports therefore remains
part of the open rendered review.

The NFL Quarto build repeated its existing warning about an output directory
outside the main Project directory but completed, and its publication verifier
passed. No package, system runtime, credential, `.env`, deployment, production
probe, PI-owned runner edit, charter edit, or parallel agent was used.

## Questions and next steps

No blocking PI question. Complete the rendered desktop/phone keyboard and
assistive-technology pass on a browser-equipped host, then conduct substantive
review before considering Version 1 complete. After normal deployment, the
public parity probe can verify the changed website bytes.

Elapsed time: 12 minutes 40 seconds (760 seconds).
