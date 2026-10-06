---
started: 2026-10-06T09:01:05Z
finished: 2026-10-06T09:06:01Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Do the three report forms really link back to one another?

## Scope

Close a narrow publication-integrity gap without reopening benchmark outcomes,
fitting another model to the heavily reused cohort, or changing the frozen
submission: verify actual reciprocal destinations among all three report forms
instead of treating an arbitrary PDF annotation count as sufficient evidence.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the older response-length, source-form, and
  distribution records needed for provenance; the current challenge README,
  evaluation and participation guides; and the current *Ipseology* analysis
  chapter and glossary.
- Confirmed that the existing verifier required links from the Executive
  Summary and Full Report landing page but did not require them from the Full
  Report evidence chapter. It also accepted any five PDF link annotations,
  even if none led to the HTML report forms.
- Added explicit reciprocal-link validation for the Executive Summary, Full
  Report landing page, and Full Report evidence chapter. Each HTML surface must
  now expose the appropriate other report forms.
- Added PDF URI-action inspection. The short report must contain the exact
  production URLs for both the Executive Summary and Full Report; annotation
  count remains a separate structural check.
- Added four focused regressions covering valid HTML and PDF reciprocity, a
  missing evidence-chapter link, and the former false positive of five
  unrelated PDF annotations. Updated the build contract and current state.

## Evidence and validation

- The focused verifier suite passed 11 tests. The new regression demonstrates
  that five unrelated PDF URI annotations no longer satisfy reciprocity.
- All 103 Project tests passed.
- The live publication verifier passed one Executive Summary figure, reciprocal
  links across both Full Report HTML surfaces and the five-page short PDF, all
  68 canonical artifacts and 68 compatibility aliases against their Project
  sources, the required phrase, and the two-column PDF layout.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 818 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets. `git diff --check` passed.

## Limitations and decisions

- This is publication assurance, not a new estimate of predictability. It
  changes no prediction, metric, interpretation, public report body, or frozen
  test artifact.
- URI inspection proves that the required destinations are embedded in the
  PDF; source-level HTML checks prove that local targets exist. These checks do
  not substitute for clicking links in a rendered browser or testing with
  assistive technology.
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
