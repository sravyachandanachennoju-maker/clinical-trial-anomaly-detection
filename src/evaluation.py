"""Evaluate the two locked detection methods on the same 600 held-out records."""
from __future__ import annotations

from pathlib import Path
import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
PRIMARY_CONTAMINATION = 0.08


def metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "TP": int(tp), "FP": int(fp), "TN": int(tn), "FN": int(fn),
        "Precision": precision_score(y_true, y_pred, zero_division=0),
        "Recall": recall_score(y_true, y_pred, zero_division=0),
        "F1": f1_score(y_true, y_pred, zero_division=0),
        "Specificity": tn / (tn + fp) if (tn + fp) else 0.0,
    }


def run():
    data = pd.read_csv(ROOT / "data" / "synthetic_clinical_trial_data.csv")
    split = pd.read_csv(RESULTS / "stage4_refined_split_assignments.csv")
    rule = pd.read_csv(RESULTS / "rule_based_detection_records.csv")
    if_preds = pd.read_csv(RESULTS / "stage4_refined_predictions.csv")

    heldout_ids = split.loc[split["split"].eq("evaluation"), "record_id"]
    base = data.loc[data["record_id"].isin(heldout_ids), [
        "record_id", "ground_truth_anomaly", "ground_truth_category"
    ]].copy()

    rule_eval = rule[["record_id", "rule_based_anomaly"]]
    base = base.merge(rule_eval, on="record_id", how="left", validate="one_to_one")
    if_eval = if_preds.loc[if_preds["contamination"].eq(PRIMARY_CONTAMINATION), [
        "record_id", "isolation_forest_flag", "anomaly_score"
    ]]
    base = base.merge(if_eval, on="record_id", how="left", validate="one_to_one")

    if len(base) != 600:
        raise RuntimeError(f"Expected 600 held-out records, found {len(base)}")

    y = base["ground_truth_anomaly"].astype(int)
    rows = []
    for method, pred_col in (("Rule-Based", "rule_based_anomaly"), ("Isolation Forest", "isolation_forest_flag")):
        m = metrics(y, base[pred_col].astype(int))
        rows.append({"Method": method, **m})
    comparison = pd.DataFrame(rows)
    comparison.to_csv(RESULTS / "stage5_final_comparison.csv", index=False)

    overlap = pd.DataFrame({
        "record_id": base["record_id"],
        "rule_based": base["rule_based_anomaly"].astype(int),
        "isolation_forest": base["isolation_forest_flag"].astype(int),
        "ground_truth_anomaly": y,
    })
    overlap["category"] = overlap.apply(
        lambda r: "both_methods_detected" if r.rule_based and r.isolation_forest
        else "rule_based_only" if r.rule_based
        else "isolation_forest_only" if r.isolation_forest
        else "neither", axis=1
    )
    overlap.groupby("category").size().rename("Records").reset_index().to_csv(
        RESULTS / "stage5_detection_overlap.csv", index=False
    )
    print(comparison.to_string(index=False))
    return comparison


if __name__ == "__main__":
    run()
