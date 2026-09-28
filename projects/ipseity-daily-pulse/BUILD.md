# Publication build

The canonical analysis is refreshed by `analysis/monitor.py`; its live mode
must run at most once per UTC day unless a suspected failure warrants a second
check. The full report is a one-chapter Quarto book sourced from `index.qmd`.
The Executive Summary and Project blog are maintained as static HTML. The
short report is derived from `short-report.md` with the optional build-only
ReportLab and pypdf packages already used elsewhere in this repository. If
they are absent, install the pinned `requirements-publication.txt` into a
temporary target and set `PYTHONPATH` for the render and verification commands;
they are not production-site dependencies.

From the repository root, refresh public aggregate artifacts after a successful
monitor run:

```bash
mkdir -p website/projects/ipseity-daily-pulse/images \
  website/projects/ipseity-daily-pulse/artifacts
cp projects/ipseity-daily-pulse/outputs/*.svg \
  website/projects/ipseity-daily-pulse/images/
cp projects/ipseity-daily-pulse/outputs/current-summary.json \
  projects/ipseity-daily-pulse/outputs/*.csv \
  projects/ipseity-daily-pulse/data/monitoring-history.csv \
  website/projects/ipseity-daily-pulse/artifacts/
python3 projects/ipseity-daily-pulse/analysis/render_blog.py
XDG_CACHE_HOME=/tmp/ipseity-pulse-quarto-cache \
  quarto render projects/ipseity-daily-pulse
PYTHONPATH=/tmp/ipseity-pulse-publishing-deps python3 \
  projects/ipseity-daily-pulse/analysis/render_short_report.py
```

The Quarto cache override uses a permitted temporary cache; it does not replace
or modify the installed runtime. The post-render normalizer makes the bypass
link first in body order, names generated navigation landmarks, and adds
explicit scope to table headers.

Validate with:

```bash
python3 -m unittest discover -s projects/ipseity-daily-pulse/tests -v
PYTHONPATH=/tmp/ipseity-pulse-publishing-deps python3 \
  projects/ipseity-daily-pulse/analysis/verify_publication.py
python3 projects/vcsserg-repo-v1/verify_v1.py
git diff --check
```

The publication contains aggregate outputs only. The canonical source file is
not committed or copied into `website/`; its URL and SHA-256 provenance are
published instead.
