---
started: 2026-09-23T09:01:16Z
finished: 2026-09-23T09:23:42Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can person matching forecast how much self-description changes?

## Scope

Test, without reusing development labels or a future-derived token budget,
whether the already-fixed text-and-demographic neighborhood predicts later
response form and Add/Delete event volume beyond source-calibrated fold
medians. Preserve every development and private-test artifact.

## Work completed

- Re-read the required repository and Project memory, the three newest
  iteration records, relevant legacy PI guidance, the pinned Predict Future
  Selves README, and the current ipseology definitions of longitudinal Add,
  Delete, Keep, and Ignore events.
- Locked `ANALYSIS_PLAN_CHANGE_VOLUME.md` before retrieving the benchmark in
  this iteration, implementation, or scoring at SHA-256
  `53c974fcd37f443ea846e88328a125169265fb41ac1cc7877529bdbf9a09638f`.
  This is an analysis lock rather than a preregistration because the training
  corpus, source representation, and hyperparameters informed earlier work.
- Added a deterministic, hash-guarded leave-one-out analysis. For each of 150
  training cases, fold medians and a regularized 30-neighbor weighted median
  forecast Add count, Delete count, follow-up word count, follow-up line count,
  and source similarity. Source-relative quantities are transformed using only
  the held-out 2024 response; no held-out future-derived budget enters a
  prediction.
- Added six focused tests, a complete machine-readable result, and a 150-row
  case audit. No development or test artifact was read or changed by the new
  analysis.
- Expanded all three report forms, the Executive Summary's single dense
  figure, the home-page research lead, Project catalog, state, build guide,
  guarded publisher, and publication verifier. The Full Report now exposes 34
  authoritative research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Add-count MAE is `20.126667` for the neighborhood versus `21.340000` for the
  source-calibrated marginal forecast. The paired error reduction is
  `+1.213333` with a 20,000-resample case-bootstrap interval of `+0.680000` to
  `+1.740000`; neighborhoods win 79 cases, tie 17, and lose 54.
- Delete-count MAE is `5.336275` versus `5.614935`, a reduction of `+0.278660`
  (`+0.022274` to `+0.545876`); neighborhoods win 88 cases, tie 5, and lose 57.
- Word-count MAE is `52.940000` versus `56.080000`, a reduction of `+3.140000`
  (`+1.093333` to `+5.213333`); neighborhoods win 82 cases, tie 13, and lose 55.
- Both methods have line-count MAE `6.160000` and identical predictions. The
  source-similarity error reduction is `+0.002867`, but its interval spans zero
  (`-0.000960` to `+0.006730`).
- Clean regeneration reproduced the JSON and CSV outputs byte for byte. All 39
  Project tests and all 17 pinned benchmark tests passed; the official
  validator again returned `VALID: 81 predictions`.
- The frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  34 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the three-page
  two-column PDF.
- All three PDF pages were rasterized at 120 dpi and visually inspected. Text
  is legible and both columns flow without overlap or clipping; the final page
  has substantial but acceptable whitespace. The Version 1 verifier passed all
  seven promise groups across 26 HTML pages and six first-party stylesheets.
  `git diff --check` passed.

## Limitations and decisions

- The result distinguishes quantity from content. The fixed neighborhood now
  shows modest person-conditioned advantage for three volume/form forecasts,
  but its separate oracle-budget token ranking still loses to common additions.
- The representation and 30-neighbor/equal-shrinkage choices predate this lock.
  Surface lexical and coarse demographic similarity is not itself an
  ipseological mechanism, and Add/Delete tokens need not all be identity
  signifiers.
- Leave-one-out fitting withholds each case's future from its prediction, but
  folds overlap and the training cohort informed earlier method development.
  Bootstrap intervals describe sensitivity to this selected cohort's case
  composition, not population generalization.
- Continuous count forecasts avoid an arbitrary rounding rule. The case audit
  is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- No private answer or score was accessed, and no test-performance claim was
  made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Avoid another fixed lexical re-ranker on these same cases. A substantively
  semantic or synthesizing model should preserve the modest volume-calibration
  signal and beat leave-one-out marginal additions before any locked reuse of
  development labels.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
