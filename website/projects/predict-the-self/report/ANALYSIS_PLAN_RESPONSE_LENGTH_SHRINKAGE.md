# Locked analysis plan: regression-to-the-mean response length

**Locked:** 2026-10-03T09:04:33Z, before inspecting any case-level audit row,
implementing the analysis, or calculating a new aggregate.

## Status and claim boundary

This is a dependent training-cohort analysis lock, not a preregistration. It
was designed after the Project established that the raw fold distribution of
follow-up word counts outperforms additive persistence and descriptively has
lower mean CRPS than the inherited three-count source-form neighborhood. The
known positive correlation between source and follow-up word count motivates
one fixed regression-to-the-mean forecast, but no case-level result from the
new comparison has been inspected.

The analysis uses only the 150-row audit from the preceding training-only
response-length decomposition. It will not read benchmark text, development
or private-test rows; generate a text prediction; alter an existing method; or
change the frozen submission. It can test whether one simple form of source-
conditioned length forecasting beats a no-source baseline within this selected
cohort. It cannot establish correct future identity content, population
generalization, untouched confirmation, development performance, or private-
test performance.

## Question

Can a cross-fitted linear adjustment for earlier response length improve
follow-up word-count CRPS beyond the raw fold distribution, after shrinking
the unit-slope additive-persistence assumption toward the cohort's observed
source-follow-up relationship?

## Fixed forecasts

For outer held-out case `i`, let `x_i` be its source word count and `y_i` its
follow-up word count. For each support case `j != i`, fit an ordinary least-
squares slope `b_{-i,-j}` of follow-up count on source count using the other
148 cases. The slope includes the usual fitted intercept in its calculation,
so it is covariance divided by source-count variance. If source-count variance
is exactly zero, set the slope to zero. Do not constrain, transform, tune, or
round the slope.

The **cross-fitted linear-persistence distribution** for case `i` consists of
149 equally weighted support values:

`max(0, y_j + b_{-i,-j} * (x_i - x_j))`.

Thus support case `j` supplies an observed follow-up count, but its follow-up
does not help estimate the slope used to transport that support value to the
held-out source count. The fixed rule generalizes the two inherited
comparators: slope zero corresponds to the **raw follow-up marginal**, whose
support is `y_j`; slope one corresponds to **additive persistence**, whose
support is `max(0, y_j + x_i - x_j)`. The inherited **source-form
neighborhood** remains a contextual comparator and is not refit.

Use the preceding audit's integer source and observed follow-up counts. Require
150 unique ordered case IDs and finite nonnegative counts. Recalculate raw and
additive supports, CRPS values, medians, and central 80% interval diagnostics;
require the raw, additive, and inherited source-form CRPS values to reproduce
the stored audit case by case within its six-decimal storage precision. Hash-
guard this plan, the corrected preceding plan and implementation, and the
preceding complete audit. Write one complete machine-readable result and one
150-row audit without response text. Do not write any development or test
artifact.

Use the inherited equally weighted empirical CRPS, left-continuous weighted
quantile, and central-interval-score definitions. The left-continuous empirical
median is the point forecast for each distribution.

## Fixed evaluation

The **primary outcome** is follow-up word-count CRPS. The **primary contrast**
is raw-marginal CRPS minus cross-fitted linear-persistence CRPS; positive
values favor the person-conditioned forecast. Report both means and paired
case wins, ties, and losses.

Prespecified secondary diagnostics are:

- additive-persistence CRPS minus linear-persistence CRPS;
- source-form-neighborhood CRPS minus linear-persistence CRPS;
- raw-marginal CRPS minus source-form-neighborhood CRPS, closing the direct
  comparison left descriptive by the preceding plan;
- raw-marginal absolute error minus linear-persistence absolute error;
- raw-marginal central-80% interval score minus linear-persistence interval
  score, alongside each method's coverage and width; and
- the distribution of the 22,350 support-specific fitted slopes, including
  its mean, standard deviation, minimum, quartiles, and maximum.

For every paired effect, use a deterministic 20,000-resample percentile
bootstrap over whole outer cases with seed `20261003`, restarting the seeded
generator for each comparison. Report 95% intervals. The primary
interpretation rests only on the one primary contrast; secondary intervals are
unadjusted dependent diagnostics.

## Interpretation rules

Describe linear source conditioning as improving response-length prediction
beyond the no-source raw distribution only if the primary interval excludes
zero in the positive direction. If the interval spans zero, conclude that this
fixed analysis does not distinguish the methods. If it excludes zero in the
negative direction, describe the raw marginal as better.

A favorable primary result would show only that earlier response length carries
incremental predictive information under this fixed regression-to-the-mean
rule. It would not establish a lexical, semantic, causal, or ipseological
mechanism, correct future signifiers, or justify development evaluation by
itself. The secondary raw-versus-source-form interval is a delayed dependent
comparison, not fresh confirmation. The support values and slopes come from
heavily overlapping folds, the analysis follows known aggregate results, and
the cohort is not a probability sample. Bootstrap intervals describe
sensitivity to this cohort's case composition, not population generalization.
Regardless of the result, do not run this count-only diagnostic on development
data or make a private-test-performance claim in this iteration.
