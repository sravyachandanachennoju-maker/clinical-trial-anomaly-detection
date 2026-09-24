"""Stage 2/4 feature-engineering specification.

Ground-truth fields and identifiers are excluded from Isolation Forest.
Raw date strings are converted to meaningful derived features in Stage 4.
"""

MODEL_EXCLUDED_COLUMNS = {
    "record_id",
    "patient_id",
    "ground_truth_anomaly",
    "ground_truth_category",
    "ground_truth_types",
}
