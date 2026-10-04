---
started: 2026-10-04T09:01:11Z
finished: 2026-10-04T09:06:20Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can the public evidence copies be trusted to match their sources?

## Scope

Close a publication-integrity gap without reopening benchmark outcomes,
tuning another model on the same cohort, or changing the frozen submission:
make the publication verifier reject canonical and compatibility artifact
copies that agree with each other but are stale relative to the authoritative
Project source.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the older source-form and distribution records
  needed for provenance; the pinned challenge README; and the complete current
  online edition of *Ipseology—A new science of the self*.
- Confirmed through the public GitHub API that the challenge remains at pinned
  commit `9b6a766712583fec8d3182957260b1123fbfa146`, with no pull requests or
  published Aleph submission. The open submission and private-score handoff is
  therefore unchanged.
- Added `validate_artifact_copy` to `analysis/verify_publication.py`. For each
  of the 68 exposed research artifacts, it reads the authoritative Project
  source once and requires both the canonical public path and the preserved
  `report/artifacts/` alias to match it byte for byte.
- Moved the optional `pypdf` import inside the end-to-end entry point. Focused
  source-copy tests can therefore remain in the ordinary standard-library
  Project suite, while PDF validation still uses the documented build-only
  environment.
- Added three regression tests covering correct copies, mutually consistent
  but stale public copies, and a stale compatibility alias. Updated the build
  guide, current state, and public Project catalog metadata/order.

## Evidence and validation

- The regression that recreates the old blind spot writes identical stale
  canonical and alias bytes; the stronger validator rejects the canonical
  copy because it differs from the Project source.
- All 94 Project tests passed, including the three new publication-integrity
  tests. The live publication verifier passed all 68 canonical artifacts and
  68 compatibility aliases against their Project sources, alongside one
  Executive Summary figure, reciprocal report links, the required phrase,
  and the five-page two-column PDF.
- All 17 pinned benchmark tests passed. The official validator returned
  `VALID: 81 predictions`, and the frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- The first Version 1 run correctly rejected stale Project-catalog metadata
  after `STATE.md` changed. After synchronizing the timestamp and newest-first
  ordering, all seven promise groups passed across 39 HTML pages, 38 named
  data tables, 817 exposed interactive or keyboard-focusable elements, and
  seven first-party stylesheets. `git diff --check` passed.

## Limitations and decisions

- This iteration strengthens provenance and publication validation; it adds no
  new estimate of predictability and changes no scientific result.
- Byte identity proves faithful publication of the repository artifact. It
  does not independently establish that an upstream analysis or interpretation
  is correct; the existing hash guards, tests, analysis locks, and claim
  boundaries remain necessary.
- No browser executable is available on this host, so rendered desktop,
  mobile, keyboard, and assistive-technology inspection remains outstanding.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Do not evaluate the failed synthesis or GloVe ranking on development data.
  Avoid additional count models, Add re-rankers, or post hoc decompositions on
  the same 150 cases without richer compositional context or new longitudinal
  evidence.
- Perform rendered accessibility and responsive-layout checks when browser
  infrastructure becomes available.
