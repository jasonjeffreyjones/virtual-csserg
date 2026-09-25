---
title: "Predict the Self"
status: Active
publication: Published
updated: 2026-09-25T09:13:22Z
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
The Project follows the current three-memory-file and three-report structure.
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
span zero. Earlier self-description carries most of the supported
response-length signal; demographics alone do not.

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
- Preserved the test artifact at SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`
  and documented the method in a submission-ready card.

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
  question/status, exactly one dense quantitative figure, eight linked findings,
  and both report choices.
- The three forms link reciprocally. The Full Report publishes forty-two research
  artifacts directly from their authoritative project paths and preserves the
  matching `report/artifacts/` aliases as byte-identical compatibility copies.
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
- Do not alter the frozen test artifact in response to private score feedback.
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
- `analysis/publish_full_report.py`, `analysis/render_short_report.py`, and
  `analysis/verify_publication.py`: guarded publication pipeline and checks.
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
3. Avoid further fixed lexical re-rankers on the same 150 cases without a
   substantively new representation. Before reusing development labels,
   require a synthesizing or semantic person-conditioned approach to preserve
   the primarily text-driven word-count distribution signal, treat the small
   conditional demographic increment cautiously, test rather than assume the
   weaker Add/Delete volume signal, and beat leave-one-out marginal additions
   in training; then lock any development comparison and avoid private test
   feedback.
4. Perform the remaining rendered accessibility and responsive-layout checks
   when browser infrastructure is available.
