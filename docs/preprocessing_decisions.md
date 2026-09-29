# M1 preprocessing decisions

Date: 2026-09-25  
Module: Member 1 — Data Collection & Preprocessing  
Code: `src/preprocessing.py`  
Notebook: `notebooks/m1_preprocessing.ipynb`

## 1. Raw data handling

- Load both sheets (`Year 2009-2010`, `Year 2010-2011`) and concatenate.
- Keep the original file at `DataSet/online_retail_II.xlsx`.

## 2. Missing Customer ID

**Decision:** Drop all rows with missing `Customer ID`.

**Reason:** Churn is defined at the customer level. Guest transactions cannot be linked across time and would bias labels.

## 3. Cancelled transactions

**Decision:** Drop invoices whose `Invoice` string starts with `C`.

**Reason:** Cancellations are not completed purchases. Including them would distort frequency/monetary behavior used later for features and would confuse purchase presence in the prediction window.

## 4. Invalid quantities and prices

**Decision:** Drop rows with `Quantity <= 0` or `Price <= 0`.

**Reason:** Non-positive quantity/price are invalid retail sales lines (returns already covered via cancellations, or data errors / zero-price adjustments).

## 5. Duplicates

**Decision:** Drop exact duplicate rows after the filters above.

**Reason:** Identical line duplicates are treated as recording artifacts, not additional purchases.

## 6. Observation period

| Field | Value |
| ----- | ----- |
| Start | 2010-01-01 |
| End | 2010-12-31 |

**Reason:** Full calendar year of post-launch activity within the dataset span (2009-12 to 2011-12), leaving a clear future window for labels.

## 7. Prediction period

| Field | Value |
| ----- | ----- |
| Start | 2011-01-01 |
| End | 2011-06-30 |

**Reason:** Six-month forward window is long enough to observe repurchase for retail customers while remaining inside the available data (through 2011-12). Remaining months after 2011-06-30 are unused for M1 labels (available later if the team extends evaluation).

## 8. Churn definition

1. **Eligible customer:** has ≥ 1 cleaned purchase in the observation period.
2. **`churn = 1`:** zero cleaned purchases in the prediction period.
3. **`churn = 0`:** ≥ 1 cleaned purchase in the prediction period.

**Important for M2/M3:** Observation-period summary columns on the customer table (`obs_*`) are computed **only** from observation-period transactions. Prediction-period data is used solely to assign the label.

## 9. Outputs

| Artifact | Path |
| -------- | ---- |
| Cleaned transactions | `data/processed/transactions_cleaned.parquet` |
| Customer churn labels (parquet) | `data/processed/customer_churn_labels.parquet` |
| Customer churn labels (csv) | `data/processed/customer_churn_labels.csv` |
| Validation report | `data/processed/m1_validation_report.json` |

## 10. Changes that require PROGRESS.md updates

If the team changes observation/prediction windows, cancellation rules, or the churn threshold, record a Decision Log entry and re-run validation before M2 proceeds.
