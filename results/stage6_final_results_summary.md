# Stage 6: Final Results Validation and Research Visualization

## 1. Results consistency audit

All Stage 5 primary results passed the internal consistency audit.

For both methods:
- TP + FP + TN + FN = 600.
- Precision = TP / (TP + FP).
- Recall = TP / (TP + FN).
- Specificity = TN / (TN + FP).
- F1 = harmonic mean of precision and recall.

The held-out evaluation population contains 600 records and 30 synthetic ground-truth anomalies:
- rule-detectable: 12
- ML-multivariate: 10
- both-detectable: 8

Detection overlap totals 600 records.

No numerical discrepancy was found.

## 2. Primary comparison

| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule-Based | 20 | 2 | 568 | 10 | 90.9% | 66.7% | 76.9% | 99.65% |
| Isolation Forest | 14 | 28 | 542 | 16 | 33.3% | 46.7% | 38.9% | 95.09% |

These are the primary apples-to-apples results on the same 600 held-out records.

## 3. Category-level findings

| Category | n | Rule-Based Recall | Isolation Forest Recall |
|---|---:|---:|---:|
| rule-detectable | 12 | 100.0% | 16.7% |
| ML-multivariate | 10 | 0.0% | 60.0% |
| both-detectable | 8 | 100.0% | 75.0% |

The ML-multivariate category is small (n=10), so its recall estimate should be interpreted cautiously.

## 4. Detection overlap

- Both methods detected: 8
- Rule-based only: 14
- Isolation Forest only: 34
- Neither: 544

Among the 34 Isolation-Forest-only records, 6 were synthetic ground-truth anomalies and 28 were ground-truth normal records. Therefore, Isolation-Forest-only must not be treated as synonymous with true anomaly.

## 5. False-positive burden

- Rule-Based: 2 false positives
- Isolation Forest: 28 false positives

The rule-based false positives were associated with the existing duplicate-rule behavior documented in Stage 3.

Isolation Forest false positives included unusual but potentially plausible combinations of laboratory, operational, and participant-level features. These should be interpreted as unusual observations requiring review, not automatically as incorrect clinical records.

## 6. Sensitivity analysis

The pre-specified primary Isolation Forest contamination was 0.08.

| Contamination | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.05 | 50.0% | 40.0% | 44.4% |
| 0.08 | 33.3% | 46.7% | 38.9% |
| 0.10 | 24.6% | 46.7% | 32.2% |

The primary setting was not selected by maximizing held-out F1.

## 7. ML-only anomaly examples

Six synthetic ground-truth anomalies were detected by Isolation Forest but missed by the rule-based system. They include subtypes such as `alt_ast_ratio`, `lab_profile`, and `visit_lab_query_pattern`.

These records illustrate multivariate unusualness in the synthetic feature space. No clinical-error interpretation is assigned to them.

## 8. Statistical uncertainty

Wilson 95% confidence intervals:

- Rule-Based precision: 90.9% (72.2%–97.5%)
- Rule-Based recall: 66.7% (48.8%–80.8%)
- Isolation Forest precision: 33.3% (21.0%–48.4%)
- Isolation Forest recall: 46.7% (30.2%–63.9%)

Category-level denominators are small, particularly for both-detectable (n=8).

## 9. Key methodological limitations

1. The experiment uses synthetic rather than real clinical-trial data.
2. Synthetic anomaly mechanisms constrain generalizability.
3. The held-out set contains only 30 anomalies.
4. Category-level sample sizes are small.
5. Isolation Forest detects unusualness, not confirmed data error.
6. The contamination value of 0.08 was pre-specified and not optimized on held-out labels.
7. The Stage 3 duplicate-rule behavior can create structurally induced false positives.
8. No clinical adjudication or human review burden was evaluated.
9. These results do not establish clinical validity, real-world performance, or statistical superiority.

## 10. Interpretation

The locked experiment provides evidence of potential complementarity: Isolation Forest detected 6 of 10 held-out ML-multivariate synthetic anomalies that the conventional rules did not detect. At the same time, it produced 28 false positives and had lower overall precision, recall, F1, and specificity than the rule-based method on the same 600 records.

The appropriate interpretation is therefore that unsupervised anomaly detection may add a complementary signal for multivariate patterns, while requiring substantial downstream review and validation. The experiment does not establish that Isolation Forest is superior to conventional rules.

No full research paper has been written at Stage 6.
