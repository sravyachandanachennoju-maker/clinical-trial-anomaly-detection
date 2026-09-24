# Stage 4: Isolation Forest

## Model design

- Algorithm: Isolation Forest
- Random seed: 20260924
- Trees: 300
- Main contamination setting: 0.08
- Sensitivity settings: [0.05, 0.08, 0.1]
- Site ID: excluded from model, retained for post-hoc analysis
- Patient/record IDs: excluded
- Ground-truth labels: excluded
- Global/group z-scores: not used
- Missing values: median imputation within the model preprocessing pipeline
- Scaling: StandardScaler after imputation
- Derived feature: ALT/AST ratio

The contamination value is a model parameter controlling the expected fraction of observations treated as outliers by the fitted detector. It is not evidence that the model independently discovered that fraction of anomalies.

## Main results

|   TP |   FP |   TN |   FN |   precision |   recall |       F1 |   specificity |   flagged |
|-----:|-----:|-----:|-----:|------------:|---------:|---------:|--------------:|----------:|
|   83 |  157 | 2693 |   67 |    0.345833 | 0.553333 | 0.425641 |      0.944912 |       240 |

## Contamination sensitivity

|   contamination |   flagged |   TP |   FP |   TN |   FN |   precision |   recall |       F1 |   specificity |
|----------------:|----------:|-----:|-----:|-----:|-----:|------------:|---------:|---------:|--------------:|
|            0.05 |       150 |   64 |   86 | 2764 |   86 |    0.426667 | 0.426667 | 0.426667 |      0.969825 |
|            0.08 |       240 |   83 |  157 | 2693 |   67 |    0.345833 | 0.553333 | 0.425641 |      0.944912 |
|            0.1  |       300 |   90 |  210 | 2640 |   60 |    0.3      | 0.6      | 0.4      |      0.926316 |

## Category-level recall

| ground_truth_category   |   records |   detected |   missed |   recall |
|:------------------------|----------:|-----------:|---------:|---------:|
| rule_detectable         |        60 |         14 |       46 | 0.233333 |
| ml_multivariate         |        50 |         36 |       14 | 0.72     |
| both_detectable         |        40 |         33 |        7 | 0.825    |

## Detection overlap

| group                 |   records |
|:----------------------|----------:|
| neither_method        |      2696 |
| isolation_forest_only |       192 |
| rules_only            |        64 |
| both_methods          |        48 |

## Interpretation

These are actual outputs from the frozen Stage 2 dataset and the independent Stage 4 feature/model pipeline.

The `ground_truth_*` columns are used only for evaluation after prediction. Site is retained separately for post-hoc analysis and is not a predictive feature.

The ML-only records should be reviewed qualitatively before making any claim that they represent meaningful additional clinical-data-quality detection. An Isolation Forest flag means that the observation is unusual in the supplied feature space; it does not establish that the record is erroneous.

The results do not determine whether Isolation Forest is better than rules. The relevant question is whether it contributes useful complementary detections without an unacceptable false-positive burden.
