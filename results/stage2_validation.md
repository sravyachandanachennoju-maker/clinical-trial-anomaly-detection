# Stage 2 Validation Report

Dataset path: `data/synthetic_clinical_trial_data.csv`
Random seed: 20260924

## Size
- Rows: 3,000
- Columns: 23
- Normal: 2,850
- Anomalous: 150
- Anomaly prevalence: 5.00%

## Category counts
ground_truth_category
normal             2850
rule_detectable      60
ml_multivariate      50
both_detectable      40

## Ground-truth type counts
ground_truth_types
visit_lab_query_pattern            17
date_plus_queries                  15
query_delay_site_pattern           15
missing_plus_queries               15
duplicate_record                   12
excessive_entry_delay              11
delay_plus_labs                    10
alt_ast_ratio                      10
date_inconsistency                  9
lab_profile                         8
missing_required_lab:hemoglobin     8
invalid_visit_sequence              7
missing_required_lab:ALT            5
missing_required_lab:creatinine     4
missing_required_lab:AST            4

## Integrity checks
- Record IDs unique: True
- Duplicate record IDs: 0
- Ground-truth anomalies without a type: 0
- Negative data-entry delays: 30 (intentional date-inconsistency injections)
- Delays >=25 days: 22
- Missing ALT: 20
- Missing AST: 4
- Missing hemoglobin: 8
- Missing creatinine: 4

## Observed variable ranges
- Age: 18.0-85.0
- ALT: 8.0-95.0
- AST: 8.0-90.0
- Hemoglobin: 8.9-17.3
- Creatinine: 0.45-1.50
- Query count: 0-9
- Visit number: 1-5
- Data-entry delay: -35-43 days
