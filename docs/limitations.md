# Limitations

1. **Synthetic dataset:** The records are entirely synthetic and therefore do not establish performance on real clinical-trial data.
2. **Injected anomalies:** Ground truth is defined by controlled injection rather than independent clinical adjudication.
3. **Small held-out anomaly count:** Only 30 anomalies were available for the primary held-out comparison.
4. **Small category sizes:** Category-level estimates, especially the 8-record `both_detectable` group, are imprecise.
5. **Synthetic assumptions:** The data-generating process and anomaly mechanisms can create behavior that would not occur in real studies.
6. **Isolation Forest false positives:** At contamination 0.08, the model produced 28 false positives on the 600-record held-out set.
7. **No clinical adjudication:** A model flag is not evidence that a clinical or data-quality error actually occurred.
8. **No external validation:** The model was not tested on an independent real-world dataset or another synthetic generator.
9. **No prospective workflow evaluation:** Reviewer workload, time-to-resolution, escalation decisions, and operational utility were not measured.
10. **Anomaly exposure during unsupervised training:** Synthetic anomalies were not removed from the training set using ground-truth labels. This preserves the unsupervised problem definition but means unusual observations were present during model fitting.
11. **Duplicate-rule structural behavior:** The R09 duplicate check can flag records because of the synthetic duplicate construction, creating a known structural side effect.
12. **Limited algorithm comparison:** Only Isolation Forest was evaluated as the unsupervised ML method.
