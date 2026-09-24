# Data

The repository contains a **fully synthetic clinical-trial-like dataset**. It contains no real patient records and no directly identifiable clinical information.

## Locked dataset

- 3,000 records
- 10 synthetic sites
- visit numbers 1–5
- 731 represented patient IDs from a pool of 750 possible IDs
- 2,850 ground-truth normal records
- 150 injected anomalies
- anomaly prevalence: 5%
- generation seed: `20260924`

The anomaly labels in the dataset are **experimental ground truth**, created by controlled injection. They are not clinical adjudications.

See `docs/dataset_generation.md` and `data/data_dictionary.csv` for the data-generating specification and field definitions.
