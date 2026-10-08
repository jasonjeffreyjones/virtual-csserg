---
started: 2026-10-08T09:01:11Z
finished: 2026-10-08T09:06:40Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can a stale Quarto artifact replace the current public report?

## Scope

Close a transactional publication-integrity gap without reopening benchmark
outcomes, fitting another model to the heavily reused cohort, or changing the
frozen submission: require every built canonical research artifact to equal
its authoritative Project source before the guarded publisher can mutate the
public report tree.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README, evaluation, and
  participation guides; and the *Ipseology* chapters and glossary.
- Confirmed that the challenge `main` branch remains at pinned commit
  `9b6a766712583fec8d3182957260b1123fbfa146` and that the repository still has
  no pull requests.
- Confirmed that the verifier rejected stale public copies only after the
  publisher had already replaced the public report tree. The publisher itself
  required built artifacts to exist but did not compare their bytes with the
  authoritative Project sources.
- Added a pre-publication identity check for all 69 inventoried canonical
  artifacts. It also rejects resource paths that resolve outside the build or
  Project tree. The check runs before public-directory creation, staging, or
  replacement.
- Added focused regressions showing that a stale built artifact and a missing
  authoritative source both fail while leaving the existing public tree
  unchanged. Updated the build contract, current state, and Full Report, then
  rendered and republished the book.

## Evidence and validation

- All 111 Project tests passed; the focused publisher suite now contains six
  tests, including the two new preservation regressions.
- Quarto rendered both chapters, and the guarded publisher accepted all 69
  built canonical artifacts against their Project sources before replacing
  the public report.
- The publication verifier passed one Executive Summary figure, reciprocal
  report links, all 69 canonical artifacts and 69 compatibility aliases
  against Project sources, the required phrase, and the five-page two-column
  PDF.
- The Version 1 verifier and final whitespace check passed.
- The frozen test artifact and both published copies remain SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.

## Limitations and decisions

- This is publication assurance, not a new estimate of predictability. No
  prediction, metric, scientific interpretation, benchmark artifact, or
  private-test claim changed.
- Byte identity proves that the rendered resources came from the current
  authoritative Project files. It does not establish that those analyses or
  interpretations are scientifically correct; analysis locks, hash guards,
  tests, and explicit claim boundaries remain necessary.
- The verifier intentionally repeats the source-to-public comparison after
  publication. The preflight protects transactionality; the postflight checks
  the final canonical and compatibility copies.
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

Jones, J. J. (2023). *Ipseology—A new science of the self*. Jason Jeffrey
Jones Productions.
https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2026). *You can predict future selves with AI (or without AI)*
[Data set and benchmark]. GitHub.
https://github.com/jasonjeffreyjones/predict-future-selves
