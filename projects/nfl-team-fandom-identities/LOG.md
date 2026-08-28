# NFL Team Fandom Identities

Below are log entries from Scholars. This is an append-only file.

## 2026-08-28 — Ceetown

- **Start:** 2026-08-28 21:52:59 UTC
- **Project:** NFL Team Fandom Identities
- **Planned scope:** Establish a reproducible RQ1 foundation by obtaining and inspecting the Ipseity Daily Expert Mode microdata, documenting its structure and relevant fields, and implementing an initial Cleveland Browns fan–`happy` risk-ratio analysis if the available data support it.
- **Work completed:** Reviewed the official Ipseity Daily site, Expert Mode instructions, Zenodo metadata, the *Building the Ipseome* preprint, and the JJJ Pro Dawg Tracker. Documented the data design and RQ1 estimand in `METHODS.md`. Implemented `analysis/rq1_risk_ratio.py` to inner-join Expert Mode files on `(hashed_respondent_id, obs_date)`, restrict to respondent-days explicitly answering both target signifiers, audit joins and duplicates, produce a 2 × 2 table, estimate the risk/prevalence ratio and prevalence difference, calculate analytic intervals, and calculate respondent-cluster bootstrap intervals. Added data provenance hashes, local data instructions/ignores, and three synthetic-data tests.
- **Preliminary result:** The first-party JJJ Pro Dawg Tracker reports rounded `happy` prevalence of 83% for Browns fans and 77% for non-fans. This implies an approximate risk (prevalence) ratio of 1.08 and a +6 percentage-point difference. This is a benchmark, not the final RQ1 result: rounding prevents recovery of exact cell counts or sampling uncertainty.
- **Verification:** `python3 -m unittest discover -s projects/nfl-team-fandom-identities/tests -v` passed all 3 tests. `python3 -m py_compile` passed for the analysis and test modules. `git diff --check` reported no whitespace errors.
- **Problems encountered:** The official and Zenodo pages were browsable, but shell network access failed DNS resolution and the browser could not save CSV responses into the workspace. The microdata therefore could not be inspected or analyzed directly in this iteration. No exact estimate was published.
- **Methodological decision:** The requested calculation is a risk ratio, but “prevalence ratio” is more precise for a contemporaneous cross-sectional comparison. The implementation uses risk (prevalence) ratio as the primary effect size and prevalence difference as a complementary measure; it does not substitute an odds ratio or make a causal claim.
- **Questions for Dr. Jones:** (1) Which label should lead in publication: risk ratio, prevalence ratio, or risk (prevalence) ratio? (2) Is the primary estimate intended to be unweighted, or should demographic/post-stratification weights be developed? (3) Does the JJJ Pro Dawg Tracker define “non-fans” as explicit No responses with same-day `happy` observation, matching this implementation?
- **Proposed next step:** Acquire the two current CSVs in a network-enabled iteration, verify their actual schema/value domains, run the estimator, compare the exact output with the 83%/77% benchmark, and inspect date sensitivity before publishing.
- **End:** 2026-08-28 22:01:46 UTC
