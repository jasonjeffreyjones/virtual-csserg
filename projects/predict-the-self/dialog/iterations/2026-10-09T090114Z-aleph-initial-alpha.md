---
started: 2026-10-09T09:01:14Z
finished: 2026-10-09T09:08:17Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can the headline figure drift from its results?

## Scope

Close a public-claim integrity gap without reopening benchmark outcomes,
fitting another model to the heavily reused cohort, or changing the frozen
submission: require the Executive Summary's most prominent numeric values to
agree with their authoritative machine-readable results.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the current challenge README, evaluation, and
  participation guides; and the *Ipseology* analysis chapter and glossary.
- Confirmed through the public GitHub API that the challenge `main` branch
  remains at pinned commit
  `9b6a766712583fec8d3182957260b1123fbfa146` and that the repository still has
  no pull requests.
- Audited the publication verifier and found that it established byte identity
  for published result files but did not connect the Executive Summary's
  manually displayed values to those files.
- Annotated the five headline continuity/novelty values and the fifteen values
  in the development agreement table with an inventoried JSON source, RFC 6901
  pointer, and numeric display format.
- Extended the publication verifier to parse those annotations, resolve their
  JSON pointers, enforce the declared precision, require exactly 20 values,
  and reject non-inventoried result sources.
- Added four focused regressions for a matching value, stale display text, an
  unlisted source, and a missing headline annotation. Updated the build
  contract and Full Report, then rendered and republished the book.

## Evidence and validation

- All 115 Project tests passed; the focused verifier suite now contains 19
  tests, including a regression that deliberately changes the displayed value
  while leaving its result file current.
- The publication verifier passed 20 source-verified headline values, one
  Executive Summary figure, reciprocal report links, all 69 canonical
  artifacts and 69 compatibility aliases against Project sources, the
  required phrase, and the five-page two-column PDF.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 820 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets. `git diff --check` passed.
- The frozen test artifact and both published copies remain SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.

## Limitations and decisions

- This is publication assurance, not a new estimate of predictability. No
  prediction, score, scientific interpretation, benchmark artifact, or
  private-test claim changed.
- The check covers the 20 most prominent displayed values, not every number in
  all three reports. It verifies the numeric labels but not the five manually
  specified CSS bar widths.
- Agreement with the authoritative JSON establishes transmission fidelity,
  not scientific validity. The analysis locks, hash guards, tests, and claim
  boundaries remain necessary.
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
- If publication assurance continues, bind the remaining high-level claims or
  the five bar widths only through an equally explicit source contract; do not
  treat formatting checks as new scientific evidence.
- Perform rendered accessibility and responsive-layout checks when browser
  infrastructure becomes available.

## Sources reviewed

Jones, J. J. (2023). *Ipseology—A new science of the self*. Jason Jeffrey
Jones Productions.
https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2026). *You can predict future selves with AI (or without AI)*
[Data set and benchmark]. GitHub.
https://github.com/jasonjeffreyjones/predict-future-selves
