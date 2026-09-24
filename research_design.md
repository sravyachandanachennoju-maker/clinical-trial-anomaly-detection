# Stage 1 Research Design

## 1. Problem

Clinical trial databases use conventional edit checks and data-quality rules to identify missing, invalid, inconsistent, or delayed data. These checks are useful because they are transparent and directly linked to predefined requirements. However, some problematic records may arise from combinations of variables rather than a single explicit rule.

This project investigates whether a simple unsupervised anomaly-detection method can provide complementary signals.

## 2. Research question

Can an unsupervised machine learning model complement conventional rule-based checks by identifying potentially problematic clinical-trial records that may not be detected by traditional data-quality rules?

## 3. Hypothesis

Isolation Forest will identify some unusual multivariate data-quality patterns that conventional rule-based checks miss, but it may also produce additional false positives.

This is a hypothesis, not a conclusion.

## 4. Unit of analysis

The primary unit will be the synthetic clinical-trial record.

Approximately 3,000 records will be generated. Each record will represent a clinical data record associated with a synthetic participant, site, visit, treatment assignment, laboratory measurements, and operational data-entry information.

## 5. Ground truth

The generator will retain an internal record-level ground-truth indicator identifying whether an anomaly was intentionally injected into the record.

This label will not be supplied to Isolation Forest as a training feature.

It will be used only after detection to calculate performance metrics.

## 6. Comparison

Two independent detection pipelines will be evaluated:

### A. Rule-based detection
Explicit rules flag records meeting predefined data-quality conditions.

### B. Isolation Forest
An unsupervised model produces anomaly scores and binary anomaly flags from selected features.

The comparison will focus on both performance and complementarity.

## 7. Why complementarity matters

The practical question is not simply whether machine learning has a higher F1-score.

For clinical data management, a useful ML system could potentially identify unusual records that deterministic checks do not capture. Conversely, a model that flags many normal records would create review burden.

Therefore, the analysis will explicitly examine:
- rule-only detections
- ML-only detections
- detections shared by both methods
- false positives
- false negatives

## 8. Planned anomaly taxonomy

| Category | Example mechanism | Expected detection characteristic |
|---|---|---|
| Missing laboratory value | Remove an otherwise required lab value | Often rule-detectable |
| Extreme laboratory value | Inject an unusually high/low lab result | May be rule-detectable; context matters |
| Duplicate record | Duplicate a clinical record | Rule-detectable with appropriate key |
| Date inconsistency | Entry date before visit date or otherwise invalid sequence | Strong candidate for deterministic rules |
| Excessive entry delay | Unusually long visit-to-entry interval | Rule-detectable, but distributional context may matter |
| Multivariable unusual combination | Individually plausible values occurring in an unusual combination | Candidate for Isolation Forest |
| Visit inconsistency | Unexpected visit number/date pattern | Rule-detectable if explicitly specified |
| Other operational anomaly | Plausible but unusual combination of operational variables | Potential ML complement |

The actual injection rates and distributions will be documented in Stage 2.

## 9. Analysis sequence

The project will follow this order:

Data generation -> anomaly injection -> rule detection -> ML preprocessing -> Isolation Forest -> evaluation -> overlap analysis -> visualization -> interpretation.

## 10. Success criteria

The project does not define success as "ML wins."

A scientifically useful result could be:
- rules detect deterministic problems effectively while ML adds some unique detections;
- ML adds little beyond rules;
- ML finds some injected anomalies but produces too many false positives;
- or the synthetic design shows that the model is poorly suited to the chosen feature representation.

All of these are legitimate experimental outcomes.

## 11. PhD-level framing

The project demonstrates:
- clinical problem formulation
- translation of clinical data-management concepts into measurable computational rules
- controlled synthetic-data generation
- unsupervised ML methodology
- quantitative evaluation
- error analysis
- reproducibility
- critical interpretation and limitations

It should be presented as a small pilot computational study, not as a validated clinical decision-support system.
