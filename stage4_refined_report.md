# Stage 4 Methodological Refinement: Train/Evaluation Isolation Forest

## Status
The original Stage 4 full-dataset Isolation Forest run is preserved unchanged as an **exploratory analysis**. This refinement is the cleaner held-out evaluation and does not overwrite the original Stage 4 result files.

## 1. Train/evaluation split
- Total: 3,000 records
- Training: 2,400 (80%)
- Held-out evaluation: 600 (20%)
- Random seed: 20260924
- Stratified by ground-truth anomaly category **only for split balance**. Ground-truth fields were never model inputs.

| Category | Train | Evaluation |
|---|---:|---:|
| Normal | 2,280 | 570 |
| Rule-detectable | 48 | 12 |
| ML-multivariate | 40 | 10 |
| Both-detectable | 32 | 8 |

The training set intentionally retains its synthetic anomalies. They were not removed because doing so would use ground truth to manufacture an artificially clean unsupervised training population and would change the stated research problem.

## 2. Final feature list
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

Excluded: record_id, patient_id, site_id, raw dates, and all ground_truth_* fields.

## 3. Preprocessing
Median imputation and StandardScaler were fit **only on the 2,400 training records**. The fitted transformations were then applied to the 600 evaluation records. No evaluation-set statistics were used to fit preprocessing.

Scaling is retained for continuity with exploratory Stage 4. Isolation Forest is tree-based, so scaling is not inherently required by the algorithm, but retaining the same preprocessing philosophy makes this refinement a cleaner comparison of data partitioning rather than a simultaneous pipeline redesign.

## 4. Isolation Forest configuration
- n_estimators: 300
- random seed: 20260924
- contamination sensitivity: 0.05, 0.08, 0.10
- primary setting: 0.08

The 0.08 primary setting was retained from the exploratory Stage 4 analysis for continuity. It was **not selected using held-out F1**. The 0.05 and 0.10 settings are sensitivity analyses. This avoids tuning the final conclusion against the evaluation labels.

The synthetic dataset contains 5% injected anomalies, but that fact was not used to select the primary contamination value. Using the known injected prevalence to choose the model threshold would make ground truth influence model configuration.

## 5. Held-out results

| Contamination | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.05 | 12 | 12 | 558 | 18 | 0.500 | 0.400 | 0.444 | 0.979 |
| 0.08 | 14 | 28 | 542 | 16 | 0.333 | 0.467 | 0.389 | 0.951 |
| 0.10 | 14 | 43 | 527 | 16 | 0.246 | 0.467 | 0.322 | 0.925 |

## 6. Category-level recall

At the primary contamination of 0.08:

- Rule-detectable: 2/12 = 16.7%
- ML-multivariate: 6/10 = 60.0%
- Both-detectable: 6/8 = 75.0%

For comparison, the 0.05 setting gave 60.0% ML-multivariate recall and 50.0% both-detectable recall; 0.10 gave 60.0% and 75.0%, respectively.

## 7. Exploratory versus locked evaluation

| Analysis | Contamination | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Exploratory full-dataset | 0.08 | 0.346 | 0.553 | 0.426 |
| Refined held-out evaluation | 0.05 | 0.500 | 0.400 | 0.444 |
| Refined held-out evaluation | 0.08 | 0.333 | 0.467 | 0.389 |
| Refined held-out evaluation | 0.10 | 0.246 | 0.467 | 0.322 |

The exploratory 0.08 run used the full dataset and reported 0.346 precision, 0.553 recall and 0.426 F1. The refined held-out 0.08 run reports 0.333 precision, 0.467 recall and 0.389 F1. The reduction in recall and F1 is expected when the model is evaluated on data it did not see during fitting, and it demonstrates why the exploratory result should not be treated as the primary generalization estimate.

## 8. Is fitting on anomalous training data appropriate?

Yes, for the stated unsupervised experiment, with an important caveat. Isolation Forest is not trained against the ground-truth labels. The training set therefore represents the unlabeled data distribution available to the detector. Synthetic anomalies remain in that distribution because removing them would require ground-truth knowledge and could make the training problem unrealistically clean. If anomalous observations form recurring or dense patterns, an unsupervised detector may partially absorb them as normal structure, reducing recall. That limitation is part of the result rather than something to engineer away.

## 9. Does the original Stage 4 conclusion remain supported?

**Directionally yes, but more cautiously.** The locked held-out analysis still detects a majority of the specifically constructed ML-multivariate anomalies at the primary setting (60%) while the deterministic rules missed that category in Stage 3. It also detects 75% of the both-detectable category. However, overall held-out recall is only 46.7% at contamination 0.08, precision is 33.3%, and false positives remain substantial. The refined result therefore supports the narrower statement that Isolation Forest **can identify some multivariate patterns that conventional rules do not capture in this synthetic experiment**, not that it reliably detects such anomalies or outperforms rules.

The result is also sensitive to contamination. The tested 0.05 setting produced the highest F1 among these three settings (0.444), but it is not promoted to the primary setting because the primary parameter was not chosen by optimizing the held-out labels. This is reported as sensitivity rather than post-hoc tuning.

## 10. Stage 4 stopping point

No Stage 5 evaluation/comparison workflow has been performed. This report closes the methodological refinement at Stage 4.
