# Local data directory

Download the two cumulative Expert Mode files from the [Ipseity Daily download page](https://jasonjones.ninja/social-science-dashboard-inator/ipseity-daily/download.html):

- `ipseity-daily-responses.csv`
- `ipseity-daily-demographics.csv`

The files are public research data, but they are not committed here because they update frequently and would add unnecessary repository history. The analysis records SHA-256 hashes and the eligible observation-date range so a result can be tied to exact inputs.

If the primary host is unavailable, use [Zenodo record 22139541](https://zenodo.org/records/22139541).

## September 11, 2026 acquisition

The primary-host files retrieved in this iteration contain only 10,570
response rows and 151 demographics rows (eligible dates July 8–14, 2025).
They do not match the page's advertised cumulative coverage. They are
retained locally under the original filenames and analyzed separately.

The current report instead uses `zenodo-responses.csv` and
`zenodo-demographics.csv` from fixed record 22139541. Published MD5 values
were verified; SHA-256 hashes and URLs are in
`../results/acquisition_20260911.json`. See `../BUILD.md` for exact commands.
The archive has 675,480 response rows and 8,776 demographics rows, with
eligible dates through August 27, 2026. Do not silently substitute a new
snapshot for these inputs or treat the old result hashes as current.
