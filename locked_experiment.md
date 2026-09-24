# Locked Experiment Manifest

This file is a compact specification of the experiment that generated the manuscript's primary results.

- Dataset: 3,000 synthetic records
- Sites: 10
- Visit numbers: 1–5
- Represented patient IDs: 731
- Participant-ID pool: 750
- Dataset seed: 20260924
- Normal records: 2,850
- Injected anomalies: 150
- Training records: 2,400
- Held-out records: 600
- Held-out normal: 570
- Held-out rule-detectable anomalies: 12
- Held-out ML-multivariate anomalies: 10
- Held-out both-detectable anomalies: 8
- Isolation Forest trees: 300
- Isolation Forest seed: 20260924
- Primary contamination: 0.08
- Sensitivity: 0.05, 0.08, 0.10
- Preprocessing: median imputation + StandardScaler fitted only on training data
- Model features: 14 locked features documented in `docs/feature_dictionary.md`
- Model exclusions: identifiers, site ID, raw dates, and ground-truth labels

The primary held-out comparison is fixed at the 600-record evaluation population.
