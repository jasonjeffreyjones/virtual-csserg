# Ipseity Daily Pulse

This Project monitors and evaluates the public
[Ipseity Daily](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/)
from outside its production system. It does not modify collection, data,
schedules, hosting, or public Ipseity Daily pages.

Start with the PI-owned [`PROJECT.md`](PROJECT.md), current handoff in
[`STATE.md`](STATE.md), and bounded [`DIALOG.md`](DIALOG.md). The current
reader-facing results are in [`CURRENT-FINDINGS.md`](CURRENT-FINDINGS.md), and
[`ANALYSIS.md`](ANALYSIS.md) documents reproduction.

From the repository root, run the project checks with:

```bash
python3 -m unittest discover -s projects/ipseity-daily-pulse/tests -v
python3 projects/vcsserg-repo-v1/verify_v1.py
```

The live monitor command is intentionally omitted from routine validation
because each successful invocation appends a new outside-in observation. Run it
at most once per UTC day unless a suspected problem warrants confirmation:

```bash
python3 projects/ipseity-daily-pulse/analysis/monitor.py
```

Current outputs include pooled trends, composition-and-calendar sensitivity,
a raw and composition-and-calendar-adjusted two-period early-versus-late
sensitivity, a four-period trajectory diagnostic, and a three-way all-response
pooled, repeat-sample pooled, and repeat-respondent fixed-effect sensitivity for
the raw trend leaders. The monitor also renders endpoint status, data lag, and
validated observation growth across the append-only check history.

Publication remains `Unpublished`; no empty report shell exists under
`website/projects/`.
