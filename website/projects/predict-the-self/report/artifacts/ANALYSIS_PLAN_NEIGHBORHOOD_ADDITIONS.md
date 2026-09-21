# Locked analysis plan: regularized neighborhood additions

**Locked:** 2026-09-21T09:02:41Z, before implementing or scoring this new
leave-one-out comparison.

## Status and claim boundary

This is a prospective lock for one training-only diagnostic, not a
preregistration. The 150 training pairs have informed earlier Project work,
including selection of the source representation reused here. Public
development labels have also been inspected repeatedly. This analysis will
not use the 50 development pairs, generate a development prediction, or create
or alter a private-test submission. It tests whether a regularized ensemble of
similar training trajectories ranks held-out additions better than their
marginal frequency within this training cohort.

## Question

Can a person's earlier self-description and recorded demographics improve the
ranking of token types they later add when information is synthesized across
multiple similar trajectories and strongly shrunk toward common Add rates?

This analysis responds to two prior failures. Copying one matched trajectory
introduced approximately the right volume but mostly the wrong novel content.
Selecting the strongest individual source-token association performed worse
than marginal Add frequency. The new method pools 30 neighbors rather than
copying one person or trusting one sparse token pair.

## Fixed leave-one-out design

For each of the 150 training cases in turn:

1. Hold out the complete case before estimating features, counts, neighbors,
   or candidate scores.
2. Tokenize the earlier and follow-up responses with the benchmark evaluator's
   case-folded Unicode word-token rule. Define observed additions as follow-up
   token types absent from the earlier response.
3. Represent each earlier response using the already documented retrieval
   representation: term-frequency/inverse-document-frequency features for its
   text plus field-qualified 2024 age, sex, simplified ethnicity, country of
   birth, country of residence, nationality, language, student status,
   employment status, and fluent languages. Fit inverse-document frequencies
   within the 149-case training fold only.
4. Rank the 149 training cases by cosine similarity to the held-out source,
   descending, with original training order breaking exact ties. Select the
   first 30. This fixed neighborhood is one fifth of the full cohort, rounded
   to an integer, and will not be tuned.
5. Clip cosine similarities below zero. Rescale the 30 neighbor weights to sum
   to 30 so their effective total weight is fixed across held-out cases. If all
   30 weights are zero, use 30 equal unit weights.
6. From the full 149-case fold, count each candidate token's Add events and
   calculate its marginal Add rate. Candidate tokens absent from all fold
   additions are unavailable; candidates already present in the held-out
   source are ineligible.
7. For each eligible candidate, calculate the similarity-weighted Add count
   among the 30 neighbors. Its **regularized-neighborhood score** is

   ```text
   (weighted_neighbor_add_count + 30 * marginal_add_rate)
   / (30 + 30)
   ```

   Thus the neighborhood contributes 30 effective cases and the marginal
   prior contributes another 30. Rank candidates by this score, then fold Add
   count, then Unicode token order. The 30-case prior is fixed before scoring
   and will not be tuned.
8. Rank the same eligible candidates by fold Add count and Unicode token order
   for the marginal comparator.
9. Give both rankings exactly as many guesses as the held-out case's observed
   number of additions. This oracle budget deliberately isolates ranking from
   forecasting novelty volume.

## Fixed evaluation

- Hash-guard the training data and authoritative evaluator at benchmark commit
  `9b6a766712583fec8d3182957260b1123fbfa146`, and hash-guard this plan.
- Report the number of positive-budget cases. Retain any zero-budget case in
  the audit but exclude it from score means and paired resampling.
- Because predicted and observed sets have equal size, precision, recall, and
  F1 are identical within each scored case. Report the shared recovered
  fraction once.
- Compare regularized neighborhood minus marginal recovered fraction. Report
  the mean paired difference, wins/ties/losses, and a deterministic 20,000-
  resample percentile bootstrap over whole scored cases with seed `20260921`.
- Report the retrospective candidate-vocabulary ceiling and the mean overlap
  between the two methods' selected token sets. The ceiling inspects observed
  follow-ups; the overlap describes how much the personalized ranking actually
  changes the guesses.
- Write a complete machine-readable result and a case audit containing
  budgets, reachability, mean selected-neighbor similarity, method hits,
  recovered fractions, paired differences, and top-set overlap.

## Interpretation rules

A positive mean paired difference whose case-bootstrap interval excludes zero
will be described as evidence that this fixed regularized-neighborhood ranking
recovers more training-cohort novel token types than marginal frequency at the
same oracle budget. Otherwise, the analysis will not claim an incremental
person-conditioned advantage.

Regardless of direction, this remains a training-cohort diagnostic. The
oracle budget uses the held-out future; demographics are coarse observed
attributes rather than a theory of the self; lexical tokens include function
words and need not be semantic identity signifiers; and repeated appearances
of the same people do not constitute a population sample. The result is not a
development or private-test score and does not establish that expressed
identity change is or is not predictable.
