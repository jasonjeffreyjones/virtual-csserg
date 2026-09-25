# Locked analysis plan: source-feature ablation

**Locked:** 2026-09-25T09:03:05Z, before reopening the pinned benchmark data
in this iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration. The training corpus, the aggregate superiority of the
combined neighborhood for word-count CRPS, the source representation, and all
neighborhood hyperparameters informed earlier Project work. The analysis can
decompose the already-observed signal between earlier self-description text
and 2024 demographics. It cannot provide untouched confirmation, support
population generalization, or establish that demographic categories are
ipseological mechanisms.

The analysis will use only the 150 public training trajectories. It will not
read the 50 development pairs, generate a development prediction, alter an
existing prediction method, or create or change a private-test submission.

## Question

Does the previously observed improvement in leave-one-out probabilistic
word-count forecasts depend on earlier self-description text, 2024
demographics, or their combination?

## Fixed representations and distributions

Use the existing field-qualified TF-IDF implementation and split its unchanged
features into three representations:

1. **Text only:** case-folded word-token counts from `tst_2024`.
2. **Demographics only:** the ten existing field-qualified, normalized 2024
   demographic values, excluding `tst_2024` tokens.
3. **Combined:** the exact existing union of text and demographic features.

Missing demographic values contribute no feature. Do not add, remove, weight,
or otherwise transform fields. Fit IDF separately within each representation
and each 149-case fold. For a zero-norm query or a fold in which all selected
similarities are zero, retain the existing deterministic behavior: cosine
similarities are zero and the 30-neighbor effective weight is divided equally
over the first 30 fold cases selected by original order.

For each held-out case and representation, use the unchanged 30-neighbor
selection, similarity weighting, 30-case neighborhood effective weight, and
30-case uniform fold prior. Reuse without modification the five outcomes,
source transformations, inverse transformations, empirical-distribution CRPS,
and bounds in `ANALYSIS_PLAN_CHANGE_DISTRIBUTIONS.md`. The source-calibrated
marginal distribution remains the same common comparator. No held-out future
may enter a representation, neighbor selection, weight, or predictive
distribution.

Hash-guard the pinned training data, authoritative evaluator, existing
trajectory-retrieval feature implementation, change-volume implementation,
probabilistic-distribution implementation, and this plan. Write one complete
machine-readable result and one 150-row case audit. Do not write a development
or test prediction.

## Fixed evaluation

The **primary outcome** is follow-up word-count CRPS because it was the only
outcome whose combined-neighborhood CRPS interval excluded zero in the prior
locked distributional analysis. For word count, report mean CRPS for the
marginal, text-only, demographics-only, and combined distributions, plus these
four paired case-level effects:

1. marginal minus text-only CRPS;
2. marginal minus demographics-only CRPS;
3. text-only minus combined CRPS; and
4. demographics-only minus combined CRPS.

Positive values favor the method named second. These comparisons separately
test whether either ablation beats the simple comparator and whether adding the
omitted feature family improves the combined model. Report case wins, ties,
and losses for every comparison.

As prespecified secondary diagnostics, report the same means and four paired
effects for Add count, Delete count, line count, and source similarity. These
secondary outcomes cannot overturn the primary word-count conclusion, and
there is no composite or outcome weighting. Require the newly calculated
combined and marginal case-level CRPS values to reproduce the existing locked
audit to numerical tolerance before reporting any ablation result.

For every paired effect, use a deterministic 20,000-resample percentile
bootstrap over whole paired cases with seed `20260925`, restarting the seeded
generator for every outcome and comparison. Report 95% intervals. These are
descriptive repeated-analysis intervals; no multiplicity-adjusted familywise
claim is planned.

## Interpretation rules

For the primary word-count outcome, describe an ablated representation as
improving over the marginal only if its paired interval excludes zero in the
positive direction. Describe an omitted feature family as adding incremental
value only if the corresponding ablated-minus-combined interval excludes zero
in the positive direction. If an interval spans zero, do not claim a stable
advantage for that contrast. If it excludes zero in the negative direction,
describe the second method as worsening CRPS.

Interpret secondary outcomes as diagnostics and name their repeated-analysis
status. Any result concerns response form or revision volume—not correct future
lexical content. The folds overlap heavily, the cohort is not a probability
sample, and exact demographic categories can be sparse. Bootstrap intervals
therefore describe sensitivity to this selected training cohort's case
composition, not population generalization. No private-test performance claim
is permitted.
