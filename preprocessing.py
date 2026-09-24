"""Locked preprocessing utilities for the held-out Isolation Forest experiment."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "age", "visit_number", "data_entry_delay", "ALT", "AST", "hemoglobin",
    "creatinine", "query_count", "protocol_deviation", "ALT_missing",
    "AST_missing", "hemoglobin_missing", "creatinine_missing", "ALT_AST_ratio",
]

EXCLUDED = [
    "record_id", "patient_id", "site_id", "visit_date", "data_entry_date",
    "ground_truth_anomaly", "ground_truth_category", "ground_truth_types",
]


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add only the derived feature specified by the locked experiment."""
    out = df.copy()
    out["ALT_AST_ratio"] = out["ALT"] / out["AST"].replace(0, np.nan)
    out["ALT_AST_ratio"] = out["ALT_AST_ratio"].replace([np.inf, -np.inf], np.nan)
    return out


def fit_preprocessor(train_df: pd.DataFrame):
    """Fit median imputation and standardization using training data only."""
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    X_train_raw = train_df[FEATURES].copy()
    X_train = scaler.fit_transform(imputer.fit_transform(X_train_raw))
    return imputer, scaler, X_train


def transform(df: pd.DataFrame, imputer, scaler):
    """Apply already-fitted preprocessing without refitting."""
    return scaler.transform(imputer.transform(df[FEATURES].copy()))
