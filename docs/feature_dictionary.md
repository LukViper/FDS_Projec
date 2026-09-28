# Feature dictionary (Member 2)

All features are computed from the **observation period only**
(2010-01-01 → 2010-12-31), unless noted.  
**Churn label is unchanged from M1** (`data/processed/customer_churn_labels.*`).

| Feature | Definition | Source | Notes |
| ------- | ---------- | ------ | ----- |
| `Customer ID` | Customer key | M1 | Join key |
| `churn` | 1 = no purchase in prediction period | M1 | **Do not redefine** |
| `recency_days` | Days from last observation-period purchase to 2010-12-31 | Cleaned tx | Higher = longer since last buy |
| `frequency` | Count of distinct invoices in observation period | Cleaned tx | ≥ 1 for all labeled customers |
| `monetary` | Sum of `Quantity × Price` in observation period | Cleaned tx | GBP |
| `avg_order_value` | `monetary / frequency` | Derived | Average invoice revenue |
| `purchase_interval_days` | Mean days between consecutive observation invoices | Cleaned tx | Imputed with multi-purchase median when frequency = 1 |
| `purchase_interval_imputed` | 1 if interval was imputed | Derived | Transparency flag for M3 |
| `product_diversity` | Distinct `StockCode` count in observation period | Cleaned tx | Breadth of assortment bought |
| `cancellation_rate` | Cancelled invoices / all invoices (obs period) | **Raw** tx | Invoice IDs starting with `C`; 0 if none |
| `spending_trend` | `(mon_H2 − mon_H1) / (mon_H1 + mon_H2 + ε)` | Cleaned tx | H1=Jan–Jun 2010, H2=Jul–Dec 2010; range ≈ [−1, 1] |
| `order_trend` | `(ord_H2 − ord_H1) / (ord_H1 + ord_H2 + ε)` | Cleaned tx | Same halves; invoice-count trend |
| `obs_n_lines` | Number of line items in observation period | Cleaned tx | Extra descriptive feature |
| `avg_line_quantity` | Mean quantity per line | Cleaned tx | Extra descriptive feature |
| `country` | Modal country from M1 customer table | M1 | Categorical; encode in M3 |

## Leakage controls

- Prediction-period transactions (2011-01-01 → 2011-06-30) are **not** used in any feature.
- `churn` is copied from M1 and validated to match exactly.

## Missing-value policy

| Case | Policy |
| ---- | ------ |
| `purchase_interval_days` when frequency = 1 | Fill with median interval among customers with frequency ≥ 2; set `purchase_interval_imputed = 1` |
| `cancellation_rate` if customer absent in raw obs invoices | Fill with `0` (should be rare for labeled customers) |
| Half-year monetary/orders if no activity in a half | Treat as `0` before trend formula |

## Outlier policy

IQR outlier counts are reported in `data/features/m2_validation_report.json`.  
Outlier rows are **not dropped** (tree models tolerate skew; dropping would bias churn base rates).  
M3 may apply scaling, winsorization, or robust transformers if needed.

## Output artifacts

| Path | Description |
| ---- | ----------- |
| `data/features/customer_features.parquet` | Modelling table |
| `data/features/customer_features.csv` | Same (CSV) |
| `data/features/feature_summary.csv` | Describe statistics |
| `data/features/m2_validation_report.json` | Validation + outlier + figure index |
| `data/features/figures/` | EDA plots |
