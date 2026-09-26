# Locked analysis plan: lexical text versus source response form

**Locked:** 2026-09-26T09:03:06Z, before reading the pinned benchmark rows in
this iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration. The training corpus, the supported text-only word-count
CRPS result, and all distributional hyperparameters informed earlier Project
work. The analysis can distinguish one fixed lexical neighborhood from one
fixed source-response-form neighborhood within the selected cohort. It cannot
provide untouched confirmation, identify a causal or semantic mechanism,
support population generalization, or measure private-test performance.

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter an
existing prediction method, or create or change a private-test submission.

## Question

Does the previously supported text-only improvement in leave-one-out
word-count CRPS exceed what can be obtained by matching only the observable
form of the earlier self-description?

## Fixed source-form representation and distribution

For each 2024 response, calculate three quantities with the authoritative
evaluator: word-token count, distinct word-token count, and line count. Apply
`log1p` to each quantity. Within each 149-case fold, calculate each feature's
population standard deviation, using `1` when the standard deviation is zero.
The distance from the held-out source to a fold source is the Euclidean
distance over their three standardized differences. Convert distance to
similarity as `1 / (1 + distance)`. Select the 30 largest similarities, with
original fold order breaking exact ties.

Use the unchanged similarity weighting, 30-case neighborhood effective
weight, 30-case uniform fold prior, five outcomes, source transformations,
inverse transformations, empirical-distribution CRPS, and bounds from the
preceding locked analyses. The source-calibrated marginal and text-only
distributions remain the fixed comparators. No held-out future may enter the
source-form representation, neighbor selection, weight, or predictive
distribution.

Hash-guard the pinned training data, authoritative evaluator, this plan, the
source-feature-ablation implementation, and its complete case audit. Require
the newly calculated marginal and text-only CRPS values to reproduce that
audit case by case before accepting a result. Write one complete
machine-readable result and one 150-row case audit. Do not write a development
or test prediction.

## Fixed evaluation

The **primary outcome** is follow-up word-count CRPS. The **primary contrast**
is source-form-only CRPS minus text-only CRPS; positive values favor text-only
matching. Also report marginal minus source-form-only CRPS and the reproduced
marginal minus text-only CRPS. Report mean CRPS and case wins, ties, and losses
for all three comparisons.

As prespecified secondary diagnostics, report the same means and paired
effects for Add count, Delete count, line count, and source similarity. These
secondary outcomes cannot overturn the primary word-count conclusion, and
there is no composite or outcome weighting.

For every paired effect, use a deterministic 20,000-resample percentile
bootstrap over whole paired cases with seed `20260926`, restarting the seeded
generator for every outcome and comparison. Report 95% intervals. These are
descriptive repeated-analysis intervals; no multiplicity-adjusted familywise
claim is planned.

## Interpretation rules

Describe lexical text matching as improving beyond source-form matching only
if the primary interval excludes zero in the positive direction. If it spans
zero, conclude that this fixed analysis does not separate their word-count
forecast skill. If it excludes zero in the negative direction, describe the
count-only source-form neighborhood as better under the fixed comparison.

Describe source-form matching as improving over the marginal only if that
paired interval excludes zero in the positive direction. Reproduction of the
earlier marginal-versus-text result is a consistency check, not new evidence.
Even if text-only wins, call the differentiating information lexical
composition rather than semantic identity: TF-IDF overlap can encode style,
template wording, and other surface regularities. The result concerns response
form, not correct future lexical content. Folds overlap heavily, the cohort is
not a probability sample, and the analysis follows a known positive result.
Bootstrap intervals therefore describe sensitivity to this selected cohort's
case composition, not population generalization. No private-test-performance
claim is permitted.
