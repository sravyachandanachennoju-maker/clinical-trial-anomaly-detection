"""Stage 4 methodological refinement: train/evaluation Isolation Forest.

Ground-truth labels are used only for stratified splitting and post-hoc evaluation,
never as model features or training targets.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

SEED = 20260924
TEST_SIZE = 0.20
CONTAMINATIONS = [0.05, 0.08, 0.10]
PRIMARY_CONTAMINATION = 0.08  # retained from exploratory Stage 4; not chosen by held-out performance
N_ESTIMATORS = 300

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_clinical_trial_data.csv"
RESULTS = ROOT / "results"

df = pd.read_csv(DATA)

features = [
    "age", "visit_number", "data_entry_delay", "ALT", "AST", "hemoglobin",
    "creatinine", "query_count", "protocol_deviation", "ALT_missing",
    "AST_missing", "hemoglobin_missing", "creatinine_missing", "ALT_AST_ratio"
]

# Derived feature created without ground truth.
df["ALT_AST_ratio"] = df["ALT"] / df["AST"].replace(0, np.nan)

# Ground truth is used ONLY to preserve category proportions in the split.
strata = df["ground_truth_category"].astype(str)
train_idx, eval_idx = train_test_split(
    np.arange(len(df)), test_size=TEST_SIZE, random_state=SEED, stratify=strata
)
train = df.iloc[train_idx].copy()
eval_df = df.iloc[eval_idx].copy()

X_train_raw = train[features].copy()
X_eval_raw = eval_df[features].copy()

imputer = SimpleImputer(strategy="median")
X_train_imp = imputer.fit_transform(X_train_raw)
X_eval_imp = imputer.transform(X_eval_raw)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_imp)
X_eval = scaler.transform(X_eval_imp)

# Model is fit only on transformed training data. No labels are supplied.
models = {}
rows = []
category_rows = []
prediction_frames = []

for contamination in CONTAMINATIONS:
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=contamination,
        random_state=SEED,
        n_jobs=-1,
    )
    model.fit(X_train)
    pred = model.predict(X_eval)
    flag = (pred == -1).astype(int)
    score = -model.decision_function(X_eval)  # larger = more anomalous

    y = eval_df["ground_truth_anomaly"].astype(int).to_numpy()
    tn, fp, fn, tp = confusion_matrix(y, flag, labels=[0,1]).ravel()
    precision = precision_score(y, flag, zero_division=0)
    recall = recall_score(y, flag, zero_division=0)
    f1 = f1_score(y, flag, zero_division=0)
    specificity = tn / (tn + fp) if (tn + fp) else 0.0

    rows.append({
        "dataset": "held_out_evaluation",
        "contamination": contamination,
        "train_rows": len(train),
        "evaluation_rows": len(eval_df),
        "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": precision, "recall": recall, "f1": f1,
        "specificity": specificity,
        "n_estimators": N_ESTIMATORS,
        "random_seed": SEED,
        "primary_setting": contamination == PRIMARY_CONTAMINATION,
    })

    for cat in ["rule_detectable", "ml_multivariate", "both_detectable"]:
        subset = eval_df["ground_truth_category"].eq(cat)
        denom = int(subset.sum())
        detected = int(flag[subset.to_numpy()].sum())
        category_rows.append({
            "contamination": contamination,
            "category": cat,
            "evaluation_anomalies": denom,
            "detected": detected,
            "missed": denom - detected,
            "recall": detected / denom if denom else np.nan,
        })

    out = eval_df[["record_id", "patient_id", "site_id", "ground_truth_anomaly", "ground_truth_category", "ground_truth_types"]].copy()
    out["contamination"] = contamination
    out["isolation_forest_flag"] = flag
    out["anomaly_score"] = score
    prediction_frames.append(out)

# Save split membership, including category distribution for auditability.
split = df[["record_id", "ground_truth_category"]].copy()
split["split"] = "evaluation"
split.loc[split["record_id"].isin(train["record_id"]), "split"] = "train"
split.to_csv(RESULTS / "stage4_refined_split_assignments.csv", index=False)

# Save transformed model-ready data separately. Includes only features, IDs, and split metadata.
model_ready = df[["record_id", "site_id"] + features].copy()
model_ready["split"] = "evaluation"
model_ready.loc[model_ready["record_id"].isin(train["record_id"]), "split"] = "train"
# Preserve raw feature values here for traceability; transformed matrices are generated in memory only.
model_ready.to_csv(RESULTS / "stage4_refined_model_ready_features.csv", index=False)

metrics = pd.DataFrame(rows)
metrics.to_csv(RESULTS / "stage4_refined_metrics.csv", index=False)
cat = pd.DataFrame(category_rows)
cat.to_csv(RESULTS / "stage4_refined_category_recall.csv", index=False)
preds = pd.concat(prediction_frames, ignore_index=True)
preds.to_csv(RESULTS / "stage4_refined_predictions.csv", index=False)

# Sensitivity file is the same metrics table with explicit parameter interpretation.
sens = metrics[["contamination", "tp", "fp", "tn", "fn", "precision", "recall", "f1", "specificity", "primary_setting"]].copy()
sens["selection_note"] = np.where(
    sens["primary_setting"],
    "Primary setting retained from exploratory Stage 4 for continuity; not selected using held-out labels or F1.",
    "Sensitivity analysis setting; not used to select the primary setting."
)
sens.to_csv(RESULTS / "stage4_refined_contamination_sensitivity.csv", index=False)

# Train/evaluation distribution audit.
dist_rows=[]
for split_name, part in [("train", train), ("evaluation", eval_df)]:
    vc = part["ground_truth_category"].value_counts().to_dict()
    for catname in ["normal", "rule_detectable", "ml_multivariate", "both_detectable"]:
        dist_rows.append({"split": split_name, "category": catname, "count": int(vc.get(catname,0)), "proportion": int(vc.get(catname,0))/len(part)})
pd.DataFrame(dist_rows).to_csv(RESULTS / "stage4_refined_split_distribution.csv", index=False)

# Compare with preserved exploratory results.
expl = pd.read_csv(RESULTS / "isolation_forest_metrics.csv")
expl_main = expl.loc[expl["contamination"].eq(PRIMARY_CONTAMINATION)].copy()
if expl_main.empty:
    # fallback if column naming differs
    expl_main = expl.iloc[[0]].copy()
comparison=[]
for _, r in expl_main.iterrows():
    comparison.append({"analysis": "Exploratory full-dataset", "contamination": r["contamination"], "precision": r["precision"], "recall": r["recall"], "f1": r["F1"]})
for _, r in metrics.iterrows():
    comparison.append({"analysis": "Refined held-out evaluation", "contamination": r["contamination"], "precision": r["precision"], "recall": r["recall"], "f1": r["f1"]})
pd.DataFrame(comparison).to_csv(RESULTS / "stage4_refined_exploratory_vs_heldout.csv", index=False)

report = f"""# Stage 4 Methodological Refinement: Train/Evaluation Isolation Forest

## Purpose
The original Stage 4 Isolation Forest analysis is preserved as an **exploratory full-dataset analysis**. This refinement creates a cleaner train/evaluation design without overwriting any original Stage 4 outputs.

## 1. Split design
- Dataset: {len(df):,} synthetic records
- Training set: {len(train):,} records ({len(train)/len(df):.0%})
- Held-out evaluation set: {len(eval_df):,} records ({len(eval_df)/len(df):.0%})
- Random seed: {SEED}
- Stratification: ground-truth anomaly category was used **only to preserve category proportions in the split**. It was not supplied to the model.

The training set still contains naturally generated synthetic anomalies. They were **not removed**. Removing them would change the unsupervised learning problem and could artificially make the detector easier to evaluate.

## 2. Features
{', '.join(features)}

Excluded from model training: `record_id`, `patient_id`, `site_id`, raw dates, and all `ground_truth_*` fields.

## 3. Preprocessing
Median imputation and standardization were fitted **only on the training feature matrix**. The fitted imputer and scaler were then applied unchanged to the held-out evaluation matrix. No evaluation-set statistics were used to fit preprocessing.

Standardization is retained for continuity with exploratory Stage 4. Isolation Forest is tree-based and does not generally require scaling, so scaling is not expected to be essential to the algorithm itself. Keeping it here makes the refinement directly comparable to the exploratory pipeline while removing the more important full-dataset preprocessing issue.

## 4. Isolation Forest
- Algorithm: Isolation Forest
- Trees: {N_ESTIMATORS}
- Random seed: {SEED}
- Contamination sensitivity: {CONTAMINATIONS}
- Primary setting: {PRIMARY_CONTAMINATION}

The primary setting was **not selected by maximizing held-out F1**. It was retained from the exploratory Stage 4 design to avoid tuning the conclusion against the evaluation set. The 0.05 and 0.10 settings are reported as sensitivity analyses.

Because this is unsupervised learning, contamination is a threshold/prior assumption about the expected fraction of outliers, not a learned clinical error rate. The synthetic dataset has a 5% injected anomaly prevalence, but that fact was not used to choose the primary contamination value, because doing so would make the evaluation labels influence model configuration.

## 5. Held-out evaluation results

{metrics.to_string(index=False)}

## 6. Category-level recall

{cat.to_string(index=False)}

## 7. Interpretation
The refined analysis should be interpreted as the locked held-out experiment. The exploratory full-dataset analysis remains useful for development history, but it should not be treated as the primary estimate of generalization.

Importantly, the training data contains synthetic anomalies. This is appropriate for the stated unsupervised scenario because an Isolation Forest is intended to learn a representation of unusual observations from the available data; artificially purging anomalies would create a cleaner-than-realistic training distribution and would use ground truth to manufacture performance. The trade-off is that if anomalies are common or form coherent clusters, the model may treat some anomalous patterns as less isolated.

## 8. Stage 4 conclusion status
The original claim is retained only if the held-out results show meaningful detection of the `ml_multivariate` category that rules miss, while acknowledging false positives and uncertainty. No superiority claim is made. The final conclusion must be based on these held-out results, not on the exploratory run.
"""
(RESULTS / "stage4_refined_report.md").write_text(report)

print(metrics.to_string(index=False))
print('\nCATEGORY RECALL')
print(cat.to_string(index=False))
print('\nSPLIT DISTRIBUTION')
print(pd.DataFrame(dist_rows).to_string(index=False))
