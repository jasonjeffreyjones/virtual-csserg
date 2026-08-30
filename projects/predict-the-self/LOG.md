# Predict The Self

Below are log entries from Scholars. This is an append-only file.

## 2026-08-28 — Aleph Initial Alpha

- **Started:** 2026-08-28 20:54:09 UTC
- **Project:** Predict the Self
- **Planned scope:** Read the project's primary background, enter the Predict
  Future Selves challenge as a participant, and establish the first Full Report
  and public Executive Summary without reporting unevaluated predictions.
- **Work completed:**
  - Read the complete online *Ipseology* book and Dr. Jones' *Predicting the
    Self with Generative AI* slides; recorded the primary sources in the Full
    Report source.
  - Recovered the prior OPTS Mark 1 design (112,541 paired 2015/2020 US Twitter
    bios) and distinguished it from the still-unread current challenge.
  - Added `report.qmd` with the research framing, sources, current result, and a
    leakage-resistant participant protocol fixed before access to challenge
    cases or answers.
  - Published the Predict the Self Executive Summary, cataloged it on the home
    page, and updated Aleph Initial Alpha's profile to the assigned project.
  - Replaced the one-line project state with current evidence, limitations,
    important files, and next steps.
- **Validation:**
  - All 7 public HTML pages passed standard-library structure, landmark,
    duplicate-ID, local-link, and fragment checks.
  - The Quarto YAML front matter parsed successfully with R, and
    `git diff --check` passed.
  - The repository's Version 1 verifier passed 5 of 6 groups. Its sole failure
    is outside this project: `nfl-team-fandom-identities`, created in the same PI
    update, does not yet have a public Executive Summary.
- **Problems encountered:**
  - GitHub publicly listed the newly created `predict-future-selves` repository,
    but the available web cache returned a cache miss for its page, README, and
    raw file; direct shell access could not resolve GitHub. I did not reconstruct
    the instructions, substitute the older OPTS dataset, inspect answers, or
    invent a score.
  - Quarto is not installed, so the validated Full Report source could not be
    rendered to `website/projects/predict-the-self/report/`.
- **Question for Dr. Jones:** If the challenge repository remains unavailable
  in the next Scholar environment, may its README and participant files be
  copied into `projects/predict-the-self/` with their source commit recorded?
- **Proposed next step:** Retrieve and hash the current challenge artifacts,
  follow their instructions, freeze predictions before evaluation, compute the
  official score and permitted baselines, then render and link the Full Report.
- **Ended:** 2026-08-28 21:01:10 UTC

## 2026-08-30 — Aleph Initial Alpha

- **Started:** 2026-08-30 17:24:56 UTC
- **Project:** Predict the Self
- **Planned scope:** To be fixed after reading the complete project corpus and
  the PI's current instructions.
- **Scoped work:** Use the PI-restored live web access to retrieve and pin the
  current challenge; develop and evaluate one reproducible participant method;
  freeze a validator-clean test artifact without accessing private answers;
  and publish the complete evidence and reproducibility materials.
- **Work completed:**
  - Retrieved the full public Predict Future Selves repository and detached it
    at commit `9b6a766712583fec8d3182957260b1123fbfa146`; read the README,
    participation guide, data statement, evaluation definition, baselines,
    source code, tests, and public training/development data.
  - Added `BENCHMARK_PROVENANCE.md` with SHA-256 hashes for all four prediction
    inputs and the governing documentation, evaluator, and validator.
  - Implemented a deterministic standard-library stable-signifier projection.
    It learns smoothed document-level token retention, ranks extractive response
    units, and uses training-only OLS length prediction. Demographics, external
    models, and external data are not used.
  - Generated 50 development predictions and the complete official scorecard.
    Compared with repeat-2024, the method improves normalized edit similarity,
    token Jaccard, ROUGE-L, word-count MAE, and source-similarity MAE; it worsens
    token-overlap F1, character n-gram F1, and line-count MAE. No composite or
    overall-winner claim was made.
  - Froze all 81 test predictions at SHA-256
    `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`
    and wrote a submission-ready method card with the full development
    scorecard, model-selection disclosure, reproduction steps, and licensing.
  - Replaced the obsolete access-blocked state, expanded `report.qmd`, updated
    the Executive Summary, and published a direct-HTML Full Report plus all six
    downloadable reproducibility artifacts.
- **Substantive result:** The method's development source-similarity MAE falls
  from `0.774317` to `0.678215`, but mean prediction-to-source ROUGE-L remains
  `0.903898` while observed follow-ups average `0.225683`. Even an extraction
  rule explicitly favoring enduring signifiers predicts far too much textual
  continuity.
- **Validation:**
  - All 17 tests in the pinned challenge and all 3 new project tests passed.
  - The official evaluator reproduced all 15 recorded development measures;
    the official validator returned `VALID: 81 predictions`.
  - A clean regeneration produced byte-identical development and test CSVs and
    metric-identical JSON. Published artifact hashes match research artifacts.
  - The new Executive Summary and Full Report passed standard-library HTML
    structure, unique-ID, local-link, and fragment checks. Report tables were
    checked against the machine-readable scorecard.
  - The Version 1 verifier passed 5 of 6 groups. Its sole failure is outside
    this project: `nfl-team-fandom-identities` has no public project index.
  - `git diff --check` passed.
- **Problems encountered:**
  - The GitHub CLI is not installed and no authenticated GitHub write channel
    is available, so the prepared CSV and method card could not be opened as a
    pull request in the challenge repository.
  - Test answers are private by design; only the organizer can calculate the
    official test scorecard. No test-performance claim was made.
  - Quarto remains unavailable. Per repository guidance, the Full Report was
    published directly as static HTML while retaining `report.qmd` as source.
- **Question for Dr. Jones:** Should a future Scholar run receive an
  authenticated GitHub submission path, or would you prefer to open the
  challenge pull request using the two frozen files in `submissions/`?
- **Proposed next step:** Submit exactly the frozen CSV and method card, then
  add the organizer's complete private scorecard unchanged. Before another
  model comparison, preregister how development data will be used.
- **Ended:** 2026-08-30 17:40:44 UTC
- **Duration:** 15 minutes 48 seconds
