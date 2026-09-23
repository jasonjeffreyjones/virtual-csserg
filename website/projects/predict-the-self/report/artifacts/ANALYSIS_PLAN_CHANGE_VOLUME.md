# Locked analysis plan: prospective change-volume forecasting

**Locked:** 2026-09-23T09:04:46Z, before retrieving the pinned benchmark data
in this iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration. The training corpus and its aggregate revision patterns have
informed earlier Project work, and the text-and-demographic representation was
selected for an earlier retrieval analysis. The analysis can test a new,
bounded question: whether that already-fixed representation predicts *how much*
a held-out self-description changes better than a source-calibrated marginal
forecast. It cannot supply untouched confirmation or population evidence.

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter any
existing method, or create or change a private-test submission.

## Question

Do 2024 source text and demographics improve leave-one-out forecasts of later
response form and Add/Delete event volume over simple fold-wide forecasts that
are calibrated to the held-out source?

## Fixed outcomes and source calibration

Use the pinned evaluator's case-folded Unicode word tokens. For each paired
training case, calculate five later outcomes:

1. distinct Add-event count: follow-up token types absent from the source;
2. distinct Delete-event count: source token types absent from the follow-up;
3. follow-up word count;
4. follow-up nonempty-line count; and
5. follow-up-to-source ROUGE-L F1 similarity.

Model source-calibrated quantities where possible: Add count directly; Delete
fraction (Delete count divided by distinct source-token count); follow-up-minus-
source word-count change; follow-up-minus-source line-count change; and source
similarity directly. Every source response is required to have at least one
token and one nonempty line.

## Fixed leave-one-out forecasts

For each case in original training-file order, hold out its complete row before
estimating outcomes. Construct two forecasts from the other 149 rows:

- **Source-calibrated marginal:** the ordinary median of the fold's modeled
  quantity, transformed back to the held-out outcome scale using only the held-
  out 2024 response where applicable.
- **Regularized neighborhood:** represent the held-out source and each fold
  source with the existing field-qualified 2024 text-and-demographic TF-IDF
  features. Select 30 neighbors by cosine similarity with original fold order
  breaking ties. Clip similarities at zero and normalize them to 30 effective
  cases. Estimate the modeled quantity by a weighted median that combines
  those neighbors with a 30-case prior distributed uniformly over all 149 fold
  observations. Transform the estimate back to the held-out outcome scale.

Clip transformed Delete forecasts to `[0, source distinct-token count]`, word-
count forecasts to at least zero, line-count forecasts to at least one, and
source-similarity forecasts to `[0, 1]`. Keep continuous forecasts rather than
rounding counts; this avoids inserting an arbitrary rounding rule into error
comparisons. The neighborhood size and equal neighbor/prior effective weights
are inherited unchanged from the earlier locked neighborhood analysis and will
not be tuned.

Hash-guard the pinned training data, authoritative evaluator, existing
trajectory-retrieval feature implementation, and this plan. Write a complete
machine-readable result and one 150-row case audit. Do not write any
development or test prediction.

## Fixed evaluation

For every outcome, report observed, marginal-predicted, and neighborhood-
predicted means and medians; mean absolute error (MAE); and root mean squared
error (RMSE). The primary paired effect is the case-level marginal absolute
error minus neighborhood absolute error, so positive values favor person-
conditioned neighborhoods.

For each primary effect, report wins, ties, and losses within cases. Use a
deterministic 20,000-resample percentile bootstrap over whole paired cases with
seed `20260923`, restarting the seeded generator for each outcome, and report
the 95% interval for the mean effect. There is no composite score and no
outcome weighting.

## Interpretation rules

If an outcome's paired interval excludes zero in the positive direction,
describe the regularized neighborhood as improving that outcome's MAE within
this cross-validation. If it spans zero, do not claim a stable improvement. If
it excludes zero in the negative direction, describe the neighborhood as
worsening MAE. Do not infer an overall winner from the five outcomes.

An advantage would concern revision *volume or form*, not correct future
content. A null or negative result would apply to this fixed surface-text and
coarse-demographic neighborhood, not to all person-conditioned forecasting.
The folds overlap heavily, the representation and hyperparameters predate this
lock, and the selected cohort is not a probability sample. Bootstrap intervals
therefore describe sensitivity to training-case composition, not population
generalization. No private-test performance claim is permitted.
