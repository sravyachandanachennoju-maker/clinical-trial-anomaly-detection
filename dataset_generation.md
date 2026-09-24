# Dataset Generation Documentation

## Locked dataset

The final synthetic dataset contains:

- 3,000 records
- 10 synthetic sites
- visit numbers 1–5
- 731 unique patient IDs represented
- 750 possible participant IDs in the generation pool
- random seed `20260924`
- 2,850 normal records
- 150 injected anomalies

The anomaly prevalence is therefore 5%.

## Synthetic data domains

The documented data-generating process includes:

### Study variables
- age
- sex
- treatment arm
- site
- visit number
- patient identifier

### Timing
- visit date
- data-entry date
- data-entry delay

### Laboratory variables
- ALT
- AST
- hemoglobin
- creatinine

### Operational variables
- query count
- protocol deviation
- laboratory missingness indicators

The values are synthetic and should not be interpreted as clinical reference ranges.

## Ground-truth categories

The 150 injected anomalies are mutually exclusive:

| Category | n |
|---|---:|
| Rule-detectable | 60 |
| ML-multivariate | 50 |
| Both-detectable | 40 |

### Rule-detectable mechanisms

- missing required laboratory value
- date inconsistency
- excessive entry delay
- duplicate record
- invalid visit sequence

### ML-multivariate mechanisms

- ALT/AST ratio anomaly while individual values remain plausible
- query-delay/site pattern
- unusual joint laboratory profile
- unusual visit/laboratory/query combination

### Both-detectable mechanisms

Examples combine an explicit deterministic problem with a multivariate signal.

## Ground-truth policy

`ground_truth_anomaly`, `ground_truth_category`, and `ground_truth_types` are evaluation fields only.

They must never be used as model inputs.

## Reproducibility

The dataset-generation seed is `20260924`. The generation specification is also preserved in:

`results/stage2_dataset_specification.md`

and validation is preserved in:

`results/stage2_validation.md`.
