---
started: 2026-09-20T09:01:04Z
finished: 2026-09-20T09:13:53Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does source-token conditioning beat common additions?

## Scope

Test, without reusing development labels, whether a fixed ranking based on
earlier source-token-to-Add associations recovers person-specific novel token
types beyond their marginal training frequency. Preserve the frozen private-
test submission and all existing development predictions.

## Work completed

- Re-read the required repository and Project memory, all three prior immutable
  iteration records, relevant legacy PI guidance, the pinned Predict Future
  Selves README and governing documentation, and the current web edition of
  *Ipseology—A new science of the self*.
- Locked `ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md` before implementation
  or scoring at SHA-256
  `e65f04fd9e55843db8ff1a1bb0544acb00ec869eb58f9b312a63d531fc5f4ec9`.
  The document explicitly calls this an analysis lock rather than a
  preregistration because the training pairs had informed prior methods.
- Added a deterministic, hash-guarded leave-one-out analysis. Each training
  case is held out; the other 149 estimate marginal Add counts and smoothed
  source-token-to-Add rates. The source-conditioned ranking uses each
  candidate's strongest source-token rate with a fixed ten-case prior toward
  the marginal rate.
- Gave both rankings the same oracle budget: the held-out case's observed
  novel-type count. Added a complete JSON result, a 150-row case audit, and six
  focused unit tests. No development or test prediction was generated or
  altered.
- Expanded all three report forms, the Executive Summary's single dense
  figure, the home-page research lead, Project catalog, state, build guide,
  guarded publisher, and publication verifier. The Full Report now exposes 22
  authoritative research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- All 150 cases have positive observed-addition budgets. At equal oracle
  budgets, mean novel-type recovered fraction is `0.145238` for the source-
  conditioned ranking and `0.160992` for the marginal ranking.
- The paired conditioned-minus-marginal difference is `-0.015754`; its 20,000-
  resample case-bootstrap interval is `-0.020829` to `-0.010736`. Conditioning
  wins 19 cases, ties 63, and loses 68. Under the locked interpretation rule,
  the fixed conditional ranking shows no incremental advantage.
- The mean leave-one-out candidate-vocabulary ceiling is `0.773139`. Roughly
  22.7% of an average held-out case's additions are absent from every other
  training case's additions and unavailable to either ranking.
- Clean regeneration reproduced the JSON and CSV outputs byte for byte. All 22
  Project unit tests and all 17 pinned benchmark tests passed. The official
  validator again returned `VALID: 81 predictions`.
- The frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`,
  including both published copies.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  22 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, artifacts, the required phrase, and the
  two-page two-column PDF.
- Both PDF pages were rasterized at 144 dpi and visually inspected. The pages
  are balanced and legible, with no overlap or clipping. The Version 1 verifier
  passed all seven promise groups across 26 HTML pages and six first-party
  stylesheets. `git diff --check` passed.

## Limitations and decisions

- The oracle budget uses the held-out follow-up and isolates ranking quality;
  neither ranking is a prospective full-text forecast.
- The result applies to one fixed maximum-association rule with an adopted
  ten-case smoothing weight. It does not show that earlier signifiers contain
  no predictive information under richer or more strongly regularized models.
- Lexical tokens include function words and generic language that need not be
  semantic identity signifiers. The analysis predicts Add events but not
  Delete events, so it is not described as a transmutation model.
- The interval describes sensitivity to training-case composition in a small,
  selected cohort, not population-generalization uncertainty. The case audit
  is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- No private answer or score was accessed, and no test-performance claim was
  made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Before another development comparison, require a synthesizing or more
  strongly regularized person-conditioned method to beat leave-one-out
  marginal additions in training. Then lock any development evaluation and
  avoid private-test feedback for tuning.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
