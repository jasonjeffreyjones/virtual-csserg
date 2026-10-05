---
started: 2026-10-05T09:01:19Z
finished: 2026-10-05T09:17:24Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Do the public scorecards expose machine-specific paths?

## Scope

Audit publication provenance without reopening benchmark outcomes, fitting
another model to the same cohort, or changing the frozen submission. Remove
machine-specific paths from public scorecards and make their recurrence a
validation failure.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README and evaluation and
  participation guides; and the current online *Ipseology* chapters and
  glossary.
- Found that the two authoritative development scorecards exposed an
  ephemeral benchmark checkout under `/tmp` and, in one case, this workspace's
  absolute location. Quarto publication had reproduced those fields in four
  public scorecard copies.
- Replaced those three machine-specific provenance fields with stable logical
  labels: the repository-relative prediction artifact and the pinned benchmark
  commit plus `data/dev.csv`. Metric values, predictions, analyses, and the
  frozen test artifact were not changed.
- Changed retrieval scorecard generation to emit the logical labels regardless
  of invocation paths. Added one focused generator regression.
- Extended the publication verifier to reject absolute POSIX paths, absolute
  Windows paths, and `file:` URIs in both scorecards while accepting stable
  logical labels. Added four focused verifier regressions and documented the
  invariant in the build guide and current state.
- Re-rendered and republished the Full Report, including the corrected
  canonical scorecards, compatibility aliases, and updated analysis script.

## Evidence and validation

- Clean regeneration from the hash-pinned benchmark produced the corrected
  retrieval scorecard and left its analysis result unchanged. A repository and
  public-report scan found no `/tmp`, `/home`, or `file:` provenance in any
  published result JSON.
- All 99 Project tests passed, including five new provenance regressions. All
  17 pinned benchmark tests passed.
- The official validator returned `VALID: 81 predictions`. The frozen test
  artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both chapters and the guarded publisher replaced the public
  report. The publication verifier passed all 68 canonical artifacts and 68
  compatibility aliases against their Project sources, as well as the one
  Executive Summary figure, reciprocal report links, required phrase, and
  five-page two-column PDF.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 817 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets. `git diff --check` passed.

## Limitations and decisions

- This is a provenance and publication-safety correction, not a new estimate
  of predictability. No numerical result or interpretation changes.
- Logical labels identify public artifacts without exposing the executing
  host. The pinned commit and recorded SHA-256 hashes—not a local path—remain
  the authority for benchmark identity.
- No browser executable is installed on this host, so rendered desktop,
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

## Sources reviewed

Jones, J. J. (2023). *Ipseology—A new science of the self.*
https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2026). *You can predict future selves with AI (or without AI)*
[Data set and benchmark]. GitHub.
https://github.com/jasonjeffreyjones/predict-future-selves
