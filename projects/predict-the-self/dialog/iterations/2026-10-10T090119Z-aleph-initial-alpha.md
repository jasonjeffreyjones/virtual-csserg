---
started: 2026-10-10T09:01:19Z
finished: 2026-10-10T09:07:03Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can the headline figure disagree with its printed values?

## Scope

Close the remaining numeric-integrity gap in the Executive Summary's one dense
figure without reopening benchmark outcomes, fitting another model to the
heavily reused cohort, or changing the frozen submission: require its five
visual bar widths and accessible numeric label to agree with the same
authoritative result claims as its printed values.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README, evaluation, and
  participation guides; and the *Ipseology* introduction, analysis chapter,
  and glossary.
- Audited the preceding source-value contract and confirmed that it protected
  20 printed values but not the five manually specified CSS widths or the five
  numbers repeated for screen-reader users.
- Gave each of the figure's five printed values a stable HTML identifier, made
  each bar and the accessible label explicitly reference those identifiers,
  and extended the publication verifier to reuse the already resolved JSON
  claims.
- Required each width to equal its authoritative 0–1 result converted to a
  four-decimal percentage, and required the accessible label to contain the
  five displayed values in bar order.
- Added three focused regressions for matching visual/nonvisual encodings, a
  stale CSS width, and stale accessible numeric text. Updated the build
  contract and Full Report, then rendered and republished the book.

## Evidence and validation

- All 118 Project tests passed; the focused publication-verifier suite now
  contains 22 tests and independently rejects a stale bar or accessible value
  even when the printed result remains current.
- The publication verifier passed 20 source-verified headline values, five
  source-verified bar widths and accessible values, one Executive Summary
  figure, reciprocal report links, all 69 canonical artifacts and 69
  compatibility aliases against Project sources, the required phrase, and the
  five-page two-column PDF.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 822 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets. `git diff --check` passed.
- The frozen test artifact and both published copies remain SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.

## Limitations and decisions

- This is publication assurance, not a new estimate of predictability. No
  prediction, metric, scientific interpretation, benchmark artifact, or
  private-test claim changed.
- The width check validates the explicit simple-class CSS declarations used by
  this figure; it does not emulate browser cascade, layout, zoom, or rendering.
  The accessible check protects the numeric sequence, not every word in the
  label's prose.
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
