---
started: 2026-09-30T09:01:11Z
finished: 2026-09-30T09:44:28Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can calibrated full-text synthesis predict the content of change?

## Scope

Test the handoff's explicit pre-development hurdle without changing the frozen
submission or reopening development labels: integrate the stable source core,
prospective word and Add-count forecasts, and common fold-only response units
into one leave-one-out full-text prediction, then compare its new content with
an equal-volume marginal-addition ranking.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README; and the current
  ipseology definitions of personally expressed identity and signifiers.
- Locked `ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md` before reading benchmark rows
  in this iteration, implementation, or scoring at SHA-256
  `ae0594e0f95f4131416be0bab4c3bfa913010dc6380d65c39966849c3a9f7253`.
  The lock defines the synthesis rule, equal-volume content control, three
  advancement gates, and a no-development decision when any gate fails.
- Added a deterministic standard-library analysis. Each held-out training
  source receives a fold-fit stable-unit ranking, a three-count source-form
  word target, a text-and-demographic Add target, and fold follow-up units that
  are exact-unit additions in at least two cases. A fixed ranked-prefix search
  balances the two targets without using the held-out future.
- Added six focused tests, a complete JSON result, a 150-row audit without raw
  source or observed follow-up text, and all 150 fold predictions. Hash guards
  cover the pinned training data, evaluator, plan, and every inherited
  implementation.
- Updated all three report forms, the Executive Summary's single dense figure,
  public research lead and catalog metadata, state, build guide, guarded
  publisher, publication verifier, and publisher tests. The Full Report now
  exposes 55 authoritative artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Relative to repeat-2024, calibrated synthesis lowers word-count MAE to
  `51.986667` from `55.580000`; the `+3.593333` error reduction has a paired
  case-bootstrap interval of `+1.440000` to `+5.726667`. ROUGE-L F1 rises to
  `0.220153` from `0.200017` (`+0.020136`, `+0.002677` to `+0.037571`), and
  source-similarity error falls sharply.
- Normalized edit similarity is `0.268883` versus `0.272662` for repeat-2024;
  the `-0.003779` difference has an interval spanning zero (`-0.013404` to
  `+0.004287`). Token Jaccard and character n-gram F1 worsen with intervals
  excluding zero. Line-count MAE rises to `27.053333` from `6.160000`.
- At the same case-level predicted novel-type volume, synthesis F1 is
  `0.075887` versus `0.134680` for the fold marginal ranking. The `-0.058793`
  difference has interval `-0.076168` to `-0.041473`; synthesis wins 33 cases,
  ties 21, and loses 96. Only the word-count gate passes, so the prespecified
  advancement decision is failure and no development prediction is permitted.
- Clean 20,000-resample regeneration reproduced the JSON at SHA-256
  `2804068d6878ae6a4f79eb6d14a414533d4163368c1105a09e33fb4b0d6518c1`,
  audit at `6cefc3e8eb85e4fbf729c50188cc1af1ad41096eada8e4d9e77dfa59f13bc3d4`,
  and predictions at
  `695c44261ee18945936b68572c50c0b92e86ea4f3fd129d7cd18309e427e15bf`.
- All 70 Project tests and all 17 pinned benchmark tests passed. The official
  validator returned `VALID: 81 predictions`; the frozen test artifact remains
  SHA-256 `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  55 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the four-page
  two-column PDF. Ghostscript rasterized all four pages at 120 dpi; inspection
  found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  34 named data tables, and seven first-party stylesheets. `git diff --check`
  passed.

## Limitations and decisions

- This is a dependent analysis designed after every inherited component's
  aggregate result was known. Its pointwise gate is conservative but is not a
  multiplicity adjustment, and overlapping folds do not create population
  evidence.
- Exact recurring follow-up units privilege generic template statements. One
  appended unit per line explains the severe response-structure mismatch.
  Better calibration of source change or ROUGE-L does not establish correct
  future identity content.
- The fixed method failed two of three advancement gates and therefore must not
  be run on development data. No development or private-test row or artifact
  was read or changed by the new analysis.
- Fold predictions and the case audit are derived benchmark-data adaptations
  under CC BY-NC-SA 4.0. No private-test-performance claim was made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Do not tune or evaluate this common-unit synthesis on development data. A
  future model needs a substantively semantic, source-relevant mechanism that
  preserves response-form calibration and beats leave-one-out marginal
  additions in training before any newly locked development comparison.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
