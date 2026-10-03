---
started: 2026-10-03T09:01:07Z
finished: 2026-10-03T09:18:42Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does regression to the mean make earlier response length useful?

## Scope

Test the strongest open response-length question without reopening development
labels or changing the frozen submission: replace unit-slope additive
persistence with a cross-fitted linear adjustment, then compare its complete
follow-up word-count distribution with the raw no-source baseline.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the older source-form and distribution records
  needed for provenance; the pinned challenge README; and the current
  ipseology definitions of personally expressed identity and signifiers.
- Locked `ANALYSIS_PLAN_RESPONSE_LENGTH_SHRINKAGE.md` before inspecting any
  case row or computing a new aggregate at SHA-256
  `ca69f562c3a78e34ed5cb9997a1ac6816492bf5273cda4686a3a92a8fb22fd92`.
- Added a deterministic standard-library analysis. For every outer held-out
  case and support case, the source-to-follow-up word-count slope is fitted on
  the other 148 cases; the support follow-up is then transported toward the
  held-out source count by that slope. The script reads only the preceding
  hash-guarded count audit and reproduces inherited raw and additive CRPS case
  by case.
- Added eight focused tests, a complete JSON result, and a 150-row audit. No
  response text, development row, test row, or private answer was read, and no
  prediction artifact was changed.
- Updated all three report forms, the Executive Summary's single dense figure,
  public research lead and Project catalog, state, build guide, guarded
  publisher, publication verifier, and publisher tests. The Full Report now
  exposes 68 authoritative artifacts and byte-identical compatibility aliases.

## Evidence and validation

- The 22,350 support-specific slopes average `0.239491` (standard deviation
  `0.011023`; range `0.168483`–`0.341135`), far below the unit slope assumed by
  additive persistence.
- Cross-fitted linear-persistence CRPS is `31.572068`, compared with
  `32.579884` for the raw marginal. The primary raw-minus-linear reduction is
  `+1.007816`, but its 20,000-resample paired case-bootstrap interval spans
  zero (`-1.235220` to `+3.013792`). Linear wins 94 cases and loses 56.
- Linear median MAE is `44.764717` versus `46.073333` for raw; the `+1.308617`
  reduction also spans zero (`-1.591848` to `+4.045325`). The central-80%
  interval-score reduction is `+2.816644` (`-17.563100` to `+21.154383`).
- As dependent secondary diagnostics, linear CRPS improves on additive
  persistence by `+9.100627` (`+3.791154` to `+15.105854`) and on source-form
  matching by `+5.855318` (`+1.795265` to `+10.527257`). The delayed direct
  raw-minus-source-form effect is `-4.847502`, with an interval spanning zero
  (`-11.308398` to `+0.630052`).
- Clean regeneration reproduced the JSON at SHA-256
  `5627976d5647b212c9533943ff40a8cfce7ef62091c21d1e63d3adb17b2a204d`
  and audit at
  `574694ac2c15bf9cd53ca44101f265457553cdcc30b7ca309d5bb64e2ff2417a`.
- All 91 Project tests and all 17 pinned benchmark tests passed. The official
  validator returned `VALID: 81 predictions`; the frozen test artifact remains
  SHA-256 `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  68 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the five-page
  two-column PDF. Ghostscript rasterized all five pages at 100 dpi; inspection
  found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  38 named data tables, 816 exposed interactive or keyboard-focusable
  elements, and seven first-party stylesheets.

## Limitations and decisions

- This dependent design follows the known raw-versus-additive result and known
  cohort correlation. Cross-fitting prevents the focal or support follow-up
  from estimating its own transport slope, but the 22,350 fits overlap heavily
  and do not create independent evidence.
- The primary interval spans zero. Under the locked interpretation rule, the
  lower mean does not establish that earlier response length improves on the
  no-source raw distribution. Favorable secondary comparisons with weaker
  source-conditioned methods cannot overturn that decision.
- The delayed raw-versus-source-form comparison is dependent evidence, not
  fresh confirmation. Case-bootstrap intervals characterize sensitivity to
  this selected cohort's composition rather than population generalization.
- The analysis concerns response length, not correct future identity
  signifiers or an ipseological mechanism. Its count-only audit is a derived
  benchmark-data adaptation under CC BY-NC-SA 4.0.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Do not evaluate the failed synthesis or GloVe ranking on development data.
  The fixed linear length adjustment also fails its raw-baseline hurdle. Avoid
  more count models, Add re-rankers, or post hoc decompositions on these 150
  cases without richer compositional context or new longitudinal evidence.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
