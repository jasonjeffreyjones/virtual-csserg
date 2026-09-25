---
started: 2026-09-25T09:01:16Z
finished: 2026-09-25T09:13:22Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Which source features predict later response length?

## Scope

Decompose the one supported probabilistic neighborhood result without reusing
development labels or changing the frozen submission: test whether earlier
self-description text, 2024 demographics, or their combination drives
leave-one-out word-count CRPS improvement.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README; and the current
  ipseology definitions of personally expressed identity, signifiers, and
  longitudinal Add, Delete, Keep, and Ignore events.
- Locked `ANALYSIS_PLAN_FEATURE_ABLATION.md` before reopening benchmark data,
  implementation, or scoring at SHA-256
  `ed9fa67b2cc1265f3710471f96d7ffbfd16986b8295ef5072da26c263d8b7da4`.
  This is a dependent analysis lock rather than a preregistration because the
  combined word-count result and representation were already known.
- Added a deterministic, hash-guarded leave-one-out ablation. It separates the
  unchanged representation into text-only, demographics-only, and combined
  TF-IDF features while holding the 30-neighbor selection, 30-case
  neighborhood weight, 30-case fold prior, outcome transformations, and CRPS
  scoring fixed.
- Made follow-up word-count CRPS primary and the other four outcomes
  prespecified secondary diagnostics. The script must reproduce every earlier
  marginal and combined case-level CRPS value before accepting a result.
- Added six focused tests, a complete machine-readable result, and a 150-row
  case audit. Expanded all three report forms, the Executive Summary's single
  dense figure, the public research lead, state, build guide, guarded
  publisher, and publication verifier. The Full Report now exposes 42
  authoritative artifacts and byte-identical compatibility aliases.

## Evidence and validation

- All preceding marginal and combined CRPS values reproduced for 150 cases
  and five outcomes. Clean regeneration reproduced the new JSON and CSV byte
  for byte.
- Text-only word-count CRPS is `38.374556` versus `40.672695` for the
  source-calibrated marginal distribution. The paired reduction is
  `+2.298139` with a 20,000-resample case-bootstrap interval of `+0.816444` to
  `+3.865823`; text-only neighborhoods win 84 cases and lose 66.
- Demographics-only word-count CRPS is `40.471984`. Its marginal-minus-
  demographics reduction is `+0.200711`, with an interval spanning zero
  (`-0.479832` to `+0.861529`).
- Combined word-count CRPS is `38.156852`. Relative to text only, adding
  demographics reduces CRPS by `+0.217704` (`+0.024229` to `+0.420871`);
  combined wins 85 cases and loses 65. Earlier self-description carries most
  of the supported signal, with a smaller conditional demographic increment.
- Add-count, Delete-count, and line-count ablation contrasts all have intervals
  spanning zero. Text only improves source-similarity CRPS by `+0.002964`, but
  its repeated-analysis interval only narrowly excludes zero (`+0.000051` to
  `+0.006065`).
- All 52 Project tests and all 17 pinned benchmark tests passed. The official
  validator returned `VALID: 81 predictions`; the frozen artifact remains
  SHA-256 `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters and the guarded publisher copied
  all 42 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the four-page
  two-column PDF. Ghostscript rasterized all four pages at 120 dpi; visual
  inspection found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages
  and six first-party stylesheets.

## Limitations and decisions

- The ablation was chosen after the combined word-count gain was known and is
  a decomposition of dependent evidence, not fresh confirmation.
- Demographic features retain the inherited exact-value encoding. Sparse
  categories and missing values can weaken demographics-only similarity, and
  a small conditional increment does not make demographics an ipseological
  mechanism.
- Secondary contrasts are unadjusted repeated-analysis diagnostics. The folds
  overlap, the selected cohort is not a probability sample, and bootstrap
  intervals describe sensitivity to its case composition only.
- The result concerns response length and form, not correct future lexical
  content. The case audit is a derived benchmark-data adaptation under CC
  BY-NC-SA 4.0.
- No development or private answer was accessed, no test artifact changed,
  and no private-test performance claim was made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Avoid another fixed lexical re-ranker on these same cases. A substantively
  semantic or synthesizing model should preserve the primarily text-driven
  word-count distribution signal, treat the small conditional demographic
  increment cautiously, test the weaker Add/Delete signal, and beat
  leave-one-out marginal additions before any locked development comparison.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
