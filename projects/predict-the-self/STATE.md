---
title: "Predict the Self"
status: Active
updated: 2026-09-12T21:06:41Z
---

# Predict the Self — Current State

## Status

Active and ready for a Scholar research iteration. The Predict Future Selves
benchmark is pinned, the deterministic stable-signifier method and its 81 test
predictions are frozen, all current public-development results are published,
and the Project now follows the current three-memory-file and three-report
structure. The private test scorecard and challenge pull request remain open.

## Current finding

On 50 public development cases, stable-signifier projection versus the
repeat-2024 baseline:

- improves normalized edit similarity (`0.298061` vs. `0.291966`), token
  Jaccard (`0.142768` vs. `0.141930`), and ROUGE-L F1 (`0.227552` vs.
  `0.225683`);
- worsens token-overlap F1 (`0.307444` vs. `0.312202`) and character n-gram F1
  (`0.292293` vs. `0.296534`), while exact match remains zero;
- reduces word-count MAE (`41.64` vs. `56.68`) and source-similarity MAE
  (`0.678215` vs. `0.774317`), but increases line-count MAE (`9.76` vs. `6.80`).

There is no composite score or overall winner. Mean prediction-to-source
ROUGE-L remains `0.903898`, versus `0.225683` for observed follow-ups. The
extractive method therefore predicts far too much textual continuity.

## Completed research and artifacts

- Retrieved the public benchmark at immutable commit
  `9b6a766712583fec8d3182957260b1123fbfa146` and recorded SHA-256 hashes for
  prediction inputs, documentation, evaluator, and validator.
- Implemented `analysis/stable_signifier_projection.py`, a deterministic,
  standard-library extractive method trained on 150 public pairs. It uses no
  demographics, external data, or generative model.
- Generated all 50 development predictions and the complete official public
  scorecard. Generated and froze all 81 private-test predictions; the pinned
  official validator reports `VALID: 81 predictions`.
- Preserved the test artifact at SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`
  and documented the method in a submission-ready card.

## Publication and build structure

- `index.qmd` and `report.qmd`, governed by `_quarto.yml`, render a two-chapter
  Quarto HTML book into ignored `_book/`. Two chapters are an editorial choice,
  not a fixed requirement.
- `analysis/publish_full_report.py` replaces the public report only from a
  complete build and removes stale generated files. Unit tests cover complete
  replacement and preservation after an incomplete build.
- `short-report.md` and `analysis/render_short_report.py` generate a linked,
  two-column PDF. Its current content fits one page; validation permits any
  nonempty length through the actual ten-page ceiling.
- The five-minute Executive Summary uses the selected evidence-brief structure:
  question/status, exactly one dense quantitative figure, six linked findings,
  and both report choices.
- The three forms link reciprocally. The Full Report publishes six research
  artifacts directly from their authoritative project paths and preserves the
  earlier `report/artifacts/` URLs as byte-identical compatibility copies.
- `BUILD.md` gives the complete build and check sequence. Five project tests,
  the publication verifier, and all seven Version 1 promise groups pass on the
  September 12 host.

## Decisions and constraints

- Test answers and follow-up demographics are private. Only the challenge
  organizer can produce an official test score; no test-performance claim is
  currently valid.
- Development data informed extractive-rule selection. Treat its scorecard as
  model-selection evidence, not an untouched confirmatory estimate.
- Do not alter the frozen test artifact in response to private score feedback.
- `PROJECT.md` remains the PI-owned charter. `DIALOG.md` is the current
  append-only conversation. Legacy `PI.md` and `LOG.md` remain intact as
  historical records pending the separately approved coordinated dialog
  migration; future iterations append to `DIALOG.md`.

## Important files

- `PROJECT.md`: PI-owned charter.
- `STATE.md` and `DIALOG.md`: current project memory and conversation.
- `BUILD.md`, `_quarto.yml`, `index.qmd`, `report.qmd`, `short-report.md`:
  publication sources and reproduction instructions.
- `BENCHMARK_PROVENANCE.md`: pinned commit, licensing, and governing hashes.
- `analysis/stable_signifier_projection.py`: prediction method.
- `analysis/publish_full_report.py`, `analysis/render_short_report.py`, and
  `analysis/verify_publication.py`: guarded publication pipeline and checks.
- `results/`: development predictions and complete public scorecard.
- `submissions/`: frozen test artifact and method card.
- `website/projects/predict-the-self/`: Executive Summary, Full Report, short
  report, and copied reproducibility artifacts.

## Problems and unresolved PI questions

- The prepared CSV and method card have not been opened as a pull request in
  the challenge repository. No authenticated GitHub write path is available in
  this workspace.
- Private test evidence remains unavailable by benchmark design.
- No browser executable is installed on this host, so the new HTML summary and
  book still need rendered desktop, phone, keyboard, and assistive-technology
  inspection. The PDF received a local rasterized visual check.
- No PI question blocks the next Scholar from useful work.

## Likely next steps

1. Submit exactly the frozen CSV and method card to the challenge organizer;
   add the complete private scorecard unchanged when returned.
2. Before another model comparison, preregister the method and the role of
   development data to limit repeated tuning.
3. Compare a non-extractive or generative approach that can model genuinely
   new signifiers and response form, without using private test feedback for
   optimization.
4. Perform the remaining rendered accessibility and responsive-layout checks
   when browser infrastructure is available.
