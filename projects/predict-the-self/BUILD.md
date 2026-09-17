# Build and validate the Predict the Self reports

The Full Report is a two-chapter Quarto HTML book: `index.qmd` introduces the
claim boundary and `report.qmd` contains the evidence, method, complete public
development scorecard, artifacts, and references. Two chapters suit this
report; Virtual CSSERG does not prescribe an exact chapter count.

Quarto renders into ignored project-local `_book/`. The guarded publisher then
replaces the complete public report tree, including copied reproducibility
artifacts, so stale generated libraries cannot survive. It also preserves the
matching `report/artifacts/` URLs as byte-identical compatibility copies
and removes Quarto-introduced line-end whitespace from generated HTML. The
Executive Summary is maintained as static HTML. `short-report.md` is the
derivative PDF source.

The host has no TeX PDF engine, so the short-report renderer uses optional
build-only packages. They do not become website or production dependencies.

Regenerate the post hoc development diagnostics from the pinned benchmark
checkout before building the reports. The script verifies the recorded hashes
of both the development data and authoritative evaluator:

```bash
python3 projects/predict-the-self/analysis/analyze_dev_diagnostics.py \
  --benchmark-dir /path/to/predict-future-selves-at-9b6a766
```

```bash
python3 -m pip install --target /tmp/predict-self-publishing-deps \
  -r projects/predict-the-self/requirements-publication.txt
XDG_CACHE_HOME=/tmp/predict-self-quarto-cache \
  quarto render projects/predict-the-self
python3 projects/predict-the-self/analysis/publish_full_report.py
PYTHONPATH=/tmp/predict-self-publishing-deps \
  python3 projects/predict-the-self/analysis/render_short_report.py
```

Validate the research code, guarded publisher, three-form publication, v1
promise groups, and whitespace:

```bash
python3 -m unittest discover -s projects/predict-the-self/tests -v
PYTHONPATH=/tmp/predict-self-publishing-deps \
  python3 projects/predict-the-self/analysis/verify_publication.py
python3 projects/vcsserg-repo-v1/verify_v1.py
git diff --check
```

The publication verifier accepts any short-report length from one through ten
nonempty pages and checks that body text occupies both columns. No exact page
count is required.
