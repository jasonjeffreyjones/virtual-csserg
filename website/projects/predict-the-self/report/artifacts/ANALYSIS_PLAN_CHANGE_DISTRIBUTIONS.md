# Locked analysis plan: probabilistic change-volume forecasting

**Locked:** 2026-09-24T09:02:34Z, before reopening the pinned benchmark data
in this iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration. The training corpus, aggregate revision patterns,
text-and-demographic representation, neighborhood size, and equal
neighborhood/prior weighting all informed earlier Project work. The analysis
can test a new, bounded question: whether that unchanged representation
improves full predictive distributions for *how much* a held-out
self-description changes. It cannot supply untouched confirmation or
population evidence.

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter any
existing prediction method, or create or change a private-test submission.

## Question

Do 2024 source text and demographics improve leave-one-out probabilistic
forecasts of later response form and Add/Delete event volume over
source-calibrated marginal predictive distributions?

## Fixed outcomes and source calibration

Reuse without modification the five outcomes and transformations fixed in
`ANALYSIS_PLAN_CHANGE_VOLUME.md`:

1. distinct Add-event count, modeled directly;
2. distinct Delete-event count, modeled as a fraction of distinct source
   tokens;
3. follow-up word count, modeled as change from source word count;
4. follow-up nonempty-line count, modeled as change from source line count;
   and
5. follow-up-to-source ROUGE-L F1 similarity, modeled directly.

Transform every support point back to the held-out outcome scale using only
the held-out 2024 response. Apply the existing bounds: Delete count within the
source distinct-token count, word count at least zero, line count at least one,
and similarity in `[0, 1]`.

## Fixed leave-one-out predictive distributions

For each case in original training-file order, hold out its complete row before
estimating outcomes. Construct two empirical predictive distributions from the
other 149 rows:

- **Source-calibrated marginal:** give every fold observation equal weight.
- **Regularized neighborhood:** use the existing field-qualified 2024
  text-and-demographic TF-IDF representation; select 30 neighbors by cosine
  similarity with original fold order breaking ties; clip similarities at
  zero and normalize them to 30 effective cases; and combine them with a
  30-case prior distributed uniformly over all 149 fold observations.

Normalize each distribution's weights to sum to one after transformation. The
neighborhood size, feature implementation, and equal neighbor/prior effective
weights are inherited unchanged from the two previous locked analyses and
will not be tuned.

Hash-guard the pinned training data, authoritative evaluator, existing
trajectory-retrieval feature implementation, existing change-volume
implementation, and this plan. Write a complete machine-readable result and
one 150-row case audit. Do not write any development or test prediction.

## Fixed evaluation

For every outcome and predictive distribution, calculate the continuous ranked
probability score (CRPS) for the weighted empirical distribution:

`sum_i w_i |x_i - y| - 0.5 sum_i sum_j w_i w_j |x_i - x_j|`.

Lower CRPS is better. The primary paired effect is case-level marginal CRPS
minus neighborhood CRPS, so positive values favor person-conditioned
neighborhoods. Report both mean CRPS values, the mean paired effect, and wins,
ties, and losses within cases.

As secondary calibration and sharpness diagnostics, use the left-continuous
inverse empirical CDF to form each distribution's central 80% interval (10th
to 90th weighted quantiles). Report inclusive empirical coverage, mean width,
and mean interval score at alpha `0.20`. The paired interval-score effect is
marginal score minus neighborhood score, again positive when the neighborhood
is better. Do not treat narrower intervals as better unless calibration and
interval score support that interpretation.

For both paired score effects, use a deterministic 20,000-resample percentile
bootstrap over whole paired cases with seed `20260924`, restarting the seeded
generator for each outcome and score. Report 95% intervals. There is no
composite score and no outcome weighting.

## Interpretation rules

If an outcome's paired CRPS interval excludes zero in the positive direction,
describe the regularized neighborhood as improving probabilistic forecasts of
that outcome within this cross-validation. If it spans zero, do not claim a
stable improvement. If it excludes zero in the negative direction, describe
the neighborhood as worsening CRPS. Treat interval-score results as secondary
and do not infer an overall winner from the five outcomes.

Any advantage concerns revision *volume or form*, not correct future content.
A null or negative result applies to this fixed surface-text and
coarse-demographic neighborhood, not to all person-conditioned forecasting.
The folds overlap heavily, the representation and hyperparameters predate this
lock, and the selected cohort is not a probability sample. Bootstrap intervals
therefore describe sensitivity to training-case composition, not population
generalization. No private-test performance claim is permitted.
