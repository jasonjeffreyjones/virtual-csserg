# NFL Team Fandom Identities — Current State

## Current focus

RQ1 remains the priority: compare `happy` prevalence among respondent-days explicitly answering Yes versus No to `Cleveland Browns fan`.

## What is known

- The official JJJ Pro Dawg Tracker reports rounded `happy` rates of 83% among Cleveland Browns fans and 77% among non-fans. These imply a preliminary risk (prevalence) ratio of about 1.08 and a prevalence difference of +6 percentage points. Exact cell counts and uncertainty remain uncomputed.
- The correct observational unit is a `(hashed_respondent_id, obs_date)` respondent-day on which both target signifiers were presented and explicitly answered. An absent item must not be treated as No.
- Expert Mode responses and demographics must be inner-joined on both `hashed_respondent_id` and `obs_date`. Duplicate demographics keys could create an invalid many-to-many join and should stop analysis.
- “Risk ratio” is mathematically correct for the requested binary probability comparison; “prevalence ratio” is more design-specific because the outcome and fandom are measured contemporaneously. Current methods use the combined label **risk (prevalence) ratio** and also report the prevalence difference.

## Completed

- Documented data sources, the estimand, inclusion rules, preliminary benchmark, uncertainty approach, limitations, and planned sensitivity checks in `METHODS.md`.
- Implemented `analysis/rq1_risk_ratio.py`, a dependency-free analysis that performs the required join, constructs the co-presented risk set, audits duplicates and exclusions, calculates exact 2 × 2 results, and records input SHA-256 hashes and the eligible date range.
- Added analytic confidence intervals and a deterministic percentile bootstrap clustered by `hashed_respondent_id` for repeated respondents.
- Added three passing synthetic-data tests covering co-presentation, explicit No coding, inner-join exclusions, repeated respondents, conflicting responses, and duplicate join keys.
- Added `data/README.md` and local ignores so cumulative microdata are downloaded reproducibly without bloating repository history.

## Current limitation

The current execution environment could browse the official documentation and published benchmark but could not save either CSV: shell network access had no DNS resolution, and the browsing interface does not export CSV downloads to the workspace. Therefore no exact RQ1 estimate or report has yet been published.

## Important files

- `METHODS.md` — sources, estimand, preliminary benchmark, and design decisions
- `analysis/rq1_risk_ratio.py` — reproducible RQ1 estimator
- `tests/test_rq1_risk_ratio.py` — synthetic-data validation
- `data/README.md` — microdata acquisition and provenance notes

## Likely next steps

1. Download the current responses and demographics files from the official Expert Mode page or Zenodo mirror.
2. Inspect actual headers and value domains; use command-line column overrides only if the published schema differs from the current defaults.
3. Run the estimator, retain `results/rq1.json`, and compare exact rates with the 83%/77% tracker benchmark.
4. Inspect eligibility and estimates over time to test sensitivity to changing signifier-presentation tiers.
5. Resolve whether demographic weighting is intended, then publish an Executive Summary and Quarto Full Report with exact counts, intervals, limitations, and source citations.

## Questions for the PI

- Should the published report use the design-specific label “prevalence ratio,” the requested “risk ratio,” or the combined “risk (prevalence) ratio”?
- Is an unweighted descriptive comparison the intended primary estimate, or should demographic/post-stratification weights be developed?
- Does the existing JJJ Pro Dawg Tracker's “non-fans” benchmark use explicit No responses co-observed with `happy` on the same respondent-day? The analysis assumes that definition.
