---
started: 2026-09-21T09:01:08Z
finished: 2026-09-21T09:11:55Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does regularized trajectory pooling beat common additions?

## Scope

Test, without reusing development labels, whether pooling Add events across
multiple similar source descriptions and demographics can recover held-out
novel token types beyond their marginal frequency. Preserve the frozen private-
test submission and all development predictions.

## Work completed

- Re-read the required repository and Project memory, the three newest
  iteration records, relevant legacy context and PI guidance, and the current
  research and publication pipeline.
- Locked `ANALYSIS_PLAN_NEIGHBORHOOD_ADDITIONS.md` before implementation or
  scoring at SHA-256
  `c7a494327dd1dd7fc83911540a6a9095fcc8d684172a7388bd610206ac4ca13d`.
  The plan is explicitly an analysis lock rather than a preregistration because
  these training pairs and the reused source representation informed earlier
  Project work.
- Added a deterministic, hash-guarded leave-one-out analysis. Fold-fit TF-IDF
  over source text and field-qualified 2024 demographics selects 30 neighbors.
  Similarity-weighted Add events contribute 30 effective cases and are shrunk
  equally toward a 30-case marginal prior. Both rankings receive the held-out
  future's novel-type count as an oracle budget.
- Added a complete JSON result, a 150-row case audit, and six focused unit
  tests. No development or test prediction was generated or altered.
- Expanded all three report forms, the Executive Summary's single dense
  figure, the home-page research lead, Project catalog, state, build guide,
  guarded publisher, and publication verifier. The Full Report now exposes 26
  authoritative research artifacts and byte-identical compatibility aliases.

## Evidence and validation

- All 150 cases have positive observed-addition budgets. Mean recovered
  fraction is `0.149007` for the regularized neighborhood and `0.160992` for
  leave-one-out marginal frequency.
- The paired neighborhood-minus-marginal difference is `-0.011984`; its
  20,000-resample case-bootstrap interval is `-0.018426` to `-0.005693`.
  Conditioning wins 25 cases, ties 60, and loses 65. Under the locked rule, it
  shows no incremental person-conditioned advantage.
- The neighborhood and marginal top sets overlap by `0.739706` on average, so
  personalization changes about 26.0% of guesses rather than simply reproducing
  the comparator. Mean cosine similarity across the 30 selected neighbors is
  `0.169564`.
- Clean regeneration reproduced the JSON and CSV outputs byte for byte. All 28
  Project tests and all 17 pinned benchmark tests passed. The official
  validator again returned `VALID: 81 predictions`.
- The frozen test artifact remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  26 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, artifacts, the required phrase, and the
  three-page two-column PDF.
- All three PDF pages were rasterized at 144 dpi and visually inspected. Text
  is legible, both columns flow without overlap or clipping, and the final
  references page has substantial but acceptable whitespace. The Version 1
  verifier passed all seven promise groups across 26 HTML pages and six first-
  party stylesheets. `git diff --check` passed.

## Limitations and decisions

- The oracle budget uses the held-out follow-up and isolates ranking quality;
  neither ranking is a prospective full-text forecast.
- The fixed neighborhood size and prior weight were not tuned, while the
  text-and-demographic representation was selected in earlier work. Coarse
  demographic similarity is not an ipseological mechanism.
- Lexical tokens include function words and generic language that need not be
  semantic identity signifiers. The interval describes sensitivity to this
  training cohort's case composition, not population generalization.
- The result is bounded but cumulative: both a sparse maximum-association rule
  and a pooled, strongly regularized neighborhood lose to common additions. It
  does not show that every individualized or semantic method must fail.
- The case audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.
  No private answer or score was accessed, and no test-performance claim was
  made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Avoid further fixed lexical re-rankers on these same 150 cases unless a
  substantively new representation motivates them. Prefer new longitudinal
  evidence or a semantic synthesis method that first beats leave-one-out
  marginal additions before any locked development comparison.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
