# Feature Dictionary

The Isolation Forest model used 14 features. The feature set was fixed before the held-out comparison and did not include identifiers, raw dates, or ground-truth labels.

| Feature | Type | Role | Rationale |
|---|---|---|---|
| `age` | numeric | model feature | Basic participant-level numerical context. |
| `visit_number` | integer | model feature | Captures longitudinal visit position. |
| `data_entry_delay` | numeric | model feature | Represents operational timing and delayed entry patterns. |
| `ALT` | numeric | model feature | Laboratory measurement used for multivariate pattern detection. |
| `AST` | numeric | model feature | Laboratory measurement used jointly with ALT and other labs. |
| `hemoglobin` | numeric | model feature | Laboratory profile component. |
| `creatinine` | numeric | model feature | Laboratory profile component. |
| `query_count` | integer | model feature | Operational indicator of data-query activity. |
| `protocol_deviation` | binary | model feature | Operational indicator of a protocol-related event. |
| `ALT_missing` | binary | model feature | Explicit missingness signal for ALT. |
| `AST_missing` | binary | model feature | Explicit missingness signal for AST. |
| `hemoglobin_missing` | binary | model feature | Explicit missingness signal for hemoglobin. |
| `creatinine_missing` | binary | model feature | Explicit missingness signal for creatinine. |
| `ALT_AST_ratio` | numeric | derived model feature | Captures a relationship between ALT and AST that individual-value rules may not encode. |

## Excluded from model features

- `record_id`
- `patient_id`
- `site_id`
- raw `visit_date` and `data_entry_date`
- `ground_truth_anomaly`
- `ground_truth_category`
- `ground_truth_types`

Ground-truth fields are used only for split stratification and post-hoc evaluation. They are never supplied as model inputs.

## Interpretation note

The synthetic laboratory values are designed for methodological experimentation. They are not clinical reference ranges and should not be used for clinical decision-making.
