# Stage 2 Synthetic Dataset Specification

## Study size
- Total records: 3,000
- Normal records: 2,850
- Injected anomalous records: 150
- Overall anomaly prevalence: 5.0%
- Random seed: 20260924

The 5% prevalence is a deliberately controlled experimental rate: low enough to create a majority-normal dataset and class imbalance, but high enough to leave approximately 150 known anomalies for meaningful error analysis.

## Ground-truth categories

| Category | Records | % of all records | % of anomalies |
|---|---:|---:|---:|
| Normal | 2,850 | 95.00% | - |
| Rule-detectable | 60 | 2.00% | 40.0% |
| ML/multivariate | 50 | 1.67% | 33.3% |
| Both-detectable | 40 | 1.33% | 26.7% |
| Total | 3,000 | 100% | 100% |

The categories are mutually exclusive by construction. They describe the intended detection mechanism, not the eventual observed performance. Stage 3 and Stage 4 will determine whether the methods actually detect them.

## Ground-truth labeling strategy

`ground_truth_anomaly` is 1 only for records that received an intentional anomaly injection and 0 otherwise.

`ground_truth_category` records the pre-specified injection category.

`ground_truth_types` records the specific injection mechanism.

These fields are retained for evaluation only. They will never be included as Isolation Forest input features.

The labels do not represent clinical truth. They represent the known truth of the synthetic experimental setup.

## Variable distributions and generation ranges

### Demographic / study variables
- Age: truncated Normal(mean=52, SD=14), bounded 18-85 years.
- Sex: F 52%, M 48%.
- Treatment: Placebo 25%, Drug_A 37.5%, Drug_B 37.5%.
- Visit number: 1-5 with probabilities 20%, 20%, 22%, 20%, 18%.
- 10 synthetic sites.
- 750 synthetic participant identifiers, assigned to one site each.

### Timing
- Visit dates: study-start anchor plus visit-based 28-day spacing with ±3-day scheduling variation.
- Data-entry delay: right-skewed Gamma(shape=2.2, scale=1.8) plus a small site effect, normally clipped to 0-21 days.
- Data-entry date = visit date + delay for normal records.

### Laboratory variables
These are synthetic values, not clinical reference standards.
- ALT: lognormal distribution centered around the mid-20s, clipped 8-95.
- AST: correlated with ALT, clipped 8-90.
- Hemoglobin: sex-dependent Normal distribution, clipped 8.5-17.5.
- Creatinine: sex-dependent Normal distribution, clipped 0.45-1.55.

### Operational variables
- Query count: Poisson distribution centered around approximately 1-2 queries, with a small site effect, clipped 0-9.
- Protocol deviation: Bernoulli probability 3.5%.

## Injected anomaly mechanisms

### Rule-detectable group, n=60
- Missing required laboratory value
- Date inconsistency
- Excessive entry delay
- Duplicate record
- Invalid visit sequence

These contain explicit conditions that a deterministic rule can be designed to identify.

### ML/multivariate group, n=50
- ALT/AST ratio anomaly while both remain individually plausible
- High query count combined with normal entry delay and site context
- Unusual joint laboratory profile
- Unusual combination of visit number, laboratory values and query activity

These are deliberately designed so that individual variables generally remain within broad plausible ranges.

### Both-detectable group, n=40
Each contains an explicit deterministic problem plus an additional multivariate signal, for example:
- missing ALT + elevated query count
- excessive entry delay + unusual laboratory profile
- date inconsistency + elevated query count

## Leakage controls

Excluded from Isolation Forest:
- `record_id`
- `patient_id`
- `ground_truth_anomaly`
- `ground_truth_category`
- `ground_truth_types`

Identifiers will not be treated as numerical predictors.

Raw dates will not be passed directly to the model. Stage 4 will derive meaningful timing features.

Categorical variables will be encoded rather than numerically ranking categories.
