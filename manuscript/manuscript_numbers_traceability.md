# Manuscript Numbers Traceability

All primary manuscript numbers below were cross-checked against the locked Stage 5/6 outputs before manuscript generation.

| Manuscript number | Source | Calculation/meaning |
|---|---|---|
| 3,000 records | `data/synthetic_clinical_trial_data.csv` | Row count |
| 10 sites | `data/synthetic_clinical_trial_data.csv` | Unique `site_id` count |
| 5 visit levels | `data/synthetic_clinical_trial_data.csv` | Unique `visit_number` values 1–5 |
| 731 represented patient IDs | `data/synthetic_clinical_trial_data.csv` | Unique `patient_id` count |
| 750 possible participant IDs | `results/stage2_dataset_specification.md` | Documented generation pool |
| 150 anomalies | `data/synthetic_clinical_trial_data.csv` | Sum of `ground_truth_anomaly` |
| 2,850 normal | `data/synthetic_clinical_trial_data.csv` | Ground-truth anomaly = 0 |
| 2,400 training / 600 evaluation | Locked Stage 4 refinement | 80/20 split |
| 570/12/10/8 held-out composition | `results/stage5_category_comparison.csv` plus split assignments | Evaluation population |
| Rule-Based TP/FP/TN/FN = 20/2/568/10 | `results/stage5_final_comparison.csv` | Locked Stage 5 comparison |
| Rule-Based 90.9/66.7/76.9/99.65% | `results/stage5_final_comparison.csv` | Precision/recall/F1/specificity |
| IF TP/FP/TN/FN = 14/28/542/16 | `results/stage5_final_comparison.csv` | Locked Stage 5 comparison |
| IF 33.3/46.7/38.9/95.09% | `results/stage5_final_comparison.csv` | Precision/recall/F1/specificity |
| Category recall | `results/stage5_category_comparison.csv` | Category-specific detected / N |
| Overlap 8/14/34/544 | `results/stage5_detection_overlap.csv` | Same 600 evaluation records |
| 6 true IF-only / 28 normal IF-only | `results/stage5_overlap_ground_truth.csv` | Ground-truth cross-reference |
| CI values | `results/stage5_confidence_intervals.csv` | Wilson 95% intervals |
| Sensitivity values | `results/stage5_contamination_sensitivity.csv` | Locked 0.05/0.08/0.10 analysis |
| Model configuration/features | Locked Stage 4 refinement and `results/stage4_refined_report.md` | 300 trees, seed 20260924, contamination 0.08 primary |

No manuscript number uses the incorrect 500-patient, 6-visit, 20-site, or seed-42 specification.
