# Locked analysis plan: source-conditioned additions

**Locked:** 2026-09-20, before implementing or scoring the new leave-one-out
comparison.

## Status and claim boundary

This is a prospective lock for one new training-only diagnostic, not a
preregistration. The 150 training pairs have already informed earlier methods,
and public development labels have been inspected repeatedly. The diagnostic
will not use the 50 development pairs, generate a new development prediction,
or create or alter a private-test submission. It tests ranking information
inside the training cohort rather than estimating performance on new people.

## Question

Do token types in a person's earlier self-description help rank which token
types they later add, beyond the marginal frequency of Add events in other
people's training trajectories?

This is a source-to-Add association test. It is not called a transmutation
model because the method does not predict which source signifier will be
deleted.

## Fixed leave-one-out design

For each of the 150 training cases in turn:

1. Hold out the complete case before estimating any count.
2. Tokenize the earlier and follow-up responses with the benchmark evaluator's
   case-folded Unicode word-token rule. Define the case's observed additions as
   the set of follow-up token types absent from its source.
3. From the other 149 cases, count for every candidate token `b` (a) the number
   of cases that add `b`; (b) the number whose source contains each token `a`;
   and (c) the number whose source contains `a` and whose follow-up adds `b`.
4. Exclude candidate additions already present in the held-out source.
5. Give both rankings exactly as many guesses as the number of observed
   additions in the held-out case. This deliberately uses an oracle budget to
   isolate token ranking from prediction of novelty volume.

The **marginal-addition ranking** orders eligible candidates by training Add
count, descending, then by Unicode token order.

The **source-conditioned ranking** calculates, for every eligible candidate
`b` and every source token `a`,

```text
smoothed_rate(a, b) = (coadd_count(a, b) + 10 * marginal_rate(b))
                      / (source_count(a) + 10)
```

where `marginal_rate(b) = add_count(b) / 149`. The candidate's score is the
largest smoothed rate over tokens in the held-out source. Candidates are
ordered by that score, then marginal Add count, then Unicode token order. The
ten-case prior weight matches the already documented smoothing strength in the
stable-signifier method and will not be tuned.

## Fixed evaluation

- Hash-guard the training data and authoritative evaluator at benchmark commit
  `9b6a766712583fec8d3182957260b1123fbfa146`.
- Report how many held-out cases have a positive observed-addition budget. If
  any budget is zero, retain the case in the audit but exclude it from the
  ranking-score mean and paired bootstrap because there is nothing to rank.
- Because prediction and observed sets have the same size, novel-type
  precision, recall, and F1 are identical within each scored case. Report the
  shared recovered fraction once rather than presenting redundant metrics.
- Compare case scores as source-conditioned minus marginal. Report the mean
  paired difference, wins/ties/losses, and a deterministic 20,000-resample
  percentile bootstrap over whole scored cases using seed `20260920`.
- Report the leave-one-out candidate-vocabulary ceiling: the fraction of each
  held-out case's observed additions that appears anywhere among the other 149
  cases' additions. This is a retrospective availability diagnostic, not an
  achievable prospective score.
- Write a complete machine-readable result and a case-level audit containing
  budgets, reachable counts, method hits, scores, and paired differences.

## Interpretation rules

A positive mean paired difference whose case-bootstrap interval excludes zero
will be described as evidence that this fixed source-conditioned ranking
recovers more training-cohort novel token types than the leave-one-out
marginal ranking at the same oracle budget. Otherwise, the analysis will not
claim an incremental advantage.

Regardless of direction, the result will remain a training-cohort diagnostic.
The oracle budget uses each held-out future, lexical tokens include function
words that need not be semantic identity signifiers, and repeated appearances
of the same people do not provide a population sample. No result will be
described as private-test performance or as proof that identity change is or is
not predictable.
