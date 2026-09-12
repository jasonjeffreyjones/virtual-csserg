---
title: "NFL Team Fandom Identities"
status: Active
updated: 2026-09-11T03:14:50Z
---

# NFL Team Fandom Identities — Current State

Updated September 11, 2026 by Aleph Initial Alpha.

## Current focus and decisions

RQ1 remains the priority. Operative PI guidance is recorded in legacy `PI.md`:
use **prevalence ratio**, define it and relate it to risk ratio, lead with an
unweighted descriptive comparison, and attempt demographic weighting in the
full report appendix. The PI confirmed that tracker non-fans are explicit No
responses co-observed with happy. These earlier questions are resolved.

`DIALOG.md` is now the ongoing iteration record. Existing `LOG.md` and `PI.md`
are preserved unchanged as historical records. The August 29 interrupted
iteration left exact results, code, and drafts beyond what the old STATE
recorded; those artifacts were recovered and assessed this iteration.

## Current verified findings

- Current publication uses Zenodo record 22139541, retrieved September 11.
  Both published MD5 checksums passed; input SHA-256 hashes are retained.
- The archive contains 675,480 response rows and 8,776 demographics rows;
  8,235 eligible respondent-days from 4,686 people, July 8, 2025–August 27, 2026.
- Exact cells: fan happy Yes/No = 263/53; explicit non-fan happy Yes/No =
  6,062/1,857. Happy endorsement is **83.23% versus 76.55%**.
- Unweighted **PR 1.087** (respondent-cluster bootstrap 95% interval
  **1.007–1.160**); difference **+6.68 points** (interval **+0.56–+12.17**).
  1,392 people recur. Bootstrap: 2,000 finite replicates, seed 20260828.
- Complete-case unweighted PR 1.085; pooled age-sex calibration PR 1.080;
  common-distribution standardization PR 1.078. Eight ACS national adult
  target counts independently verified. Weights are appendix sensitivities,
  not population estimates; weighted intervals are not yet computed.
- Twelve of fourteen monthly PRs exceed 1, but monthly fan counts are 15–29.
  No causal, representative-population, or game-specific claim is supported.

## Publication and completed work

- Full Report: `index.qmd` and `_quarto.yml`, a single-chapter Quarto HTML
  book with executed R tables/calculation, figures, APA bibliography, appendix,
  provenance comparison, downloadable aggregate artifacts, and report links.
- Generated book: `website/projects/nfl-team-fandom-identities/report/index.html`.
- Executive summary: `website/projects/nfl-team-fandom-identities/index.html`,
  seven findings and exactly one dense key figure.
- Short report: `short-report.md` and `analysis/render_short_report.py` produce
  `website/projects/nfl-team-fandom-identities/short-report.pdf`, two pages,
  two columns, with references and links to both HTML reports.
- Homepage links and Aleph Initial Alpha's current project assignment updated.
- Seven existing synthetic-data tests pass. Publication verifier passes:
  exact arithmetic, input consistency, artifact copies, local links/anchors,
  reported numbers, bibliography, figure count, required phrase, PDF page count
  and two-column text placement. Both PDF pages and key figure visually checked.
- Automation commits, pushes, and deploys after the Scholar finishes. This
  iteration prepared the website files; it did not deploy them manually.

## Active data issue

The primary-host URLs returned only 10,570 response rows and 151 demographics
rows, eligible dates July 8–14, 2025, despite the page advertising 677,121 rows
through August 28, 2026. Cause unknown. The subset was analyzed and kept
separate; it is not cumulative data. Zenodo provides a usable fixed archive.

Historical `results/rq1.json` reports 8,253 eligible days through August 28,
PR 1.088. Its exact inputs were unavailable this iteration. Retained unchanged;
not described as independently reproduced. Historical `report.qmd` and
`report.rmarkdown` are not active render targets; `BUILD.md` identifies these.

## Important files

- `METHODS.md`, `BUILD.md`: current methods, source citations, build instructions.
- `analysis/rq1_risk_ratio.py`: primary estimator and audit.
- `analysis/rq1_weighted_sensitivity.py`: weighting, complete-case estimate,
  input provenance, cell diagnostics.
- `results/rq1_zenodo_20260911.json`, `results/rq1_weighted_zenodo_20260911.json`:
  current verified results.
- `results/acquisition_20260911.json`, `results/acs_target_check_20260911.json`:
  source verification; `results/rq1_retrieved_20260911.json`: short-host subset.
- `analysis/verify_publication.py`: publication checks.

## Host and build limitations

Preflight: 2 logical CPUs, 3.7 GiB RAM, 65 GiB free disk; hard envelope of
1 CPU, 3000M memory, no Scholar swap, 55 minutes. Work used lightweight
streaming CSV analysis within that envelope. Installed Quarto 1.10.18,
Python 3.12.3, and R 4.3.3 were usable. No TeX PDF engine was available;
ordinary build-only ReportLab/pypdf packages supplied PDF production in the
existing Python runtime. No system runtime was installed or replaced.
Quarto required a writable cache path via XDG_CACHE_HOME; details in BUILD.md.

## Next steps and PI question

1. PI question: Is the primary-host one-week response intentional, or should
   those endpoints expose the advertised cumulative snapshot? Current work
   proceeds using the fixed archive; no answer is required to use this report.
2. Recover or archive the exact historical August 28 input files if available.
3. Evaluate equal-respondent weighting and calendar composition sensitivity;
   current intervals do not handle common date shocks.
4. Add uncertainty for demographic sensitivity if it becomes substantively useful.
5. Continue RQ1 before expanding to all-team RQ2 or weekly-season RQ3.
