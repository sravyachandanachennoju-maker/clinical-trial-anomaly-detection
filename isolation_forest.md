# Isolation Forest

Isolation Forest is used as an unsupervised anomaly-detection layer.

## Locked model

- 300 trees
- random seed: `20260924`
- primary contamination: `0.08`
- sensitivity settings: `0.05`, `0.08`, `0.10`

The primary setting was retained from the experimental design and was not selected by maximizing held-out F1.

## Features

The model used:

- age
- visit_number
- data_entry_delay
- ALT
- AST
- hemoglobin
- creatinine
- query_count
- protocol_deviation
- ALT_missing
- AST_missing
- hemoglobin_missing
- creatinine_missing
- ALT_AST_ratio

Excluded:

- record_id
- patient_id
- site_id
- raw dates
- ground-truth labels

## Preprocessing

Median imputation and StandardScaler were fitted only on the 2,400-record training set. The fitted transformations were then applied to the 600 held-out evaluation records.

## Primary held-out result

- TP = 14
- FP = 28
- TN = 542
- FN = 16
- Precision = 33.3%
- Recall = 46.7%
- F1 = 38.9%
- Specificity = 95.09%

## Interpretation

An Isolation Forest flag indicates unusualness in the modeled feature space. It does not establish that a record is erroneous.

The model detected 6/10 held-out ML-multivariate synthetic ground-truth anomalies, but it also generated 28 false positives.
