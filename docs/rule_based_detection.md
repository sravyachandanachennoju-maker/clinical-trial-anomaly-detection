# Rule-Based Detection

The rule-based detector is the conventional comparison layer.

## Locked rules

| Rule | Description |
|---|---|
| R01 | Required laboratory missingness |
| R02 | Extreme ALT |
| R03 | Extreme AST |
| R04 | Extreme hemoglobin |
| R05 | Extreme creatinine |
| R06 | Data entry before visit date |
| R07 | Excessive entry delay |
| R08 | Invalid visit number |
| R09 | Duplicate composite record |
| R10 | Delay/date mismatch |
| R11 | Joint high ALT and AST |

The implementation is in:

`src/rule_based_detection.py`

## Methodological principle

Rules are applied independently of ground-truth labels.

Ground truth is used only after predictions have been generated.

## Locked held-out result

On the 600-record held-out evaluation set:

- TP = 20
- FP = 2
- TN = 568
- FN = 10
- Precision = 90.9%
- Recall = 66.7%
- F1 = 76.9%
- Specificity = 99.65%

## Important structural limitation

The duplicate rule can flag records because of the synthetic duplicate construction. This is documented as a structural side effect and was not removed from the locked experiment.
