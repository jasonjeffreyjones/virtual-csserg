# Locked analysis plan: matched-trajectory retrieval

**Locked:** 2026-09-18, before generating or scoring the trajectory-retrieval
development predictions in this iteration.

## Status and claim boundary

This is a prospective lock for one new analysis, not a preregistration. The
development responses and aggregate results for stable-signifier projection
were already examined in earlier iterations. The new result will therefore be
reported as exploratory model-comparison evidence. The private test responses
remain unavailable and the frozen 81-case stable-signifier submission will not
be changed or supplemented.

## Question

Can a transparent matched-trajectory method reproduce the observed amount of
lexical change without losing agreement on *which* signifiers appear? The
analysis distinguishes forecasting the quantity of novelty from forecasting
its person-specific content.

## Training-only model choice

Four deterministic one-nearest-neighbor variants were compared by
leave-one-out prediction of the 150 training follow-ups. The candidates crossed
set-Jaccard versus TF-IDF cosine matching with text-only versus text plus all
nonblank 2024 demographic fields. Training token-overlap F1 was fixed as the
selection criterion because the analysis concerns recovery of later lexical
content. The complete development scorecard will still be reported, and the
benchmark's no-composite/no-winner policy remains in force.

| Matching rule | Training token Jaccard | Training token-overlap F1 |
| --- | ---: | ---: |
| Set Jaccard, text | 0.0682 | 0.1797 |
| TF-IDF cosine, text | 0.0729 | 0.1819 |
| Set Jaccard, text + demographics | 0.0728 | 0.1848 |
| TF-IDF cosine, text + demographics | **0.0737** | **0.1925** |

The locked method is therefore TF-IDF cosine over 2024 response tokens and
field-qualified 2024 demographic values.

## Locked method

1. Tokenize each training and query response with the benchmark evaluator's
   case-folded Unicode word-token rule.
2. Add one field-qualified categorical feature for every nonblank 2024
   demographic field. Values are case-folded and internal whitespace is
   collapsed. A value in one field can never equal the same text in another.
3. Estimate smoothed inverse document frequency on the 150 training inputs as
   `log((N + 1) / (df + 1)) + 1`. Weight within-document counts as
   `1 + log(tf)` and L2-normalize the sparse vectors.
4. Select the training source with greatest cosine similarity to the query.
   Resolve exact ties by the training-file order.
5. Use that neighbor's observed follow-up verbatim as the query prediction.

This is non-extractive with respect to the focal person's earlier response but
is retrieval rather than synthesis: it transfers another public training
trajectory. The prediction artifact is consequently an adaptation of the
CC BY-NC-SA 4.0 benchmark data. It will be published only as an auditable
research baseline, not as a factual characterization of any participant.

## Locked evaluation

- Generate predictions only for the 50 public development cases. Do not
  generate or submit trajectory-retrieval predictions for private test cases.
- Hash-guard the pinned training data, development data, and authoritative
  evaluator at benchmark commit
  `9b6a766712583fec8d3182957260b1123fbfa146`.
- Report all 15 official scorecard fields for trajectory retrieval, stable-
  signifier projection, and repeat-2024. Do not calculate a composite or call
  any method an overall winner.
- For the nine directional metrics, report paired case-bootstrap differences
  between retrieval and each comparator using 20,000 percentile resamples of
  whole cases and seed `20260918`. These intervals describe development-case
  composition, not population-generalization uncertainty.
- Report predicted-to-source unique-token novelty and occurrence novelty, with
  the same statistics for observed follow-ups. Also report precision, recall,
  and F1 for retrieved novel token types relative to the observed novel token
  types. These token diagnostics are descriptive and post-method-lock.
- Interpret the method as successful on novelty calibration only if its mean
  predicted unique-token novelty is closer to the observed mean than both
  comparators. Interpret novel-content recovery from the full precision,
  recall, and F1 pattern rather than a threshold.

## Known limitations

Development evidence is exploratory because its labels were previously seen.
The train-only selection criterion privileges one lexical measure, the cohort
is small and selected, demographic matching can encode social categories
without establishing causal relevance, and copying a neighbor's one observed
future is not a claim that the future is uniquely plausible. Reference-based
agreement remains agreement with one realized self-description, not a complete
measure of forecast quality.
