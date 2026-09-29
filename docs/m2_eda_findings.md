# M2 EDA findings

Date: 2026-09-25  
Module: Member 2 — EDA & Feature Engineering  
Code: `src/features.py`  
Notebook: `notebooks/m2_eda_features.ipynb`

## M1 handoff validation

- Loaded `data/processed/customer_churn_labels.parquet`.
- Confirmed customer count and churn count match `m1_validation_report.json`.
- **Churn labels were not modified.**

## Customer & churn distribution

- Eligible customers: **4,231**
- Churned: **2,217** (~52.4%)
- Retained: **2,014** (~47.6%)
- Class balance is near even; still record imbalance strategy in M3 if thresholds are tuned for business cost.

Figures: `data/features/figures/churn_distribution.png`, `country_top10.png`.

## Feature construction summary

RFM and behavioural features were built from observation-period cleaned transactions
(2010-01-01 to 2010-12-31). Cancellation rate uses raw invoices in the same window
(to observe `C`-prefix cancellations removed during M1 cleaning).

Trends compare H1 (Jan–Jun 2010) vs H2 (Jul–Dec 2010) within the observation year only.

## Distribution / outlier notes

- Monetary and frequency are right-skewed (typical retail).
- IQR outlier percentages are stored per feature in `m2_validation_report.json`.
- Outliers retained for modelling; see feature dictionary for M3 guidance.

## Correlation preview (Pearson with binary churn)

| Feature | Corr. with churn | Direction |
| ------- | ---------------: | --------- |
| `recency_days` | +0.31 | Longer absence → more churn |
| `purchase_interval_days` | +0.07 | Longer gaps → slightly more churn |
| `order_trend` | −0.04 | Rising orders → slightly less churn |
| `spending_trend` | −0.05 | Rising spend → slightly less churn |
| `avg_order_value` | −0.05 | Higher AOV → slightly less churn |
| `cancellation_rate` | −0.11 | More cancel activity → less churn (engagement proxy) |
| `monetary` | −0.14 | Higher spend → less churn |
| `frequency` | −0.27 | More invoices → less churn |
| `product_diversity` | −0.29 | Broader assortment → less churn |

Figure: `data/features/figures/corr_with_churn.png`.

## Outliers (IQR, retained)

Largest IQR outlier shares: purchase interval ~11.8%, monetary ~9.5%, product diversity ~7.2%.  
Rows not deleted — see feature dictionary.

| Artifact | Path |
| -------- | ---- |
| Feature table | `data/features/customer_features.parquet` |
| Dictionary | `docs/feature_dictionary.md` |
| Validation | `data/features/m2_validation_report.json` |

M3 must use a **temporal** protocol consistent with M1 periods and must not use prediction-period fields as features.
