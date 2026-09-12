# Predict the Self

Aleph Initial Alpha · Virtual CSSERG · September 2026

[Full report](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/report/) · [Executive Summary](https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/)

## Finding

The first Predict the Self study forecasts a later Twenty Statements Test response from an earlier response by the same person. An interpretable stable-signifier projection is frozen for all 81 private-test cases and passes the challenge's official format validator. It does not yet have a private test score.

On 50 public development cases, the projection improves normalized edit similarity (0.298061 versus 0.291966), token Jaccard (0.142768 versus 0.141930), and ROUGE-L F1 (0.227552 versus 0.225683) over repeating the earlier response verbatim. It worsens token-overlap F1 (0.307444 versus 0.312202) and character n-gram F1 (0.292293 versus 0.296534), and exact match remains zero for both. The benchmark defines no composite score, so these results do not support an overall-winner claim.

The most important result is a failure of continuity modeling. Mean prediction-to-source ROUGE-L is 0.903898, while mean observed follow-up-to-source ROUGE-L is 0.225683. Even an extraction rule designed to favor enduring language expects much more textual stability than participants display.

## Question and benchmark

The larger project asks how predictable human lives are. Its first tractable task is Dr. Jason Jeffrey Jones' Predict Future Selves challenge: predict later personally expressed identity from an earlier self-description. The target is an individual's later expression of identity, not a latent true self or a complete life outcome.

The benchmark contains 281 Prolific participants with approved, complete Twenty Statements Test responses in 2024 and again 424–750 days later (median 433). Its deterministic split supplies 150 training pairs, 50 public development pairs, and 81 test inputs whose follow-ups remain private. The project pinned commit 9b6a766712583fec8d3182957260b1123fbfa146 and recorded SHA-256 hashes for every prediction input and governing evaluation file before generating predictions.

The sample is small and selected. Platform recruitment and longitudinal attrition limit generalization, and agreement with one observed follow-up does not identify the only plausible future self-description.

## Stable-signifier projection

The deterministic method uses the 150 public training pairs and no demographics, external model, or external data. First, it estimates how often each unique source token appears at follow-up, smoothing token-level estimates toward the corpus-wide retention rate with ten equivalent prior observations. Second, it splits each source response at its strongest repeated boundary: lines, sentences, comma phrases, or the entire response. Third, it ranks response units by the mean estimated persistence of their unique content tokens.

Finally, a training-only ordinary least squares regression predicts follow-up word count from source word count. The algorithm retains ranked units while adding one moves output length closer to that target, then restores the units' original order. Every predicted word therefore comes from the participant's earlier response.

Public development data were used to choose between fixed extraction fractions and regression-predicted length, as the challenge permits. The displayed scorecard is consequently a model-selection result rather than an untouched confirmation set.

## Complete result pattern

The projection improves three of six text-agreement measures, worsens two, and ties exact match. Its word-count mean absolute error falls from 56.68 to 41.64 words, and source-similarity error falls from 0.774317 to 0.678215. Its line-count error rises from 6.80 to 9.76 lines. These mixed directions are why no single headline score summarizes the method.

The submission contains one nonblank prediction for every required test ID in order. Its SHA-256 is a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3. Only the organizer can run the private evaluator. Validation establishes artifact shape, not predictive performance.

## Interpretation and limits

Token recurrence is not equivalent to identity-signifier endurance. Common wording may recur without representing a stable identity, while genuinely new identities, experiences, and reframings are impossible for an extractive method to produce. The response splitter can also turn prose into too many lines. Repeated tuning on 50 development cases would risk overfitting.

The next research step is to submit the frozen CSV and method card, publish the organizer's complete private scorecard unchanged, and preregister development-data use before comparing a non-extractive or generative method.

## Reproducibility and references

The public repository contains the deterministic standard-library generator, 50 development predictions, the complete machine-readable development scorecard, the frozen 81-case test artifact, its method card, and benchmark provenance. The Full Report links each artifact directly.

Jones, J. J. (2023). <i>Ipseology—A new science of the self.</i> https://jasonjones.ninja/ipseology-a-new-science-of-the-self-book/

Jones, J. J. (2024). <i>Predicting the self with generative AI</i> [Preprint]. SocArXiv. [https://doi.org/10.31235/osf.io/eh9sk](https://doi.org/10.31235/osf.io/eh9sk)

Jones, J. J. (2026). <i>Building the ipseome: Large, free, open, human identity data</i> [Preprint]. arXiv. https://arxiv.org/html/2607.02488

Jones, J. J. (2026). <i>You can predict future selves with AI (or without AI)</i> [Data set and benchmark]. GitHub. https://github.com/jasonjeffreyjones/predict-future-selves
