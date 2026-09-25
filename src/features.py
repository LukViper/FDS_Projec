"""
M2 — EDA support helpers and observation-period feature engineering.

Consumes M1 artifacts:
  - data/processed/customer_churn_labels.parquet
  - data/processed/transactions_cleaned.parquet
  - DataSet/online_retail_II.xlsx (cancellation rate only)

Does NOT redefine M1 churn labels.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.preprocessing import (
    OBS_END,
    OBS_START,
    PRED_END,
    PRED_START,
    ROOT,
    load_raw,
)

PROCESSED_DIR = ROOT / "data" / "processed"
FEATURES_DIR = ROOT / "data" / "features"
FIGURES_DIR = FEATURES_DIR / "figures"

CUSTOMERS_PATH = PROCESSED_DIR / "customer_churn_labels.parquet"
TX_PATH = PROCESSED_DIR / "transactions_cleaned.parquet"
M1_REPORT_PATH = PROCESSED_DIR / "m1_validation_report.json"

# Midpoint split of observation year for trend features
OBS_MID = pd.Timestamp("2010-06-30 23:59:59")

FEATURE_COLUMNS = [
    "Customer ID",
    "churn",
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
    "country",
]


def load_m1_customers(path: Path = CUSTOMERS_PATH) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_cleaned_transactions(path: Path = TX_PATH) -> pd.DataFrame:
    tx = pd.read_parquet(path)
    tx["InvoiceDate"] = pd.to_datetime(tx["InvoiceDate"])
    return tx


def validate_m1_handoff(
    customers: pd.DataFrame,
    report_path: Path = M1_REPORT_PATH,
) -> dict[str, Any]:
    """Confirm M1 labels are intact and match the validation report."""
    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected = report["validation"]

    checks: dict[str, Any] = {
        "n_customers": int(len(customers)),
        "n_churn": int(customers["churn"].sum()),
        "churn_rate": float(customers["churn"].mean()),
        "duplicate_customer_ids": int(customers["Customer ID"].duplicated().sum()),
        "null_churn": int(customers["churn"].isna().sum()),
        "matches_m1_n_customers": int(len(customers)) == int(expected["n_customers"]),
        "matches_m1_n_churn": int(customers["churn"].sum()) == int(expected["n_churn"]),
        "churn_values_binary": bool(set(customers["churn"].unique()) <= {0, 1}),
        "m1_report_all_passed": bool(expected.get("all_passed", False)),
    }
    checks["all_passed"] = all(
        [
            checks["duplicate_customer_ids"] == 0,
            checks["null_churn"] == 0,
            checks["matches_m1_n_customers"],
            checks["matches_m1_n_churn"],
            checks["churn_values_binary"],
            checks["m1_report_all_passed"],
        ]
    )
    return checks


def _obs_mask(dates: pd.Series) -> pd.Series:
    return (dates >= OBS_START) & (dates <= OBS_END)


def compute_cancellation_rates(customer_ids: pd.Series) -> pd.DataFrame:
    """
    Cancellation rate in the observation period using raw invoices.

    rate = n_cancelled_invoices / n_invoices_with_customer_id
    (among invoices dated in the observation window).
    """
    raw = load_raw()
    raw = raw.loc[raw["Customer ID"].notna()].copy()
    raw["Customer ID"] = raw["Customer ID"].astype("int64")
    raw["InvoiceDate"] = pd.to_datetime(raw["InvoiceDate"])
    raw = raw.loc[_obs_mask(raw["InvoiceDate"])].copy()
    raw = raw.loc[raw["Customer ID"].isin(set(customer_ids))].copy()

    raw["Invoice"] = raw["Invoice"].astype(str)
    raw["is_cancel"] = raw["Invoice"].str.startswith("C")

    inv = (
        raw.groupby(["Customer ID", "Invoice"], as_index=False)["is_cancel"]
        .max()
    )
    agg = inv.groupby("Customer ID", as_index=False).agg(
        n_invoices_raw=("Invoice", "size"),
        n_cancel_invoices=("is_cancel", "sum"),
    )
    agg["cancellation_rate"] = (
        agg["n_cancel_invoices"] / agg["n_invoices_raw"].clip(lower=1)
    )
    return agg[["Customer ID", "cancellation_rate", "n_cancel_invoices", "n_invoices_raw"]]


def engineer_features(
    customers: pd.DataFrame,
    cleaned: pd.DataFrame,
    cancel_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Build RFM + behavioural features from observation-period cleaned transactions.
    Churn label is copied unchanged from M1 customers.
    """
    labeled_ids = set(customers["Customer ID"])
    obs = cleaned.loc[
        _obs_mask(cleaned["InvoiceDate"]) & cleaned["Customer ID"].isin(labeled_ids)
    ].copy()

    if obs.empty:
        raise ValueError("No observation-period transactions for labeled customers.")

    # Invoice-level table for interval / frequency
    invoices = (
        obs.groupby(["Customer ID", "Invoice"], as_index=False)
        .agg(
            invoice_date=("InvoiceDate", "min"),
            invoice_revenue=("line_revenue", "sum"),
            invoice_qty=("Quantity", "sum"),
            n_lines=("Invoice", "size"),
            n_products=("StockCode", "nunique"),
        )
        .sort_values(["Customer ID", "invoice_date"])
    )

    def _avg_gap(s: pd.Series) -> float:
        if len(s) < 2:
            return np.nan
        gaps = s.sort_values().diff().dt.days.dropna()
        return float(gaps.mean()) if len(gaps) else np.nan

    inv_agg = invoices.groupby("Customer ID").agg(
        frequency=("Invoice", "nunique"),
        monetary=("invoice_revenue", "sum"),
        first_purchase=("invoice_date", "min"),
        last_purchase=("invoice_date", "max"),
        purchase_interval_days=("invoice_date", _avg_gap),
    )

    line_agg = obs.groupby("Customer ID").agg(
        product_diversity=("StockCode", "nunique"),
        obs_n_lines=("Invoice", "size"),
        qty_sum=("Quantity", "sum"),
    )
    line_agg["avg_line_quantity"] = line_agg["qty_sum"] / line_agg["obs_n_lines"]

    # Half-year trends (observation only)
    h1 = obs.loc[obs["InvoiceDate"] <= OBS_MID]
    h2 = obs.loc[obs["InvoiceDate"] > OBS_MID]
    mon_h1 = h1.groupby("Customer ID")["line_revenue"].sum().rename("mon_h1")
    mon_h2 = h2.groupby("Customer ID")["line_revenue"].sum().rename("mon_h2")
    ord_h1 = h1.groupby("Customer ID")["Invoice"].nunique().rename("ord_h1")
    ord_h2 = h2.groupby("Customer ID")["Invoice"].nunique().rename("ord_h2")

    feats = inv_agg.join(line_agg[["product_diversity", "obs_n_lines", "avg_line_quantity"]])
    feats = feats.join(mon_h1, how="left").join(mon_h2, how="left")
    feats = feats.join(ord_h1, how="left").join(ord_h2, how="left")
    feats = feats.fillna({"mon_h1": 0.0, "mon_h2": 0.0, "ord_h1": 0.0, "ord_h2": 0.0})

    feats["recency_days"] = (OBS_END.normalize() - feats["last_purchase"].dt.normalize()).dt.days
    feats["avg_order_value"] = feats["monetary"] / feats["frequency"].clip(lower=1)
    # Relative half-year change; 0 if both halves empty (should not happen for labeled)
    feats["spending_trend"] = (feats["mon_h2"] - feats["mon_h1"]) / (
        feats["mon_h1"] + feats["mon_h2"] + 1e-9
    )
    feats["order_trend"] = (feats["ord_h2"] - feats["ord_h1"]) / (
        feats["ord_h1"] + feats["ord_h2"] + 1e-9
    )

    if cancel_df is None:
        cancel_df = compute_cancellation_rates(customers["Customer ID"])
    feats = feats.join(cancel_df.set_index("Customer ID")[["cancellation_rate"]], how="left")
    feats["cancellation_rate"] = feats["cancellation_rate"].fillna(0.0)

    # Single-purchase customers: no inter-purchase gap — impute with median of multi-purchase
    multi_median = float(feats["purchase_interval_days"].median())
    if np.isnan(multi_median):
        multi_median = float(
            (OBS_END.normalize() - OBS_START.normalize()).days
        )
    feats["purchase_interval_days"] = feats["purchase_interval_days"].fillna(multi_median)
    feats["purchase_interval_imputed"] = inv_agg["purchase_interval_days"].isna().astype("int64")

    country = customers.set_index("Customer ID")["country"]
    churn = customers.set_index("Customer ID")["churn"]

    out = feats.copy()
    out["churn"] = churn
    out["country"] = country
    out = out.reset_index()

    # Ensure every M1 customer appears exactly once
    missing = labeled_ids - set(out["Customer ID"])
    if missing:
        raise ValueError(f"Feature table missing {len(missing)} M1 customers.")

    keep = [c for c in FEATURE_COLUMNS if c in out.columns] + [
        c for c in out.columns if c == "purchase_interval_imputed"
    ]
    # de-dup while preserving order
    seen: set[str] = set()
    ordered: list[str] = []
    for c in keep:
        if c not in seen:
            ordered.append(c)
            seen.add(c)
    return out[ordered].sort_values("Customer ID").reset_index(drop=True)


def detect_outliers_iqr(features: pd.DataFrame, cols: list[str]) -> dict[str, Any]:
    """IQR outlier counts per feature (report only; values not dropped)."""
    summary: dict[str, Any] = {}
    for col in cols:
        s = features[col].astype(float)
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((s < low) | (s > high)).sum())
        summary[col] = {
            "q1": float(q1),
            "q3": float(q3),
            "iqr": float(iqr),
            "low": float(low),
            "high": float(high),
            "n_outliers": n_out,
            "pct_outliers": float(n_out / len(s)) if len(s) else 0.0,
        }
    return summary


def validate_features(
    features: pd.DataFrame,
    customers: pd.DataFrame,
) -> dict[str, Any]:
    numeric_cols = [
        "recency_days",
        "frequency",
        "monetary",
        "avg_order_value",
        "purchase_interval_days",
        "product_diversity",
        "cancellation_rate",
        "spending_trend",
        "order_trend",
    ]
    checks: dict[str, Any] = {
        "n_rows": int(len(features)),
        "n_m1_customers": int(len(customers)),
        "row_count_matches_m1": len(features) == len(customers),
        "duplicate_customer_ids": int(features["Customer ID"].duplicated().sum()),
        "churn_unchanged": bool(
            features.set_index("Customer ID")["churn"]
            .sort_index()
            .equals(customers.set_index("Customer ID")["churn"].sort_index())
        ),
        "null_counts": {c: int(features[c].isna().sum()) for c in numeric_cols},
        "recency_non_negative": bool((features["recency_days"] >= 0).all()),
        "frequency_positive": bool((features["frequency"] >= 1).all()),
        "monetary_positive": bool((features["monetary"] > 0).all()),
        "cancellation_rate_bounds": bool(
            (features["cancellation_rate"] >= 0).all()
            and (features["cancellation_rate"] <= 1).all()
        ),
        "trend_bounds": bool(
            (features["spending_trend"] >= -1).all()
            and (features["spending_trend"] <= 1).all()
            and (features["order_trend"] >= -1).all()
            and (features["order_trend"] <= 1).all()
        ),
    }
    checks["no_null_numeric"] = all(v == 0 for v in checks["null_counts"].values())
    checks["all_passed"] = all(
        [
            checks["row_count_matches_m1"],
            checks["duplicate_customer_ids"] == 0,
            checks["churn_unchanged"],
            checks["no_null_numeric"],
            checks["recency_non_negative"],
            checks["frequency_positive"],
            checks["monetary_positive"],
            checks["cancellation_rate_bounds"],
            checks["trend_bounds"],
        ]
    )
    return checks


def generate_eda_figures(features: pd.DataFrame, figures_dir: Path = FIGURES_DIR) -> list[str]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []

    # Churn distribution
    fig, ax = plt.subplots(figsize=(5, 4))
    counts = features["churn"].value_counts().sort_index()
    ax.bar(["Retained (0)", "Churned (1)"], counts.values, color=["#2a9d8f", "#e76f51"])
    ax.set_ylabel("Customers")
    ax.set_title("Churn distribution (M1 labels)")
    for i, v in enumerate(counts.values):
        ax.text(i, v, str(v), ha="center", va="bottom")
    path = figures_dir / "churn_distribution.png"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    saved.append(str(path.relative_to(ROOT)))

    # Country top-10
    fig, ax = plt.subplots(figsize=(8, 4))
    top = features["country"].value_counts().head(10)
    ax.barh(top.index[::-1], top.values[::-1], color="#264653")
    ax.set_xlabel("Customers")
    ax.set_title("Top 10 countries (observation-period customers)")
    path = figures_dir / "country_top10.png"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    saved.append(str(path.relative_to(ROOT)))

    # RFM by churn
    for col, title in [
        ("recency_days", "Recency (days) by churn"),
        ("frequency", "Frequency by churn"),
        ("monetary", "Monetary by churn (log1p)"),
    ]:
        fig, ax = plt.subplots(figsize=(6, 4))
        data0 = features.loc[features["churn"] == 0, col]
        data1 = features.loc[features["churn"] == 1, col]
        if col == "monetary":
            data0, data1 = np.log1p(data0), np.log1p(data1)
        ax.boxplot([data0, data1], tick_labels=["Retained", "Churned"], showfliers=False)
        ax.set_title(title)
        path = figures_dir / f"box_{col}_by_churn.png"
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        saved.append(str(path.relative_to(ROOT)))

    # Feature histograms
    hist_cols = [
        "recency_days",
        "frequency",
        "avg_order_value",
        "purchase_interval_days",
        "product_diversity",
        "cancellation_rate",
        "spending_trend",
        "order_trend",
    ]
    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.ravel()
    for ax, col in zip(axes, hist_cols):
        ax.hist(features[col], bins=30, color="#457b9d", edgecolor="white")
        ax.set_title(col, fontsize=9)
    fig.suptitle("Feature distributions")
    path = figures_dir / "feature_histograms.png"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    saved.append(str(path.relative_to(ROOT)))

    # Correlation with churn (point-biserial via pearson on 0/1)
    num = features[
        [
            "churn",
            "recency_days",
            "frequency",
            "monetary",
            "avg_order_value",
            "purchase_interval_days",
            "product_diversity",
            "cancellation_rate",
            "spending_trend",
            "order_trend",
        ]
    ]
    corr = num.corr(numeric_only=True)["churn"].drop("churn").sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    colors = ["#e76f51" if v > 0 else "#2a9d8f" for v in corr.values]
    ax.barh(corr.index, corr.values, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("Feature correlation with churn")
    path = figures_dir / "corr_with_churn.png"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    saved.append(str(path.relative_to(ROOT)))

    return saved


def run_pipeline(
    features_dir: Path = FEATURES_DIR,
) -> dict[str, Any]:
    features_dir.mkdir(parents=True, exist_ok=True)

    customers = load_m1_customers()
    cleaned = load_cleaned_transactions()
    m1_checks = validate_m1_handoff(customers)
    if not m1_checks["all_passed"]:
        raise RuntimeError(f"M1 handoff validation failed: {m1_checks}")

    cancel_df = compute_cancellation_rates(customers["Customer ID"])
    features = engineer_features(customers, cleaned, cancel_df=cancel_df)
    feat_checks = validate_features(features, customers)

    outlier_cols = [
        "recency_days",
        "frequency",
        "monetary",
        "avg_order_value",
        "purchase_interval_days",
        "product_diversity",
    ]
    outliers = detect_outliers_iqr(features, outlier_cols)
    figures = generate_eda_figures(features)

    feat_parquet = features_dir / "customer_features.parquet"
    feat_csv = features_dir / "customer_features.csv"
    report_path = features_dir / "m2_validation_report.json"
    summary_path = features_dir / "feature_summary.csv"

    features.to_parquet(feat_parquet, index=False)
    features.to_csv(feat_csv, index=False)

    summary = features.drop(columns=["Customer ID", "country"], errors="ignore").describe(
        percentiles=[0.05, 0.25, 0.5, 0.75, 0.95]
    ).T
    summary.to_csv(summary_path)

    report = {
        "periods": {
            "observation_start": str(OBS_START.date()),
            "observation_end": str(OBS_END.date()),
            "prediction_start": str(PRED_START.date()),
            "prediction_end": str(PRED_END.date()),
            "obs_midpoint_for_trends": str(OBS_MID.date()),
        },
        "m1_handoff_validation": m1_checks,
        "feature_validation": feat_checks,
        "outlier_iqr_summary": outliers,
        "churn_rate": float(features["churn"].mean()),
        "n_features_numeric": len(
            [
                c
                for c in features.columns
                if c not in {"Customer ID", "churn", "country", "purchase_interval_imputed"}
            ]
        ),
        "purchase_interval_impute_median": float(
            features.loc[features["purchase_interval_imputed"] == 0, "purchase_interval_days"].median()
        )
        if (features["purchase_interval_imputed"] == 0).any()
        else None,
        "n_purchase_interval_imputed": int(features["purchase_interval_imputed"].sum()),
        "figures": figures,
        "outputs": {
            "customer_features_parquet": str(feat_parquet.relative_to(ROOT)),
            "customer_features_csv": str(feat_csv.relative_to(ROOT)),
            "feature_summary_csv": str(summary_path.relative_to(ROOT)),
        },
        "note": "M1 churn labels copied unchanged. Features use observation-period data only.",
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(report_path.relative_to(ROOT))

    if not feat_checks["all_passed"]:
        raise RuntimeError(f"M2 feature validation failed: {feat_checks}")
    return report


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2))
    print("M2 pipeline completed successfully.")
