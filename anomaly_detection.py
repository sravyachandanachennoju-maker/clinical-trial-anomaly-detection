"""Stage 4: Isolation Forest anomaly detection."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "synthetic_clinical_trial_data.csv"
RESULTS = ROOT / "results"
SEED = 20260924
N_ESTIMATORS = 300

FEATURES = [
    "age","visit_number","data_entry_delay","ALT","AST","hemoglobin",
    "creatinine","query_count","protocol_deviation",
    "ALT_missing","AST_missing","hemoglobin_missing","creatinine_missing",
]

def make_features(df):
    X = df[FEATURES].copy()
    X["ALT_AST_ratio"] = X["ALT"] / X["AST"].replace(0, np.nan)
    X["ALT_AST_ratio"] = X["ALT_AST_ratio"].replace([np.inf,-np.inf],np.nan)
    pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    return pipe.fit_transform(X), list(X.columns)

def run(contamination=0.08):
    df = pd.read_csv(DATA_PATH, parse_dates=["visit_date","data_entry_date"])
    X, feature_names = make_features(df)
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=contamination,
        random_state=SEED,
        n_jobs=-1,
    )
    model.fit(X)
    decision = model.decision_function(X)
    score = -decision
    flag = (model.predict(X) == -1).astype(int)
    return df, model, feature_names, score, flag

if __name__ == "__main__":
    df, model, features, score, flag = run()
    output = df[["record_id","site_id"]].copy()
    output["isolation_forest_anomaly_score"] = score
    output["isolation_forest_anomaly"] = flag
    output.to_csv(RESULTS / "isolation_forest_predictions.csv", index=False)
