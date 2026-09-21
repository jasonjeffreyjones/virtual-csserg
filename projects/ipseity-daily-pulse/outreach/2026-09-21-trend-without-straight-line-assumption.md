# A trend without the straight-line assumption

**Draft status:** Internal; not published or approved by Dr. Jones.

## Suggested post

A straight line is not the only way to check whether an identity signifier is
changing.

We split Ipseity Daily's current observation window into two calendar halves
and compared endorsement prevalence after February 12, 2026, with prevalence
on or before that date. All 20 signifiers selected as the most extreme linear
trends kept the same direction in this simpler comparison. For `beautiful`,
endorsement was 33.2% in the early half and 50.7% in the late half, a
17.5-percentage-point difference (respondent-clustered 95% interval 8.4 to
26.7 points).

That agreement is a robustness check, not proof of population change. The
signifiers were selected from 704 linear trends, no primary trend survived
either multiplicity screen, and different respondents contributed over time.
The useful result is narrower: these selected directions are not artifacts of
fitting one straight line through the whole period.

Source: [Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html)

## Visual

Use
[`outputs/leader-early-late-sensitivity.svg`](../outputs/leader-early-late-sensitivity.svg).

Suggested alt text: “Point and interval plot of late-half minus early-half
endorsement prevalence for five positive and five negative linear-trend
leaders. All ten displayed contrasts point in the same direction as their
linear slopes; several clustered intervals cross zero.”

## Evidence note

The values use canonical microdata through 2026-09-20, retrieved at
2026-09-21T10:06:18Z. The common split is the full dataset window's calendar
midpoint: the early period is 2025-07-08 through 2026-02-12, and the late
period is 2026-02-13 through 2026-09-20. The contrast is unweighted and does
not adjust for changing sample composition, shorter reversals, or selection of
extreme linear slopes. Full estimates and limitations are recorded in
[`CURRENT-FINDINGS.md`](../CURRENT-FINDINGS.md) and
[`outputs/leader-early-late-sensitivity.csv`](../outputs/leader-early-late-sensitivity.csv).
