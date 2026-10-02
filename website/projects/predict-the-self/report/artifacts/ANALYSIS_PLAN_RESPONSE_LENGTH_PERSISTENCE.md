# Locked analysis plan: response-length persistence baseline

**Locked:** 2026-10-02T09:03:16Z, before reading the pinned benchmark rows in
this iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration. The training cohort and the previously supported
source-form word-count result informed earlier Project work. This analysis can
test whether that fixed three-count neighborhood improves on a still simpler
one-count persistence forecast within the selected cohort. It cannot provide
untouched confirmation, identify a causal identity mechanism, support
population generalization, or measure private-test performance.

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter an
existing prediction method, or create or change a private-test submission.

## Question

Does the fixed source-form neighborhood improve follow-up word-count CRPS
beyond a one-variable forecast that adds the fold distribution of observed
year-to-year word-count changes to the focal person's earlier word count?

## Fixed forecasts

Count words with the authoritative benchmark evaluator. For held-out case
`i`, let `x_i` be its 2024 response word count. For each of the other 149 fold
cases `j`, let `x_j` be its 2024 word count and `y_j` its follow-up word count.

The **additive persistence distribution** for case `i` is the 149 equally
weighted values `max(0, x_i + y_j - x_j)`. This is a prospective forecast:
the held-out follow-up `y_i` may enter only after the distribution is fixed.
The transformation is additive because word-count change is measured on the
benchmark's original count scale. No coefficient, bandwidth, neighbor count,
or other hyperparameter will be fit or tuned.

The **marginal distribution** is the 149 equally weighted fold follow-up word
counts `y_j`. Its median is the marginal point forecast. The median of the
additive persistence distribution is the additive point forecast. The
unchanged-source point forecast is `x_i`.

The inherited **source-form neighborhood** is exactly the fixed three-count
distribution in `ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md`: source word-token,
distinct-token, and line counts; 30 neighbors; the locked similarity weights;
and the locked fold prior. Reuse its stored case-level word-count CRPS rather
than changing or refitting it.

Hash-guard the pinned training data, authoritative evaluator, this plan, the
source-form implementation, and its complete case audit. Require identical
ordered IDs and case-level reproduction of source word count, observed
follow-up word count, and marginal word-count CRPS before accepting a result.
Write one complete machine-readable result and one 150-row case audit without
raw response text. Do not write a development or test prediction.

## Fixed evaluation

The **primary outcome** is follow-up word-count CRPS. The **primary contrast**
is additive-persistence CRPS minus inherited source-form-neighborhood CRPS;
positive values favor the source-form neighborhood. Report both means and
case wins, ties, and losses.

Prespecified secondary diagnostics are:

- marginal CRPS minus additive-persistence CRPS;
- absolute-error reductions for the additive median versus the marginal
  median and versus unchanged-source word count;
- central 80% interval coverage, width, and interval score for the marginal
  and additive distributions, plus their paired interval-score difference;
- the cohort's Pearson correlation between source and follow-up word count,
  and descriptive distributions of source, follow-up, and change counts.

Use the inherited empirical-distribution CRPS, left-continuous weighted
quantiles, and central-interval score definitions. For every paired effect,
use a deterministic 20,000-resample percentile bootstrap over whole paired
cases with seed `20261002`, restarting the seeded generator for each
comparison. Report 95% intervals. The primary interpretation rests only on
the one primary contrast; secondary intervals are unadjusted diagnostics.

## Interpretation rules

Describe the three-count source-form neighborhood as improving beyond the
one-count additive persistence forecast only if the primary interval excludes
zero in the positive direction. If it spans zero, conclude that this fixed
analysis does not separate their word-count forecast skill. If it excludes
zero in the negative direction, describe additive persistence as better under
the fixed comparison.

Describe additive persistence as improving over the fold marginal only if the
paired CRPS interval excludes zero in the positive direction. Point and
central-interval diagnostics cannot overturn the primary comparison. A
forecast based on response length concerns persistence in response form, not
correct future identity content. The analysis follows known positive results,
the folds overlap heavily, and the cohort is not a probability sample.
Bootstrap intervals therefore describe sensitivity to this selected cohort's
case composition, not population generalization. Regardless of the result,
do not run the method on development data or make a private-test-performance
claim.
