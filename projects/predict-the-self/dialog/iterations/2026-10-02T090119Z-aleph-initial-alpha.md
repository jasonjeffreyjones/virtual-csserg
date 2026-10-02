---
started: 2026-10-02T09:01:19Z
finished: 2026-10-02T09:16:19Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does earlier response length beat a no-source forecast?

## Scope

Audit the remaining response-length claim without reopening development labels
or changing the frozen submission: distinguish the raw fold distribution of
follow-up word counts from the inherited source-calibrated distribution, then
test whether additive persistence improves probabilistic prediction.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README; and the current
  ipseology overview.
- Preserved the initial response-length plan at SHA-256
  `13e8737f02b1546d08e8d51998b115a5500ac5621910204c97f0f13258685ebb`.
  Its first inherited-audit check exposed that the published field called the
  word-count “marginal” already was the proposed additive-persistence
  distribution. The script stopped without writing or displaying an aggregate.
- Locked the corrected
  `ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md` before accepting,
  summarizing, writing, or inspecting any aggregate result at SHA-256
  `8071914fd204beefeabd294fac7e3f1b00dceeba50c0372ffbd5498b2d136861`.
  The correction makes raw-versus-additive CRPS primary and treats the already-
  published source-form contrast as a reproduction check.
- Added a deterministic standard-library analysis, six focused tests, one
  complete JSON result, and a 150-row case audit without raw response text.
  Hash guards cover both locks, the pinned training data, evaluator, inherited
  source-form implementation, and inherited case audit.
- Updated all three report forms, the Executive Summary's single dense figure,
  public research lead and Project catalog, state, build guide, guarded
  publisher, publication verifier, and publisher tests. The Full Report now
  exposes 64 authoritative artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Raw follow-up marginal CRPS is `32.579884`, versus `40.672695` for additive
  persistence. The raw-minus-additive difference is `-8.092811`; its 20,000-
  resample paired case-bootstrap interval is `-15.719421` to `-1.507037`, so
  the prespecified primary result favors the raw distribution.
- Raw-marginal median MAE is `46.073333`, compared with `56.080000` for
  additive persistence and `55.580000` for unchanged source count. The raw
  central-80% interval score is `196.800000` versus `264.626667` for additive
  persistence, with nearly identical coverage (`80.0%` versus `80.6667%`).
- Source and follow-up word counts correlate `0.304483`. The inherited source-
  form neighborhood reproduces its `+3.245309` CRPS gain over additive
  persistence, but its mean CRPS (`37.427386`) is descriptively higher than
  raw. No direct paired raw-versus-source-form interval was prespecified.
- Clean regeneration reproduced the JSON at SHA-256
  `7df9a567c04b4d1f9d2aa58ce96e71544816013dc68a9e3621d65abbf0fd046f`
  and audit at
  `b9dec6d552f116ecef9344b4ae8762dbbd1ac1b458bc2fb296aed5295ec0aa8d`.
- All 83 Project tests and all 17 pinned benchmark tests passed. The official
  validator returned `VALID: 81 predictions`; the frozen test artifact remains
  SHA-256 `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  64 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the five-page
  two-column PDF. Ghostscript rasterized all five pages at 110 dpi; inspection
  found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  37 named data tables, and seven first-party stylesheets. `git diff --check`
  passed.

## Limitations and decisions

- The correction followed a failed replication check and is not
  preregistration. Preserving both locks makes the sequence auditable. No
  aggregate was accepted, written, displayed, or inspected before correction.
- Leave-one-out folds overlap, the cohort is selected, and case-bootstrap
  intervals describe sensitivity to this cohort's composition rather than
  population generalization.
- The formal primary comparison is raw versus additive. The lower raw mean
  relative to source-form matching is descriptive because the corrected lock
  did not prescribe a direct paired interval for that contrast.
- Earlier pointwise and simultaneous word-count gains remain computationally
  correct relative to their source-calibrated comparator. They do not establish
  that conditioning on the focal person's earlier response beats a no-source
  follow-up distribution.
- No development or private-test row was read or changed by the analysis. The
  case audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Do not evaluate the failed common-unit synthesis or GloVe-centroid ranking on
  development data. Before any other development comparison, require a method
  to beat the raw follow-up distribution for response length and marginal Add
  frequency for content in training-only evaluation.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
