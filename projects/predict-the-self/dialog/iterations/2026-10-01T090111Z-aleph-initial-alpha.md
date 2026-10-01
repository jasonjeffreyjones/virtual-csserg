---
started: 2026-10-01T09:01:11Z
finished: 2026-10-01T09:17:16Z
scholar: "Aleph Initial Alpha"
scholar_slug: aleph-initial-alpha
project: predict-the-self
---

# Can external semantics predict person-specific additions?

## Scope

Test the current handoff's semantic content hurdle without reopening
development labels or changing the frozen submission: replace surface lexical
source matching with a fixed pretrained distributional-semantic
representation, then compare held-out novel-token recovery with marginal Add
frequency and the inherited surface neighborhood at the same oracle budget.

## Work completed

- Re-read the required repository, Scholar, and Project memory; the three
  newest iteration records; the pinned challenge README; and the current
  ipseology definitions of personally expressed identity, signifiers, and Add
  events.
- Retrieved the public-domain 25-dimensional GloVe Twitter conversion outside
  the repository, verified its 104 MB artifact at SHA-256
  `63877d71151688baf6f31d5437374f637f737a5e100e12150a5bd61a9f273c3f`,
  and recorded its source, license, and Pennington et al. (2014) DOI. The vector
  file is not committed.
- Locked `ANALYSIS_PLAN_SEMANTIC_NEIGHBORHOOD_ADDITIONS.md` before reading
  benchmark rows, implementation, or scoring at SHA-256
  `6a6a536a11c552b0e75f40ce6d79100902727958fa908cb57a662ac85df5fdcf`.
  The plan fixes the source centroid, 30-neighbor shrinkage, inherited
  comparators, oracle-budget limitation, primary hurdle, and no-development
  decision.
- Added a deterministic standard-library analysis that streams only required
  GloVe vectors, fits source-only IDF within each leave-one-out fold, and
  requires exact reproduction of all inherited marginal and surface-
  neighborhood hit counts. Added seven focused tests, a complete JSON result,
  and a 150-row audit without raw source or follow-up text.
- Updated all three report forms, the Executive Summary's single dense figure,
  public research lead and catalog metadata, state, build guide, guarded
  publisher, publication verifier, and publisher tests. The Full Report now
  exposes 59 authoritative artifacts and byte-identical compatibility aliases.

## Evidence and validation

- GloVe covers `2409` of `2537` distinct source token types (`94.9547%`), with
  mean case coverage `0.959380` and no zero-coverage case.
- The semantic neighborhood recovers a mean `0.148760` of held-out additions
  versus `0.160992` for marginal frequency. The semantic-minus-marginal
  difference is `-0.012232` with a 20,000-resample paired case-bootstrap
  interval of `-0.018361` to `-0.006322`; semantic wins 22 cases, ties 65, and
  loses 63. The prespecified primary hurdle fails.
- Semantic and marginal top sets overlap by `0.746530` on average. The semantic
  result is nearly identical to the inherited surface neighborhood's
  `0.149007`: their difference is `-0.000247`, with an interval spanning zero
  (`-0.006521` to `+0.005834`).
- Clean regeneration reproduced the JSON at SHA-256
  `104f0ef262ce5446f921763c1550e6c835b550a19f640b8eeee986212a5fbae6`
  and the audit at
  `19d19c40c564b45b9e0694bbf1b55f2e35be74d20d886a04a8fdb6adcee5d60f`.
- All 77 Project tests and all 17 pinned benchmark tests passed. The official
  validator returned `VALID: 81 predictions`; the frozen test artifact remains
  SHA-256 `a463d9e314069357f050c9f2270acfad59165db2c0bab19322d46517444d9ab3`.
- Quarto rendered both Full Report chapters; the guarded publisher copied all
  59 artifacts plus aliases. The publication verifier passed one Executive
  Summary figure, reciprocal links, the required phrase, and the five-page
  two-column PDF. Ghostscript rasterized all five pages at 110 dpi; inspection
  found legible text, intact columns, and no overlap or clipping.
- The Version 1 verifier passed all seven promise groups across 39 HTML pages,
  35 named data tables, and seven first-party stylesheets.

## Limitations and decisions

- This is a dependent analysis designed after earlier content failures were
  known. Its leave-one-out folds overlap, and its intervals describe
  sensitivity to this selected training cohort's case composition rather than
  population generalization.
- The oracle budget uses each held-out follow-up and therefore evaluates
  ranking, not a prospective forecast. Candidate Add tokens include function
  words and need not be semantic identity signifiers.
- GloVe proximity is distributional rather than a validated ipseological
  identity measure. The fixed centroid discards word order, polysemy, negation,
  and response structure; Twitter-trained vectors can encode social bias and
  domain mismatch.
- The failed hurdle rejects this fixed representation and ranking rule, not all
  semantic conditioning. No development prediction was generated, no private-
  test-performance claim was made, and the frozen submission was unchanged.
  The case audit is a derived benchmark-data adaptation under CC BY-NC-SA 4.0.

## Questions and next steps

- No PI question blocks further work.
- Submit exactly the frozen stable CSV and method card; publish the organizer's
  first complete private scorecard unchanged.
- Do not evaluate either failed synthesis or the GloVe-centroid ranking on
  development data. Avoid further fixed Add re-rankers on these 150 cases
  without richer compositional context or new longitudinal evidence.
- Perform rendered desktop, mobile, keyboard, and assistive-technology checks
  when browser infrastructure is available.
