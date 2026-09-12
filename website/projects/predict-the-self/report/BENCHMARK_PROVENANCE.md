# Predict Future Selves benchmark provenance

The public benchmark was retrieved over HTTPS from
[`jasonjeffreyjones/predict-future-selves`](https://github.com/jasonjeffreyjones/predict-future-selves)
on 2026-08-30 and checked out at the following immutable commit:

```text
9b6a766712583fec8d3182957260b1123fbfa146
```

The commit's subject is `Publish Future Selves benchmark v1`. The checkout was
detached at that commit before any input was read or prediction was generated.

## SHA-256 checksums

### Prediction inputs

```text
720aea3c4a9f7ad96ff3960ad6faa36991e1771dc43793c9e16e33b583bd4a48  data/train.csv
afe74265475f1897161f54ac91395ded74d839e43236e8f4d189d91f9b40651a  data/dev.csv
abb06130b70f4d8a34024bd4094843952a10ad85a451fc336619ec7ef63cc024  data/test_input.csv
4240d8332290f57a92d6d2c0bbf3cf6fd7b6d1569d88502cd2b43cffe3d5f063  data/sample_submission.csv
```

### Governing documentation and evaluation tools

```text
5560011676e902194a69011a5ff05824c71dad3c79a1db7dfb540e44d7557811  README.md
adb84983176bb6cae981cba1f2ac3adcb6337b465f1604ca046d45b3db2054a2  docs/data_statement.md
dac4f93308b27023a8cd9b0dba2fcbcdf25ea8e84284caf5be8790846561a96e  docs/evaluation.md
80edfe8f690ac08d70fcb48a368f8cd0c49323528385cb4065e19366683c8715  docs/participation.md
1236dbcca70129f6200c2703dd67649dbfa760a2a7f74402fa1d3d956b97b2ae  scripts/evaluate_predictions.py
3eaa792366719f7582a5fa1c1b78d6ad84afa528d1309b3372130b950fbdaf85  scripts/validate_submission.py
```

The benchmark CSVs were not copied into this repository. They remain licensed
CC BY-NC-SA 4.0 by Dr. Jason Jeffrey Jones. The submitted prediction CSV is a
data adaptation and is distributed under the same license.
