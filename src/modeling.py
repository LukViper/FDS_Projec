"""
M3 — Temporal train/val/test modelling for customer churn.

Consumes M2: data/features/customer_features.parquet
Uses M1 dates: data/processed/customer_churn_labels.parquet (obs_last_purchase only for split)

Does not redefine churn labels. Does not use prediction-period fields as features.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

from src.preprocessing import ROOT

FEATURES_PATH = ROOT / "data" / "features" / "customer_features.parquet"
LABELS_PATH = ROOT / "data" / "processed" / "customer_churn_labels.parquet"
M2_REPORT_PATH = ROOT / "data" / "features" / "m2_validation_report.json"
MODELS_DIR = ROOT / "models"

# Temporal split on observation-period last purchase (cohort / time order)
TRAIN_LAST_END = pd.Timestamp("2010-08-31 23:59:59")
VAL_LAST_END = pd.Timestamp("2010-10-31 23:59:59")
# Test: obs_last_purchase > VAL_LAST_END (through end of observation year)

NUMERIC_FEATURES = [
    "recency_days",
    "frequency",
    "monetary",
    "avg_order_value",
    "purchase_interval_days",
    "product_diversity",
    "cancellation_rate",
    "spending_trend",
    "order_trend",
    "obs_n_lines",
    "avg_line_quantity",
    "purchase_interval_imputed",
]
CATEGORICAL_FEATURES = ["country"]
TARGET = "churn"
ID_COL = "Customer ID"


def validate_m2_handoff(features: pd.DataFrame) -> dict[str, Any]:
    report = json.loads(M2_REPORT_PATH.read_text(encoding="utf-8"))
    fv = report.get("feature_validation", {})
    checks = {
        "n_rows": int(len(features)),
        "expected_rows": int(fv.get("n_rows", -1)),
        "row_count_matches_m2": int(len(features)) == int(fv.get("n_rows", -1)),
        "has_required_numeric": all(c in features.columns for c in NUMERIC_FEATURES),
        "has_country": "country" in features.columns,
        "has_churn": TARGET in features.columns,
        "null_numeric": {c: int(features[c].isna().sum()) for c in NUMERIC_FEATURES},
        "m2_feature_validation_passed": bool(fv.get("all_passed", False)),
        "m2_churn_unchanged": bool(fv.get("churn_unchanged", False)),
        "no_prediction_leak_columns": not any(
            c in features.columns
            for c in ["purchased_in_prediction", "prediction_start", "prediction_end"]
        ),
    }
    checks["all_passed"] = all(
        [
            checks["row_count_matches_m2"],
            checks["has_required_numeric"],
            checks["has_country"],
            checks["has_churn"],
            all(v == 0 for v in checks["null_numeric"].values()),
            checks["m2_feature_validation_passed"],
            checks["m2_churn_unchanged"],
            checks["no_prediction_leak_columns"],
        ]
    )
    return checks


def load_modelling_frame(
    features_path: Path = FEATURES_PATH,
    labels_path: Path = LABELS_PATH,
) -> pd.DataFrame:
    features = pd.read_parquet(features_path)
    labels = pd.read_parquet(labels_path)[
        [ID_COL, "obs_first_purchase", "obs_last_purchase"]
    ]
    # Ensure churn from features (M2) matches — do not take churn from a redefinition
    df = features.merge(labels, on=ID_COL, how="inner", validate="one_to_one")
    if len(df) != len(features):
        raise ValueError("Merge with M1 dates changed row count — check Customer ID alignment.")
    df["obs_first_purchase"] = pd.to_datetime(df["obs_first_purchase"])
    df["obs_last_purchase"] = pd.to_datetime(df["obs_last_purchase"])
    return df


def assign_temporal_split(df: pd.DataFrame) -> pd.Series:
    """
    Split by obs_last_purchase (when the customer was last observed in 2010).

    Train: last purchase on/before 2010-08-31
    Val:   2010-09-01 .. 2010-10-31
    Test:  on/after 2010-11-01
    """
    last = df["obs_last_purchase"]
    split = pd.Series(index=df.index, dtype="object")
    split.loc[last <= TRAIN_LAST_END] = "train"
    split.loc[(last > TRAIN_LAST_END) & (last <= VAL_LAST_END)] = "val"
    split.loc[last > VAL_LAST_END] = "test"
    if split.isna().any():
        raise ValueError("Unassigned rows in temporal split.")
    return split


def split_summary(df: pd.DataFrame, split: pd.Series) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in ["train", "val", "test"]:
        part = df.loc[split == name]
        out[name] = {
            "n": int(len(part)),
            "n_churn": int(part[TARGET].sum()),
            "churn_rate": float(part[TARGET].mean()) if len(part) else None,
            "last_purchase_min": str(part["obs_last_purchase"].min()),
            "last_purchase_max": str(part["obs_last_purchase"].max()),
        }
    out["rule"] = {
        "train": "obs_last_purchase <= 2010-08-31",
        "val": "2010-09-01 <= obs_last_purchase <= 2010-10-31",
        "test": "obs_last_purchase >= 2010-11-01",
        "rationale": (
            "Calendar temporal/cohort split on last observation-period activity. "
            "Avoids random mixing of earlier and later cohorts. Features remain "
            "observation-only; label remains M1 prediction-period churn."
        ),
    }
    return out


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric, NUMERIC_FEATURES),
            ("cat", categorical, CATEGORICAL_FEATURES),
        ]
    )


def _metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5) -> dict[str, Any]:
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "pr_auc": float(average_precision_score(y_true, y_prob)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "threshold": threshold,
        "classification_report": classification_report(
            y_true, y_pred, output_dict=True, zero_division=0
        ),
    }


def make_models(scale_pos_weight: float) -> dict[str, Any]:
    return {
        "logistic_regression": LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            solver="lbfgs",
            random_state=42,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
        "xgboost": XGBClassifier(
            n_estimators=300,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            reg_lambda=1.0,
            objective="binary:logistic",
            eval_metric="auc",
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            n_jobs=-1,
        ),
    }


def train_and_evaluate(
    df: pd.DataFrame,
    split: pd.Series,
) -> tuple[dict[str, Any], dict[str, Pipeline], str]:
    feature_cols = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[feature_cols]
    y = df[TARGET].astype(int)

    X_train, y_train = X.loc[split == "train"], y.loc[split == "train"]
    X_val, y_val = X.loc[split == "val"], y.loc[split == "val"]
    X_test, y_test = X.loc[split == "test"], y.loc[split == "test"]

    n_pos = int((y_train == 1).sum())
    n_neg = int((y_train == 0).sum())
    scale_pos_weight = float(n_neg / n_pos) if n_pos else 1.0

    imbalance = {
        "train_n_pos": n_pos,
        "train_n_neg": n_neg,
        "train_churn_rate": float(y_train.mean()),
        "val_churn_rate": float(y_val.mean()),
        "test_churn_rate": float(y_test.mean()),
        "handling": {
            "logistic_regression": "class_weight='balanced'",
            "random_forest": "class_weight='balanced'",
            "xgboost": f"scale_pos_weight={scale_pos_weight:.4f} (n_neg/n_pos on train)",
        },
    }

    results: dict[str, Any] = {"imbalance": imbalance, "models": {}}
    pipelines: dict[str, Pipeline] = {}

    for name, clf in make_models(scale_pos_weight).items():
        pipe = Pipeline(
            steps=[
                ("preprocess", build_preprocessor()),
                ("model", clf),
            ]
        )
        pipe.fit(X_train, y_train)
        pipelines[name] = pipe

        val_prob = pipe.predict_proba(X_val)[:, 1]
        test_prob = pipe.predict_proba(X_test)[:, 1]
        train_prob = pipe.predict_proba(X_train)[:, 1]

        results["models"][name] = {
            "train": _metrics(y_train.to_numpy(), train_prob),
            "val": _metrics(y_val.to_numpy(), val_prob),
            "test": _metrics(y_test.to_numpy(), test_prob),
        }

    # Select by validation PR-AUC, tie-break ROC-AUC, then F1
    ranking = sorted(
        results["models"].keys(),
        key=lambda m: (
            results["models"][m]["val"]["pr_auc"],
            results["models"][m]["val"]["roc_auc"],
            results["models"][m]["val"]["f1"],
        ),
        reverse=True,
    )
    best = ranking[0]
    results["selection"] = {
        "criterion": "Highest validation PR-AUC; ties broken by validation ROC-AUC then F1",
        "ranking_by_val_pr_auc": ranking,
        "selected_model": best,
        "selected_val_metrics": results["models"][best]["val"],
        "selected_test_metrics": results["models"][best]["test"],
        "reason": (
            f"{best} achieved the best validation PR-AUC among LR, RF, and XGBoost "
            "under the temporal split. Test metrics are reported for the frozen selection only."
        ),
    }
    return results, pipelines, best


def run_pipeline(models_dir: Path = MODELS_DIR) -> dict[str, Any]:
    models_dir.mkdir(parents=True, exist_ok=True)

    df = load_modelling_frame()
    handoff = validate_m2_handoff(df)
    if not handoff["all_passed"]:
        raise RuntimeError(f"M2 handoff validation failed: {handoff}")

    split = assign_temporal_split(df)
    summary = split_summary(df, split)
    results, pipelines, best = train_and_evaluate(df, split)

    # Persist all fitted pipelines + final alias
    for name, pipe in pipelines.items():
        joblib.dump(pipe, models_dir / f"{name}_pipeline.joblib")
    final_path = models_dir / "final_model.joblib"
    joblib.dump(pipelines[best], final_path)
    # Explicit preprocess+model bundle metadata for M4
    joblib.dump(
        {
            "model_name": best,
            "pipeline": pipelines[best],
            "numeric_features": NUMERIC_FEATURES,
            "categorical_features": CATEGORICAL_FEATURES,
            "target": TARGET,
            "temporal_split_rule": summary["rule"],
        },
        models_dir / "final_bundle.joblib",
    )

    metrics_path = models_dir / "model_metrics.json"
    comparison_path = models_dir / "model_comparison.json"
    report = {
        "m2_handoff_validation": handoff,
        "temporal_split": summary,
        "experiments": results,
        "artifacts": {
            "final_model": str(final_path.relative_to(ROOT)),
            "final_bundle": str((models_dir / "final_bundle.joblib").relative_to(ROOT)),
            "pipelines": {
                name: str((models_dir / f"{name}_pipeline.joblib").relative_to(ROOT))
                for name in pipelines
            },
        },
        "leakage_controls": [
            "Features are M2 observation-period engineered fields only",
            "No prediction-period purchase flags used as inputs",
            "Temporal split by obs_last_purchase (no random row shuffle)",
            "Customer ID excluded from features",
            "Churn label unchanged from M2/M1",
        ],
    }
    metrics_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # Compact comparison table for docs / PROGRESS
    rows = []
    for name, block in results["models"].items():
        rows.append(
            {
                "model": name,
                "val_roc_auc": block["val"]["roc_auc"],
                "val_pr_auc": block["val"]["pr_auc"],
                "val_precision": block["val"]["precision"],
                "val_recall": block["val"]["recall"],
                "val_f1": block["val"]["f1"],
                "test_roc_auc": block["test"]["roc_auc"],
                "test_pr_auc": block["test"]["pr_auc"],
                "test_precision": block["test"]["precision"],
                "test_recall": block["test"]["recall"],
                "test_f1": block["test"]["f1"],
                "selected": name == best,
            }
        )
    comparison = {
        "selected_model": best,
        "selection_criterion": results["selection"]["criterion"],
        "rows": rows,
    }
    comparison_path.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    report["comparison_path"] = str(comparison_path.relative_to(ROOT))
    report["metrics_path"] = str(metrics_path.relative_to(ROOT))
    return report


if __name__ == "__main__":
    out = run_pipeline()
    print(json.dumps(out["experiments"]["selection"], indent=2))
    print(json.dumps(json.loads((MODELS_DIR / "model_comparison.json").read_text()), indent=2))
    print("M3 pipeline completed successfully.")
