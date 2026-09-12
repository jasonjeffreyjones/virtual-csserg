---
title: "Predict the Self"
status: Active
updated: 2026-08-31
---

# Predict the Self — Current State

## Status

Active. The Predict Future Selves benchmark is retrieved and pinned, a
reproducible stable-signifier method has a complete public-development
scorecard, and all 81 test predictions are frozen and validator-clean. The
private test scorecard and challenge pull request remain outstanding.

## What is complete

- Read the challenge README, participation guide, data statement, evaluation
  specification, baseline prompt, source code, and all public training and
  development data at benchmark commit
  `9b6a766712583fec8d3182957260b1123fbfa146`.
- Recorded SHA-256 hashes for every prediction input and the governing
  documentation, evaluator, and validator in `BENCHMARK_PROVENANCE.md`.
- Implemented `analysis/stable_signifier_projection.py`, a deterministic,
  standard-library extractive method trained on 150 public pairs. It estimates
  token retention, ranks response units, and uses training-only length
  regression. It does not use demographics, external data, or a generative
  model.
- Generated and froze all 50 development predictions, their full official
  scorecard, and all 81 test predictions. The pinned official validator reports
  `VALID: 81 predictions`; test artifact SHA-256 is
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Documented the complete method and public-development scorecard in
  `submissions/aleph_initial_alpha_method.md`.
- Published a direct-HTML Full Report, Executive Summary update, and all
  reproducibility artifacts. This follows the repository's Quarto-unavailable
  fallback.

## Current evidence

On the 50 public development cases, stable-signifier projection versus the
repeat-2024 baseline:

- improves normalized edit similarity (`0.298061` vs. `0.291966`), token
  Jaccard (`0.142768` vs. `0.141930`), and ROUGE-L F1 (`0.227552` vs.
  `0.225683`);
- worsens token-overlap F1 (`0.307444` vs. `0.312202`) and character n-gram F1
  (`0.292293` vs. `0.296534`), while exact-match remains zero;
- reduces word-count MAE (`41.64` vs. `56.68`) and source-similarity MAE
  (`0.678215` vs. `0.774317`), but increases line-count MAE (`9.76` vs. `6.80`).

There is no composite score or overall winner. The strongest substantive
finding is a remaining failure: mean prediction-to-source ROUGE-L is
`0.903898`, versus `0.225683` for observed follow-ups. The extractive method
still predicts far too much textual continuity.

## Current problems and unknowns

- Test answers and follow-up demographics are private. Only the challenge
  organizer can produce the official test scorecard; no test-performance claim
  is currently valid.
- The submission CSV and method card have not yet been opened as a pull request
  in the challenge repository.
- Development data informed selection among extractive rules. Its scorecard is
  a model-selection result and may be optimistic for held-out performance.
- Quarto is not installed. The Full Report is published as validated direct
  HTML, while `report.qmd` remains the parallel research source.

## Important files

- `PROJECT.md` — stable charter (PI-owned)
- `PI.md` — PI instructions (PI-owned)
- `BENCHMARK_PROVENANCE.md` — pinned commit, licensing, and input hashes
- `analysis/stable_signifier_projection.py` — reproducible prediction method
- `results/stable_signifier_dev_predictions.csv` — 50 development predictions
- `results/stable_signifier_dev_scorecard.json` — complete public scorecard
- `submissions/aleph_initial_alpha_submission.csv` — frozen 81-case artifact
- `submissions/aleph_initial_alpha_method.md` — submission-ready method card
- `report.qmd` — Full Report research source
- `website/projects/predict-the-self/index.html` — Executive Summary
- `website/projects/predict-the-self/report/index.html` — published Full Report

## Likely next steps

1. Open a challenge pull request containing only the frozen submission CSV and
   method card; do not revise the test artifact in response to test feedback.
2. Add the organizer's complete private scorecard unchanged to project results,
   the Full Report, and Executive Summary.
3. Before further model comparison, preregister a non-extractive or generative
   method and the role of development data to limit repeated tuning.
4. Improve response-form modeling, especially line count, without treating any
   single scorecard metric as an overall objective.
