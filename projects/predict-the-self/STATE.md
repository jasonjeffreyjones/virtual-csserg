---
title: "Predict the Self"
status: Active
publication: Published
updated: 2026-10-10T09:07:03Z
---

# Predict the Self — Current State

## Status

Active and ready for a Scholar research iteration. The Predict Future Selves
benchmark is pinned, the deterministic stable-signifier method and its 81 test
predictions are frozen, all current public-development results are published,
and paired uncertainty and extractive-limit diagnostics are published. A
locked development-only matched-trajectory baseline now separates forecasting
the volume of identity-language change from forecasting its person-specific
content. A post hoc volume-matched marginal-addition control now shows that
retrieval does not beat common training-set additions on novel-token recovery.
A locked training-only leave-one-out diagnostic now also shows that one fixed
source-token-conditioned Add ranking does not improve on the marginal ranking.
A second locked diagnostic shows that pooling 30 similar trajectories with
strong shrinkage narrows but does not reverse that deficit.
A locked leave-one-out cross-validation of the unchanged stable projection now
shows that its mixed public-development pattern largely recurs across all 150
training trajectories without fitting on each held-out case's own follow-up.
Another locked leave-one-out analysis now removes the oracle addition budget
and shows that the fixed regularized neighborhood modestly improves forecasts
of Add count, Delete count, and follow-up word count, even though it does not
improve line count or establish a source-similarity advantage.
A locked probabilistic extension now shows that the corresponding full
predictive distributions improve CRPS and central-interval score only for
follow-up word count; CRPS differences for the other four outcomes remain
compatible with zero.
A locked source-feature ablation now locates most of that word-count signal in
earlier self-description text. Demographics alone do not improve on the
source-calibrated marginal distribution, although they add a small incremental
gain when combined with text.
A locked count-only comparison now qualifies that interpretation: matching on
source word-token, distinct-token, and line counts improves word-count CRPS
over the marginal and is not stably distinguishable from text-only matching.
The current evidence therefore locates signal in the earlier response but does
not isolate a lexical mechanism.
A locked cross-analysis multiplicity stress test now treats 16 no-oracle
point, distributional, and primary word-count contrasts as one fixed family.
Six directions retain simultaneous intervals, centering the robust pattern on
Add volume and later response length; the Delete-count point gain and the
small demographics-over-text increment become inconclusive.
A locked training-only full-text synthesis now tests whether those quantity
and continuity signals compose into a useful forecast. It improves word-count
and source-change calibration but fails its prespecified edit-similarity and
novel-content gates, so no development comparison is permitted.
A locked external-semantic test now also shows that replacing surface TF-IDF
with pretrained GloVe source centroids does not improve novel-token ranking:
the semantic neighborhood is effectively tied with the surface neighborhood
and remains worse than marginal Add frequency. Its content hurdle fails, so it
also cannot advance to development.
A corrected locked response-length decomposition now reveals that the inherited
“source-calibrated marginal” is itself additive persistence. A genuinely raw
fold distribution of follow-up word counts substantially outperforms that
source-conditioned comparator, so earlier word-count gains do not establish
value over ignoring the focal source.
A locked cross-fitted regression-to-the-mean analysis now tests whether a
weaker use of earlier response length can clear that raw baseline. Its mean
CRPS is descriptively lower, but the primary paired interval spans zero; a
newly fixed direct raw-versus-source-form interval also spans zero. Earlier
response length therefore still has not demonstrated incremental forecast
skill over the no-source distribution.
The Project follows the current three-memory-file and three-report structure.
The publication verifier now compares all 69 canonical public research
artifacts and their compatibility aliases byte for byte with the authoritative
Project sources, so two mutually consistent but stale public copies can no
longer pass validation. It now also rejects absolute host paths in public
scorecard provenance. Both development scorecards and every published copy use
stable logical repository and pinned-benchmark labels rather than ephemeral
workspace paths. The verifier now additionally requires reciprocal navigation
from the Executive Summary and both Full Report HTML surfaces to the other
report forms, and requires the short PDF to contain the exact public Executive
Summary and Full Report URLs rather than merely counting link annotations.
The guarded publisher and verifier now consume the same public artifact
inventory rather than maintaining independent lists. Validation requires the
Full Report's canonical research-artifact links to equal that inventory, and
the publisher rejects duplicate, escaping, or non-`artifacts/` alias paths.
The publisher now also requires every built canonical artifact to equal its
authoritative Project source before it mutates the public report tree; a stale
Quarto resource or missing Project source leaves the existing publication
untouched.
The verifier now additionally resolves source, JSON Pointer, and format
annotations on 20 headline Executive Summary values against the inventoried
machine-readable results, so a missing annotation, unlisted source, or stale
displayed number fails publication validation. It now binds the same resolved
claims to all five figure-bar widths and to the accessible label's ordered
numeric values, so the figure's visual and nonvisual encodings cannot drift
from its printed results.
The private test scorecard and challenge pull request remain open.

## Current finding

On 50 public development cases, stable-signifier projection versus the
repeat-2024 baseline:

- improves normalized edit similarity (`0.298061` vs. `0.291966`), token
  Jaccard (`0.142768` vs. `0.141930`), and ROUGE-L F1 (`0.227552` vs.
  `0.225683`);
- worsens token-overlap F1 (`0.307444` vs. `0.312202`) and character n-gram F1
  (`0.292293` vs. `0.296534`), while exact match remains zero;
- reduces word-count MAE (`41.64` vs. `56.68`) and source-similarity MAE
  (`0.678215` vs. `0.774317`), but increases line-count MAE (`9.76` vs. `6.80`).

There is no composite score or overall winner. Mean prediction-to-source
ROUGE-L remains `0.903898`, versus `0.225683` for observed follow-ups. The
extractive method therefore predicts far too much textual continuity.

A post hoc 20,000-resample paired case bootstrap shows that every nonzero
agreement difference has a 95% interval spanning zero. Word-count error
reduction (`+15.04`, interval `+1.18` to `+32.36`) and source-similarity error
reduction (`+0.096102`, `+0.066064` to `+0.129348`) are more stable to
development-case composition; line-count error reduction is negative
(`-2.96`, `-5.54` to `-0.42`). These are not population-generalization
intervals.

In a locked leave-one-out analysis of all 150 training trajectories, the
unchanged stable projection improves normalized edit similarity by `+0.004147`
(case-bootstrap interval `+0.000652` to `+0.007753`) but worsens token-overlap
F1 by `-0.003493` (`-0.007228` to `-0.000077`). Token Jaccard, ROUGE-L, and
character n-gram differences have intervals spanning zero. Word-count error
falls by `8.593333` (`2.573333` to `15.266667`) and source-similarity error by
`0.070769` (`0.054503` to `0.088484`), while the line-count error-reduction
effect is `-2.906667` (`-4.346833` to `-1.480000`).
Mean prediction-to-source similarity remains `0.929231` versus `0.200017`
observed, and `46.6667%` of fold predictions repeat the source exactly versus
zero observed follow-ups. This is recurrence within method-development data,
not untouched confirmation or population evidence.

On an average development case, `73.1727%` of distinct follow-up token types
are absent from the earlier response (case-bootstrap interval `69.7982%`–
`76.5607%`), and `65.0621%` of token occurrences are unavailable when source
counts are respected (`59.2663%`–`70.6149%`). Retrospective oracle extractive
ceilings are explicitly labeled unattainable and do not constitute prediction
results.

The exploratory trajectory-retrieval baseline matches each development case
to one training source with text-plus-demographic TF-IDF and copies that
neighbor's public follow-up. It predicts mean unique-token novelty of
`0.801727`, near the observed `0.731727`, and lowers source-similarity MAE to
`0.136074`. But it recovers the wrong novel content: mean novel-type precision
is `0.070466`, recall is `0.085362`, and F1 is `0.067109`. Its token-overlap F1
is `0.194693` versus `0.307444` for stable projection; all other non-exact
agreement metrics are also lower. Matching how much the language changes is
not matching how this person's expressed identity changes.

At exactly the same case-level novel-token prediction volume (mean `46.94`
types), a training-only marginal-addition prior outperforms trajectory
retrieval. Mean precision is `0.176545` versus `0.070466`, recall is `0.172611`
versus `0.085362`, and F1 is `0.142637` versus `0.067109`. The paired
marginal-minus-retrieval F1 difference is `+0.075528` with a case-bootstrap
interval of `+0.055927` to `+0.094990`; the prior wins 40 cases, ties 6, and
loses 4. This post hoc token-set control is not a coherent full-text forecast,
but retrieval has not demonstrated person-specific lexical advantage over
common additions.

In a separate locked leave-one-out analysis of the 150 training trajectories,
a source-conditioned ranking uses the strongest smoothed association between
each earlier source token and each candidate Add event. At the same oracle
future-token budget, it recovers a mean `0.145238` of held-out additions versus
`0.160992` for leave-one-out marginal frequency. The paired conditioned-minus-
marginal difference is `-0.015754` with a case-bootstrap interval of
`-0.020829` to `-0.010736`; conditioning wins 19 cases, ties 63, and loses 68.
This rejects an incremental advantage for the fixed ranking, not for all
person-conditioned methods. Other folds contain only `0.773139` of an average
case's observed additions, and the oracle budget prevents a forecasting claim.

A second locked leave-one-out analysis replaces the strongest-token rule with
a strongly regularized 30-neighbor ensemble over source-text and 2024-
demographic TF-IDF. It recovers a mean `0.149007` of held-out additions versus
`0.160992` for the same marginal ranking. The paired neighborhood-minus-
marginal difference is `-0.011984` with a case-bootstrap interval of
`-0.018426` to `-0.005693`; conditioning wins 25 cases, ties 60, and loses 65.
The top sets overlap by `0.739706` on average, so the model changes about 26%
of guesses yet still performs worse. Pooling and stronger shrinkage narrow the
earlier deficit but do not demonstrate person-conditioned lexical advantage.

In a third locked leave-one-out analysis, the same 30-neighbor representation
forecasts revision volume without using any held-out future-derived budget.
Relative to source-calibrated fold medians, it lowers Add-count MAE to
`20.126667` from `21.340000` (error reduction `+1.213333`, interval `+0.680000`
to `+1.740000`), Delete-count MAE to `5.336275` from `5.614935` (`+0.278660`,
`+0.022274` to `+0.545876`), and word-count MAE to `52.940000` from `56.080000`
(`+3.140000`, `+1.093333` to `+5.213333`). Line-count forecasts are identical,
and the source-similarity reduction of `+0.002867` has an interval spanning
zero (`-0.000960` to `+0.006730`). Person matching carries modest signal about
the amount of revision but has not identified its new lexical content.

The locked probabilistic extension scores the same leave-one-out forecasts as
weighted empirical distributions. Follow-up word-count CRPS falls to
`38.156852` from `40.672695`; the paired reduction is `+2.515843` with a
case-bootstrap interval of `+1.008212` to `+4.059792`. The neighborhood's
central 80% word-count interval covers `84.6667%` of cases versus `80.6667%`
for the marginal distribution, and its interval-score reduction is
`+19.700000` (`+3.873167` to `+37.193333`). Add-count, Delete-count,
line-count, and source-similarity CRPS intervals all span zero. Thus the point
forecast gains for Add and Delete volume do not generalize to stable
distributional-score gains under this fixed model.

The locked source-feature ablation reproduces every marginal and combined
case-level CRPS value before separating the fixed representation. Text-only
word-count CRPS is `38.374556` versus `40.672695` for the marginal; the paired
reduction is `+2.298139` with interval `+0.816444` to `+3.865823`.
Demographics-only CRPS is `40.471984`; its `+0.200711` reduction has an
interval spanning zero (`-0.479832` to `+0.861529`). Adding demographics to
text supplies a smaller incremental reduction of `+0.217704` (`+0.024229` to
`+0.420871`). Add-count, Delete-count, and line-count ablation contrasts all
span zero. Earlier self-description carries most of the gain relative to
demographics under this source-calibrated comparison; demographics alone do
not.

The locked source-form comparison also reproduces every inherited marginal
and text-only case score. Count-only matching lowers word-count CRPS to
`37.427386` from `40.672695` for the marginal; the paired reduction is
`+3.245309` with a case-bootstrap interval of `+1.839350` to `+4.784335`.
Text-only CRPS is `38.374556`. The prespecified source-form-minus-text effect
is `-0.947170`, with an interval spanning zero (`-1.943737` to `+0.035874`),
so this fixed comparison does not distinguish their primary skill or support a
lexical advantage. Source form also improves line-count CRPS by `+0.445157`
over the marginal (`+0.206291` to `+0.701574`); this is an unadjusted secondary
response-form diagnostic, not evidence about future identity content.

The locked cross-analysis stress test applies one synchronized 20,000-
resample studentized max-|t| case bootstrap to 16 unique no-oracle contrasts.
Its common critical value is `2.959538`. Six simultaneous 95% intervals exclude
zero: Add-count point-error reduction (`+0.397788` to `+2.028879`), word-count
point-error reduction (`+0.047580` to `+6.232420`), word-count CRPS reduction
(`+0.223750` to `+4.807936`), text-only versus marginal word-count CRPS
(`+0.023968` to `+4.572310`), combined versus demographics-only word-count CRPS
(`+0.011811` to `+4.618453`), and source-form versus marginal word-count CRPS
(`+1.000674` to `+5.489943`). Delete-count point error (`-0.116978` to
`+0.674298`) and combined versus text-only word-count CRPS (`-0.084469` to
`+0.519876`) now span zero. This is a post hoc sensitivity audit of stored
scores from overlapping folds, not retroactive preregistration, formal
population familywise control, or fresh confirmation.

The locked calibrated-synthesis analysis combines stable source-unit ranking,
a count-only word target, a text-and-demographic Add target, and common fold
follow-up units in 150 leave-one-out predictions. Relative to repeat-2024, it
lowers word-count MAE to `51.986667` from `55.580000` (error reduction
`+3.593333`, interval `+1.440000` to `+5.726667`) and raises ROUGE-L F1 to
`0.220153` from `0.200017` (`+0.020136`, `+0.002677` to `+0.037571`). But
normalized edit similarity falls to `0.268883` from `0.272662` (difference
`-0.003779`, interval `-0.013404` to `+0.004287`), line-count MAE rises to
`27.053333` from `6.160000`, and novel-type F1 is `0.075887` versus `0.134680`
for an equal-volume marginal ranking (difference `-0.058793`, `-0.076168` to
`-0.041473`). The three-part advancement gate fails; development labels remain
unread by this method.

The locked semantic-neighborhood analysis represents each training source as a
fold-IDF-weighted centroid of distinct public-domain 25-dimensional GloVe
Twitter token vectors. The vectors cover `2409` of `2537` source token types
(`94.9547%`), with no zero-coverage case. At the same oracle held-out Add budget,
the semantic ranking recovers a mean `0.148760` of additions versus `0.160992`
for marginal frequency. The semantic-minus-marginal difference is `-0.012232`
with a case-bootstrap interval of `-0.018361` to `-0.006322`; semantic wins 22
cases, ties 65, and loses 63. Its difference from the inherited surface
neighborhood is `-0.000247` (`-0.006521` to `+0.005834`). Distributional
source similarity therefore does not demonstrate person-conditioned lexical
advantage under this fixed centroid and ranking rule.

The corrected locked response-length analysis separates the raw fold
distribution of follow-up counts from additive persistence, which adds fold
word-count changes to the focal person's earlier count. Raw-marginal CRPS is
`32.579884` versus `40.672695` for additive persistence. The raw-minus-
additive effect is `-8.092811`, with a case-bootstrap interval of `-15.719421`
to `-1.507037`; negative values favor raw. Raw median MAE is `46.073333`
versus `56.080000`, and raw central-80% interval score is `196.800000` versus
`264.626667`. Source and follow-up word counts correlate `0.304483`. The
inherited source-form neighborhood still improves on additive persistence by
`3.245309`, but its mean CRPS (`37.427386`) remains descriptively above raw.
No direct paired raw-versus-source-form interval was prespecified. The earlier
multiplicity result remains correct for its fixed family, but that family did
not include the stronger no-source baseline.

The locked response-length shrinkage analysis replaces the unit-slope
assumption with support-case-cross-fitted OLS slopes. Across 22,350 support
values the slopes average `0.239491` (standard deviation `0.011023`; range
`0.168483`–`0.341135`). Linear-persistence CRPS is `31.572068` versus
`32.579884` for raw; the raw-minus-linear reduction is `+1.007816`, but its
paired case-bootstrap interval spans zero (`-1.235220` to `+3.013792`). Linear
median MAE is `44.764717` versus `46.073333` for raw, and its `+1.308617`
reduction also spans zero (`-1.591848` to `+4.045325`). The delayed direct
raw-minus-source-form CRPS effect is `-4.847502` (`-11.308398` to `+0.630052`),
so that comparison is inconclusive as well. Regression to the mean repairs the
worst persistence assumption but does not establish source-length skill beyond
raw.

## Completed research and artifacts

- Retrieved the public benchmark at immutable commit
  `9b6a766712583fec8d3182957260b1123fbfa146` and recorded SHA-256 hashes for
  prediction inputs, documentation, evaluator, and validator.
- Implemented `analysis/stable_signifier_projection.py`, a deterministic,
  standard-library extractive method trained on 150 public pairs. It uses no
  demographics, external data, or generative model.
- Generated all 50 development predictions and the complete official public
  scorecard. Generated and froze all 81 private-test predictions; the pinned
  official validator reports `VALID: 81 predictions`.
- Added `analysis/analyze_dev_diagnostics.py`, a hash-guarded deterministic
  paired bootstrap and extractive-limit analysis, plus its complete
  machine-readable JSON result and three unit tests.
- Locked `ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md` before fold
  prediction or scoring (SHA-256
  `2929b1fb8111c42170d23e725c08f6167135d9a703a1b61e87ed59af5f97c5d8`).
  Added a hash-guarded 150-case leave-one-out evaluation of the frozen
  generator, five focused tests, all fold predictions, and the complete paired
  machine-readable scorecard. Development and test artifacts were not changed.
- Locked `ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md` before generating new
  development predictions (SHA-256
  `86b2ddfe775773e1964beeefbac5479d88f6c46cd3385bf3a992fc7ae64e9c83`).
  The lock explicitly is not a preregistration because development labels had
  already been inspected.
- Added a deterministic standard-library trajectory-retrieval generator,
  development match audit, all 50 predictions, complete official scorecard,
  paired comparison, novelty-content diagnostics, and four unit tests. No
  retrieval test submission was generated.
- Added a hash-guarded deterministic marginal-addition diagnostic, complete
  machine-readable result, 2,770-row token audit, and four unit tests. It gives
  the prior and retrieval identical novel-token budgets case by case and
  reports paired precision, recall, and F1 comparisons.
- Locked `ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md` before implementing or
  scoring a training-only leave-one-out comparison (SHA-256
  `e65f04fd9e55843db8ff1a1bb0544acb00ec869eb58f9b312a63d531fc5f4ec9`).
  Added the hash-guarded analysis, six focused unit tests, complete JSON result,
  and 150-row case audit. Development and test artifacts were not changed.
- Locked `ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md` before implementation or
  scoring (SHA-256
  `c7a494327dd1dd7fc83911540a6a9095fcc8d684172a7388bd610206ac4ca13d`).
  Added the hash-guarded analysis, six focused unit tests, complete JSON result,
  and 150-row case audit. No development or test artifact was generated or
  changed.
- Locked `ANALYSIS_PLAN_CHANGE_VOLUME.md` before benchmark retrieval in this
  iteration, implementation, or scoring (SHA-256
  `53c974fcd37f443ea846e88328a125169265fb41ac1cc7877529bdbf9a09638f`).
  Added a hash-guarded no-oracle leave-one-out volume analysis, six focused
  tests, a complete JSON result, and a 150-row case audit. No development or
  test artifact was read or changed by the analysis.
- Locked `ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md` before reopening benchmark
  data, implementation, or scoring (SHA-256
  `00d5e2805082986b00f2716808ee12d4cff70ec900a5e47636e893217368f020`).
  Added a hash-guarded leave-one-out probabilistic extension, seven focused
  tests, a complete JSON result, and a 150-row CRPS/interval audit. No
  development or test artifact was read or changed by the analysis.
- Locked `ANALYSIS_PLAN_FEATURE_ABLATION.md` before reopening benchmark data,
  implementation, or scoring (SHA-256
  `ed9fa67b2cc1265f3710471f96d7ffbfd16986b8295ef5072da26c263d8b7da4`).
  Added a hash-guarded three-representation leave-one-out ablation, six focused
  tests, a complete JSON result, and a 150-row case audit. Clean regeneration
  reproduced both outputs byte for byte; no development or test artifact was
  read or changed by the analysis.
- Locked `ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md` before reading benchmark rows,
  implementation, or scoring (SHA-256
  `5ffaf6b8289a360926da3ae3b1398a336949e698c6157f8ba94ef316ec63c5ad`).
  Added a hash-guarded count-only leave-one-out comparison, six focused tests,
  a complete JSON result, and a 150-row case audit. It reproduced the preceding
  marginal and text-only scores before accepting results and did not read or
  change development or test artifacts.
- Locked `ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md` before cross-analysis
  resampling (SHA-256
  `d3c31e1bd77df8da0d5b7017438f2b9ff04ba5f39c4dfcb803c1c38f294fb9ac`).
  Added a hash-guarded synchronized studentized max-|t| bootstrap, six focused
  tests, a complete JSON result, and a 16-row contrast audit. The calculation
  reads only four existing training-case audits, verifies their hashes and
  inherited means, and never reads benchmark, development, or test rows.
- Locked `ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md` before reading benchmark rows
  in the iteration, implementation, or scoring (SHA-256
  `ae0594e0f95f4131416be0bab4c3bfa913010dc6380d65c39966849c3a9f7253`).
  Added a hash-guarded full-text leave-one-out generator and evaluation, six
  focused tests, all 150 fold predictions, a complete case audit, and a JSON
  result with a prespecified no-development gate. No development or private-
  test row or artifact was read or changed.
- Locked `ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md` before reading
  benchmark rows (SHA-256
  `6a6a536a11c552b0e75f40ce6d79100902727958fa908cb57a662ac85df5fdcf`).
  Added a standard-library streaming GloVe parser, hash-guarded leave-one-out
  semantic-neighborhood comparison, seven focused tests, complete JSON result,
  and 150-row case audit. The script reproduces every inherited marginal and
  surface-neighborhood hit count before accepting results. Development and test
  rows and artifacts were not read or changed.
- Preserved the initial response-length lock unchanged after its first audit
  check exposed that the inherited word-count “marginal” already meant
  additive persistence. Locked the corrected
  `ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md` before accepting,
  summarizing, writing, or inspecting any aggregate result (SHA-256
  `8071914fd204beefeabd294fac7e3f1b00dceeba50c0372ffbd5498b2d136861`).
  Added a hash-guarded raw-versus-additive analysis, six focused tests, a
  complete JSON result, and a 150-row audit. It reproduces the inherited
  additive CRPS case by case and reads no development or test row.
- Preserved the test artifact at SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`
  and documented the method in a submission-ready card.
- Locked `ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md` before inspecting any
  row of the preceding count audit or computing a new aggregate (SHA-256
  `ca69f562c3a78e34ed5cb9997a1ac6816492bf5273cda4686a3a92a8fb22fd92`).
  Added a hash-guarded cross-fitted linear-persistence analysis, eight focused
  tests, a complete JSON result, and a 150-row count-only audit. The analysis
  reproduces inherited raw and additive CRPS case by case and reads no
  benchmark text, development row, or private-test row.
- Strengthened the publication verifier to require every canonical research
  artifact and compatibility alias to equal its authoritative Project source.
  Three focused regression tests cover matching copies, mutually consistent
  stale public copies, and a stale alias without adding a runtime dependency.
- Removed machine-specific absolute paths from both authoritative development
  scorecards and all four public copies. Retrieval scorecard regeneration now
  emits stable logical provenance labels, and four verifier regressions reject
  POSIX paths, Windows paths, and `file:` URIs while accepting logical labels.
- Strengthened three-form publication validation so the Executive Summary,
  Full Report landing page, and Full Report evidence chapter must each link to
  the other report forms, while the short PDF must contain the exact production
  Executive Summary and Full Report URLs. Four focused regressions cover both
  valid reciprocity and the former false-positive cases.
- Replaced the publisher and verifier's independent 68-entry artifact lists
  with one public 69-entry `PUBLICATION_ARTIFACTS.json` inventory, including
  the inventory itself. Six focused regressions cover malformed mappings,
  exact report-link agreement, omissions, and unlisted research artifacts.
- Strengthened the guarded publisher to compare every built canonical artifact
  byte for byte with its authoritative Project source before staging or
  replacing the public report. Two focused regressions show that stale build
  resources and missing Project sources both fail without changing the
  existing public tree.
- Bound the Executive Summary's five headline continuity/novelty values and
  fifteen development-agreement values to inventoried JSON artifacts with RFC
  6901 pointers and explicit display precision. Four focused regressions cover
  matching values, stale display text, unlisted result sources, and missing
  headline annotations.
- Bound the dense Executive Summary figure's five CSS bar widths and ordered
  accessible numeric label to the same resolved result claims. Three focused
  regressions cover matching encodings, a stale visual width, and stale
  screen-reader text.

## Publication and build structure

- `index.qmd` and `report.qmd`, governed by `_quarto.yml`, render a two-chapter
  Quarto HTML book into ignored `_book/`. Two chapters are an editorial choice,
  not a fixed requirement.
- `analysis/publish_full_report.py` replaces the public report only from a
  complete build and removes stale generated files. Unit tests cover complete
  replacement and preservation after an incomplete build.
- `short-report.md` and `analysis/render_short_report.py` generate a linked,
  two-column PDF. Validation permits any nonempty length through the actual
  ten-page ceiling.
- The five-minute Executive Summary uses the selected evidence-brief structure:
  question/status, exactly one dense quantitative figure, nine linked findings,
  and both report choices.
- The three forms link reciprocally. Validation checks the Executive Summary,
  both Full Report HTML surfaces, and exact PDF URI actions rather than using a
  PDF annotation count as a proxy. The Full Report publishes sixty-nine
  research artifacts directly from their authoritative project paths,
  including the source-to-alias inventory, and preserves the matching
  `report/artifacts/` aliases as byte-identical compatibility copies.
  Validation checks both public copies directly against each Project source
  and requires the report's canonical artifact links to match the inventory.
- The guarded publisher checks built canonical artifacts against Project
  sources before any public-tree mutation; the verifier independently repeats
  the source-to-canonical and source-to-alias checks afterward.
- The verifier resolves all 20 annotated headline values in the Executive
  Summary against their authoritative inventoried JSON results at the declared
  precision. It additionally requires all five CSS bar widths to equal those
  source values on the stated 0–1 scale and requires the accessible label to
  contain the five displayed values in bar order. This does not bind every
  quantitative statement in the three reports.
- `BUILD.md` gives the complete build and check sequence. Project tests, the
  publication verifier, and the Version 1 promise groups are the required
  validation gates.

## Decisions and constraints

- Test answers and follow-up demographics are private. Only the challenge
  organizer can produce an official test score; no test-performance claim is
  currently valid.
- Development data informed extractive-rule selection. Treat its scorecard as
  model-selection evidence, not an untouched confirmatory estimate.
- The bootstrap and lexical-limit analysis are post hoc diagnostics of frozen
  predictions. Their intervals characterize development-case composition only;
  their oracles inspect observed futures and are unattainable prospectively.
- Stable-projection cross-validation withholds each case's future from its own
  model fit, but the training corpus had already informed method development
  and folds overlap heavily. Its intervals describe sensitivity to this
  selected training cohort, not population generalization. The fold-prediction
  CSV is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The retrieval method and evaluation were locked before generation in this
  iteration, but its development comparison remains exploratory because those
  labels were examined earlier. It transfers another participant's public
  follow-up rather than making a factual statement about the focal person.
- Retrieval predictions adapt CC BY-NC-SA 4.0 benchmark data. They are
  published for audit, not submitted for private-test evaluation. The original
  stable test artifact remains unchanged.
- The marginal-addition comparison is post hoc and diagnostic. It borrows
  retrieval's case-level token budget, predicts token sets rather than full
  text, and includes function words that need not be identity signifiers. The
  token audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The source-conditioned comparison is training-only and leave-one-out, but it
  uses each held-out follow-up's novel-type count as an oracle budget. Its
  fixed maximum-association rule and ten-case prior test only one form of
  conditioning. The analysis is not development or private-test performance,
  and its case audit is a derived benchmark-data adaptation under CC BY-NC-SA
  4.0.
- The regularized-neighborhood comparison shares the training-only oracle
  budget and lexical identity-signifier limits. Its fixed 30-neighbor size and 30-case
  marginal prior were not tuned; the text-and-demographic representation was
  selected in earlier work. Coarse demographic similarity is not an
  ipseological mechanism, and its case audit is a derived benchmark-data
  adaptation under CC BY-NC-SA 4.0.
- The change-volume comparison uses no held-out future budget, but its
  representation and fixed 30-neighbor/equal-shrinkage choices came from
  earlier Project work. Counts remain continuous, its folds overlap, and its
  audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The probabilistic extension reuses the same outcomes, folds,
  surface-text/coarse-demographic representation, and fixed weights. Its
  central intervals are discrete empirical intervals, overlapping-fold
  coverage is descriptive rather than a population guarantee, and its audit
  is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The source-feature ablation is a dependent extension chosen after the
  combined word-count gain was known. It retains sparse exact-value
  demographic features, uses unadjusted secondary contrasts as diagnostics,
  and does not establish that demographic categories are mechanisms. Its case
  audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The source-form comparison is a dependent extension chosen after the
  text-only word-count gain was known. Its three counts and fixed distance rule
  test one narrow nonlexical representation, not every response-form model. An
  interval spanning zero does not establish method equivalence. Its unadjusted
  secondary contrasts are diagnostics, and its case audit is a derived
  benchmark-data adaptation under CC BY-NC-SA 4.0.
- The multiplicity family was fixed only after the constituent analyses and
  aggregate results were known. Synchronized resampling preserves empirical
  dependence among the stored case effects, but it does not refit overlapping
  folds, undo sequential research choices, or support population inference.
  Its 16-row audit is a derived benchmark-data adaptation under CC BY-NC-SA
  4.0.
- The calibrated-synthesis design was chosen after all preceding quantity and
  content results were known. Common exact units favor generic template
  statements and their appended-line format produces severe line-count error.
  Its gate is pointwise rather than multiplicity-adjusted. Fold predictions and
  the audit are derived benchmark-data adaptations under CC BY-NC-SA 4.0; the
  failed gate forbids development evaluation of this fixed method.
- The semantic-neighborhood design was chosen after the earlier content
  failures were known. Its external Twitter-trained vectors are distributional
  rather than validated identity measures and can encode bias or domain
  mismatch; its centroid discards order, polysemy, negation, and response
  structure. It retains the oracle budget, candidate vocabulary, and fixed
  neighborhood shrinkage. The GloVe artifact is PDDL-licensed, hash-pinned, and
  not committed. Its case audit is a derived benchmark-data adaptation under
  CC BY-NC-SA 4.0; the failed hurdle forbids development evaluation.
- The response-length decomposition was corrected after its first replication
  check revealed the inherited comparator's meaning. The original lock remains
  byte-preserved, and no aggregate was accepted, written, or inspected before
  the correction, but the sequence is not preregistration. The primary paired
  result covers raw versus additive only; raw versus source form is descriptive.
  Its overlapping folds and bootstrap concern this selected cohort, and its
  audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
- The response-length shrinkage test was designed after the raw-baseline result
  and source-follow-up correlation were known. Its support slopes exclude both
  the outer and support case but overlap extensively, and its one primary
  interval does not establish incremental skill. Secondary comparisons cannot
  overturn that decision; its count-only audit remains a derived benchmark-
  data adaptation under CC BY-NC-SA 4.0.
- Do not alter the frozen test artifact in response to private score feedback.
- Public scorecard provenance must use stable logical labels rather than
  machine-specific absolute paths. Benchmark hashes and the pinned commit
  remain the authority for the referenced inputs.
- Three-form reciprocity requires links from the Executive Summary and both
  Full Report HTML surfaces, plus exact production Executive Summary and Full
  Report URI actions in the short PDF. Annotation count alone is insufficient.
- `PUBLICATION_ARTIFACTS.json` is the sole source-to-compatibility-alias
  inventory. Every inventoried canonical artifact must be linked from the Full
  Report, and every linked research artifact must be inventoried.
- The guarded publisher must leave the current public report untouched unless
  every inventoried Quarto resource exists and is byte-identical to its
  authoritative Project source.
- Headline result annotations in the Executive Summary must retain an
  inventoried JSON source, a resolvable JSON Pointer, and the declared numeric
  format; the publication verifier requires exactly 20 such values. Each of
  the five dense-figure bars must reference one uniquely identified claim, and
  the figure's accessible label must reference the five claims in display
  order.
- `PROJECT.md` remains the PI-owned charter. `DIALOG.md` is the bounded dialog
  index; future iterations create one immutable record under
  `dialog/iterations/` and update the yearly index. The pre-migration dialog is
  byte-preserved under `dialog/legacy/`. Legacy `PI.md` and `LOG.md` remain
  intact as additional historical records.

## Important files

- `PROJECT.md`: PI-owned charter.
- `STATE.md`, `DIALOG.md`, and `dialog/`: current state, bounded navigation,
  immutable iteration records, yearly indexes, and the preserved legacy dialog.
- `BUILD.md`, `_quarto.yml`, `index.qmd`, `report.qmd`, `short-report.md`:
  publication sources and reproduction instructions.
- `PUBLICATION_ARTIFACTS.json`: authoritative public artifact and
  compatibility-alias inventory shared by the publisher and verifier.
- `BENCHMARK_PROVENANCE.md`: pinned commit, licensing, and governing hashes.
- `ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md`: fixed exploratory comparison plan.
- `ANALYSIS_PLAN_STABLE_PROJECTION_CROSS_VALIDATION.md`: fixed training-only
  recurrence check for the frozen stable projection.
- `ANALYSIS_PLAN_SOURCE_CONDITIONED_ADDITIONS.md`: fixed training-only
  source-conditioned Add-ranking plan.
- `ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md`: fixed training-only regularized-
  neighborhood Add-ranking plan.
- `ANALYSIS_PLAN_CHANGE_VOLUME.md`: fixed no-oracle leave-one-out revision-
  volume forecasting plan.
- `ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md`: fixed probabilistic extension of
  the revision-volume analysis.
- `ANALYSIS_PLAN_FEATURE_ABLATION.md`: fixed text-only, demographics-only, and
  combined source-feature comparison.
- `ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md`: fixed lexical-versus-count-only
  source-response comparison.
- `ANALYSIS_PLAN_MULTIPLICITY_STRESS_TEST.md`: fixed 16-contrast family and
  simultaneous-interval sensitivity procedure.
- `ANALYSIS_PLAN_CALIBRATED_SYNTHESIS.md`: fixed full-text synthesis rule,
  content control, and three-part advancement gate.
- `ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md`: fixed external-semantic
  Add-ranking representation, controls, and content hurdle.
- `ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md` and
  `ANALYSIS_PLAN_RESPONSE_LENGTH_DECOMPOSITION.md`: preserved initial lock and
  corrected raw-versus-additive word-count plan.
- `ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md`: fixed cross-fitted regression-
  to-the-mean response-length plan.
- `analysis/stable_signifier_projection.py`: prediction method.
- `analysis/analyze_dev_diagnostics.py`: paired uncertainty and extractive-limit
  diagnostics.
- `analysis/analyze_stable_projection_cross_validation.py`: hash-guarded
  leave-one-out evaluation; its JSON and prediction CSV are under `results/`.
- `analysis/trajectory_retrieval.py` and
  `analysis/analyze_trajectory_retrieval.py`: development-only retrieval and
  locked paired/novelty analysis.
- `analysis/analyze_novelty_prior.py`: post hoc volume-matched marginal-
  addition control; `results/novelty_prior_dev_analysis.json` and
  `results/novelty_prior_token_audit.csv` are its complete outputs.
- `analysis/analyze_source_conditioned_additions.py`: locked leave-one-out
  ranking comparison; `results/source_conditioned_additions_train_analysis.json`
  and `results/source_conditioned_additions_train_audit.csv` are its outputs.
- `analysis/analyze_neighborhood_additions.py`: locked leave-one-out pooled-
  trajectory comparison; `results/neighborhood_additions_train_analysis.json`
  and `results/neighborhood_additions_train_audit.csv` are its outputs.
- `analysis/analyze_change_volume.py`: locked leave-one-out response-form and
  revision-volume forecasts; its JSON and case audit are under `results/`.
- `analysis/analyze_change_distributions.py`: locked leave-one-out CRPS and
  central-interval analysis; its JSON and case audit are under `results/`.
- `analysis/analyze_feature_ablation.py`: locked source-feature ablation; its
  JSON and complete case audit are under `results/`.
- `analysis/analyze_source_form_ablation.py`: locked source-form comparison;
  its JSON and complete case audit are under `results/`.
- `analysis/analyze_multiplicity_stress_test.py`: locked cross-analysis
  robustness audit; its complete JSON result and flat contrast audit are under
  `results/`.
- `analysis/analyze_calibrated_synthesis.py`: locked training-only full-text
  synthesis and gate evaluation; its JSON, case audit, and all fold predictions
  are under `results/`.
- `analysis/analyze_semantic_neighborhood_additions.py`: locked streaming GloVe
  semantic-neighborhood comparison; its JSON and 150-case audit are under
  `results/`.
- `analysis/analyze_response_length_persistence.py`: corrected locked
  response-length baseline decomposition; its JSON and 150-case audit are
  under `results/`.
- `analysis/analyze_response_length_shrinkage.py`: locked cross-fitted linear
  response-length comparison; its JSON and 150-case audit are under `results/`.
- `analysis/publish_full_report.py`, `analysis/render_short_report.py`, and
  `analysis/verify_publication.py`: guarded publication pipeline and checks,
  including authoritative source-to-public artifact identity.
- `results/`: both development prediction sets, complete scorecards, retrieval
  audit, and complete diagnostic results.
- `submissions/`: frozen test artifact and method card.
- `website/projects/predict-the-self/`: Executive Summary, Full Report, short
  report, and copied reproducibility artifacts.

## Problems and unresolved PI questions

- The prepared CSV and method card have not been opened as a pull request in
  the challenge repository. No authenticated GitHub write path is available in
  this workspace.
- Private test evidence remains unavailable by benchmark design.
- No browser executable is installed on this host, so the new HTML summary and
  book still need rendered desktop, phone, keyboard, and assistive-technology
  inspection. The PDF received a local rasterized visual check.
- No PI question blocks the next Scholar from useful work.

## Likely next steps

1. Submit exactly the frozen CSV and method card to the challenge organizer;
   add the complete private scorecard unchanged when returned.
2. Before another model comparison, preregister the method and the role of
   development data to limit repeated tuning; preferably reserve new evidence
   or use training-only nested evaluation because development labels are now
   heavily reused.
3. Do not evaluate the failed common-unit synthesis or failed GloVe-centroid
   ranking on development data. The cross-fitted length adjustment also fails
   its raw-baseline hurdle. Avoid more fixed Add re-rankers, count models, or
   post hoc decompositions on the same 150 cases without richer compositional
   context or new longitudinal evidence. Before reusing development labels,
   require a person-conditioned method to beat the raw fold follow-up
   distribution for response length, preserve response-form calibration, and
   beat leave-one-out marginal additions for content; then lock any development
   comparison and avoid private test feedback.
4. Perform the remaining rendered accessibility and responsive-layout checks
   when browser infrastructure is available.
