"""Run the locked held-out Isolation Forest experiment.

This module intentionally preserves the Stage 4 refined design:
- 80/20 stratified split by synthetic anomaly category
- 2,400 training / 600 held-out evaluation records
- preprocessing fitted on training data only
- 300 trees, seed 20260924
- contamination sensitivity 0.05, 0.08, 0.10
- no ground-truth labels used as model inputs or training targets
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from preprocessing import add_derived_features, fit_preprocessor, transform, FEATURES

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_clinical_trial_data.csv"
RESULTS = ROOT / "results"
SEED = 20260924
TEST_SIZE = 0.20
N_ESTIMATORS = 300
CONTAMINATIONS = (0.05, 0.08, 0.10)
PRIMARY_CONTAMINATION = 0.08


def run() -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(DATA_PATH, parse_dates=["visit_date", "data_entry_date"])
    df = add_derived_features(df)

    indices = np.arange(len(df))
    train_idx, eval_idx = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=SEED,
        stratify=df["ground_truth_category"].astype(str),
    )
    train = df.iloc[train_idx].copy()
    evaluation = df.iloc[eval_idx].copy()

    imputer, scaler, X_train = fit_preprocessor(train)
    X_eval = transform(evaluation, imputer, scaler)

    metric_rows = []
    category_rows = []
    prediction_frames = []

    y_true = evaluation["ground_truth_anomaly"].astype(int).to_numpy()

    for contamination in CONTAMINATIONS:
        model = IsolationForest(
            n_estimators=N_ESTIMATORS,
            contamination=contamination,
            random_state=SEED,
            n_jobs=-1,
        )
        model.fit(X_train)
        flags = (model.predict(X_eval) == -1).astype(int)
        scores = -model.decision_function(X_eval)

        tn, fp, fn, tp = confusion_matrix(y_true, flags, labels=[0, 1]).ravel()
        metric_rows.append({
            "dataset": "held_out_evaluation",
            "contamination": contamination,
            "train_rows": len(train),
            "evaluation_rows": len(evaluation),
            "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
            "precision": precision_score(y_true, flags, zero_division=0),
            "recall": recall_score(y_true, flags, zero_division=0),
            "f1": f1_score(y_true, flags, zero_division=0),
            "specificity": tn / (tn + fp) if (tn + fp) else 0.0,
            "n_estimators": N_ESTIMATORS,
            "random_seed": SEED,
            "primary_setting": contamination == PRIMARY_CONTAMINATION,
        })

        for category in ("rule_detectable", "ml_multivariate", "both_detectable"):
            mask = evaluation["ground_truth_category"].eq(category).to_numpy()
            denominator = int(mask.sum())
            detected = int(flags[mask].sum())
            category_rows.append({
                "contamination": contamination,
                "category": category,
                "evaluation_anomalies": denominator,
                "detected": detected,
                "missed": denominator - detected,
                "recall": detected / denominator if denominator else np.nan,
            })

        pred = evaluation[[
            "record_id", "patient_id", "site_id", "ground_truth_anomaly",
            "ground_truth_category", "ground_truth_types"
        ]].copy()
        pred["contamination"] = contamination
        pred["isolation_forest_flag"] = flags
        pred["anomaly_score"] = scores
        prediction_frames.append(pred)

    split = df[["record_id", "ground_truth_category"]].copy()
    split["split"] = "evaluation"
    split.loc[split["record_id"].isin(train["record_id"]), "split"] = "train"
    split.to_csv(RESULTS / "stage4_refined_split_assignments.csv", index=False)

    model_ready = df[["record_id", "site_id"] + FEATURES].copy()
    model_ready["split"] = "evaluation"
    model_ready.loc[model_ready["record_id"].isin(train["record_id"]), "split"] = "train"
    model_ready.to_csv(RESULTS / "stage4_refined_model_ready_features.csv", index=False)

    metrics = pd.DataFrame(metric_rows)
    metrics.to_csv(RESULTS / "stage4_refined_metrics.csv", index=False)
    pd.DataFrame(category_rows).to_csv(RESULTS / "stage4_refined_category_recall.csv", index=False)
    pd.concat(prediction_frames, ignore_index=True).to_csv(
        RESULTS / "stage4_refined_predictions.csv", index=False
    )
    return metrics, pd.DataFrame(category_rows)


if __name__ == "__main__":
    metrics, categories = run()
    print(metrics.to_string(index=False))
    print(categories.to_string(index=False))
