# Stage 3: Rule-Based Anomaly Detection

## Overall evaluation

| Metric | Value |
|---|---:|
| Records checked | 3,000 |
| Records flagged | 112 |
| True positives | 100 |
| False positives | 12 |
| True negatives | 2,838 |
| False negatives | 50 |
| Precision | 0.893 |
| Recall | 0.667 |
| F1-score | 0.763 |

## Rule definitions

| rule_id   | category                | description                                 | threshold_or_logic                                               | rationale                                                                                      |
|:----------|:------------------------|:--------------------------------------------|:-----------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|
| R01       | Missing-data            | Required laboratory value is missing        | Any ALT, AST, hemoglobin, or creatinine is missing               | Required clinical measurements should be complete or explicitly managed.                       |
| R02       | Laboratory-value        | ALT outside broad plausibility range        | ALT < 5 or ALT > 150 U/L                                         | Extremely unusual values warrant review for transcription, unit, or entry errors.              |
| R03       | Laboratory-value        | AST outside broad plausibility range        | AST < 5 or AST > 150 U/L                                         | Broad threshold is a review trigger, not a clinical diagnosis.                                 |
| R04       | Laboratory-value        | Hemoglobin outside broad plausibility range | Hemoglobin < 7 or > 20 g/dL                                      | Extreme values can indicate entry or unit problems.                                            |
| R05       | Laboratory-value        | Creatinine outside broad plausibility range | Creatinine < 0.2 or > 3.0 mg/dL                                  | Very unusual values can merit data review.                                                     |
| R06       | Date/timeliness         | Data entry occurs before visit              | data_entry_date < visit_date                                     | This is temporally inconsistent in the simplified study database.                              |
| R07       | Date/timeliness         | Excessive data-entry delay                  | data_entry_delay > 21 days                                       | Long delays may indicate delayed capture or site follow-up needs.                              |
| R08       | Visit-sequence          | Invalid visit number                        | visit_number outside 1..5                                        | The synthetic protocol defines five scheduled visits.                                          |
| R09       | Duplicate detection     | Duplicate clinical record                   | Duplicate patient_id + visit_number + visit_date + treatment_arm | Repeated records for the same participant/visit can indicate duplicate entry.                  |
| R10       | Cross-field consistency | Stored delay disagrees with dates           | data_entry_delay != date-derived delay                           | Derived fields should agree with their source dates.                                           |
| R11       | Cross-field consistency | Jointly high ALT and AST                    | ALT > 120 AND AST > 120                                          | A joint extreme profile can trigger review without making the rule perfectly match injections. |

## Rule flag counts

R01_missing_required_lab     36
R06_entry_before_visit       30
R09_duplicate_composite      24
R07_excessive_entry_delay    22
R02_ALT_extreme               0
R03_AST_extreme               0
R05_creatinine_extreme        0
R04_hemoglobin_extreme        0
R08_invalid_visit_number      0
R10_delay_date_mismatch       0
R11_joint_ALT_AST_high        0

## Rule overlap

{'no_rule_flag': 2888, 'exactly_one_rule': 112, 'two_or_more_rules': 0, 'maximum_rules_on_one_record': 1}

## Ground-truth category evaluation

| ground_truth_category   |   records |   flagged_by_rules |   missed_by_rules |
|:------------------------|----------:|-------------------:|------------------:|
| rule_detectable         |        60 |                 60 |                 0 |
| ml_multivariate         |        50 |                  0 |                50 |
| both_detectable         |        40 |                 40 |                 0 |

The ground-truth categories were used only after detection for this evaluation. They were not referenced by any rule.
