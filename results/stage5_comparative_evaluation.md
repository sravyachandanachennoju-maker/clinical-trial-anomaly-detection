# Stage 5: Final Comparative Evaluation

## 1. Evaluation design
The primary comparison uses the exact 600-record held-out evaluation set defined during Stage 4 refinement. The Stage 3 rule set was applied unchanged to these records; no rule retraining or redesign occurred. The locked Isolation Forest predictions at contamination 0.08 were used without refitting. Ground-truth labels were used only for evaluation.

The synthetic dataset contains 150 anomalies overall. The held-out set contains 30 anomalies: 12 rule-detectable, 10 ML-multivariate, and 8 both-detectable, plus 570 normal records.

## 2. Overall performance

| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule-Based | 20 | 2 | 568 | 10 | 0.909 | 0.667 | 0.769 | 0.996 |\n| Isolation Forest | 14 | 28 | 542 | 16 | 0.333 | 0.467 | 0.389 | 0.951 |\n
These values are directly comparable because both methods were evaluated against the same 600 records and the same ground-truth labels.

## 3. Category-level performance

| Category | Rule-Based Recall | Isolation Forest Recall | N |
|---|---:|---:|---:|
| rule_detectable | 1.000 | 0.167 | 12 |\n| ml_multivariate | 0.000 | 0.600 | 10 |\n| both_detectable | 1.000 | 0.750 | 8 |\n
The `both_detectable` category contains only 8 held-out anomalies, so its recall estimate is especially unstable and should not be overinterpreted.

### Subtype recall
See `stage5_subtype_recall.csv` for subtype-level results where at least 3 held-out examples were available.

## 4. Detection overlap

- both_methods_detected: 8 records
- rule_based_only: 14 records
- isolation_forest_only: 34 records
- neither: 544 records

Among true anomalies, some were detected by both methods, some only by rules, and some only by Isolation Forest. The `Isolation Forest only` group is not equivalent to confirmed erroneous data: it means the record was flagged by the model but not by the rule set.

## 5. Complementary detections

There were 6 true anomalies detected only by Isolation Forest on the held-out set. Their subtypes and feature values are provided in `stage5_true_if_only_examples.csv`. These records were generated as synthetic ground-truth anomalies involving multivariate patterns such as lab profiles, query-delay-site relationships, or visit/lab/query combinations. The relevant interpretation is that the model identified unusual feature combinations that were not triggered by the deterministic rules. This does not establish that such records would be clinically erroneous in a real trial.

## 6. False-positive analysis

Rule-based detection produced 2 false positives that were rule-only. Isolation Forest produced 28 false positives that were IF-only. Representative records are provided in `stage5_rule_based_false_positives.csv` and `stage5_isolation_forest_false_positives.csv`.

The Isolation Forest false positives illustrate the central limitation of unsupervised anomaly detection: unusual does not mean incorrect. Plausible but uncommon laboratory combinations, unusual query activity, protocol deviations, or missingness patterns can be isolated even when there is no ground-truth error. The deterministic rules can also flag records that are unusual because of structural properties of the synthetic dataset, including the previously documented duplicate-rule behavior.

## 7. Statistical uncertainty

Wilson 95% confidence intervals were calculated for precision and recall. Because the same finite held-out population is used for each method, these intervals describe uncertainty around the corresponding binomial proportions; they are not a test of clinical effectiveness.

See `stage5_confidence_intervals.csv` for exact values.

## 8. Interpretation

The apples-to-apples comparison provides evidence that Isolation Forest can recover some synthetic multivariate anomalies missed by the conventional rule set. In the held-out evaluation, Isolation Forest detected 6 of 10 ML-multivariate anomalies, while the rules detected none of those 10. However, Isolation Forest also generated substantially more false positives than the rule set on this evaluation set. Overall recall was 0.467 and precision was 0.333.

Therefore, the evidence supports **potential complementarity, not superiority**. The experiment demonstrates a useful signal for multivariate anomaly detection, but the false-positive burden means the model would require human review and further validation before being considered a practical clinical data-management control.

## 9. Answer to research question

**Research question:** Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?

**Evidence-based answer:** **Evidence of potential complementarity.** On the same 600 held-out records, Isolation Forest detected 6/10 ML-multivariate anomalies that were missed by the rule-based method. This finding is accompanied by 28 false positives at the pre-specified 0.08 contamination setting and incomplete overall recall. The result therefore supports the possibility of complementarity in this synthetic experiment, while not establishing clinical validity or superiority.

## 10. Limitations

1. The data are fully synthetic, so the findings do not establish performance on real clinical-trial data.
2. The anomaly mechanisms and category definitions were designed by the study author, which can create dataset-specific behavior.
3. The held-out anomaly counts are small, especially the 8 `both_detectable` records.
4. The primary contamination setting of 0.08 was retained from the exploratory design rather than selected using held-out labels, but this is still a design choice rather than a universally optimal operating point.
5. Isolation Forest flags unusual observations, not proven data errors.
6. The rule-based method contains a documented structural side effect: the duplicate composite rule can flag records affected by the synthetic visit/record construction.
7. Confidence intervals are descriptive and do not replace external validation.
8. The experiment does not assess operational workload, review time, or clinical adjudication burden.
