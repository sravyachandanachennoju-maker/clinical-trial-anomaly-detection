# Machine Learning-Assisted Detection of Data Quality Anomalies in Synthetic Clinical Trial Data

**A controlled, reproducible comparison of deterministic rule-based checks and unsupervised Isolation Forest anomaly detection.**

> **Research question:** Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?

## 1. Research question

This project asks whether an unsupervised anomaly detector can add useful signals beyond conventional deterministic clinical data-quality checks, particularly for multivariate patterns that are difficult to encode as individual rules.

## 2. Hypothesis

> Isolation Forest may identify some multivariate data-quality patterns that are not detected by conventional deterministic rules, but may produce additional false-positive signals requiring human review.

The hypothesis is deliberately modest. The study does not assume that machine learning should replace established data-management controls.

## 3. Background

Clinical-trial data management relies heavily on deterministic edit checks, validation rules, discrepancy management, reconciliation, and review workflows. These controls are interpretable and can be linked to explicit data requirements. A limitation of a purely rule-based approach is that a pattern must generally be anticipated and encoded before it can be flagged.

This project tests a complementary idea: an unsupervised model may identify unusual combinations of otherwise plausible variables without requiring anomaly labels during model fitting. Isolation Forest was selected as an established, relatively simple unsupervised anomaly-detection method for this controlled methodological comparison.

The project is a **synthetic proof-of-concept**, not a clinical validation study.

## 4. Study design

The experiment was locked before final evaluation. Stages 1–7 produced the dataset, detection methods, held-out comparison, audit, figures, and manuscript.

| Component | Locked specification |
|---|---|
| Dataset | 3,000 synthetic clinical-trial-like records |
| Synthetic sites | 10 |
| Visit numbers | 1–5 |
| Represented patient IDs | 731 |
| Possible participant-ID pool | 750 |
| Dataset seed | `20260924` |
| Ground-truth normal | 2,850 |
| Injected anomalies | 150 |
| Training set | 2,400 |
| Held-out evaluation set | 600 |
| Primary IF contamination | `0.08` |
| IF trees | 300 |
| IF seed | `20260924` |

### Held-out evaluation population

| Category | Records |
|---|---:|
| Normal | 570 |
| Rule-detectable anomalies | 12 |
| ML-multivariate anomalies | 10 |
| Both-detectable anomalies | 8 |
| **Total** | **600** |

The split was stratified by synthetic anomaly category to preserve the experimental category structure. Ground-truth labels were not used as model features or training targets.

## 5. Synthetic dataset

All patient and clinical-trial-like data in this repository are **synthetic**. No real patient records are included.

The 150 injected anomalies were mutually exclusive across three experimental categories:

- 60 rule-detectable
- 50 ML-multivariate
- 40 both-detectable

Synthetic anomaly mechanisms included missing required laboratory values, date inconsistencies, excessive entry delays, duplicate structural patterns, invalid visit sequences, ALT/AST relationship anomalies, unusual laboratory profiles, and unusual combinations of visit, laboratory, and query features.

The synthetic laboratory values are for computational experimentation only. They are not clinical reference ranges.

See [`docs/dataset_generation.md`](docs/dataset_generation.md) and [`data/data_dictionary.csv`](data/data_dictionary.csv).

## 6. Rule-based methodology

The deterministic detector contains 11 locked checks:

- R01 required laboratory missingness
- R02 extreme ALT
- R03 extreme AST
- R04 extreme hemoglobin
- R05 extreme creatinine
- R06 data entry before visit date
- R07 excessive entry delay
- R08 invalid visit number
- R09 duplicate composite record
- R10 stored-delay/date mismatch
- R11 joint high ALT and AST

The rules are applied without ground-truth labels. The duplicate rule has a documented structural side effect because duplicated composite groups are flagged as a group in the synthetic construction.

See [`docs/rule_dictionary.md`](docs/rule_dictionary.md) and [`src/rule_based_detection.py`](src/rule_based_detection.py).

## 7. Isolation Forest methodology

Isolation Forest was used as the unsupervised comparison layer.

### Model configuration

- 300 trees
- random seed `20260924`
- primary contamination `0.08`
- sensitivity analysis: `0.05`, `0.08`, `0.10`

The 0.08 setting was retained from the pre-specified experimental design. It was **not selected by maximizing held-out F1**.

### Model features

The 14 locked features were:

`age`, `visit_number`, `data_entry_delay`, `ALT`, `AST`, `hemoglobin`, `creatinine`, `query_count`, `protocol_deviation`, `ALT_missing`, `AST_missing`, `hemoglobin_missing`, `creatinine_missing`, `ALT_AST_ratio`.

Excluded from the model:

- `record_id`
- `patient_id`
- `site_id`
- raw dates
- all `ground_truth_*` fields

Median imputation and standardization were fitted **only on the 2,400 training records** and then applied unchanged to the 600 held-out records.

See [`docs/feature_dictionary.md`](docs/feature_dictionary.md), [`docs/isolation_forest.md`](docs/isolation_forest.md), and [`src/isolation_forest.py`](src/isolation_forest.py).

## 8. Evaluation strategy

The final comparison is deliberately apples-to-apples:

1. The same 600 held-out records were used for both methods.
2. The same synthetic ground-truth labels were used only after predictions were generated.
3. The Stage 3 rule set was applied unchanged.
4. Isolation Forest predictions at the locked 0.08 setting were evaluated without optimizing the model against held-out labels.
5. Precision, recall, F1, specificity, category-level recall, detection overlap, false-positive burden, and contamination sensitivity were examined.

## 9. Main results

### Overall held-out performance

| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule-Based | 20 | 2 | 568 | 10 | 90.9% | 66.7% | 76.9% | 99.65% |
| Isolation Forest | 14 | 28 | 542 | 16 | 33.3% | 46.7% | 38.9% | 95.09% |

### Category-level recall

| Category | Rule-Based | Isolation Forest |
|---|---:|---:|
| Rule-detectable | 100.0% (12/12) | 16.7% (2/12) |
| ML-multivariate | 0.0% (0/10) | 60.0% (6/10) |
| Both-detectable | 100.0% (8/8) | 75.0% (6/8) |

### Detection overlap

- Both methods: 8 records
- Rule-based only: 14 records
- Isolation Forest only: 34 records
- Neither: 544 records

Among the 34 Isolation Forest-only records, 6 were synthetic ground-truth anomalies and 28 were ground-truth normal records.

## 10. Interpretation

The results do **not** support a claim that Isolation Forest is superior to deterministic data-quality rules. In the primary held-out comparison, the rule-based detector had higher overall precision, recall, F1, and specificity and generated substantially fewer false positives.

The scientifically relevant complementary signal is category-specific: Isolation Forest detected **6 of 10** held-out ML-multivariate synthetic anomalies, whereas the rule-based method detected **0 of 10**. This suggests that an unsupervised model can identify some multivariate patterns that a predefined rule set does not encode.

At the same time, the Isolation Forest produced **28 false positives**. A model flag therefore represents an unusual pattern or potential data-quality signal, not a confirmed clinical error. Any practical implementation would require human review, adjudication, governance, and external validation.

## 11. Limitations

The principal limitations are:

- fully synthetic dataset
- injected rather than clinically adjudicated anomalies
- only 30 held-out anomalies
- small category sizes, especially the 8-record both-detectable category
- dependence on synthetic data-generation assumptions
- substantial Isolation Forest false-positive burden
- no clinical adjudication
- no external validation
- no prospective workflow evaluation
- synthetic anomalies remained in unsupervised training data rather than being removed using ground truth
- structural side effect of the duplicate rule
- no comparison with additional unsupervised algorithms

Full details are in [`docs/limitations.md`](docs/limitations.md).

## 12. Reproducibility

### Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Pipeline

```bash
python src/generate_data.py
python src/rule_based_detection.py
python src/isolation_forest.py
python src/evaluation.py
python src/stage5_comparative_evaluation.py
```

The saved Stage 5 and Stage 6 outputs provide the audit trail for the manuscript. See [`docs/reproducibility.md`](docs/reproducibility.md) for details.

## 13. Repository structure

```text
clinical-trial-anomaly-detection/
├── README.md
├── CITATION.cff
├── LICENSE
├── requirements.txt
├── research_design.md
├── data/
│   ├── README.md
│   ├── synthetic_clinical_trial_data.csv
│   └── data_dictionary.csv
├── src/
│   ├── generate_data.py
│   ├── preprocessing.py
│   ├── rule_based_detection.py
│   ├── isolation_forest.py
│   ├── evaluation.py
│   ├── feature_engineering.py
│   ├── stage4_refinement.py
│   └── stage5_comparative_evaluation.py
├── results/
│   ├── tables/
│   ├── metrics/
│   ├── figures/
│   └── locked stage outputs and audit files
├── manuscript/
│   ├── research_report.md
│   ├── results_tables.md
│   ├── references.md
│   └── manuscript_numbers_traceability.md
├── docs/
│   ├── methodology.md
│   ├── feature_dictionary.md
│   ├── rule_dictionary.md
│   ├── dataset_generation.md
│   ├── isolation_forest.md
│   ├── reproducibility.md
│   ├── limitations.md
│   └── phd_professor_explanation.md
└── notebooks/
    └── clinical_trial_anomaly_detection.ipynb
```

The original staged result files remain under `results/` so that the development history and manuscript traceability are not lost.

## 14. Ethical and data statement

This repository contains synthetic data created for methodological research and education. It contains no real patient-level clinical-trial data. The project does not establish clinical validity, patient-safety performance, regulatory acceptability, or readiness for deployment. A future real-data study would require appropriate de-identification, governance, data-use permissions, security controls, and expert adjudication.

## 15. Future research

The next research step is validation using appropriately de-identified real clinical-trial data with expert adjudication of anomaly flags. A stronger study would also:

- compare multiple unsupervised anomaly-detection methods
- incorporate temporal and site-level context
- evaluate explainable feature contributions
- measure reviewer workload and alert acceptance
- assess stability across independent studies
- examine prospective workflow integration
- define an explicit human-in-the-loop adjudication protocol

The intended research trajectory is therefore:

**synthetic controlled experiment → de-identified retrospective validation → human adjudication → prospective workflow evaluation**

## 16. Citation

See [`CITATION.cff`](CITATION.cff). The file contains a placeholder GitHub URL that should be replaced with the repository's actual URL after the GitHub repository is created.

## 17. Research manuscript

The complete manuscript is available at [`manuscript/research_report.md`](manuscript/research_report.md), with a DOCX copy preserved at `results/research_report.docx`.

The figures and numerical traceability files are preserved under `results/`.

## Scope

This repository is a reproducible research prototype. It is not a validated clinical-trial data-management system and should not be used to make clinical, regulatory, or patient-safety decisions.
