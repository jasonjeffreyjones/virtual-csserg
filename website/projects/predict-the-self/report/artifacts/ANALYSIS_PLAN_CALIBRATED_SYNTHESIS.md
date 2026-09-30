# Locked analysis plan: calibrated full-text synthesis

**Locked:** 2026-09-30T09:08:29Z, before reading benchmark rows in this
iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration or untouched confirmation. The training corpus, frozen
stable-signifier projection, source-form response-length result, combined
neighborhood Add-count result, and marginal-addition result all informed the
design. The new question is whether those separately observed signals can be
assembled into a coherent full-text forecast without using a held-out future.

Use only the 150 public training trajectories. Do not read the development
pairs, generate a development prediction, alter an existing prediction, or
create or change a private-test submission.

## Question

Can one fixed synthesis rule combine a person's stable earlier response units,
a prospective response-length forecast, a prospective Add-volume forecast,
and common follow-up response units to improve full-text prediction while
recovering more person-specific novel token types than a volume-matched
marginal-addition ranking?

## Fixed outer leave-one-out design

For each case in original training-file order, remove its complete row before
all fitting, candidate construction, and scoring. The held-out predictor may
use its 2024 response and 2024 demographics but no held-out follow-up field.
Fit all components independently within each 149-case fold:

1. **Stable source units.** Reuse the frozen response-unit splitter,
   document-level token-retention estimates with prior strength 10, stop-token
   list, and unit score. Rank the held-out source units by decreasing retention
   score with original position breaking ties; any chosen source units return
   to their original order.
2. **Follow-up word-count target.** Reuse the fixed three-count source-form
   distance (log source word-token, distinct-token, and line counts), 30
   neighbors, 30-case neighborhood weight, and 30-case fold prior. Take the
   weighted median of fold follow-up-minus-source word counts, transform it
   with the held-out source word count, round to the nearest integer, and bound
   the result below at one.
3. **distinct-Add target.** Reuse the fixed combined surface-text and
   2024-demographic TF-IDF representation, 30 neighbors, 30-case neighborhood
   weight, and 30-case fold prior. Take the weighted median fold distinct-Add
   count, round to the nearest integer, and bound it below at zero.
4. **Common novel response units.** Split every fold source and follow-up with
   the frozen response-unit splitter and normalize units by case-folding and
   collapsing whitespace. A follow-up unit is novel for a fold case when its
   normalized form is absent from that case's source units. Count each
   normalized unit at most once per case, retain only units novel in at least
   two fold cases, represent each by its first observed surface form, and rank
   by decreasing case count then normalized text. Remove candidates already
   present in the held-out source.

Construct candidates from every nonempty prefix of the ranked stable source
units and every prefix, including empty, of the ranked common novel units.
Remove duplicate normalized units. For each candidate response, count words
and distinct token types absent from the held-out source. Minimize:

`|words - target_words| / target_words + |novel_types - target_adds| / max(1, target_adds)`.

Break exact ties by smaller absolute word-count error, smaller absolute
Add-count error, more retained source units, fewer appended units, then the
two prefix lengths. Emit retained source units in source order followed by
appended units in ranking order. This fixed search makes a nonblank prediction
and does not inspect the held-out future.

## Fixed comparators and scoring

Generate the unchanged frozen stable-signifier prediction within the same
outer fold. The full-text comparators are that prediction and repeat-2024.
Use every official evaluator metric and report paired case-bootstrap intervals
for calibrated synthesis versus each comparator. Preserve the official rule
that there is no composite score, metric weighting, ranking, or overall
winner.

For a separate content diagnostic, define observed and predicted distinct-Add
sets relative to the held-out source. Give a fold-wide marginal Add-token
ranking exactly the calibrated synthesis prediction's number of distinct novel
types for that case. Candidates exclude held-out source tokens and use
decreasing fold case frequency, then lexical order. Compare macro case-level
precision, recall, and F1. The synthesis and marginal sets have equal size;
zero-size pairs receive precision, recall, and F1 of zero. This is a
volume-matched ranking comparison, not a standalone marginal full-text
forecast.

Use 20,000 paired whole-case percentile-bootstrap resamples with seed
`20260930`, restarting the seeded generator for every contrast. Report 95%
intervals, wins, ties, and losses. The three prespecified gate effects are:

1. calibrated-synthesis minus repeat-2024 normalized edit similarity;
2. repeat-2024 word-count error minus calibrated-synthesis word-count error;
3. calibrated-synthesis minus volume-matched marginal novel-type F1.

Do not advance this method to development data unless all three mean effects
are positive and all three pointwise intervals exclude zero in the positive
direction. This conservative gate is a design decision, not multiplicity-
adjusted inference.

## Artifacts and interpretation

Hash-guard the pinned training data, evaluator, this plan, and every inherited
implementation used. Write a complete JSON result, one row per held-out case,
and all fold predictions. Do not publish raw source or observed follow-up text
in the audit.

An agreement improvement would concern this selected training cohort, not
population generalization. Common response units and token metrics include
function words and generic statements that need not be identity signifiers.
Transferred fold text is a benchmark-data adaptation under CC BY-NC-SA 4.0.
Overlapping leave-one-out fits and post-selection of this design after earlier
results preclude untouched confirmation. Failure of the fixed rule does not
show that all synthesis or semantic models fail; success does not establish
that the correct future identity content has been recovered.
