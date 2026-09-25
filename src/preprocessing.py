"""
M1 — Data collection & preprocessing for Online Retail II churn labeling.

Produces:
  - cleaned transaction-level data
  - customer-level churn dataset (observation-period eligibility + label)
  - validation summary
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

# --- Project paths (repo root = parent of src/) ---
ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "DataSet" / "online_retail_II.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"

SHEETS = ("Year 2009-2010", "Year 2010-2011")

# Temporal windows (documented in docs/preprocessing_decisions.md)
OBS_START = pd.Timestamp("2010-01-01")
OBS_END = pd.Timestamp("2010-12-31 23:59:59")
PRED_START = pd.Timestamp("2011-01-01")
PRED_END = pd.Timestamp("2011-06-30 23:59:59")


@dataclass
class CleaningStats:
    rows_raw: int
    rows_after_missing_customer_id: int
    rows_after_cancellations: int
    rows_after_invalid_qty_price: int
    rows_after_duplicates: int
    missing_customer_id_dropped: int
    cancellations_dropped: int
    invalid_qty_price_dropped: int
    duplicates_dropped: int
    date_min: str
    date_max: str


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load and concatenate both Online Retail II sheets."""
    frames = [pd.read_excel(path, sheet_name=sheet) for sheet in SHEETS]
    df = pd.concat(frames, ignore_index=True)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def clean_transactions(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningStats]:
    """
    Clean transaction records:
      1. Drop missing Customer ID
      2. Drop cancelled invoices (Invoice starting with 'C')
      3. Drop invalid Quantity (<=0) or Price (<=0)
      4. Drop exact duplicate rows
    """
    work = df.copy()
    rows_raw = len(work)

    date_min = str(work["InvoiceDate"].min())
    date_max = str(work["InvoiceDate"].max())

    missing_mask = work["Customer ID"].isna()
    missing_dropped = int(missing_mask.sum())
    work = work.loc[~missing_mask].copy()
    after_missing = len(work)

    invoice_str = work["Invoice"].astype(str)
    cancel_mask = invoice_str.str.startswith("C")
    cancel_dropped = int(cancel_mask.sum())
    work = work.loc[~cancel_mask].copy()
    after_cancel = len(work)

    invalid_mask = (work["Quantity"] <= 0) | (work["Price"] <= 0)
    invalid_dropped = int(invalid_mask.sum())
    work = work.loc[~invalid_mask].copy()
    after_invalid = len(work)

    before_dedup = len(work)
    work = work.drop_duplicates()
    dup_dropped = before_dedup - len(work)
    after_dedup = len(work)

    work["Customer ID"] = work["Customer ID"].astype("int64")
    work["InvoiceDate"] = pd.to_datetime(work["InvoiceDate"])
    work["Invoice"] = work["Invoice"].astype(str)
    work["StockCode"] = work["StockCode"].astype(str)
    work["Description"] = work["Description"].astype(str)
    work["Country"] = work["Country"].astype(str)
    work["line_revenue"] = work["Quantity"] * work["Price"]

    stats = CleaningStats(
        rows_raw=rows_raw,
        rows_after_missing_customer_id=after_missing,
        rows_after_cancellations=after_cancel,
        rows_after_invalid_qty_price=after_invalid,
        rows_after_duplicates=after_dedup,
        missing_customer_id_dropped=missing_dropped,
        cancellations_dropped=cancel_dropped,
        invalid_qty_price_dropped=invalid_dropped,
        duplicates_dropped=dup_dropped,
        date_min=date_min,
        date_max=date_max,
    )
    return work.reset_index(drop=True), stats


def build_customer_churn_dataset(
    cleaned: pd.DataFrame,
    obs_start: pd.Timestamp = OBS_START,
    obs_end: pd.Timestamp = OBS_END,
    pred_start: pd.Timestamp = PRED_START,
    pred_end: pd.Timestamp = PRED_END,
) -> pd.DataFrame:
    """
    Build customer-level dataset with temporal churn labels.

    Eligible customers: at least one cleaned purchase in the observation period.
    Churn = 1 if the customer has zero purchases in the prediction period; else 0.

    Observation-period summary fields are included for validation / M2 handoff.
    They use only observation-period transactions (no prediction-period leakage).
    """
    obs = cleaned.loc[
        (cleaned["InvoiceDate"] >= obs_start) & (cleaned["InvoiceDate"] <= obs_end)
    ].copy()
    pred = cleaned.loc[
        (cleaned["InvoiceDate"] >= pred_start) & (cleaned["InvoiceDate"] <= pred_end)
    ].copy()

    if obs.empty:
        raise ValueError("No transactions in observation period — check date windows.")

    obs_agg = (
        obs.groupby("Customer ID", as_index=False)
        .agg(
            obs_first_purchase=("InvoiceDate", "min"),
            obs_last_purchase=("InvoiceDate", "max"),
            obs_n_invoices=("Invoice", "nunique"),
            obs_n_lines=("Invoice", "size"),
            obs_n_unique_products=("StockCode", "nunique"),
            obs_quantity_sum=("Quantity", "sum"),
            obs_monetary=("line_revenue", "sum"),
            country=("Country", lambda s: s.mode().iloc[0] if len(s.mode()) else s.iloc[0]),
        )
    )

    pred_customers = set(pred["Customer ID"].unique())
    obs_agg["purchased_in_prediction"] = obs_agg["Customer ID"].isin(pred_customers)
    obs_agg["churn"] = (~obs_agg["purchased_in_prediction"]).astype("int64")

    obs_agg["observation_start"] = obs_start.normalize()
    obs_agg["observation_end"] = obs_end.normalize()
    obs_agg["prediction_start"] = pred_start.normalize()
    obs_agg["prediction_end"] = pred_end.normalize()

    column_order = [
        "Customer ID",
        "churn",
        "purchased_in_prediction",
        "observation_start",
        "observation_end",
        "prediction_start",
        "prediction_end",
        "obs_first_purchase",
        "obs_last_purchase",
        "obs_n_invoices",
        "obs_n_lines",
        "obs_n_unique_products",
        "obs_quantity_sum",
        "obs_monetary",
        "country",
    ]
    return obs_agg[column_order].sort_values("Customer ID").reset_index(drop=True)


def validate_customer_dataset(customers: pd.DataFrame, cleaned: pd.DataFrame) -> dict[str, Any]:
    """Run sanity checks on churn labels and observation-only aggregates."""
    checks: dict[str, Any] = {}

    checks["n_customers"] = int(len(customers))
    checks["n_churn"] = int(customers["churn"].sum())
    checks["n_retained"] = int((customers["churn"] == 0).sum())
    checks["churn_rate"] = float(customers["churn"].mean())
    checks["duplicate_customer_ids"] = int(customers["Customer ID"].duplicated().sum())
    checks["null_churn_labels"] = int(customers["churn"].isna().sum())

    # Label consistency: churn==1 iff not purchased_in_prediction
    label_consistent = bool(
        (
            (customers["churn"] == 1) == (~customers["purchased_in_prediction"])
        ).all()
    )
    checks["label_matches_prediction_flag"] = label_consistent

    # Observation aggregates must not use prediction-period dates
    obs_dates_ok = bool(
        (customers["obs_first_purchase"] >= customers["observation_start"]).all()
        and (customers["obs_last_purchase"] <= customers["observation_end"]).all()
    )
    checks["obs_purchase_dates_within_observation"] = obs_dates_ok

    # Every labeled customer has >=1 cleaned obs transaction
    obs = cleaned.loc[
        (cleaned["InvoiceDate"] >= OBS_START) & (cleaned["InvoiceDate"] <= OBS_END)
    ]
    obs_ids = set(obs["Customer ID"].unique())
    label_ids = set(customers["Customer ID"])
    checks["all_labeled_customers_in_observation"] = label_ids <= obs_ids
    checks["no_extra_observation_customers_missing"] = obs_ids <= label_ids

    # Monetary / invoice counts positive
    checks["all_obs_monetary_positive"] = bool((customers["obs_monetary"] > 0).all())
    checks["all_obs_invoices_positive"] = bool((customers["obs_n_invoices"] >= 1).all())

    checks["all_passed"] = all(
        [
            checks["duplicate_customer_ids"] == 0,
            checks["null_churn_labels"] == 0,
            checks["label_matches_prediction_flag"],
            checks["obs_purchase_dates_within_observation"],
            checks["all_labeled_customers_in_observation"],
            checks["no_extra_observation_customers_missing"],
            checks["all_obs_monetary_positive"],
            checks["all_obs_invoices_positive"],
            checks["n_customers"] > 0,
        ]
    )
    return checks


def run_pipeline(
    raw_path: Path = RAW_PATH,
    processed_dir: Path = PROCESSED_DIR,
) -> dict[str, Any]:
    """Execute full M1 pipeline and write artifacts under data/processed/."""
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw = load_raw(raw_path)
    cleaned, cleaning_stats = clean_transactions(raw)
    customers = build_customer_churn_dataset(cleaned)
    validation = validate_customer_dataset(customers, cleaned)

    cleaned_path = processed_dir / "transactions_cleaned.parquet"
    customers_path = processed_dir / "customer_churn_labels.parquet"
    customers_csv_path = processed_dir / "customer_churn_labels.csv"
    report_path = processed_dir / "m1_validation_report.json"

    cleaned.to_parquet(cleaned_path, index=False)
    customers.to_parquet(customers_path, index=False)
    customers.to_csv(customers_csv_path, index=False)

    report = {
        "raw_path": str(raw_path.relative_to(ROOT)),
        "sheets": list(SHEETS),
        "periods": {
            "observation_start": str(OBS_START.date()),
            "observation_end": str(OBS_END.date()),
            "prediction_start": str(PRED_START.date()),
            "prediction_end": str(PRED_END.date()),
            "churn_definition": (
                "Eligible customers purchased at least once in the observation period. "
                "churn=1 if they have zero purchases in the prediction period; else 0."
            ),
        },
        "cleaning": asdict(cleaning_stats),
        "validation": validation,
        "outputs": {
            "transactions_cleaned": str(cleaned_path.relative_to(ROOT)),
            "customer_churn_labels_parquet": str(customers_path.relative_to(ROOT)),
            "customer_churn_labels_csv": str(customers_csv_path.relative_to(ROOT)),
        },
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    report["report_path"] = str(report_path.relative_to(ROOT))
    return report


if __name__ == "__main__":
    result = run_pipeline()
    print(json.dumps(result, indent=2))
    if not result["validation"]["all_passed"]:
        raise SystemExit("M1 validation checks failed — see m1_validation_report.json")
    print("M1 pipeline completed successfully.")
