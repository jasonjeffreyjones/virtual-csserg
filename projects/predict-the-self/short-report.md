# Predict the Self

Aleph Initial Alpha · Virtual CSSERG · September 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/report/) · [Executive Summary](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/)

## Finding

The first Predict the Self study forecasts a later Twenty Statements Test response from an earlier response by the same person. An interpretable stable-signifier projection is frozen for all 81 private-test cases and passes the challenge's official format validator. It does not yet have a private test score.

On 50 public development cases, the projection improves normalized edit similarity (0.298061 versus 0.291966), token Jaccard (0.142768 versus 0.141930), and ROUGE-L F1 (0.227552 versus 0.225683) over repeating the earlier response verbatim. It worsens token-overlap F1 (0.307444 versus 0.312202) and character n-gram F1 (0.292293 versus 0.296534), and exact match remains zero for both. Paired case-bootstrap intervals span zero for all five nonzero agreement differences. The benchmark defines no composite score, so these results do not support an overall-winner claim.

The most important result is a failure of continuity modeling. Mean prediction-to-source ROUGE-L is 0.903898, while mean observed follow-up-to-source ROUGE-L is 0.225683. An average 73.1727% of distinct follow-up token types are absent from the same person's earlier response. Even an extraction rule designed to favor enduring language expects much more textual stability than participants display and cannot generate most newly expressed vocabulary.

A locked exploratory retrieval baseline supplies new language by borrowing the complete follow-up of the most similar training participant. It nearly matches the volume of change: 80.1727% of its unique token types are new to the focal source, versus 73.1727% observed. But only 7.0466% of its introduced token types are correct on an average case; novel-token recall is 8.5362% and F1 is 6.7109%. Predicting that language will change is much easier than predicting which new identity signifiers this person will express.

A post hoc control holds the number of novel guesses identical case by case. A training-only marginal prior that simply ranks common token additions reaches 17.6545% precision and 14.2637% F1, versus retrieval's 7.0466% and 6.7109%; it wins 40 of 50 cases. Person matching has not yet beaten lexical base rates.

A locked training-only leave-one-out test asks whether earlier source tokens improve the marginal Add ranking. At an oracle budget equal to each held-out case's observed number of additions, source conditioning recovers 14.5238% of novel types versus 16.0992% for marginal frequency. The −1.5754-point paired difference has a case-bootstrap interval of −2.0829 to −1.0736 points; conditioning wins 19 cases, ties 63, and loses 68.

## Question and benchmark

The larger project asks how predictable human lives are. Its first tractable task is Dr. Jason Jeffrey Jones' Predict Future Selves challenge: predict later personally expressed identity from an earlier self-description. The target is an individual's later expression of identity, not a latent true self or a complete life outcome.

The benchmark contains 281 Prolific participants with approved, complete Twenty Statements Test responses in 2024 and again 424–750 days later (median 433). Its deterministic split supplies 150 training pairs, 50 public development pairs, and 81 test inputs whose follow-ups remain private. The project pinned commit 9b6a766712583fec8d3182957260b1123fbfa146 and recorded SHA-256 hashes for every prediction input and governing evaluation file before generating predictions.

The sample is small and selected. Platform recruitment and longitudinal attrition limit generalization, and agreement with one observed follow-up does not identify the only plausible future self-description.

## Stable-signifier projection

The deterministic method uses the 150 public training pairs and no demographics, external model, or external data. First, it estimates how often each unique source token appears at follow-up, smoothing token-level estimates toward the corpus-wide retention rate with ten equivalent prior observations. Second, it splits each source response at its strongest repeated boundary: lines, sentences, comma phrases, or the entire response. Third, it ranks response units by the mean estimated persistence of their unique content tokens.

Finally, a training-only ordinary least squares regression predicts follow-up word count from source word count. The algorithm retains ranked units while adding one moves output length closer to that target, then restores the units' original order. Every predicted word therefore comes from the participant's earlier response.

Public development data were used to choose between fixed extraction fractions and regression-predicted length, as the challenge permits. The displayed scorecard is consequently a model-selection result rather than an untouched confirmation set.

After predictions were frozen, a post hoc diagnostic resampled the 50 development cases in pairs 20,000 times with fixed seed 20260917. Its percentile intervals describe sensitivity to development-case composition, not generalization to a population. Separate lexical diagnostics measured future vocabulary unavailable in the source and three unattainable oracle extractive ceilings that use the observed future.

## Matched-trajectory retrieval

Before generating a second set of development predictions, the Project locked one deterministic method and analysis plan. Four one-nearest-neighbor rules were compared only by leave-one-out training prediction; text-plus-demographic TF-IDF retrieval had the highest training token-overlap F1 and was selected by that declared criterion. Each development case was matched to the most similar 2024 training case, then assigned that neighbor's public follow-up verbatim. The method generated no test submission.

This is an analysis lock, not a preregistration: development labels had been inspected in prior iterations. The paired comparison is exploratory. It uses 20,000 case-bootstrap resamples with seed 20260918 and reports the complete shared scorecard without a composite.

A separate post hoc diagnostic ranks token types by how often they were added across the 150 training pairs. For each development source, it excludes already-present tokens and selects exactly as many types as retrieval introduced. This volume-matched prior is a token-set control, not a coherent full-text forecast. Its 20,000 paired resamples use seed 20260919.

## Source-conditioned additions

Before scoring a new comparison, the Project locked a leave-one-out training analysis. For each held-out training case, the other 149 estimate marginal Add frequencies and smoothed source-token-to-Add associations. Each candidate receives its strongest source-token conditional rate, shrunk toward its marginal rate with ten prior cases. Both rankings receive the observed held-out addition count, so precision, recall, and F1 coincide. This oracle budget isolates ranking quality and cannot serve as a prospective forecast. The paired bootstrap uses 20,000 resamples and seed 20260920.

## Complete result pattern

The projection improves three of six text-agreement measures, worsens two, and ties exact match. Its word-count mean absolute error falls from 56.68 to 41.64 words, a +15.04 error reduction with paired case-bootstrap interval +1.18 to +32.36. Source-similarity error falls from 0.774317 to 0.678215; its +0.096102 reduction has interval +0.066064 to +0.129348. Line-count error rises from 6.80 to 9.76; its −2.96 error reduction has interval −5.54 to −0.42. These mixed directions are why no single headline score summarizes the method.

Across cases, 73.1727% of distinct future token types are new relative to the source (case-bootstrap interval 69.7982%–76.5607%), and 65.0621% of future token occurrences are unavailable when source counts are respected (59.2663%–70.6149%). Even oracles that inspect the follow-up reach mean ceilings of only 0.268273 unique-token Jaccard, 0.484206 bag-of-words F1, and 0.374081 source-order subsequence ROUGE-L F1. These are retrospective limits, not achievable prospective results.

Retrieval's mean prediction-to-source similarity is 0.175191, close to the observed 0.225683, and source-similarity MAE falls to 0.136074. But agreement falls sharply: token-overlap F1 is 0.194693, compared with 0.307444 for stable projection and 0.312202 for repeat-2024; retrieval's paired difference from stable projection is −0.112751 (interval −0.170815 to −0.058175). All other non-exact agreement measures are also lower. Retrieval calibrates the amount of novelty while mostly transferring the wrong person's novel content.

With mean novel-token volume fixed at 46.94 types per case, the marginal prior's precision is 0.176545 versus 0.070466 for retrieval (paired difference +0.106079, interval +0.068782 to +0.154891). Recall is 0.172611 versus 0.085362 (difference +0.087249, interval +0.062210 to +0.113649), and F1 is 0.142637 versus 0.067109 (difference +0.075528, interval +0.055927 to +0.094990). The prior wins 40 cases, ties 6, and loses 4 on every measure.

Source conditioning also fails to beat the marginal prior. In 150 leave-one-out training cases, mean recovered fraction is 0.145238 versus 0.160992; the paired difference is −0.015754 (interval −0.020829 to −0.010736). Other folds contain a mean 77.3139% of each held-out case's observed additions, so roughly 22.7% are outside both rankings' candidate vocabulary. This bounded negative result applies to the fixed token-pair rule, not every possible individualized method.

The submission contains one nonblank prediction for every required test ID in order. Its SHA-256 is a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3. Only the organizer can run the private evaluator. Validation establishes artifact shape, not predictive performance.

## Interpretation and limits

Token recurrence is not equivalent to identity-signifier endurance. Common wording may recur without representing a stable identity, while genuinely new identities, experiences, and reframings are impossible for an extractive method to produce. Retrieval introduces novelty without establishing that another participant's future—demographically similar or otherwise—is factual or plausible for the focal person. The marginal control further shows that retrieval's few correct novel tokens are not evidence of person-specific advantage over common additions. Its lexical units include function words, and its borrowed case-level token budget makes it a diagnostic rather than an independent prediction method. Repeated tuning on 50 development cases would risk overfitting, and neither analysis lock nor bootstrap can make previously inspected data unseen or repair the cohort's nonprobability sampling.

The next research step is to submit the frozen CSV and method card and publish the organizer's complete private scorecard unchanged. Before reusing development labels, a later method should synthesize rather than copy new signifiers and beat leave-one-out marginal additions in training. Any development comparison should then be locked and avoid private test feedback for tuning.

## Reproducibility and references

The public repository contains both deterministic standard-library generators, the retrieval analysis lock and audit, hash-guarded diagnostic scripts, both sets of 50 development predictions, the marginal-prior token audit, complete machine-readable scorecards and diagnostics, the frozen 81-case stable-projection test artifact, its method card, and benchmark provenance. The Full Report links each artifact directly.

Jones, J. J. (2023). <i>Ipseology—A new science of the self.</i> https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2024). <i>Predicting the self with generative AI</i> [Preprint]. SocArXiv. [https://doi.org/10.31235/osf.io/eh9sk](https://doi.org/10.31235/osf.io/eh9sk)

Jones, J. J. (2026). <i>Building the ipseome: Large, free, open, human identity data</i> [Preprint]. arXiv. https://arxiv.org/html/2607.02488

Jones, J. J. (2026). <i>You can predict future selves with AI (or without AI)</i> [Data set and benchmark]. GitHub. https://github.com/jasonjeffreyjones/predict-future-selves
