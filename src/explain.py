"""
M4 — SHAP explainability and statistical analysis for the final M3 model.

Loads models/final_model.joblib (Random Forest Pipeline). Does not retrain.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from scipy import stats
from sklearn.pipeline import Pipeline

from src.modeling import (
    CATEGORICAL_FEATURES,
    FEATURES_PATH,
    ID_COL,
    MODELS_DIR,
    NUMERIC_FEATURES,
    TARGET,
    load_modelling_frame,
)
from src.preprocessing import ROOT

XAI_DIR = ROOT / "docs" / "xai"
FIGURES_DIR = XAI_DIR / "figures"
FINAL_MODEL_PATH = MODELS_DIR / "final_model.joblib"
M3_COMPARISON_PATH = MODELS_DIR / "model_comparison.json"

FEATURE_COLS = NUMERIC_FEATURES + CATEGORICAL_FEATURES

RISK_LOW = 0.33
RISK_HIGH = 0.66


def risk_category(prob: float) -> str:
    if prob < RISK_LOW:
        return "Low"
    if prob < RISK_HIGH:
        return "Medium"
    return "High"


def load_final_pipeline(path: Path = FINAL_MODEL_PATH) -> tuple[Pipeline, str | None, str]:
    if not path.exists():
        raise FileNotFoundError(f"Final model not found: {path}")
    pipe = joblib.load(path)
    if not isinstance(pipe, Pipeline) or "model" not in pipe.named_steps:
        raise TypeError("Expected sklearn Pipeline with a 'model' step from M3.")
    comparison = json.loads(M3_COMPARISON_PATH.read_text(encoding="utf-8"))
    selected = comparison.get("selected_model")
    model_type = type(pipe.named_steps["model"]).__name__
    return pipe, selected, model_type


def validate_m3_handoff(pipe: Pipeline) -> dict[str, Any]:
    comparison = json.loads(M3_COMPARISON_PATH.read_text(encoding="utf-8"))
    checks = {
        "final_model_exists": FINAL_MODEL_PATH.exists(),
        "selected_model_in_comparison": comparison.get("selected_model"),
        "pipeline_steps": list(pipe.named_steps.keys()),
        "model_class": type(pipe.named_steps["model"]).__name__,
        "is_random_forest": type(pipe.named_steps["model"]).__name__
        == "RandomForestClassifier",
        "matches_selected_rf": comparison.get("selected_model") == "random_forest",
    }
    checks["all_passed"] = all(
        [
            checks["final_model_exists"],
            checks["is_random_forest"],
            checks["matches_selected_rf"],
            "preprocess" in checks["pipeline_steps"],
            "model" in checks["pipeline_steps"],
        ]
    )
    return checks


def transform_matrix(pipe: Pipeline, X: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    pre = pipe.named_steps["preprocess"]
    Xt = pre.transform(X[FEATURE_COLS])
    names = list(pre.get_feature_names_out())
    return np.asarray(Xt), names


def _positive_class_shap(shap_output: Any, n_rows: int) -> np.ndarray:
    """Normalize SHAP outputs across shap versions to shape (n_rows, n_features)."""
    if isinstance(shap_output, list):
        arr = np.asarray(shap_output[1] if len(shap_output) > 1 else shap_output[0])
    elif hasattr(shap_output, "values"):
        arr = np.asarray(shap_output.values)
        # Explanation for classifiers may be (n, features, classes)
        if arr.ndim == 3:
            arr = arr[:, :, 1] if arr.shape[-1] > 1 else arr[:, :, 0]
    else:
        arr = np.asarray(shap_output)
        if arr.ndim == 3:
            arr = arr[:, :, 1] if arr.shape[-1] > 1 else arr[:, :, 0]
    arr = np.asarray(arr, dtype=float)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.shape[0] != n_rows and arr.shape[1] == n_rows:
        arr = arr.T
    return arr


def compute_shap_values(
    pipe: Pipeline,
    X: pd.DataFrame,
    max_background: int = 200,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """TreeExplainer on the RF using transformed features."""
    model = pipe.named_steps["model"]
    Xt, names = transform_matrix(pipe, X)
    rng = np.random.default_rng(random_state)
    if len(Xt) > max_background:
        idx = rng.choice(len(Xt), size=max_background, replace=False)
        background = Xt[idx]
    else:
        background = Xt
    explainer = shap.TreeExplainer(model, data=background)
    sv = explainer.shap_values(Xt)
    shap_pos = _positive_class_shap(sv, n_rows=len(Xt))
    return shap_pos, Xt, names


def global_importance(shap_values: np.ndarray, feature_names: list[str]) -> pd.DataFrame:
    mean_abs = np.abs(shap_values).mean(axis=0)
    out = pd.DataFrame(
        {"feature": feature_names, "mean_abs_shap": mean_abs}
    ).sort_values("mean_abs_shap", ascending=False)
    return out.reset_index(drop=True)


def local_explanation(
    shap_row: np.ndarray,
    feature_names: list[str],
    top_k: int = 10,
) -> pd.DataFrame:
    values = np.asarray(shap_row, dtype=float).ravel()
    names = list(feature_names)
    if len(values) != len(names):
        raise ValueError(f"SHAP length {len(values)} != n_features {len(names)}")
    order = np.argsort(np.abs(values))[::-1][:top_k]
    return pd.DataFrame(
        {
            "feature": [names[int(i)] for i in order],
            "shap_value": [float(values[int(i)]) for i in order],
            "abs_shap": [float(abs(values[int(i)])) for i in order],
            "direction": [
                "increases_churn" if float(values[int(i)]) > 0 else "decreases_churn"
                for i in order
            ],
        }
    )


def run_statistical_tests(df: pd.DataFrame) -> dict[str, Any]:
    """
    Hypothesis tests relating features to churn label (data-level, not model SHAP).

    Numeric: Mann-Whitney U (churn vs retained) + point-biserial correlation.
    Country: Chi-square independence (top countries + Other).
    """
    alpha = 0.05
    results: dict[str, Any] = {"alpha": alpha, "numeric_tests": [], "categorical_tests": []}

    churned = df[TARGET] == 1
    retained = df[TARGET] == 0

    for col in NUMERIC_FEATURES:
        a = df.loc[churned, col].astype(float)
        b = df.loc[retained, col].astype(float)
        u_stat, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")
        # point-biserial
        r_pb, r_p = stats.pointbiserialr(df[TARGET].astype(float), df[col].astype(float))
        results["numeric_tests"].append(
            {
                "feature": col,
                "test": "mannwhitney_u",
                "statistic": float(u_stat),
                "p_value": float(u_p),
                "significant": bool(u_p < alpha),
                "point_biserial_r": float(r_pb),
                "point_biserial_p": float(r_p),
                "mean_churned": float(a.mean()),
                "mean_retained": float(b.mean()),
            }
        )

    # Chi-square on country (collapse rare levels)
    top = df["country"].value_counts().nlargest(8).index
    country_group = df["country"].where(df["country"].isin(top), other="Other")
    contingency = pd.crosstab(country_group, df[TARGET])
    chi2, chi_p, dof, _ = stats.chi2_contingency(contingency)
    results["categorical_tests"].append(
        {
            "feature": "country",
            "test": "chi_square",
            "statistic": float(chi2),
            "p_value": float(chi_p),
            "dof": int(dof),
            "significant": bool(chi_p < alpha),
        }
    )

    sig = [t for t in results["numeric_tests"] if t["significant"]]
    sig.sort(key=lambda t: t["p_value"])
    results["significant_numeric_features"] = [t["feature"] for t in sig]
    results["n_significant_numeric"] = len(sig)
    results["country_significant"] = bool(chi_p < alpha)
    return results


def save_shap_figures(
    shap_values: np.ndarray,
    Xt: np.ndarray,
    feature_names: list[str],
    global_df: pd.DataFrame,
    figures_dir: Path = FIGURES_DIR,
) -> list[str]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []

    # Global bar
    top = global_df.head(15).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top["feature"], top["mean_abs_shap"], color="#264653")
    ax.set_xlabel("Mean |SHAP|")
    ax.set_title("Global feature importance (SHAP)")
    fig.tight_layout()
    path = figures_dir / "shap_global_importance.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    saved.append(str(path.relative_to(ROOT)))

    # Beeswarm-style via shap summary (matplotlib)
    plt.figure(figsize=(8, 6))
    shap.summary_plot(
        shap_values,
        Xt,
        feature_names=feature_names,
        show=False,
        max_display=15,
    )
    path = figures_dir / "shap_summary.png"
    plt.tight_layout()
    plt.savefig(path, dpi=120, bbox_inches="tight")
    plt.close()
    saved.append(str(path.relative_to(ROOT)))

    return saved


def predict_customer(pipe: Pipeline, row: pd.Series) -> dict[str, Any]:
    X = pd.DataFrame([row[FEATURE_COLS]])
    prob = float(pipe.predict_proba(X)[0, 1])
    return {
        "Customer ID": int(row[ID_COL]) if ID_COL in row else None,
        "churn_probability": prob,
        "risk_category": risk_category(prob),
        "actual_churn_label": int(row[TARGET]) if TARGET in row else None,
        "country": row.get("country"),
    }


def run_pipeline(
    sample_size: int = 500,
    local_examples: int = 5,
    random_state: int = 42,
) -> dict[str, Any]:
    XAI_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    pipe, selected, model_type = load_final_pipeline()
    handoff = validate_m3_handoff(pipe)
    if not handoff["all_passed"]:
        raise RuntimeError(f"M3 handoff validation failed: {handoff}")

    df = load_modelling_frame()
    # Use a reproducible sample for SHAP (full set can be slow)
    rng = np.random.default_rng(random_state)
    if len(df) > sample_size:
        idx = rng.choice(len(df), size=sample_size, replace=False)
        sample = df.iloc[idx].reset_index(drop=True)
    else:
        sample = df.reset_index(drop=True)

    shap_values, Xt, names = compute_shap_values(pipe, sample)
    glob = global_importance(shap_values, names)
    figures = save_shap_figures(shap_values, Xt, names, glob)

    # Local explanations for highest-prob churn customers in sample
    probs = pipe.predict_proba(sample[FEATURE_COLS])[:, 1]
    sample = sample.copy()
    sample["pred_proba"] = probs
    top_idx = np.argsort(probs)[::-1][:local_examples]
    locals_out = []
    for i in top_idx:
        row = sample.iloc[int(i)]
        pred = predict_customer(pipe, row)
        loc = local_explanation(shap_values[int(i)], names, top_k=8)
        locals_out.append(
            {
                "prediction": pred,
                "top_factors": loc.to_dict(orient="records"),
            }
        )

    stats_results = run_statistical_tests(df)

    glob_path = XAI_DIR / "shap_global_importance.csv"
    glob.to_csv(glob_path, index=False)
    locals_path = XAI_DIR / "shap_local_examples.json"
    locals_path.write_text(json.dumps(locals_out, indent=2), encoding="utf-8")
    stats_path = XAI_DIR / "statistical_tests.json"
    stats_path.write_text(json.dumps(stats_results, indent=2), encoding="utf-8")

    report = {
        "m3_handoff_validation": handoff,
        "model_loaded": str(FINAL_MODEL_PATH.relative_to(ROOT)),
        "selected_model": selected,
        "model_class": model_type,
        "shap_sample_size": int(len(sample)),
        "global_importance_top10": glob.head(10).to_dict(orient="records"),
        "figures": figures,
        "statistical_summary": {
            "alpha": stats_results["alpha"],
            "n_significant_numeric": stats_results["n_significant_numeric"],
            "significant_numeric_features": stats_results["significant_numeric_features"],
            "country_significant": stats_results["country_significant"],
        },
        "outputs": {
            "shap_global_importance_csv": str(glob_path.relative_to(ROOT)),
            "shap_local_examples_json": str(locals_path.relative_to(ROOT)),
            "statistical_tests_json": str(stats_path.relative_to(ROOT)),
        },
        "risk_thresholds": {"low_lt": RISK_LOW, "high_gte": RISK_HIGH},
        "note": "Explanations use the frozen M3 final_model.joblib; model was not retrained.",
    }
    report_path = XAI_DIR / "m4_xai_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(report_path.relative_to(ROOT))
    return report


if __name__ == "__main__":
    out = run_pipeline()
    print(json.dumps(out, indent=2))
    print("M4 explainability pipeline completed successfully.")
