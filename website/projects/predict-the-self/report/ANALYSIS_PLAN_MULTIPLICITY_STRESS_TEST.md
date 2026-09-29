# Locked analysis plan: cross-analysis multiplicity stress test

**Locked:** 2026-09-29T09:04:25Z, after the constituent aggregate results
were known but before calculating any cross-analysis resample or simultaneous
interval.

## Status and claim boundary

This is a dependent robustness audit of already-published training-cohort
analyses, not a preregistration, new model evaluation, or correction that can
make earlier analytic choices prospective. It asks how the current directional
claims change when a fixed family of related comparisons is considered
together. It will not read benchmark CSVs, development data, or private test
data; generate a prediction; or alter the frozen submission.

The resampling unit remains one derived leave-one-out case. Because the fitted
folds overlap, resampling stored case scores does not reproduce model fitting.
The resulting intervals describe a simultaneous sensitivity check for the 150
selected training cases and the fixed 16-contrast family. They are not
population-generalization intervals and do not establish formal prospective
familywise error control.

## Fixed contrast family

Use the four existing complete case audits and retain their 150 common case IDs
in canonical order. Include exactly these 16 unique paired contrasts, with the
same effect directions as the constituent analyses:

1. Marginal minus neighborhood absolute error for each of Add count, Delete
   count, follow-up word count, follow-up line count, and source similarity
   (five contrasts from the point forecast).
2. Marginal minus neighborhood CRPS for those same five outcomes (five
   contrasts from the probabilistic forecast).
3. For follow-up word-count CRPS, marginal minus text only, marginal minus
   demographics only, text only minus combined, and demographics only minus
   combined (four contrasts from the source-feature ablation).
4. For follow-up word-count CRPS, marginal minus source form and source form
   minus text only (two contrasts from the source-form ablation).

Positive values favor the method named second in each subtraction. The exact
zero line-count point effect remains in the family. Do not include central-
interval scores, secondary ablation outcomes, oracle-budget Add rankings, the
stable projection's full-text scorecard, development analyses, or duplicated
copies of inherited case contrasts. Those exclusions define a coherent family
of no-oracle revision-volume and response-form forecasts rather than a
post-result selection of intervals that happened to exclude zero.

Hash-guard all four input audits and this plan. Require identical ordered IDs,
150 complete finite rows, exact reproduction of every constituent mean from
the stored paired differences, and algebraic reproduction of the six ablation
differences from their component CRPS columns before accepting a result.

## Fixed simultaneous interval procedure

Use one synchronized deterministic case bootstrap so dependencies among all 16
contrasts are preserved. Draw 20,000 samples of 150 case indices with
replacement using Python's `random.Random(20260929)`. For each sample and each
nonconstant contrast, calculate the bootstrap mean and its sample standard
error. Calculate the absolute studentized deviation from the observed mean.
For that sample, retain the maximum across all nonconstant contrasts.

Define the common two-sided 95% critical value as the nearest-rank 95th
percentile of the 20,000 maxima: sorted position `ceil(0.95 * 20000) - 1`.
For each nonconstant contrast, report the observed mean plus or minus this
critical value times its original sample standard error. Report a constant
contrast as its exact point value with a zero-width interval. Use no stepdown
or contrast-specific adjustment.

Write one complete machine-readable JSON result and one 16-row contrast audit.
The JSON must include input hashes, family definition, resampling parameters,
the common critical value, all contrast means and standard errors, simultaneous
intervals, and direction classifications. The CSV must contain the same
contrast-level result in a flat audit form.

## Interpretation rules

Call a direction **simultaneously stable within this audit** only when its
two-sided simultaneous interval excludes zero. An interval containing zero is
inconclusive, not evidence of equivalence or no effect. The exact line-count
tie is descriptive rather than a stable directional effect.

Compare these classifications with the already-published pointwise interval
pattern, but do not relabel earlier locks as confirmatory and do not calculate
a composite score. If a previously pointwise-stable direction becomes
inconclusive, narrow the Project's wording. If a direction remains stable,
describe it only as robust to this fixed multiplicity stress test within the
selected cohort. Emphasize that dependence across serial analyses, reuse of
method-development data, overlapping folds, and post hoc construction of this
family remain limitations that no resampling calculation removes.
