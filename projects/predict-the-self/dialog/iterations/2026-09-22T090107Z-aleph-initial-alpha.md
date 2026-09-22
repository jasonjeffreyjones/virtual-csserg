---
started: 2026-09-22T09:01:07Z
finished: 2026-09-22T09:18:27Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does the frozen projection's mixed result recur?

## Scope

Test whether the already-frozen stable-signifier projection's small and mixed
public-development differences from repeat-2024 recur across leave-one-out
training predictions. Preserve every development and private-test artifact,
and avoid introducing another lexical content re-ranker.

## Work completed

- Re-read the required repository and Project memory, all three newest
  iteration records, relevant legacy PI guidance, the pinned Predict Future
  Selves README, and the current web edition of *Ipseology—A new science of the
  self*.
- Locked `ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md` before
  generating or scoring a fold prediction at SHA-256
  `2929b1fb8111c42170d23e725c08f6167135d9a703a1b61e87ed59af5f97c5d8`.
  The plan is explicitly an analysis lock rather than a preregistration because
  both training and development data informed earlier method work.
- Added a deterministic, hash-guarded leave-one-out analysis. Each of 150
  training cases is predicted from its 2024 response after the unchanged
  stable projection is refit on the other 149 cases. The script guards the
  training data, evaluator, plan, and frozen generator hashes.
- Added five focused tests, a complete paired machine-readable result, and all
  150 fold predictions. No development prediction or test submission was read
  by the analysis, generated, or altered.
- Expanded all three report forms, the Executive Summary's single dense
  figure, the home-page research lead, Project catalog, state, build guide,
  guarded publisher, and publication verifier. The Full Report now exposes 30
  authoritative research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Normalized edit similarity is `0.276809` for stable projection versus
  `0.272662` for repeat-2024. The paired difference is `+0.004147` with a
  20,000-resample case-bootstrap interval of `+0.000652` to `+0.007753`.
- Token-overlap F1 is `0.276737` versus `0.280231`. The paired difference is
  `-0.003493`, interval `-0.007228` to `-0.000077`. Token Jaccard, ROUGE-L,
  and character n-gram intervals span zero; exact match remains zero.
- Word-count error falls by `8.593333` (`+2.573333` to `+15.266667`) and
  source-similarity error falls by `0.070769` (`+0.054503` to `+0.088484`).
  Line-count error reduction is `-2.906667` (`-4.346833` to `-1.480000`). All
  three directions match the public-development result.
- Mean prediction-to-source similarity remains `0.929231` versus `0.200017`
  observed. The method repeats 46.7% of held-out sources exactly, while none of
  the observed follow-ups repeats its source. Better length and continuity
  calibration still does not solve future content.
- Clean regeneration reproduced the JSON and CSV outputs byte for byte. The
  pinned official evaluator independently reproduced all 15 scorecard values.
  All 33 Project tests and all 17 pinned benchmark tests passed; the official
  validator again returned `VALID: 81 predictions`.
- The frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  30 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, artifacts, the required phrase, and the
  three-page two-column PDF.
- All three PDF pages were rasterized at 144 dpi and visually inspected. Text
  is legible and both columns flow without overlap or clipping; the final
  references page has substantial but acceptable whitespace. The Version 1
  verifier passed all seven promise groups across 26 HTML pages and six first-
  party stylesheets. `git diff --check` passed.

## Limitations and decisions

- Leave-one-out fitting prevents each case's own follow-up from entering its
  model, but the training corpus had already informed method development and
  the folds overlap heavily. This is recurrence within method-development data,
  not untouched confirmation.
- The paired intervals describe sensitivity to this selected training cohort's
  case composition, not population generalization. The fold-prediction CSV is
  a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- Opposing agreement results and the absence of a composite preclude an overall
  winner claim. The replicated error directions are useful but substantively
  inadequate because predicted responses remain far too close to the past.
- No private answer or score was accessed, and no test-performance claim was
  made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Treat additional development comparisons as high-risk for overfitting. A new
  method should use a substantively semantic or synthesizing representation,
  clear the training-only marginal-addition baseline, and be locked before any
  reuse of development labels.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
