# Build and validate the VCSSERG v1 reports

The Full Report source is `index.qmd`, currently configured as a one-chapter
Quarto book by `_quarto.yml`; that chapter count is an editorial choice, not a
requirement. Quarto renders into the ignored project-local `_book/`, then
`analysis/publish_full_report.py` safely replaces the complete generated tree at
`website/projects/vcsserg-repo-v1/report/`. Keeping Quarto's output inside its
project lets it clean stale libraries without warnings. The Executive Summary
is maintained as static HTML, and `short-report.md` is the derivative PDF
source.

Quarto uses a writable temporary cache. The host has no TeX PDF engine, so the
short-report renderer uses the optional build-only packages in
`requirements-publication.txt`. These packages do not become website or
production dependencies. The current short report occupies two pages; the
requirement is two columns and no more than ten pages, not an exact page count.

```bash
python3 -m pip install --target /tmp/vcsserg-v1-publishing-deps \
  -r projects/vcsserg-repo-v1/requirements-publication.txt
XDG_CACHE_HOME=/tmp/vcsserg-v1-quarto-cache \
  quarto render projects/vcsserg-repo-v1
python3 projects/vcsserg-repo-v1/analysis/publish_full_report.py
PYTHONPATH=/tmp/vcsserg-v1-publishing-deps \
  python3 projects/vcsserg-repo-v1/analysis/render_short_report.py
```

Validate the scaffold workflow, three-form publication, all Version 1 promise
groups, and repository whitespace:

```bash
python3 python/scholar_roster.py
python3 -m unittest discover -s projects/vcsserg-repo-v1/tests -v
PYTHONPATH=/tmp/vcsserg-v1-publishing-deps \
  python3 projects/vcsserg-repo-v1/analysis/verify_publication.py
python3 projects/vcsserg-repo-v1/verify_v1.py
git diff --check
```

The publication verifier checks reciprocal local links and fragments, exactly
one Executive Summary figure, the required Full Report phrase, PDF link
annotations, both PDF body columns, nonempty pages, and the ten-page ceiling.

After the normal commit, push, and deployment, compare every expected public
file byte with its production URL:

```bash
python3 projects/vcsserg-repo-v1/analysis/check_production_parity.py
```

This network check does not use `.env` and cannot detect extra stale remote
files. The normal deployment therefore follows its deleting transfer with an
authenticated checksum/inventory dry run and exits nonzero on any residual
difference. Do not run the deployment manually during a Scholar iteration;
observe its result in the host-managed post-iteration workflow.
