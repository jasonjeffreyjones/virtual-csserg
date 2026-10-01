# Locked analysis plan: semantic neighborhood additions

**Locked:** 2026-10-01T09:04:21Z, before reading benchmark rows in this
iteration and before implementing or scoring this analysis.

## Status and claim boundary

This is a prospective lock for one training-only leave-one-out diagnostic, not
a preregistration or untouched confirmation. The 150 training trajectories and
earlier aggregate findings have informed Project development. The source
representation is new to the Project, but the 30-neighbor regularization rule,
oracle content budget, marginal comparator, and evaluation procedure are
inherited from the earlier neighborhood-addition analysis.

Use only the 150 public training trajectories. Do not read development rows,
generate a development prediction, alter an existing prediction, or create or
change a private-test submission.

## Question

Can external distributional semantics identify source-similar trajectories
whose later Add events recover more of a held-out person's novel token types
than fold-wide Add frequency at the same retrospective volume?

## Fixed external representation

Use the 25-dimensional uncased GloVe Twitter vectors distributed as
`glove-twitter-25.gz` by the Gensim-data project. The artifact is a word2vec-
format conversion of Stanford's GloVe vectors trained on 2 billion tweets (27
billion tokens). It contains 1,193,514 vectors, is distributed under the Open
Data Commons Public Domain Dedication and License 1.0, and is pinned here:

```text
URL: https://github.com/RaRe-Technologies/gensim-data/releases/download/glove-twitter-25/glove-twitter-25.gz
SHA-256: 63877d71151688baf6f31d5437374f637f737a5e100e12150a5bd61a9f273c3f
header: 1193514 25
```

Read the gzip stream with the Python standard library. Require the exact hash,
header, dimensionality, finite numeric coordinates, and a unique row for every
retained token. Retain vectors only for the union of evaluator-tokenized source
tokens; this vocabulary filter may inspect all 150 source responses because it
does not estimate a feature or use any follow-up. Do not retain, publish, or
commit the external vector artifact.

For each fold, fit document frequency on the 149 source responses. Represent a
response by the weighted centroid of the distinct in-vocabulary token types in
that response, with each token weighted once by

`log((149 + 1) / (source_document_frequency + 1)) + 1`.

Do not use term frequency, demographics, follow-up text, or any fitted
projection. Report token-type and case coverage. A response with no usable
vector or a zero-norm centroid receives cosine similarity zero to every fold
case.

## Fixed leave-one-out ranking

For each case in original training-file order:

1. Hold out the complete row before estimating document frequencies, Add
   counts, neighbors, or candidate scores.
2. Tokenize source and follow-up with the pinned evaluator's case-folded
   Unicode word-token rule. Define observed additions as follow-up token types
   absent from source token types.
3. Calculate cosine similarity between the held-out semantic centroid and each
   of the 149 fold source centroids. Rank by decreasing similarity and original
   fold order; select 30 neighbors.
4. Clip similarities below zero and rescale them to 30 effective cases. If all
   selected weights are zero, assign equal weights summing to 30.
5. Count each candidate token's Add events across the full fold. Exclude tokens
   absent from all fold additions and tokens already present in the held-out
   source.
6. For each candidate, combine its similarity-weighted count among the 30
   semantic neighbors with a 30-effective-case marginal prior:

   ```text
   (weighted_neighbor_add_count + 30 * fold_marginal_add_rate) / 60
   ```

   Rank by this score, then fold Add count, then Unicode token order.
7. Recompute the inherited surface-text-plus-demographic TF-IDF neighborhood
   and the fold-marginal ranking exactly. Require their case-level recovered
   fractions to reproduce the pinned earlier audit before accepting the new
   result.
8. Give all three rankings the held-out case's observed number of additions.
   This oracle budget isolates ranking and does not create a prospective
   forecast.

Hash-guard the pinned training data, evaluator, this plan, the inherited
neighborhood implementation, and its stored 150-case audit. Do not read or
write a development or private-test artifact.

## Fixed evaluation

Exclude zero-budget cases from score means and resampling but retain them in
the audit. With equal predicted and observed set sizes, case precision, recall,
and F1 coincide; report the shared recovered fraction.

The primary effect is semantic-neighborhood minus marginal recovered fraction.
The secondary effect is semantic-neighborhood minus inherited surface-TF-IDF
neighborhood recovered fraction. For each, report means, wins/ties/losses, and
a paired whole-case 20,000-resample percentile-bootstrap 95% interval with seed
`20261001`, restarting the seeded generator for each contrast. Also report the
candidate-vocabulary ceiling, source-vector coverage, selected-neighbor cosine
similarity, and top-set overlap with each comparator.

Claim an incremental semantic ranking advantage only if the primary mean is
positive and its interval excludes zero in the positive direction. Otherwise,
do not claim that this fixed semantic representation beats common additions.
Regardless of outcome, do not evaluate it on development data in this
iteration. If the primary hurdle passes, a later locked prospective method
must still forecast novelty volume, preserve response-form calibration,
demonstrate value beyond simple source counts, and pass a full-text training
gate before any development comparison.

## Interpretation limits

GloVe cosine proximity is a distributional representation, not a validated
measure of ipseological identity. An IDF-weighted centroid discards word order,
polysemy, negation, line structure, and out-of-vocabulary signifiers. Twitter-
trained vectors can encode social bias and may mismatch Twenty Statements Test
language. The oracle budget inspects each held-out future, lexical additions
include function words that need not be identity signifiers, folds overlap,
and this selected cohort is not a probability sample. Bootstrap intervals
describe sensitivity to training-case composition, not population
generalization. Success would not establish correct future identity content;
failure would reject only this fixed representation and ranking rule.

## External source

Pennington, J., Socher, R., & Manning, C. (2014). GloVe: Global vectors for
word representation. In *Proceedings of the 2014 Conference on Empirical
Methods in Natural Language Processing (EMNLP)* (pp. 1532–1543). Association
for Computational Linguistics. https://doi.org/10.3115/v1/D14-1162
