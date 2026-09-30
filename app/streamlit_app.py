"""
M4 Streamlit app — Customer Churn Prediction with SHAP explanations.

Run from repo root:
  streamlit run app/streamlit_app.py

Loads the frozen M3 model at models/final_model.joblib (does not retrain).
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.explain import (
    FEATURE_COLS,
    _positive_class_shap,
    local_explanation,
    load_final_pipeline,
    predict_customer,
    transform_matrix,
    validate_m3_handoff,
)
from src.modeling import FEATURES_PATH, ID_COL, NUMERIC_FEATURES, TARGET


@st.cache_resource
def get_pipeline():
    pipe, selected, model_type = load_final_pipeline()
    return pipe, selected, model_type


@st.cache_data
def load_customers() -> pd.DataFrame:
    return pd.read_parquet(FEATURES_PATH)


@st.cache_resource
def get_shap_background(_pipe, df: pd.DataFrame, n: int = 100, seed: int = 42):
    """Cache transformed SHAP background once per session/resource."""
    bg = df.sample(n=min(n, len(df)), random_state=seed)
    Xt_bg, names = transform_matrix(_pipe, bg)
    return Xt_bg, names


def main() -> None:
    st.set_page_config(
        page_title="Churn Prediction + SHAP",
        page_icon="📉",
        layout="wide",
    )
    st.title("Customer Churn Prediction with Explainable AI")
    st.caption("Member 4 demo — uses frozen M3 Random Forest pipeline")

    try:
        pipe, selected, model_type = get_pipeline()
        handoff = validate_m3_handoff(pipe)
        df = load_customers()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Failed to load model/data: {exc}")
        st.code(traceback.format_exc())
        st.stop()

    if not handoff["all_passed"]:
        st.error("M3 handoff validation failed. Check models/final_model.joblib.")
        st.json(handoff)
        st.stop()

    st.sidebar.success(f"Model loaded: {selected} ({model_type})")
    st.sidebar.caption("Artifact: models/final_model.joblib")
    st.sidebar.write(f"Customers available: {len(df):,}")

    mode = st.sidebar.radio(
        "Input mode",
        ["Select existing customer", "Manual feature entry"],
    )

    try:
        if mode == "Select existing customer":
            id_min = int(df[ID_COL].min())
            id_max = int(df[ID_COL].max())
            default_id = int(df[ID_COL].iloc[0])
            cid = st.sidebar.number_input(
                "Customer ID",
                min_value=id_min,
                max_value=id_max,
                value=default_id,
                step=1,
            )
            matches = df.loc[df[ID_COL] == int(cid)]
            if matches.empty:
                st.error(f"Customer ID {int(cid)} not found in the feature table.")
                st.stop()
            row = matches.iloc[0]
        else:
            st.sidebar.markdown("### Enter observation-period features")
            defaults = df[NUMERIC_FEATURES].median(numeric_only=True)
            values = {}
            for col in NUMERIC_FEATURES:
                values[col] = st.sidebar.number_input(
                    col,
                    value=float(defaults[col]),
                    format="%.4f",
                )
            countries = sorted(df["country"].dropna().astype(str).unique().tolist())
            values["country"] = st.sidebar.selectbox("country", countries)
            row = pd.Series({ID_COL: -1, TARGET: -1, **values})

        # Basic input validation
        errors = []
        if float(row["recency_days"]) < 0:
            errors.append("recency_days must be ≥ 0")
        if float(row["frequency"]) < 1:
            errors.append("frequency must be ≥ 1")
        if float(row["monetary"]) <= 0:
            errors.append("monetary must be > 0")
        if not (0 <= float(row["cancellation_rate"]) <= 1):
            errors.append("cancellation_rate must be in [0, 1]")
        if errors:
            st.error("Input validation failed:\n- " + "\n- ".join(errors))
            st.stop()

        pred = predict_customer(pipe, row)
        c1, c2, c3 = st.columns(3)
        c1.metric("Churn probability", f"{pred['churn_probability']:.3f}")
        c2.metric("Risk category", pred["risk_category"])
        if pred["actual_churn_label"] is not None and pred["actual_churn_label"] >= 0:
            c3.metric("Actual label (M1)", int(pred["actual_churn_label"]))
        else:
            c3.metric("Actual label (M1)", "n/a")

        st.subheader("Customer information")
        info_cols = [ID_COL, "country"] + NUMERIC_FEATURES
        present = [c for c in info_cols if c in row.index]
        st.dataframe(pd.DataFrame([row[present]]), width="stretch")

        st.subheader("SHAP explanation (local)")
        run_shap = st.button("Compute SHAP explanation", type="primary")
        if run_shap:
            with st.spinner("Computing SHAP values…"):
                import shap

                Xt_bg, names = get_shap_background(pipe, df)
                X_one = pd.DataFrame([row[FEATURE_COLS]])
                Xt_one, _ = transform_matrix(pipe, X_one)
                model = pipe.named_steps["model"]
                explainer = shap.TreeExplainer(model, data=Xt_bg)
                sv = explainer.shap_values(Xt_one)
                shap_row = _positive_class_shap(sv, n_rows=1)[0]
                loc = local_explanation(shap_row, names, top_k=10)
                st.write(
                    "Top contributing factors "
                    "(positive SHAP → higher churn probability):"
                )
                st.dataframe(loc, width="stretch")
                st.bar_chart(loc.iloc[::-1].set_index("feature")["shap_value"])
        else:
            st.info("Click **Compute SHAP explanation** to generate local feature attributions.")

        st.subheader("Risk legend")
        st.markdown(
            """
            - **Low**: probability < 0.33
            - **Medium**: 0.33 ≤ probability < 0.66
            - **High**: probability ≥ 0.66
            """
        )
        st.info(
            "Features must reflect the observation period only. "
            "Do not enter prediction-period purchase information."
        )
    except Exception as exc:  # noqa: BLE001
        st.error(f"App error: {exc}")
        st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
