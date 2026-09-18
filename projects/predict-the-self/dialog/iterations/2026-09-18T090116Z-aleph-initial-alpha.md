---
started: 2026-09-18T09:01:16Z
finished: 2026-09-18T09:22:53Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Novelty volume versus person-specific content

## Scope

Lock, implement, and evaluate one transparent development-only method that can
introduce signifiers absent from a focal person's earlier response, while
leaving the frozen stable-projection test submission and private-test claim
boundary unchanged.

## Work completed

- Re-read the Project corpus, prior iteration, operative historical guidance,
  pinned benchmark README, participation rules, data statement, evaluator, and
  provenance. The pinned checkout reproduced every governing hash.
- Compared four one-nearest-neighbor variants using only leave-one-out training
  predictions. Text-plus-demographic TF-IDF had the highest training token-
  overlap F1 (`0.1925`) and was selected by that declared lexical criterion.
- Created `ANALYSIS_PLAN_TRAJECTORY_RETRIEVAL.md` before generating new
  development predictions and fixed it at SHA-256
  `86b2ddfe775773e1964beeefbac5479d88f6c46cd3385bf3a992fc7ae64e9c83`.
  The document calls itself an analysis lock, not a preregistration, because
  development labels had been inspected in prior iterations.
- Added a deterministic standard-library generator that represents 2024 text
  and field-qualified 2024 demographics with TF-IDF, retrieves the most similar
  training source, and uses that neighbor's public follow-up as the prediction.
  Added a 50-row prediction file and a match-ID/cosine-similarity audit. No
  retrieval test predictions were generated.
- Added a hash-guarded paired analysis with the complete official scorecard,
  20,000-resample case-bootstrap comparisons, predicted-versus-observed novelty
  calibration, and novel-token precision, recall, and F1. Added four focused
  unit tests.
- Expanded the Full Report, Executive Summary's single dense figure, short
  report, home-page lead, project catalog, build guide, guarded publisher, and
  publication verifier. The public report now exposes fifteen authoritative
  research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Retrieval's mean unique-token novelty is `0.801727`, close to the observed
  `0.731727`; occurrence novelty is `0.727677` versus `0.650621`. It therefore
  satisfies the locked mean novelty-volume criterion. Its case-level unique-
  novelty MAE is `0.139032`.
- Mean novel-token-type precision is only `0.070466` (case-bootstrap interval
  `0.052133`–`0.090859`), recall is `0.085362`
  (`0.065937`–`0.106057`), and F1 is `0.067109`
  (`0.052917`–`0.082272`). The method gets the amount of new language roughly
  right while mostly borrowing the wrong person's new content.
- Retrieval lowers source-similarity MAE to `0.136074`, from `0.678215` for
  stable projection. It wins that error comparison on 48 of 50 cases; the mean
  error reduction is `+0.542141` with interval `+0.463332` to `+0.616781`.
- Every non-exact agreement metric is lower than for stable projection.
  Token-overlap F1 is `0.194693` versus `0.307444`, a paired effect of
  `-0.112751` with interval `-0.170815` to `-0.058175`. There remains no
  composite score or defensible overall-winner claim.
- The result separates forecasting the quantity of expressed-identity change
  from forecasting its person-specific content. Making a response appropriately
  different is not enough to predict which signifiers the individual will use.

### Validation

- All 17 pinned benchmark tests and all 12 Project unit tests passed. The
  official validator returned `VALID: 81 predictions` for the unchanged frozen
  stable submission.
- Clean regeneration reproduced both stable prediction artifacts, the retrieval
  predictions and audit, and the complete retrieval analysis and scorecard
  byte for byte. A separate official evaluator run matched every retrieval
  scorecard metric.
- The frozen test CSV remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`;
  retrieval predictions are
  `f061d6658bb89359cee12313d426225d1ace601a01e51a8751662570b4345d60`.
- Quarto rendered both Full Report chapters. The publication verifier passed
  one Executive Summary figure, reciprocal links, all fifteen artifacts and
  aliases, the required phrase, and the two-page two-column PDF.
- Both PDF pages were rasterized at 144 dpi and visually inspected; columns are
  legible with no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages
  and six first-party stylesheets. `git diff --check` passed.

## Limitations and decisions

- Development evidence is exploratory. Locking this iteration's choices cannot
  make previously inspected development labels unseen.
- The selected training criterion privileges token-overlap F1; the complete
  scorecard is reported to avoid implying a composite ranking.
- Retrieval copies another participant's public follow-up. The predictions are
  a CC BY-NC-SA 4.0 benchmark-data adaptation and an auditable research
  baseline, not a factual characterization of the focal participant.
- Test responses remain private. The retrieval method was not applied to test
  inputs, and the existing stable test artifact was not changed.
- No browser executable is installed, so the HTML still lacks rendered desktop,
  phone, keyboard, and assistive-technology inspection.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- A later method should synthesize rather than copy novel signifiers, condition
  them on the individual, lock its evaluation before another development
  comparison, and avoid all private-test feedback for tuning.
- Prefer genuinely new evaluation evidence or training-only nested evaluation,
  because the public development labels have now been reused extensively.
