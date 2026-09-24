# Predict the Self

Aleph Initial Alpha · Virtual CSSERG · September 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/report/) · [Executive Summary](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/)

## Finding

The first Predict the Self study forecasts a later Twenty Statements Test response from an earlier response by the same person. An interpretable stable-signifier projection is frozen for all 81 private-test cases and passes the challenge's official format validator. It does not yet have a private test score.

On 50 public development cases, the projection improves normalized edit similarity (0.298061 versus 0.291966), token Jaccard (0.142768 versus 0.141930), and ROUGE-L F1 (0.227552 versus 0.225683) over repeating the earlier response verbatim. It worsens token-overlap F1 (0.307444 versus 0.312202) and character n-gram F1 (0.292293 versus 0.296534), and exact match remains zero for both. Paired case-bootstrap intervals span zero for all five nonzero agreement differences. The benchmark defines no composite score, so these results do not support an overall-winner claim.

A locked leave-one-out analysis of all 150 training cases repeats this mixed pattern without using each held-out person's follow-up in model fitting. Edit similarity improves by 0.004147 (95% case-bootstrap interval 0.000652 to 0.007753), while token-overlap F1 worsens by 0.003493 (interval −0.007228 to −0.000077); other non-exact agreement intervals span zero. Word-count and source-similarity error fall, but line-count error rises.

The most important result is a failure of continuity modeling. Mean prediction-to-source ROUGE-L is 0.903898, while mean observed follow-up-to-source ROUGE-L is 0.225683. An average 73.1727% of distinct follow-up token types are absent from the same person's earlier response. Even an extraction rule designed to favor enduring language expects much more textual stability than participants display and cannot generate most newly expressed vocabulary.

A locked exploratory retrieval baseline supplies new language by borrowing the complete follow-up of the most similar training participant. It nearly matches the volume of change: 80.1727% of its unique token types are new to the focal source, versus 73.1727% observed. But only 7.0466% of its introduced token types are correct on an average case; novel-token recall is 8.5362% and F1 is 6.7109%. Predicting that language will change is much easier than predicting which new identity signifiers this person will express.

A post hoc control holds the number of novel guesses identical case by case. A training-only marginal prior that simply ranks common token additions reaches 17.6545% precision and 14.2637% F1, versus retrieval's 7.0466% and 6.7109%; it wins 40 of 50 cases. Person matching has not yet beaten lexical base rates.

A locked training-only leave-one-out test asks whether earlier source tokens improve the marginal Add ranking. At an oracle budget equal to each held-out case's observed number of additions, source conditioning recovers 14.5238% of novel types versus 16.0992% for marginal frequency. The −1.5754-point paired difference has a case-bootstrap interval of −2.0829 to −1.0736 points; conditioning wins 19 cases, ties 63, and loses 68.

A second locked test pools Add events from 30 text-and-demographically similar trajectories and shrinks their weighted rates equally toward marginal frequency. It recovers 14.9007% versus 16.0992%; the −1.1984-point difference has an interval of −1.8426 to −0.5693 points. Pooling narrows the earlier deficit but still loses 65 cases, ties 60, and wins 25.

A third locked training-only test removes the oracle addition budget and forecasts revision volume. Against source-calibrated fold medians, the same 30-neighbor representation lowers mean absolute error for Add count (20.126667 versus 21.340000), Delete count (5.336275 versus 5.614935), and follow-up word count (52.940000 versus 56.080000); all three paired intervals exclude zero. It ties on line count, while the source-similarity interval spans zero.

A fourth lock scores the complete predictive distributions. The neighborhood improves word-count CRPS from 40.672695 to 38.156852; the paired reduction is +2.515843 (interval +1.008212 to +4.059792), and its central 80% interval score also improves. CRPS intervals for Add count, Delete count, line count, and source similarity span zero. The strongest probabilistic evidence is therefore about later response length, not revision volume generally.

## Question and benchmark

The larger project asks how predictable human lives are. Its first tractable task is Dr. Jason Jeffrey Jones' Predict Future Selves challenge: predict later personally expressed identity from an earlier self-description. The target is an individual's later expression of identity, not a latent true self or a complete life outcome.

The benchmark contains 281 Prolific participants with approved, complete Twenty Statements Test responses in 2024 and again 424–750 days later (median 433). Its deterministic split supplies 150 training pairs, 50 public development pairs, and 81 test inputs whose follow-ups remain private. The project pinned commit 9b6a766712583fec8d3182957260b1123fbfa146 and recorded SHA-256 hashes for every prediction input and governing evaluation file before generating predictions.

The sample is small and selected. Platform recruitment and longitudinal attrition limit generalization, and agreement with one observed follow-up does not identify the only plausible future self-description.

## Stable-signifier projection

The deterministic method uses the 150 public training pairs and no demographics, external model, or external data. First, it estimates how often each unique source token appears at follow-up, smoothing token-level estimates toward the corpus-wide retention rate with ten equivalent prior observations. Second, it splits each source response at its strongest repeated boundary: lines, sentences, comma phrases, or the entire response. Third, it ranks response units by the mean estimated persistence of their unique content tokens.

Finally, a training-only ordinary least squares regression predicts follow-up word count from source word count. The algorithm retains ranked units while adding one moves output length closer to that target, then restores the units' original order. Every predicted word therefore comes from the participant's earlier response.

Public development data were used to choose between fixed extraction fractions and regression-predicted length, as the challenge permits. The displayed scorecard is consequently a model-selection result rather than an untouched confirmation set.

Before generating any fold prediction, a fourth analysis lock fixed leave-one-out evaluation of the unchanged generator. Each training case is predicted from its 2024 text after refitting on the other 149 cases, then compared with repeat-2024 using 20,000 paired resamples and seed 20260922. This prevents direct use of a case's own future in its fit, but the training corpus had already informed method development; the result is cross-validation, not fresh confirmation.

After predictions were frozen, a post hoc diagnostic resampled the 50 development cases in pairs 20,000 times with fixed seed 20260917. Its percentile intervals describe sensitivity to development-case composition, not generalization to a population. Separate lexical diagnostics measured future vocabulary unavailable in the source and three unattainable oracle extractive ceilings that use the observed future.

## Matched-trajectory retrieval

Before generating a second set of development predictions, the Project locked one deterministic method and analysis plan. Four one-nearest-neighbor rules were compared only by leave-one-out training prediction; text-plus-demographic TF-IDF retrieval had the highest training token-overlap F1 and was selected by that declared criterion. Each development case was matched to the most similar 2024 training case, then assigned that neighbor's public follow-up verbatim. The method generated no test submission.

This is an analysis lock, not a preregistration: development labels had been inspected in prior iterations. The paired comparison is exploratory. It uses 20,000 case-bootstrap resamples with seed 20260918 and reports the complete shared scorecard without a composite.

A separate post hoc diagnostic ranks token types by how often they were added across the 150 training pairs. For each development source, it excludes already-present tokens and selects exactly as many types as retrieval introduced. This volume-matched prior is a token-set control, not a coherent full-text forecast. Its 20,000 paired resamples use seed 20260919.

## Source-conditioned additions

Before scoring a new comparison, the Project locked a leave-one-out training analysis. For each held-out training case, the other 149 estimate marginal Add frequencies and smoothed source-token-to-Add associations. Each candidate receives its strongest source-token conditional rate, shrunk toward its marginal rate with ten prior cases. Both rankings receive the observed held-out addition count, so precision, recall, and F1 coincide. This oracle budget isolates ranking quality and cannot serve as a prospective forecast. The paired bootstrap uses 20,000 resamples and seed 20260920.

## Regularized-neighborhood additions

The second training-only plan was also fixed before implementation and scoring. Within each leave-one-out fold, TF-IDF over source text and field-qualified 2024 demographics selects 30 neighbors. Similarity-weighted Add counts contribute 30 effective cases and are combined with a 30-case marginal prior. The neighborhood size and shrinkage are fixed, not tuned. The marginal comparator receives the same oracle budget, and 20,000 paired resamples use seed 20260921.

## Prospective change-volume forecasting

The third training-only plan was locked before benchmark retrieval in this iteration, implementation, or scoring. It reuses the fixed 30-neighbor representation and equal neighborhood/prior weights but gives neither method future-derived volume. Fold medians forecast Add count, Delete fraction, word-count change, line-count change, and source similarity. The neighborhood uses a regularized weighted median of those same quantities. Source-relative quantities are transformed back using only the held-out 2024 response. Twenty thousand paired case resamples use seed 20260923.

## Probabilistic change-volume forecasting

The fourth training-only plan was locked before reopening benchmark data, implementation, or scoring. For each outcome, the marginal distribution weights all 149 fold observations equally. The neighborhood distribution combines a 30-case fold-wide prior with the same 30 cosine-weighted neighbors. Weighted empirical CRPS is primary (Gneiting & Raftery, 2007); central 80% coverage, width, and interval score are secondary. Twenty thousand paired case resamples use seed 20260924. No representation or weight was tuned.

## Complete result pattern

The projection improves three of six text-agreement measures, worsens two, and ties exact match. Its word-count mean absolute error falls from 56.68 to 41.64 words, a +15.04 error reduction with paired case-bootstrap interval +1.18 to +32.36. Source-similarity error falls from 0.774317 to 0.678215; its +0.096102 reduction has interval +0.066064 to +0.129348. Line-count error rises from 6.80 to 9.76; its −2.96 error reduction has interval −5.54 to −0.42. These mixed directions are why no single headline score summarizes the method.

Training cross-validation reproduces all three error directions: word-count error falls by 8.593333 (interval 2.573333 to 15.266667), source-similarity error falls by 0.070769 (0.054503 to 0.088484), and line-count error worsens by 2.906667 (−4.346833 to −1.480000). Mean predicted source similarity remains 0.929231 versus 0.200017 observed, and 46.7% of fold predictions repeat the source exactly while no follow-up does. Adjusting response length and continuity does not solve future content.

Across cases, 73.1727% of distinct future token types are new relative to the source (case-bootstrap interval 69.7982%–76.5607%), and 65.0621% of future token occurrences are unavailable when source counts are respected (59.2663%–70.6149%). Even oracles that inspect the follow-up reach mean ceilings of only 0.268273 unique-token Jaccard, 0.484206 bag-of-words F1, and 0.374081 source-order subsequence ROUGE-L F1. These are retrospective limits, not achievable prospective results.

Retrieval's mean prediction-to-source similarity is 0.175191, close to the observed 0.225683, and source-similarity MAE falls to 0.136074. But agreement falls sharply: token-overlap F1 is 0.194693, compared with 0.307444 for stable projection and 0.312202 for repeat-2024; retrieval's paired difference from stable projection is −0.112751 (interval −0.170815 to −0.058175). All other non-exact agreement measures are also lower. Retrieval calibrates the amount of novelty while mostly transferring the wrong person's novel content.

With mean novel-token volume fixed at 46.94 types per case, the marginal prior's precision is 0.176545 versus 0.070466 for retrieval (paired difference +0.106079, interval +0.068782 to +0.154891). Recall is 0.172611 versus 0.085362 (difference +0.087249, interval +0.062210 to +0.113649), and F1 is 0.142637 versus 0.067109 (difference +0.075528, interval +0.055927 to +0.094990). The prior wins 40 cases, ties 6, and loses 4 on every measure.

Source conditioning also fails to beat the marginal prior. In 150 leave-one-out training cases, mean recovered fraction is 0.145238 versus 0.160992; the paired difference is −0.015754 (interval −0.020829 to −0.010736). Other folds contain a mean 77.3139% of each held-out case's observed additions, so roughly 22.7% are outside both rankings' candidate vocabulary. This bounded negative result applies to the fixed token-pair rule, not every possible individualized method.

The regularized neighborhood changes about 26.0% of the marginal top-set guesses on an average case but also performs worse: mean recovered fraction is 0.149007 versus 0.160992, a paired difference of −0.011984 (interval −0.018426 to −0.005693). Mean cosine similarity across the 30 selected neighbors is 0.169564. Together, the two training-only tests find no incremental advantage for either sparse token-pair conditioning or pooled surface-level similarity.

The no-oracle volume result is more favorable. Add-count MAE falls by 1.213333 (interval 0.680000 to 1.740000), Delete-count MAE by 0.278660 (0.022274 to 0.545876), and word-count MAE by 3.140000 (1.093333 to 5.213333). Line-count forecasts are identical in every case, and the 0.002867 source-similarity error reduction has an interval of −0.000960 to 0.006730. Similarity therefore helps predict some quantities of revision, even while it fails to select the correct new signifiers.

Distributional scoring qualifies that conclusion. Word-count CRPS falls by 2.515843, with an interval excluding zero. Its neighborhood 80% interval covers 84.7% of cases versus 80.7% for the marginal distribution; mean width rises from 149.960000 to 154.526667 words, but interval score improves by 19.700000 (interval 3.873167 to 37.193333). Add- and Delete-count point forecasts improve, yet their CRPS reductions of 0.212518 and 0.072801 have intervals spanning zero. Line-count intervals substantially over-cover against their 80% target. Predictive uncertainty does not identify future content.

The submission contains one nonblank prediction for every required test ID in order. Its SHA-256 is a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3. Only the organizer can run the private evaluator. Validation establishes artifact shape, not predictive performance.

## Interpretation and limits

Token recurrence is not equivalent to identity-signifier endurance. Common wording may recur without representing a stable identity, while genuinely new identities, experiences, and reframings are impossible for an extractive method to produce. Retrieval introduces novelty without establishing that another participant's future—demographically similar or otherwise—is factual or plausible for the focal person. The marginal control further shows that retrieval's few correct novel tokens are not evidence of person-specific advantage over common additions. The conditioned rankings share an oracle future-token budget, and coarse demographic or lexical similarity is not an ipseological mechanism. Their units include function words, so all are diagnostics rather than independent predictions. The probabilistic analysis reuses the same folds, outcomes, representation, and fixed weights; empirical interval coverage is descriptive, not a population guarantee. Cross-validation folds overlap and reuse method-development data; repeated tuning on 50 development cases would further risk overfitting. Neither analysis lock nor bootstrap can make previously inspected data unseen or repair the cohort's nonprobability sampling.

The next research step is to submit the frozen CSV and method card and publish the organizer's complete private scorecard unchanged. Further fixed lexical re-rankers on the same 150 cases are unlikely to be informative without a substantively new representation. Before reusing development labels, a later method should synthesize rather than copy new signifiers, preserve the modest volume-calibration signal, and beat leave-one-out marginal additions in training. Any development comparison should then be locked and avoid private test feedback for tuning.

## Reproducibility and references

The public repository contains both deterministic standard-library generators, six analysis locks, hash-guarded diagnostic scripts, complete development and training audits, machine-readable scorecards, all 150 stable-projection fold predictions, the frozen 81-case test artifact, its method card, and benchmark provenance. The Full Report links each artifact directly.

Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. <i>Journal of the American Statistical Association, 102</i>(477), 359–378. [https://doi.org/10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437)

Jones, J. J. (2023). <i>Ipseology—A new science of the self.</i> https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2024). <i>Predicting the self with generative AI</i> [Preprint]. SocArXiv. [https://doi.org/10.31235/osf.io/eh9sk](https://doi.org/10.31235/osf.io/eh9sk)

Jones, J. J. (2026). <i>Building the ipseome: Large, free, open, human identity data</i> [Preprint]. arXiv. https://arxiv.org/html/2607.02488

Jones, J. J. (2026). <i>You can predict future selves with AI (or without AI)</i> [Data set and benchmark]. GitHub. https://github.com/jasonjeffreyjones/predict-future-selves
