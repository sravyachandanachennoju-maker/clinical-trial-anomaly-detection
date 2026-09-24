"""Stage 3: independent rule-based clinical data-quality detection."""
from pathlib import Path
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_clinical_trial_data.csv"
RESULTS = ROOT / "results"

def detect(df):
    flags = pd.DataFrame(index=df.index)
    flags["R01_missing_required_lab"] = df[["ALT","AST","hemoglobin","creatinine"]].isna().any(axis=1)
    flags["R02_ALT_extreme"] = df["ALT"].notna() & ((df["ALT"] < 5) | (df["ALT"] > 150))
    flags["R03_AST_extreme"] = df["AST"].notna() & ((df["AST"] < 5) | (df["AST"] > 150))
    flags["R04_hemoglobin_extreme"] = df["hemoglobin"].notna() & ((df["hemoglobin"] < 7) | (df["hemoglobin"] > 20))
    flags["R05_creatinine_extreme"] = df["creatinine"].notna() & ((df["creatinine"] < 0.2) | (df["creatinine"] > 3))
    flags["R06_entry_before_visit"] = df["data_entry_date"] < df["visit_date"]
    flags["R07_excessive_entry_delay"] = df["data_entry_delay"] > 21
    flags["R08_invalid_visit_number"] = ~df["visit_number"].between(1, 5)
    flags["R09_duplicate_composite"] = df.duplicated(
        subset=["patient_id","visit_number","visit_date","treatment_arm"], keep=False)
    flags["R10_delay_date_mismatch"] = df["data_entry_delay"] != (
        df["data_entry_date"] - df["visit_date"]).dt.days
    flags["R11_joint_ALT_AST_high"] = (
        df["ALT"].notna() & df["AST"].notna() &
        (df["ALT"] > 120) & (df["AST"] > 120))
    flags = flags.astype(int)
    flags["rule_based_anomaly"] = flags.any(axis=1).astype(int)
    return flags

def evaluate(result):
    y_true = result["ground_truth_anomaly"].astype(int)
    y_pred = result["rule_based_anomaly"].astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true,y_pred,labels=[0,1]).ravel()
    return {
        "total_records": len(result),
        "total_flagged": int(y_pred.sum()),
        "true_positives": int(tp),
        "false_positives": int(fp),
        "true_negatives": int(tn),
        "false_negatives": int(fn),
        "precision": precision_score(y_true,y_pred,zero_division=0),
        "recall": recall_score(y_true,y_pred,zero_division=0),
        "f1_score": f1_score(y_true,y_pred,zero_division=0),
    }

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH, parse_dates=["visit_date","data_entry_date"])
    result = pd.concat([df, detect(df)], axis=1)
    result.to_csv(RESULTS / "rule_based_detection_records.csv", index=False)
    pd.DataFrame([evaluate(result)]).to_csv(RESULTS / "rule_based_metrics.csv", index=False)
