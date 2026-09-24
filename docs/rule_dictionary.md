# Rule Dictionary

The locked deterministic detector contains 11 rules. Rules are applied without using ground-truth labels.

| ID | Rule | Purpose |
|---|---|---|
| R01 | Required laboratory missingness | Flags records with a missing required laboratory value. |
| R02 | Extreme ALT | Flags ALT below 5 or above 150. |
| R03 | Extreme AST | Flags AST below 5 or above 150. |
| R04 | Extreme hemoglobin | Flags hemoglobin below 7 or above 20. |
| R05 | Extreme creatinine | Flags creatinine below 0.2 or above 3. |
| R06 | Entry before visit | Flags records where data entry precedes the visit date. |
| R07 | Excessive entry delay | Flags entry delays greater than 21 days. |
| R08 | Invalid visit number | Flags visit numbers outside 1–5. |
| R09 | Duplicate composite record | Flags duplicated patient/visit/date/treatment combinations. |
| R10 | Delay/date mismatch | Flags disagreement between stored delay and date-derived delay. |
| R11 | Joint high ALT and AST | Flags records with ALT >120 and AST >120 simultaneously. |

## Structural limitation

R09 uses `keep=False`, so all records in a duplicated composite group are flagged. Because duplicate construction is part of the synthetic dataset design, this can create a structural side effect relative to the injected-row ground truth. The rule was retained unchanged in the locked experiment.
