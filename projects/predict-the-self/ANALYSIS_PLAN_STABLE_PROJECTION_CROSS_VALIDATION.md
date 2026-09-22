# Locked analysis plan: leave-one-out stable-signifier projection

**Locked:** 2026-09-22T09:03:54Z, before generating or scoring any fold
prediction.

## Status and claim boundary

This is a prospective lock for one training-only cross-validation diagnostic,
not a preregistration. The stable-signifier method was developed after the
training data and public development data were available, and both datasets
have informed prior Project work. The analysis therefore cannot provide an
untouched confirmatory estimate. It can test whether the already-frozen method's
small public-development differences from repeat-2024 recur when each of the
150 training trajectories is predicted without its own follow-up in model
fitting.

The analysis will not read the 50 development pairs, generate a development
prediction, alter the method, or create or change a private-test submission.
The stable generator is fixed at SHA-256
`ae1eb8b653cd704fcc411790b39f83109e0f92c9af3bfe4fc347d5fb0e04b8c3`.

## Question

When refit leave-one-out, does the deterministic stable-signifier projection
improve agreement, response form, or predicted continuity over simply
repeating each person's 2024 response?

## Fixed leave-one-out design

For each of the 150 training cases in original file order:

1. Hold out the complete case before model fitting.
2. Fit the unchanged stable-signifier projection on the other 149 cases. Use
   its fixed `10.0` equivalent-observation smoothing prior, document-level
   token retention estimator, response-unit ranking, and ordinary-least-squares
   word-count target without modification.
3. Generate one prediction from only the held-out case's 2024 response. Do not
   use its follow-up text or demographics in prediction.
4. Retain the prediction in a complete audit CSV. The repeat-2024 comparator is
   the held-out source response itself.

Hash-guard the pinned training data, authoritative evaluator, this plan, and
the frozen generator before analysis. Write only training-cross-validation
outputs; do not overwrite any development or test artifact.

## Fixed evaluation

Use the pinned benchmark evaluator's case definitions for:

- normalized exact match;
- normalized edit similarity;
- token Jaccard similarity;
- token-overlap F1;
- ROUGE-L F1;
- character n-gram F1;
- word-count absolute error;
- line-count absolute error; and
- source-similarity absolute error.

For each measure, report the stable and repeat-2024 means. Define paired effects
so positive values always favor stable projection: stable minus repeat-2024 for
agreement, and repeat-2024 error minus stable error for error measures. Report
wins, ties, and losses within cases. Use a deterministic 20,000-resample
percentile bootstrap over whole paired cases with seed `20260922` and report
the 95% interval for each mean effect.

Also report the two descriptive official scorecard quantities needed to
interpret form and change: prediction and reference mean word count, prediction
and observed repeat-2024 rates, and prediction and observed mean source
similarity. Store the complete machine-readable result and the 150 fold
predictions.

## Interpretation rules

For a metric whose paired interval excludes zero in the positive direction,
describe the fixed projection as improving that measure within this
cross-validation. If an interval spans zero, do not claim a stable difference.
If it excludes zero in the negative direction, describe the projection as
worsening that measure. Do not aggregate the metrics into a composite or name
an overall winner.

Compare directions with the public-development analysis as a descriptive
replication check, but do not pool the datasets or call the training folds new
evidence. The 150 trajectories are a selected cohort, and case-bootstrap
intervals characterize sensitivity to its composition rather than population
generalization. Cross-validation prevents each case's own future from entering
its fitted model, but it does not undo method selection after exposure to the
training corpus or repeated development-label inspection. No private-test
performance claim is permitted.
