# M3 experiment notes — Machine Learning

Date: 2026-09-28  
Module: Member 3  
Code: `src/modeling.py`  
Notebook: `notebooks/m3_modeling.ipynb`

## Input

- `data/features/customer_features.parquet` (M2)
- `data/processed/customer_churn_labels.parquet` (M1 dates for temporal split only)
- Churn label **unchanged** from M2/M1

## Temporal split (no random shuffle)

| Split | Rule (`obs_last_purchase`) | N | Churn rate |
| ----- | -------------------------- | - | ---------- |
| Train | ≤ 2010-08-31 | (see `models/model_metrics.json`) | higher |
| Val | 2010-09-01 … 2010-10-31 | | |
| Test | ≥ 2010-11-01 | | |

**Why:** Customers are scored in time order of last observation-period activity. This avoids randomly mixing early and late cohorts. Features remain observation-only; labels remain prediction-period churn.

## Leakage controls

- No prediction-period columns as features
- `Customer ID` excluded
- Split uses observation-period timestamps only
- Preprocessing (`StandardScaler`, `OneHotEncoder`) fit on **train** only inside each `sklearn` Pipeline

## Class imbalance

Train churn rate is elevated vs test (temporal drift). Handling:

| Model | Strategy |
| ----- | -------- |
| Logistic Regression | `class_weight='balanced'` |
| Random Forest | `class_weight='balanced'` |
| XGBoost | `scale_pos_weight = n_neg/n_pos` on train |

## Models trained

1. Logistic Regression (`lbfgs`, max_iter=2000)
2. Random Forest (300 trees, max_depth=10, min_samples_leaf=5)
3. XGBoost (300 estimators, max_depth=4, learning_rate=0.05)

## Selection rule

**Highest validation PR-AUC**, ties broken by validation ROC-AUC, then F1.  
Test metrics reported only for the frozen selected model (and full comparison table for transparency).

## Results (actual run)

See `models/model_comparison.json` for exact numbers.

| Model | Val ROC-AUC | Val PR-AUC | Val F1 | Test ROC-AUC | Test PR-AUC | Selected |
| ----- | ----------: | ---------: | -----: | -----------: | ----------: | -------- |
| Logistic Regression | 0.670 | 0.691 | 0.416 | 0.715 | 0.595 | No |
| **Random Forest** | **0.691** | **0.725** | **0.637** | **0.755** | **0.625** | **Yes** |
| XGBoost | 0.659 | 0.691 | 0.693 | 0.709 | 0.573 | No |

**Selected final model: `random_forest`**

Rationale: best validation PR-AUC under the temporal protocol. XGBoost had higher val F1/recall but lower PR-AUC/ROC-AUC; LR collapsed on test recall at threshold 0.5 under cohort shift.

## Artifacts for Member 4

| Path | Description |
| ---- | ----------- |
| `models/final_model.joblib` | Full sklearn Pipeline (preprocess + RF) |
| `models/final_bundle.joblib` | Bundle with metadata + pipeline |
| `models/random_forest_pipeline.joblib` | Same as final (explicit name) |
| `models/logistic_regression_pipeline.joblib` | Comparison artifact |
| `models/xgboost_pipeline.joblib` | Comparison artifact |
| `models/model_metrics.json` | Full metrics + split + leakage notes |
| `models/model_comparison.json` | Compact comparison table |

## Handoff note

M4 must load `models/final_model.joblib` (or `final_bundle.joblib`) — do not retrain a substitute without a Decision Log entry.
