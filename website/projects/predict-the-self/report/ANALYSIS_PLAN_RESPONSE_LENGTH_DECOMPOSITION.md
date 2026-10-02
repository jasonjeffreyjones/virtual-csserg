# Corrected locked analysis plan: decomposing response-length skill

**Locked:** 2026-10-02T09:06:54Z, after an inherited-audit replication check
failed but before any aggregate result was accepted, summarized, written, or
inspected.

## Why this correction exists

This plan supersedes `ANALYSIS_PLAN_RESPONSE_LENGTH_PERSISTENCE.md` without
altering that earlier lock. The initial implementation calculated case scores
in memory and then stopped on the first inherited-audit check. That check
revealed that the inherited audit's field named `word_count_marginal_crps` is
not a raw distribution of fold follow-up counts. It is already source-
calibrated: each fold follow-up-minus-source word-count change is added to the
held-out source word count. In other words, it is exactly the proposed
additive persistence distribution.

No result file had been written, no aggregate had been computed or displayed,
and no comparison had been interpreted. The corrected plan makes the new
quantity of interest explicit and converts the already-published source-form
contrast from a proposed primary result into a required reproduction check.
This correction is a transparent analysis lock, not a preregistration or
untouched design.

## Status and claim boundary

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter an
existing prediction method, or create or change a private-test submission. It
can decompose response-length forecast skill within this selected cohort. It
cannot identify a causal identity mechanism, support population
generalization, or measure private-test performance.

## Question

How much does a person's earlier word count improve prediction of follow-up
word count beyond the raw cohort distribution, before using the inherited
three-count source-form neighborhood?

## Fixed forecasts

Count words with the authoritative benchmark evaluator. For held-out case
`i`, let `x_i` be its 2024 response word count. For each of the other 149 fold
cases `j`, let `x_j` be its 2024 word count and `y_j` its follow-up word count.

The **raw follow-up marginal distribution** is the 149 equally weighted fold
follow-up counts `y_j`.

The **additive persistence distribution** is the 149 equally weighted values
`max(0, x_i + y_j - x_j)`. This must reproduce the inherited audit's
`word_count_marginal_crps` case by case. The transformation is additive
because word-count change is measured on the original count scale. No
coefficient, bandwidth, neighbor count, or other hyperparameter will be fit or
tuned.

The **source-form neighborhood** is the inherited fixed three-count
distribution: source word-token, distinct-token, and line counts; 30
neighbors; locked similarity weights; and locked fold prior. Reuse its stored
case-level word-count CRPS unchanged.

The left-continuous empirical median of each raw and additive distribution is
its point forecast. Unchanged-source word count `x_i` is a separate point
comparator.

Hash-guard the pinned training data, authoritative evaluator, this corrected
plan, the unchanged initial lock, the source-form implementation, and its
complete case audit. Require identical ordered IDs and case-level reproduction
of source word count, observed follow-up word count, and additive-persistence
CRPS before accepting a result. Write one complete machine-readable result and
one 150-row case audit without raw response text. Do not write a development
or test prediction.

## Fixed evaluation

The **primary outcome** is follow-up word-count CRPS. The **primary contrast**
is raw-marginal CRPS minus additive-persistence CRPS; positive values favor
additive persistence. Report both means and case wins, ties, and losses.

Prespecified secondary diagnostics are:

- additive-persistence CRPS minus inherited source-form-neighborhood CRPS,
  required to reproduce the published paired comparison up to stored audit
  precision;
- absolute-error reductions for the additive median versus the raw marginal
  median and versus unchanged-source word count;
- central 80% interval coverage, width, and interval score for the raw and
  additive distributions, plus their paired interval-score difference;
- the cohort's Pearson correlation between source and follow-up word count,
  and descriptive distributions of source, follow-up, and change counts.

Use the inherited empirical-distribution CRPS, left-continuous weighted
quantiles, and central-interval score definitions. For every paired effect,
use a deterministic 20,000-resample percentile bootstrap over whole paired
cases with seed `20261002`, restarting the seeded generator for each
comparison. Report 95% intervals. The primary interpretation rests only on
the one primary contrast; secondary intervals are unadjusted diagnostics.

## Interpretation rules

Describe prior response length as improving CRPS beyond the raw cohort
distribution only if the primary interval excludes zero in the positive
direction. If it spans zero, conclude that this fixed analysis does not
separate their forecast skill. If it excludes zero in the negative direction,
describe the raw marginal as better under the fixed comparison.

The source-form comparison is a reproduction of known evidence, not a new
confirmatory result. Point and central-interval diagnostics cannot overturn
the primary comparison. Any supported skill concerns persistence in response
form, not correct future identity content. The analysis follows known positive
results, the folds overlap heavily, and the cohort is not a probability
sample. Bootstrap intervals describe sensitivity to this cohort's case
composition, not population generalization. Regardless of the result, do not
run the method on development data or make a private-test-performance claim.
