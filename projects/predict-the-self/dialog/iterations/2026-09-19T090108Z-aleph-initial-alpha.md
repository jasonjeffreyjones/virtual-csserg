---
started: 2026-09-19T09:01:08Z
finished: 2026-09-19T09:14:07Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Does person matching beat common additions?

## Scope

Test whether the matched-trajectory baseline's limited recovery of novel token
types reflects person-specific matching or merely the base rates of common
follow-up additions, without changing the frozen private-test submission.

## Work completed

- Re-read the required repository and Project memory, both post-migration
  iteration records, the pinned Predict Future Selves README and governing
  documentation, and the current web edition of *Ipseology—A new science of
  the self*.
- Added `analysis/analyze_novelty_prior.py`, a deterministic, hash-guarded post
  hoc diagnostic. It counts document-level token additions in the 150 training
  pairs and ranks them by frequency, with alphabetical tie-breaking.
- For each development case, excluded tokens already present in the focal
  source and gave the marginal prior exactly the same novel-token budget as
  trajectory retrieval. This isolates token choice while holding the number of
  opportunities for correct overlap equal.
- Added four focused unit tests, the complete machine-readable result, and a
  2,770-row audit reporting token ranks, training frequencies, development
  occurrences, predictions, and correct recoveries.
- Expanded all three report forms, the home-page research lead, Project
  catalog, build guide, guarded publisher, and publication verifier. The Full
  Report now exposes eighteen authoritative artifacts and byte-identical
  compatibility aliases.

## Evidence and validation

- Both methods predict a mean `46.94` novel token types per case by
  construction; case-level budgets range from 1 to 114.
- The marginal prior's mean novel-type precision is `0.176545`, versus
  `0.070466` for trajectory retrieval. The paired difference is `+0.106079`
  with a 95% case-bootstrap interval of `+0.068782` to `+0.154891`.
- Mean recall is `0.172611` versus `0.085362`, a difference of `+0.087249`
  (`+0.062210` to `+0.113649`). Mean F1 is `0.142637` versus `0.067109`, a
  difference of `+0.075528` (`+0.055927` to `+0.094990`).
- The marginal prior wins 40 cases, ties 6, and loses 4 for precision, recall,
  and F1. Person-matched retrieval therefore has not demonstrated a lexical
  advantage over common training-set additions.
- Frequent correct additions include function and connective words as well as
  candidate identity content. Token recovery must not be equated automatically
  with recovery of semantic identity signifiers.

### Validation

- All 17 pinned benchmark tests and all 16 Project unit tests passed. The
  official validator returned `VALID: 81 predictions` for the unchanged frozen
  submission, whose SHA-256 remains
  `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Clean regeneration reproduced the new JSON result and CSV audit byte for
  byte.
- Quarto rendered both Full Report chapters, and the guarded publisher copied
  all eighteen artifacts plus aliases. The publication verifier passed one
  Executive Summary figure, reciprocal links, the required phrase, artifacts,
  and the two-page two-column PDF.
- Both PDF pages were rasterized at 144 dpi and visually inspected; the two
  columns are legible with no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 26 HTML pages
  and six first-party stylesheets after the Project catalog was reordered by
  its authoritative `STATE.md` timestamp. `git diff --check` passed.

## Limitations and decisions

- This is a post hoc development diagnostic, not a preregistered comparison or
  a private-test result. Development labels have been inspected repeatedly.
- The marginal prior borrows retrieval's per-case novel-token count and emits
  a token set, not coherent full text. It is a volume-matched control rather
  than an independent challenge submission.
- Lexical tokens include function words and generic vocabulary that need not
  denote identity signifiers. The token audit is a derived adaptation of the
  CC BY-NC-SA 4.0 benchmark data.
- The paired intervals describe sensitivity to the composition of these 50
  development cases, not population-generalization uncertainty.
- No test prediction was generated or altered, and no test-performance claim
  was made.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card, then publish the
  organizer's first complete private scorecard unchanged.
- Evaluate any future person-conditioned novelty model against this
  volume-matched marginal prior. Prefer training-only nested evaluation or new
  evidence, and lock the comparison before reusing development labels.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
