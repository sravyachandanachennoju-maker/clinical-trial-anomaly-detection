# Methodology

## Research question

> Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?

## Hypothesis

Isolation Forest may identify some multivariate data-quality patterns that are not detected by conventional deterministic rules, but may produce additional false-positive signals requiring human review.

## Study design

A controlled computational experiment was conducted using 3,000 fully synthetic clinical-trial-like records. The dataset contained 150 injected anomalies divided into three mutually exclusive categories: 60 rule-detectable, 50 ML-multivariate, and 40 both-detectable. Ground-truth labels were created by the data-generation process and were not supplied to the anomaly detector as features or targets.

The final comparison used a stratified 80/20 split: 2,400 training records and 600 held-out evaluation records. The held-out set contained 570 normal records and 30 anomalies: 12 rule-detectable, 10 ML-multivariate, and 8 both-detectable.

## Detection layers

### Rule-based layer

Eleven deterministic checks were applied independently of ground truth. The rules target explicit missingness, extreme laboratory values, timing inconsistencies, excessive delays, invalid visit values, duplicate structural patterns, and a joint high-ALT/AST condition.

### Isolation Forest layer

Isolation Forest was used as an unsupervised anomaly detector with 300 trees and random seed `20260924`. The primary contamination setting was `0.08`, retained from the experimental design rather than selected after inspecting held-out performance. Sensitivity analyses used `0.05` and `0.10`.

Preprocessing consisted of median imputation and standardization. Both transformations were fitted only on the 2,400-record training set and then applied unchanged to the held-out set.

## Primary comparison

The rule-based predictions and the fixed Isolation Forest predictions were evaluated on exactly the same 600 held-out records. Metrics were calculated from the synthetic ground-truth labels only after predictions were generated.

## Interpretation framework

The experiment distinguishes four concepts:

1. **Synthetic ground-truth anomaly:** an anomaly intentionally injected by the experimental data generator.
2. **Algorithmic anomaly flag:** a record flagged by a detector.
3. **Potential data-quality signal:** a flag that may warrant human review.
4. **Confirmed clinical error:** not established by this study.

The intended interpretation is therefore complementarity and signal generation, not replacement of conventional controls or clinical validation.
