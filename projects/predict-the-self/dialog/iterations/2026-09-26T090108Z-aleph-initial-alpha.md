---
started: 2026-09-26T09:01:08Z
finished: 2026-09-26T09:13:37Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does lexical text beat simple source form for predicting response length?

## Scope

Qualify the supported text-only word-count result without reusing development
labels or changing the frozen submission: test whether lexical TF-IDF matching
outperforms a neighborhood based only on observable counts from the earlier
self-description.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README; and the current
  ipseology definitions of personally expressed identity, signifiers, and
  longitudinal Add, Delete, Keep, and Ignore events.
- Locked `ANALYSIS_PLAN_SOURCE_FORM_ABLATION.md` before reading benchmark rows,
  implementation, or scoring at SHA-256
  `5ffaf6b8289a360926da3ae3b1398a336949e698c6157f8ba94ef316ec63c5ad`.
  This is a dependent analysis lock rather than a preregistration because the
  text-only word-count result and distributional design were already known.
- Added a deterministic, hash-guarded leave-one-out comparison. The count-only
  neighborhood uses log word-token, distinct-token, and line counts from the
  2024 response, fold-fit standard deviations, and a fixed inverse-distance
  similarity. It retains the 30-neighbor selection, 30-case neighborhood
  weight, 30-case fold prior, outcome transformations, and CRPS scoring.
- Made source-form CRPS minus text-only CRPS the primary word-count contrast.
  The script must reproduce every inherited marginal and text-only case score
  before accepting a result. Added six focused tests, a complete JSON result,
  and a 150-row case audit.
- Updated all three report forms, the Executive Summary's single dense figure,
  the public research lead and catalog, state, build guide, guarded publisher,
  and publication verifier. The Full Report now exposes 46 authoritative
  artifacts and byte-identical compatibility aliases.

## Evidence and validation

- Count-only source-form matching lowers word-count CRPS to `37.427386` from
  `40.672695` for the source-calibrated marginal. The paired reduction is
  `+3.245309` with a 20,000-resample case-bootstrap interval of `+1.839350` to
  `+4.784335`; source form wins 96 cases and loses 54.
- Text-only word-count CRPS is `38.374556`. The prespecified source-form-minus-
  text effect is `-0.947170` with an interval spanning zero (`-1.943737` to
  `+0.035874`); text wins 65 cases and loses 85. Under the locked rule, the
  fixed comparison does not distinguish their primary skill and supplies no
  stable lexical advantage beyond simple response form.
- Source form lowers line-count CRPS by `+0.445157` over the marginal (interval
  `+0.206291` to `+0.701574`) and by `+0.472157` over text only (`+0.235305` to
  `+0.721005`). These are unadjusted secondary response-form diagnostics.
  Add-count and Delete-count comparisons span zero.
- Every inherited marginal and text-only score reproduced for 150 cases and
  five outcomes. Clean regeneration reproduced the new JSON and CSV byte for
  byte. All 58 Project tests and all 17 pinned benchmark tests passed. The
  official validator returned `VALID: 81 predictions`; the frozen artifact
  remains SHA-256
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  46 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the four-page
  two-column PDF. Ghostscript rasterized all four pages at 120 dpi; visual
  inspection found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages,
  27 named data tables, and six first-party stylesheets. `git diff --check`
  passed.

## Limitations and decisions

- The comparison was chosen after a positive text-only result and tests one
  fixed three-count representation. It is not fresh confirmation and cannot
  rule on every lexical or nonlexical model.
- A direct interval spanning zero means this analysis does not distinguish the
  methods; it does not prove their predictive distributions are equivalent.
- TF-IDF overlap can encode style and template wording rather than semantic
  identity. Count-only performance concerns response form, not the correct
  future signifiers or identity content.
- Secondary contrasts are unadjusted repeated-analysis diagnostics. The folds
  overlap, the selected cohort is not a probability sample, and bootstrap
  intervals describe sensitivity to its case composition only.
- No development or private answer was accessed, no test artifact changed,
  and no private-test-performance claim was made. The case audit is a derived
  benchmark-data adaptation under CC BY-NC-SA 4.0.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Avoid further fixed lexical re-rankers or post hoc decompositions on these
  same 150 cases without a substantively new representation or new evidence.
  A later synthesizing or semantic method should preserve response-form
  calibration, add value beyond simple source counts, and beat leave-one-out
  marginal additions before any locked development comparison.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
