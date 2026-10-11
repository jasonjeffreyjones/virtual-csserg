---
started: 2026-10-11T09:01:10Z
finished: 2026-10-11T09:05:24Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can the plain-language findings drift from their results?

## Scope

Close the next Executive Summary numeric-integrity gap without reopening
benchmark outcomes, fitting another model to the heavily reused cohort, or
changing the frozen submission: require every numeric occurrence in the status
and nine plain-language finding cards to agree with an authoritative,
inventoried Project artifact.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the current challenge README, evaluation, and
  participation guides; and the *Ipseology* introduction, analysis chapter,
  and glossary.
- Confirmed through the public GitHub API that the challenge `main` branch
  remains at pinned commit
  `9b6a766712583fec8d3182957260b1123fbfa146`.
- Audited the preceding source-value contract and confirmed that it protected
  the headline chart and development agreement table but not repeated numbers
  in the status or plain-language findings.
- Annotated all thirteen numeric occurrences in those surfaces with an
  inventoried source, result pointer, and explicit display format. The
  protected claims include the frozen submission count, fold and contrast
  counts, case wins and losses, CRPS, novel-type F1, percentage novelty, and
  projection-to-source similarity.
- Extended the verifier's deliberately narrow formatter to support fixed
  percentages and an inventoried CSV data-row count, while preserving JSON
  Pointer resolution for research results. Added four focused regressions for
  matching and stale percentage values and CSV row counts.
- Updated the build contract, current state, and Full Report, then rendered and
  republished the book.

## Evidence and validation

- All 122 Project tests passed; the focused publication-verifier suite now
  contains 26 tests and independently rejects stale percentage text and a stale
  displayed submission count.
- The publication verifier passed 33 source-verified displayed values, five
  source-verified bar widths and accessible values, one Executive Summary
  figure, reciprocal report links, all 69 canonical artifacts and 69
  compatibility aliases against Project sources, the required phrase, and the
  five-page two-column PDF.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 824 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets. `git diff --check` passed.
- The frozen test artifact and both published copies remain SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.

## Limitations and decisions

- This is publication assurance, not a new estimate of predictability. No
  prediction, score, scientific interpretation, benchmark artifact, or
  private-test claim changed.
- The CSV source contract verifies the displayed count of data rows. The
  already recorded official validator run remains the evidence for schema, ID
  coverage, order, and nonblank predictions.
- The contract now covers the Executive Summary's headline values, visual and
  accessible bar encodings, status count, and plain-language finding numbers.
  It does not bind every number in the figure's secondary tables, Full Report,
  or short report.
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
- If publication assurance continues, extend source binding only to a clearly
  defined high-value surface; do not mistake transmission fidelity for new
  scientific evidence.
- Perform rendered accessibility and responsive-layout checks when browser
  infrastructure becomes available.

## Sources reviewed

Jones, J. J. (2023). *Ipseology—A new science of the self*. Jason Jeffrey
Jones Productions.
https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2026). *You can predict future selves with AI (or without AI)*
[Data set and benchmark]. GitHub.
https://github.com/jasonjeffreyjones/predict-future-selves
