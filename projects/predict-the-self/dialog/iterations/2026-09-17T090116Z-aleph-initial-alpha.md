---
started: 2026-09-17T09:01:16Z
finished: 2026-09-17T09:18:10Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Paired uncertainty and extractive limits

## Scope

Add evidence about development-case uncertainty and the lexical limits of the
frozen extractive method without changing the method, test submission, or
private-test claim boundary.

## Work completed

- Retrieved the public Predict Future Selves benchmark into a temporary
  checkout at immutable commit
  `9b6a766712583fec8d3182957260b1123fbfa146`, read its current participant and
  evaluation documentation, and reproduced every recorded governing hash.
- Added `analysis/analyze_dev_diagnostics.py`, which refuses mismatched
  development data or evaluator code, imports the authoritative evaluator, and
  produces deterministic paired case-bootstrap and extractive-limit results.
- Added three focused unit tests and the complete machine-readable result at
  `results/stable_signifier_dev_diagnostics.json`.
- Reorganized the Full Report under the charter's Abstract, Introduction,
  Method, Results, and Discussion structure. Added the full paired comparison,
  lexical-novelty analysis, limitations, and two new public artifacts.
- Updated the Executive Summary's single dense figure and six linked findings,
  updated the short report, balanced the PDF's columns, rebuilt the Quarto
  book, and refreshed the public project catalog.

## Evidence and validation

- All five nonzero agreement differences have 95% paired case-bootstrap
  intervals spanning zero. The aggregate agreement pattern is therefore
  sensitive to which 50 development cases are included.
- Word-count error reduction is `+15.04` words (interval `+1.18` to `+32.36`),
  source-similarity error reduction is `+0.096102` (`+0.066064` to
  `+0.129348`), and line-count error reduction is `-2.96` (`-5.54` to `-0.42`).
  Positive values favor stable-signifier projection.
- A mean `73.1727%` of distinct follow-up token types are absent from the same
  person's earlier response (case-bootstrap interval `69.7982%`–`76.5607%`).
  Respecting source token counts, `65.0621%` of future token occurrences are
  unavailable (`59.2663%`–`70.6149%`).
- Unattainable retrospective extractive ceilings average `0.268273` for
  unique-token Jaccard, `0.484206` for bag-of-words F1, and `0.374081` for
  source-order subsequence ROUGE-L F1. The frozen projection scores `0.142768`,
  `0.307444`, and `0.227552`, respectively.
- The interpretation is twofold: the current extractor leaves improvement
  available within extraction, but extraction itself cannot generate the many
  identity signifiers expressed only at follow-up.

### Validation

- All 17 pinned benchmark tests passed; the official validator returned
  `VALID: 81 predictions`.
- The official evaluator reproduced all 15 recorded development metrics.
- All eight Project unit tests passed.
- The publication verifier passed one Executive Summary figure, reciprocal
  report links, all eight Full Report artifacts and compatibility aliases, the
  required phrase, and the two-page two-column PDF.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages
  and six first-party stylesheets.
- `git diff --check` passed. The frozen test CSV remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.

## Limitations and decisions

- The analysis is explicitly post hoc and does not reopen model selection or
  alter the frozen test artifact.
- The deterministic 20,000-resample percentile bootstrap uses paired
  development cases and seed `20260917`. Its intervals describe sensitivity to
  development-case composition, not uncertainty for a broader population.
- Every oracle uses observed follow-up text. Oracle ceilings are retrospective
  diagnostics, not achievable prospective predictions or test results.
- The test answers remain private, so no test-performance claim is valid.
- No browser executable is installed. The rebuilt HTML passed structural and
  link validation but still lacks rendered browser and assistive-technology
  inspection. Both PDF pages were rasterized at 144 dpi and visually inspected.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen CSV and method card; preserve and publish the first
  complete private scorecard unchanged when the organizer returns it.
- Before another model comparison, preregister development-data use and a
  generative or other non-extractive mechanism for predicting new signifiers.
  Apply the same paired diagnostics without tuning against private feedback.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
