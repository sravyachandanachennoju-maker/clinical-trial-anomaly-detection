# Results Tables

## Table 1. Dataset and held-out evaluation composition

| Population/category | Records |
|---|---:|
| Full synthetic dataset | 3,000 |
| Ground-truth normal records | 2,850 |
| Injected anomalies | 150 |
| Training set | 2,400 |
| Held-out evaluation set | 600 |
| Held-out normal records | 570 |
| Held-out rule-detectable anomalies | 12 |
| Held-out ML-multivariate anomalies | 10 |
| Held-out both-detectable anomalies | 8 |
| Held-out anomalies, total | 30 |

## Table 2. Primary apples-to-apples performance comparison

| Method | TP | FP | TN | FN | Precision | Recall | F1 | Specificity |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rule-Based | 20 | 2 | 568 | 10 | 90.9% | 66.7% | 76.9% | 99.65% |
| Isolation Forest | 14 | 28 | 542 | 16 | 33.3% | 46.7% | 38.9% | 95.09% |

## Table 3. Category-level recall

| Category | n | Rule-Based Recall | Isolation Forest Recall |
|---|---:|---:|---:|
| Rule-detectable | 12 | 100.0% (12/12) | 16.7% (2/12) |
| ML-multivariate | 10 | 0.0% (0/10) | 60.0% (6/10) |
| Both-detectable | 8 | 100.0% (8/8) | 75.0% (6/8) |

## Table 4. Detection overlap

| Detection pattern | Records |
|---|---:|
| Both methods detected | 8 |
| Rule-based only | 14 |
| Isolation Forest only | 34 |
| Neither | 544 |

## Table 5. Isolation Forest contamination sensitivity

| Contamination | Precision | Recall | F1 |
|---:|---:|---:|---:|
| 0.05 | 50.0% | 40.0% | 44.4% |
| **0.08, primary** | **33.3%** | **46.7%** | **38.9%** |
| 0.10 | 24.6% | 46.7% | 32.2% |

## Table 6. Wilson 95% confidence intervals

| Method | Metric | Estimate | 95% CI |
|---|---|---:|---:|
| Rule-Based | Precision | 90.9% | 72.2–97.5% |
| Rule-Based | Recall | 66.7% | 48.8–80.8% |
| Isolation Forest | Precision | 33.3% | 21.0–48.4% |
| Isolation Forest | Recall | 46.7% | 30.2–63.9% |
