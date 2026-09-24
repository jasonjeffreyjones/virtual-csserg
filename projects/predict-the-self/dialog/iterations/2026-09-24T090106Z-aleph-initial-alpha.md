---
started: 2026-09-24T09:01:06Z
finished: 2026-09-24T09:14:13Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does person matching improve probabilistic revision-volume forecasts?

## Scope

Test, without reusing development labels or changing the frozen submission,
whether the already-fixed regularized neighborhood improves complete
leave-one-out predictive distributions for response form and revision volume
beyond source-calibrated marginal distributions.

## Work completed

- Re-read the required repository and Project memory, the three newest
  iteration records, the pinned Predict Future Selves README, and the current
  ipseology definitions of personally expressed identity, signifiers, and
  longitudinal Add, Delete, Keep, and Ignore events.
- Locked `ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md` before reopening benchmark
  data, implementation, or scoring at SHA-256
  `00d5e2805082986b00f2716808ee12d4cff70ec900a5e47636e893217368f020`.
  This is an analysis lock rather than a preregistration because the training
  corpus, representation, neighborhood size, and shrinkage informed earlier
  Project work.
- Added a deterministic, hash-guarded leave-one-out analysis. For each of 150
  training cases and five outcomes, it compares a source-calibrated fold
  distribution with the unchanged 30-neighbor/30-case-prior mixture using
  weighted empirical CRPS and central 80% interval diagnostics. No held-out
  future enters either predictive distribution.
- Added seven focused tests, a complete machine-readable result, and a 150-row
  case audit. Added the standard CRPS reference in APA form with its DOI.
- Expanded all three report forms, the Executive Summary's single dense
  figure, the home-page research lead, state, build guide, guarded publisher,
  and publication verifier. The Full Report now exposes 38 authoritative
  research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Word-count CRPS is `38.156852` for the neighborhood versus `40.672695` for
  the source-calibrated marginal distribution. The paired reduction is
  `+2.515843` with a 20,000-resample case-bootstrap interval of `+1.008212` to
  `+4.059792`; neighborhoods win 83 cases and lose 67.
- The neighborhood central 80% word-count interval covers `84.6667%` of cases
  versus `80.6667%` for the marginal distribution. Mean width increases from
  `149.960000` to `154.526667` words, but interval score improves by
  `+19.700000` (`+3.873167` to `+37.193333`).
- Add-count, Delete-count, line-count, and source-similarity CRPS reductions
  are `+0.212518`, `+0.072801`, `-0.011761`, and `+0.002486`; every paired
  interval spans zero. The Add/Delete point-forecast gains therefore do not
  establish corresponding distributional-score gains.
- Clean regeneration reproduced the JSON and CSV outputs byte for byte. All 46
  Project tests and all 17 pinned benchmark tests passed; the official
  validator again returned `VALID: 81 predictions`.
- The frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  38 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the three-page
  two-column PDF. The PDF was rasterized at 120 dpi and inspected; text remains
  legible and both columns flow without overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages
  and six first-party stylesheets. `git diff --check` passed.

## Limitations and decisions

- The probabilistic analysis reuses the point analysis's five outcomes,
  overlapping folds, surface-text/coarse-demographic representation, and fixed
  weights. It is a dependent extension, not independent confirmation.
- CRPS is the primary distributional score. Central 80% coverage and width are
  interpreted jointly through interval score; narrower intervals are not
  called better merely for being narrow.
- Line-count intervals over-cover substantially against their 80% target.
  Empirical coverage within this selected training cohort is descriptive, not
  a population guarantee.
- The result concerns response length and revision volume, not correct future
  lexical content. The case audit is a derived benchmark-data adaptation under
  CC BY-NC-SA 4.0.
- No development or private answer was accessed, no test artifact changed, and
  no private-test performance claim was made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Avoid another fixed lexical re-ranker on these same cases. A substantively
  semantic or synthesizing model should preserve the supported word-count
  distribution signal, test rather than assume the weaker Add/Delete signal,
  and beat leave-one-out marginal additions before any locked reuse of
  development labels.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
