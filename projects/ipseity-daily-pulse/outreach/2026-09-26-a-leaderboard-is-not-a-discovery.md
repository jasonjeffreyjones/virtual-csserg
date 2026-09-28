# A trend leaderboard is not a discovery list

**Publication status:** Published in the Project blog on September 26, 2026.

## Post

Ipseity Daily offers hundreds of identity signifiers to explore. That makes the
most dramatic trend estimates easy to find—and easy to overread.

In the current data, 704 signifiers have enough observations and calendar
coverage for the same descriptive trend model. `beautiful` has the largest
positive point estimate at +24.0 percentage points per year, while
`star wars fan` has the most negative at -14.2. Yet after screening all 704
tests together, **none** passes either the 5% Benjamini–Hochberg or Bonferroni
threshold.

This does not make the data uninteresting. It changes the question. The
leaderboard identifies patterns to monitor and test on later data; it does not
identify 704 independent chances to announce a winner.

Source: [Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html)

## Visual

Use
[`outputs/annual-prevalence-growth-histogram.svg`](../outputs/annual-prevalence-growth-histogram.svg).

Suggested alt text: “Histogram of estimated annual prevalence slopes for 704
identity signifiers. Most estimates cluster near zero, with a median of +0.5
percentage points per year and sparse negative and positive tails.”

## Evidence note

The values use canonical microdata through 2026-09-25, retrieved at
2026-09-26T10:02:00Z. Models are unweighted linear-probability descriptions
with respondent-clustered uncertainty. Neither adjustment establishes
population representativeness or corrects changing unobserved composition,
functional-form error, or the selection of extrema. Full methods and results
are in [`CURRENT-FINDINGS.md`](../CURRENT-FINDINGS.md) and
[`outputs/signifier-growth.csv`](../outputs/signifier-growth.csv).
