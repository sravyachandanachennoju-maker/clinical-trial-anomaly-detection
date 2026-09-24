# Machine Learning-Assisted Detection of Data Quality Anomalies in Synthetic Clinical Trial Data: A Comparative Evaluation of Rule-Based and Isolation Forest Methods

## Abstract

### Background
Clinical trials generate data across visits, sites, laboratory measurements, and operational workflows. Conventional clinical data-management processes commonly use deterministic checks and review procedures to identify explicit inconsistencies. Such rules are interpretable, but patterns involving multiple individually plausible variables may be difficult to encode exhaustively. Risk-based approaches to clinical-trial oversight emphasize focusing quality activities on important risks and critical data and processes. [1–4]

### Objective
To evaluate whether an unsupervised Isolation Forest model could provide a complementary signal to conventional rule-based checks by identifying potentially problematic records containing multivariate patterns that were not detected by deterministic rules in a controlled synthetic clinical-trial-like dataset.

### Methods
A fully synthetic dataset of 3,000 clinical-trial-like records was generated using 10 synthetic sites and visit numbers 1–5. The final dataset represented 731 unique patient identifiers from a pool of 750 possible identifiers and contained 150 injected anomalies and 2,850 ground-truth normal records. Anomalies were constructed as rule-detectable, ML-multivariate, or both-detectable categories. Eleven deterministic data-quality rules were applied unchanged. For the unsupervised model, the data were split into 2,400 training and 600 held-out evaluation records using category-stratified sampling. Median imputation and standardization were fitted only on the training data. Isolation Forest used 300 trees, random seed 20260924, and a pre-specified contamination of 0.08; 0.05 and 0.10 were examined in sensitivity analysis. Ground-truth labels were used only for post-hoc evaluation.

### Results
On the same 600 held-out records, rule-based detection produced 20 true positives, 2 false positives, 568 true negatives, and 10 false negatives, corresponding to 90.9% precision, 66.7% recall, 76.9% F1, and 99.65% specificity. Isolation Forest produced 14 true positives, 28 false positives, 542 true negatives, and 16 false negatives, corresponding to 33.3% precision, 46.7% recall, 38.9% F1, and 95.09% specificity. The rule-based method detected 0/10 ML-multivariate anomalies, whereas Isolation Forest detected 6/10. Among 34 records flagged only by Isolation Forest, 6 were synthetic ground-truth anomalies and 28 were ground-truth normal records.

### Conclusion
Within this controlled synthetic experiment, Isolation Forest provided an additional signal for some multivariate anomaly patterns missed by deterministic rules, but at a substantial false-positive cost. The findings support potential complementarity rather than replacement or superiority of unsupervised anomaly detection.

## Keywords

Clinical data management; clinical trials; data quality; anomaly detection; Isolation Forest; risk-based monitoring; machine learning; synthetic data; risk-based quality management

## 1. Introduction

Clinical trials produce complex datasets spanning participant visits, laboratory measurements, protocol-related information, site activity, data-entry timing, and query management. Maintaining data integrity and focusing oversight on important risks are established components of modern clinical-trial quality management. ICH E6(R3) places quality by design, critical thinking, and proportionate risk-based approaches within its Good Clinical Practice framework. [1] FDA guidance similarly describes risk-based monitoring as an approach for focusing sponsor oversight on important aspects of study conduct and reporting. [2,3]

Conventional clinical data-management workflows use deterministic edit checks, validation rules, data listings, query review, and other quality-control procedures to identify explicit inconsistencies. These approaches have an important practical advantage: their logic is transparent and can be tied directly to predefined data requirements. Literature on clinical-trial data-quality monitoring has also described the value of multifaceted approaches that combine established quality-control processes with statistical or other analytical signals. [4,5]

A limitation of deterministic checking is that a multivariate pattern may be unusual even when its individual components are not outside simple univariate thresholds. For example, a laboratory profile, visit context, and operational query pattern can jointly form an unusual observation without any single value necessarily violating a predefined range. Unsupervised anomaly detection offers one possible way to generate additional review signals without requiring labelled examples during model fitting.

Isolation Forest is an established unsupervised anomaly-detection method that identifies observations through their relative ease of isolation in randomly partitioned trees. The original method was proposed by Liu, Ting, and Zhou in 2008 and was subsequently developed further in the literature. [6,7] Its use in this study is methodological rather than novel: Isolation Forest is used as a representative unsupervised anomaly detector in a controlled comparison.

The specific research gap addressed here is narrower. Rather than proposing a new anomaly-detection algorithm, this study evaluates whether a conventional deterministic rule layer and an unsupervised anomaly-detection layer identify overlapping or complementary subsets of synthetic clinical-trial data-quality anomalies under a reproducible experimental design.

## 2. Research Question

**Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?**

## 3. Hypothesis

**Isolation Forest may identify some multivariate data-quality patterns that are not detected by conventional deterministic rules, but may produce additional false-positive signals requiring human review.**

## 4. Methods

### 4.1 Study design

This was a controlled computational experiment using entirely synthetic clinical-trial-like data. The primary comparison was performed on the same 600-record held-out evaluation population. The rule-based system was applied without retraining or redesign, while Isolation Forest was fitted only on the separate training set.

The dataset-generation random seed was 20260924. The experiment was designed to distinguish explicit, deterministic anomalies from multivariate patterns intended to be less directly detectable by the predefined rules.

### 4.2 Synthetic dataset generation

The final dataset contained 3,000 records, 10 synthetic sites, and visit numbers 1–5. It represented 731 unique patient identifiers drawn from a pool of 750 possible synthetic identifiers. There were 150 injected anomalous records and 2,850 records classified as normal by the synthetic ground-truth labels.

The dataset included demographic/study variables, timing variables, laboratory variables, and operational variables. The documented generation specification included age, sex, treatment arm, visit number, visit date, data-entry timing, ALT, AST, hemoglobin, creatinine, query count, protocol-deviation status, and laboratory missingness indicators. Laboratory values and other measurements were synthetic and were not intended to represent clinical reference standards.

The dataset-generation specification documented a 5% overall anomaly prevalence. The anomaly-generation process and its category assignments were fixed before the comparative evaluation.

### 4.3 Ground-truth anomaly construction

Ground truth was created by controlled synthetic injection and was used only for post-hoc evaluation.

The 150 injected anomalies comprised three mutually exclusive categories:

1. **Rule-detectable anomalies (n=60):** explicit missing required laboratory values, date inconsistencies, excessive entry delays, duplicate records, and invalid visit sequences.
2. **ML-multivariate anomalies (n=50):** multivariate patterns such as unusual ALT/AST relationships, query-delay/site patterns, unusual laboratory profiles, and unusual combinations of visit, laboratory, and query variables.
3. **Both-detectable anomalies (n=40):** records containing an explicit rule-detectable issue together with an additional multivariate signal.

The ground-truth fields represented the known state of the synthetic experiment rather than clinical truth. They were never supplied as Isolation Forest model inputs.

### 4.4 Rule-based detection

The conventional detector contained 11 predefined checks spanning missingness, laboratory values, dates/timeliness, visit validity, duplicate records, and cross-field consistency:

- R01: required laboratory missingness
- R02: extreme ALT
- R03: extreme AST
- R04: extreme hemoglobin
- R05: extreme creatinine
- R06: data entry before visit date
- R07: excessive entry delay
- R08: invalid visit number
- R09: duplicate composite record
- R10: delay/date mismatch
- R11: joint high ALT and AST

The rules were applied independently of ground-truth labels. The Stage 3 implementation was retained unchanged for the held-out comparison.

An important methodological limitation was retained: the duplicate-record rule can flag records as duplicates because of the synthetic construction even when a record is classified as ground-truth normal. This structural side effect was not removed or re-engineered for the final comparison.

### 4.5 Train/evaluation split

The 3,000 records were divided into 80% training and 20% held-out evaluation data, corresponding to 2,400 and 600 records, respectively. The split used random seed 20260924 and was stratified by anomaly category to preserve the experimental category distribution.

The held-out evaluation set contained:

- 570 normal records
- 12 rule-detectable anomalies
- 10 ML-multivariate anomalies
- 8 both-detectable anomalies
- 30 total anomalies

The category labels were used for stratification and subsequent evaluation, but were not supplied to the Isolation Forest model as predictive features.

### 4.6 Feature engineering and preprocessing

Isolation Forest used the following features:

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

The model excluded record_id, patient_id, site_id, raw dates, and all ground-truth fields.

Median imputation was fitted only on the training data. StandardScaler was also fitted only on the training data. The resulting transformations were then applied unchanged to the held-out evaluation records. No ground-truth labels were used in either transformation.

### 4.7 Isolation Forest

Isolation Forest was configured with 300 trees and random seed 20260924. The pre-specified primary contamination setting was 0.08. Sensitivity analysis examined contamination values of 0.05, 0.08, and 0.10.

The primary value of 0.08 was retained from the exploratory Stage 4 design for continuity and was not selected by maximizing held-out F1 or another evaluation metric. Isolation Forest was trained only on the 2,400-record training set.

### 4.8 Evaluation metrics

Predictions from both methods were evaluated against the synthetic ground-truth labels only after predictions had been generated.

The primary measures were:

- **True positive (TP):** a synthetic ground-truth anomaly correctly flagged.
- **False positive (FP):** a ground-truth normal record incorrectly flagged.
- **True negative (TN):** a ground-truth normal record not flagged.
- **False negative (FN):** a synthetic ground-truth anomaly not flagged.
- **Precision:** TP/(TP+FP).
- **Recall:** TP/(TP+FN).
- **F1:** harmonic mean of precision and recall.
- **Specificity:** TN/(TN+FP).

The primary comparison used the same 600 held-out records for both methods.

### 4.9 Statistical uncertainty

Wilson 95% confidence intervals were calculated for precision and recall. These intervals are descriptive measures of uncertainty around the observed proportions. No inferential test of statistical superiority was performed.

## 5. Results

### 5.1 Dataset and evaluation composition

**Table 1. Dataset and held-out evaluation composition**

| Population/category | Records |
|---|---:|
| Full synthetic dataset | 3,000 |
| Ground-truth normal records | 2,850 |
| Injected anomalies | 150 |
| Training set | 2,400 |
| Held-out evaluation set | 600 |
| Held-out normal records | 570 |
| Held-out rule-detectable anomalies | 12 |
| Held-out ML-multivariate anomalies | 10 |
| Held-out both-detectable anomalies | 8 |
| Held-out anomalies, total | 30 |

### 5.2 Primary apples-to-apples comparison

**Table 2. Primary performance comparison on the same 600 held-out records**

| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule-Based | 20 | 2 | 568 | 10 | 90.9% | 66.7% | 76.9% | 99.65% |
| Isolation Forest | 14 | 28 | 542 | 16 | 33.3% | 46.7% | 38.9% | 95.09% |

On the same evaluation population, rule-based detection had higher observed precision, recall, F1, and specificity. Isolation Forest generated substantially more false positives.

### 5.3 Category-level recall

**Table 3. Category-level recall**

| Category | n | Rule-Based Recall | Isolation Forest Recall |
|---|---:|---:|---:|
| Rule-detectable | 12 | 100.0% (12/12) | 16.7% (2/12) |
| ML-multivariate | 10 | 0.0% (0/10) | 60.0% (6/10) |
| Both-detectable | 8 | 100.0% (8/8) | 75.0% (6/8) |

The rule-based system detected none of the 10 held-out ML-multivariate anomalies. Isolation Forest detected six of these ten records. The small denominators, particularly n=8 for the both-detectable category, require cautious interpretation.

### 5.4 Detection overlap

**Table 4. Detection overlap**

| Detection pattern | Records |
|---|---:|
| Both methods detected | 8 |
| Rule-based only | 14 |
| Isolation Forest only | 34 |
| Neither | 544 |

The 34 Isolation-Forest-only records should not be interpreted as confirmed anomalies. Cross-reference with ground truth showed that 6 were synthetic ground-truth anomalies and 28 were ground-truth normal records.

### 5.5 ML-only detections

Six synthetic ground-truth anomalies were detected only by Isolation Forest. Their synthetic anomaly subtypes included ALT/AST ratio patterns, unusual laboratory profiles, and combinations involving visit, laboratory, and query variables.

These observations illustrate the intended multivariate aspect of the experiment: individual measurements can remain within broad plausible ranges while their joint configuration may be unusual in feature space. Because the data are synthetic, these records should not be interpreted as clinical errors or patient-safety events.

### 5.6 Contamination sensitivity

**Table 5. Isolation Forest contamination sensitivity**

| Contamination | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.05 | 50.0% | 40.0% | 44.4% |
| **0.08, primary** | **33.3%** | **46.7%** | **38.9%** |
| 0.10 | 24.6% | 46.7% | 32.2% |

The primary contamination setting was pre-specified and was not chosen after observing held-out results.

### 5.7 Statistical uncertainty

**Table 6. Wilson 95% confidence intervals**

| Method | Metric | Estimate | 95% CI |
|---|---|---:|---:|
| Rule-Based | Precision | 90.9% | 72.2–97.5% |
| Rule-Based | Recall | 66.7% | 48.8–80.8% |
| Isolation Forest | Precision | 33.3% | 21.0–48.4% |
| Isolation Forest | Recall | 46.7% | 30.2–63.9% |

The confidence intervals are relatively wide because the held-out evaluation set contained only 30 synthetic anomalies.

### 5.8 Visual results

The Stage 6 visualizations provide the corresponding graphical summaries of overall performance, category-level recall, detection overlap, false-positive burden, contamination sensitivity, and Isolation Forest anomaly scores. The figures were generated at 300 DPI from the locked Stage 5/6 outputs and were not regenerated from modified experimental results.

## 6. Discussion

This controlled experiment produced two distinct findings that should be considered together.

First, conventional rule-based detection showed substantially higher overall observed performance on the same 600-record held-out population. It achieved 90.9% precision, 66.7% recall, 76.9% F1, and 99.65% specificity, compared with 33.3% precision, 46.7% recall, 38.9% F1, and 95.09% specificity for Isolation Forest. The rule-based approach therefore generated considerably fewer false-positive signals.

Second, the methods detected different subsets of the synthetic anomaly categories. The rule-based system detected 0/10 ML-multivariate anomalies, whereas Isolation Forest detected 6/10. This finding provides evidence that the unsupervised method can generate additional signals for patterns that were intentionally designed to be less directly captured by the deterministic checks.

These findings support a **potential complementarity** interpretation rather than a superiority interpretation. The results do not suggest that Isolation Forest should replace conventional clinical data-management checks. Instead, an unsupervised model could conceptually serve as a second-layer signal-generation mechanism whose outputs are reviewed by qualified clinical data-management or monitoring personnel.

This distinction is important because an Isolation Forest flag represents unusualness in the model's feature space, not confirmation that a clinical-trial record is erroneous. In the present experiment, 28 of the 34 Isolation-Forest-only records were ground-truth normal records. In a real clinical environment, such flags could reflect legitimate patient variability, unusual but valid site behavior, operational circumstances, or other patterns that warrant contextual review rather than automatic correction.

The result is consistent with the broader principle that clinical-trial quality management can use multiple complementary approaches rather than relying on a single mechanism. Current ICH E6(R3) emphasizes quality by design and proportionate risk-based approaches, while FDA guidance describes risk-based monitoring as a means of focusing oversight on important aspects of study conduct and reporting. [1–3] Existing clinical-trial literature has likewise discussed multifaceted data-quality detection and statistical monitoring approaches. [4,5]

The present experiment should therefore be interpreted as an initial methodological demonstration. It does not establish whether an ML-assisted workflow would reduce reviewer workload, improve detection of consequential errors, or improve trial quality in operational settings.

## 7. Practical Implications for Clinical Data Management

The findings suggest a possible layered workflow rather than an ML replacement model.

A conventional rule layer can continue to handle explicit, interpretable conditions such as missing required data, date inconsistencies, invalid sequences, and predefined threshold violations. An unsupervised layer could then generate additional review candidates from multivariate patterns not represented by existing rules.

Such a workflow would require human review. An anomaly flag should not automatically trigger a data correction, query, protocol-deviation classification, or clinical judgment. Instead, the flag could serve as a prioritization signal for further investigation.

In a real clinical-trial implementation, additional considerations would include explainability, auditability, reviewer workload, threshold governance, study-specific feature selection, site and visit context, validation across studies, and procedures for documenting decisions made in response to model-generated signals.

## 8. Limitations

Several limitations constrain interpretation.

**Synthetic data.** The experiment used entirely synthetic records. The distributions and relationships therefore do not reproduce the complexity of real clinical-trial data.

**Artificial anomaly injection.** Ground-truth anomalies were intentionally constructed. Their detectability and structure depend on the assumptions used during dataset generation.

**Limited held-out anomaly count.** Only 30 anomalies were present in the primary evaluation set. Consequently, overall recall estimates and their confidence intervals have substantial uncertainty.

**Small category sizes.** The ML-multivariate category contained 10 held-out observations and the both-detectable category contained only 8. These estimates should not be generalized beyond this experiment.

**Synthetic-generation assumptions.** The experiment necessarily reflects the selected distributions, feature relationships, anomaly mechanisms, and operational assumptions.

**False-positive burden.** Isolation Forest generated 28 false positives on the held-out evaluation population. Any operational implementation would need to assess whether the additional review burden justified the additional signals.

**No clinical adjudication.** No clinician or clinical data-management adjudication was performed to determine whether an algorithmic flag represented a meaningful data-quality issue.

**No external validation.** The experiment was conducted on one synthetic dataset and was not externally validated across independent datasets or studies.

**No prospective workflow evaluation.** Reviewer workload, time-to-resolution, query burden, and downstream effects on monitoring were not measured.

**Anomalies in unsupervised training data.** The training set was not artificially cleaned of synthetic anomalies. This was deliberate because removing them using ground-truth labels would change the unsupervised learning problem. However, anomalous observations in the training distribution can affect the model's representation of unusualness and therefore constitute an important limitation.

**Duplicate-rule structural side effect.** The Stage 3 duplicate rule can flag records because of the synthetic construction of duplicate records. This was preserved rather than redesigned so that the final comparison represented the locked rule system.

**Algorithmic scope.** Only Isolation Forest was evaluated. The experiment therefore does not establish how other anomaly-detection methods would perform.

## 9. Future Research

Future work should validate the approach on appropriately de-identified real clinical-trial datasets and include human adjudication of model-generated signals. External validation across independent studies and sites would be important for assessing generalizability.

Further work could compare Isolation Forest with other unsupervised and semi-supervised approaches, investigate temporal representations of patient and site behavior, develop explainable anomaly scores, and examine how anomaly signals could be integrated with risk-based monitoring and quality-management workflows.

An important practical endpoint would be reviewer workload. Future studies should measure not only detection metrics but also the number of actionable findings, time required for review, false-positive review burden, and whether model-generated signals identify consequential data-quality issues that existing workflows would otherwise miss.

## 10. Conclusion

Within this controlled synthetic clinical-trial experiment, conventional rule-based detection produced higher overall precision, recall, F1, and specificity than Isolation Forest on the same 600-record held-out evaluation population. However, the rule-based system detected none of the 10 ML-multivariate anomalies, whereas Isolation Forest detected 6.

These findings provide evidence of **potential complementarity**: unsupervised anomaly detection can provide additional signals for some multivariate patterns that predefined deterministic checks do not capture. The substantial false-positive burden, incomplete detection, synthetic nature of the data, and absence of clinical adjudication mean that Isolation Forest should not be considered a replacement for conventional clinical data-management rules.

The most appropriate interpretation is therefore a potential **second-layer signal-generation mechanism requiring human review**, rather than an autonomous clinical-trial data-quality decision system.

## 11. References

1. International Council for Harmonisation of Technical Requirements for Pharmaceuticals for Human Use. *ICH E6(R3) Guideline for Good Clinical Practice*. Final version, 6 January 2025. citeturn1search24
2. U.S. Food and Drug Administration. *Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring: Guidance for Industry*. August 2013. citeturn0search0
3. U.S. Food and Drug Administration. *A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers*. April 2023. citeturn0search1turn0search48
4. TransCelerate BioPharma Inc. *Detecting Data Quality Issues in Clinical Trials: Current Practices and Recommendations*. *Clinical Trials*. 2018. PMID: 30236017. citeturn0search12
5. Dirks A, Florez M, Torche F, Young S, Slizgi B, Getz K. Comprehensive Assessment of Risk-Based Quality Management Adoption in Clinical Trials. *Therapeutic Innovation & Regulatory Science*. 2024;58(3):520–527. doi:10.1007/s43441-024-00618-5. citeturn0search2
6. Liu FT, Ting KM, Zhou Z-H. Isolation Forest. In: *Proceedings of the Eighth IEEE International Conference on Data Mining*. IEEE; 2008:413–422. doi:10.1109/ICDM.2008.17. citeturn1search1turn1search7
7. Liu FT, Ting KM, Zhou Z-H. Isolation-Based Anomaly Detection. *ACM Transactions on Knowledge Discovery from Data*. 2012;6(1):Article 3. doi:10.1145/2133360.2133363. citeturn1search11
8. Agrafiotis DK, Lobanov VS, Farnum MA, et al. Risk-based Monitoring of Clinical Trials: An Integrative Approach. *Clinical Therapeutics*. 2018;40(7):1204–1212. doi:10.1016/j.clinthera.2018.04.020. PMID:30100201. citeturn0search6
9. Suprin M, et al. Quality Risk Management Framework: Guidance for Successful Implementation of Risk Management in Clinical Development. *Therapeutic Innovation & Regulatory Science*. 2019. doi:10.1177/2168479018817752. citeturn0search11
