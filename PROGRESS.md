# Project Progress

> This file records what has actually been completed.
> Do not mark work complete without repository evidence.

**Last repository inspection:** 2026-09-25

---

## Current Project Status

| Module                  | Owner    | Status      | Completion | Evidence |
| ----------------------- | -------- | ----------- | ---------: | -------- |
| M1 Data & Preprocessing | Member 1 | Completed   |       ~100% | Artifacts + commits on branch `Shasank` (`c9d5a74`). |
| M2 EDA & Features       | Member 2 | In Progress |         ~90% | Features/EDA exist; M2 git commit may still be pending on some machines. |
| M3 Machine Learning     | Member 3 | In Progress |         ~90% | Models trained + `final_model.joblib`; M3 git commit pending. |
| M4 XAI & Deployment     | Member 4 | Not Started |          — | Final model ready for M4; no SHAP/Streamlit yet. |

---

## Repository State

Recorded from inspection on **2026-09-25**.

### Git

| Item | Value |
| ---- | ----- |
| Git repository initialized? | **Yes** |
| Current branch | `Shasank` (tracks `origin/Shasank`) |
| Remote / GitHub | Configured (`origin`) |
| Planned feature branches | Not used yet (`feature/member-2-eda-features` not created) |
| Recent commits | `c9d5a74` Data Preprocessing Done - by Shasank; `238adfb` Plan, Progress and Readme Updated |

### Important directories

| Path | Notes |
| ---- | ----- |
| Project root | `PLAN.md`, `PROGRESS.md`, `viva.tex` remain here |
| `DataSet/` | Raw dataset |
| `notebooks/` | `m1_preprocessing.ipynb`, `m2_eda_features.ipynb` |
| `src/` | `preprocessing.py`, `features.py` |
| `data/processed/` | M1 outputs |
| `data/features/` | M2 outputs + `figures/` |
| `models/` | M3 artifacts present (`final_model.joblib`, metrics) |
| `app/` | Empty (M4) |
| `docs/` | M1 + M2 + M3 documentation |

### Existing datasets

| Path | Size | Notes |
| ---- | ---- | ----- |
| `DataSet/online_retail_II.xlsx` | ~44 MB | Raw UCI Online Retail II |
| `data/processed/transactions_cleaned.parquet` | ~6.0 MB | 779,425 cleaned line items |
| `data/processed/customer_churn_labels.parquet` | ~160 KB | 4,231 customers |
| `data/features/customer_features.parquet` | ~193 KB | 4,231 customers × engineered features |
| `data/features/customer_features.csv` | ~506 KB | CSV twin |
| `models/final_model.joblib` | ~2.1 MB | Selected RF Pipeline for M4 |

### Existing notebooks

| Path | Notes |
| ---- | ----- |
| `notebooks/m1_preprocessing.ipynb` | M1 |
| `notebooks/m2_eda_features.ipynb` | M2 |
| `notebooks/m3_modeling.ipynb` | M3 |

### Existing scripts

| Path | Notes |
| ---- | ----- |
| `src/preprocessing.py` | M1 pipeline |
| `src/features.py` | M2 EDA helpers + feature engineering |
| `src/modeling.py` | M3 temporal split + LR/RF/XGB + selection |
| `src/__init__.py` | Package marker |
| `requirements.txt` | pandas, sklearn, xgboost, joblib, … |

### Existing models

| Path | Notes |
| ---- | ----- |
| `models/final_model.joblib` | Selected Random Forest + preprocess Pipeline |
| `models/final_bundle.joblib` | Pipeline + metadata |
| `models/*_pipeline.joblib` | LR / RF / XGB comparison pipelines |
| `models/model_metrics.json` | Full metrics |
| `models/model_comparison.json` | Comparison table |

### Existing documentation

| Path | Notes |
| ---- | ----- |
| `PLAN.md` / `PROGRESS.md` / `README.md` / `viva.tex` | Project tracking |
| `docs/dataset_source.md` | UCI source |
| `docs/preprocessing_decisions.md` | M1 decisions |
| `docs/m1_faculty_evidence.md` | M1 checklist |
| `docs/feature_dictionary.md` | M2 feature definitions |
| `docs/m2_eda_findings.md` | M2 EDA write-up |
| `docs/m2_faculty_evidence.md` | M2 checklist |
| `docs/experiment_notes.md` | M3 experiments + selection |
| `docs/m3_faculty_evidence.md` | M3 checklist |
| `data/processed/m1_validation_report.json` | M1 validation |
| `data/features/m2_validation_report.json` | M2 validation |

### Existing tests

Validation via `validate_customer_dataset()` (M1) and `validate_features()` / `validate_m1_handoff()` (M2); both report `all_passed: true`.

---

## Member 1 Progress — Data Collection & Preprocessing

### Status

Completed

### Completed

- [x] Download Online Retail II dataset — `DataSet/online_retail_II.xlsx`
- [x] Document source — `docs/dataset_source.md`
- [x] Inspect dataset structure — notebook + pipeline load of both sheets
- [x] Identify columns and data types — documented in source doc / notebook
- [x] Check missing values — 243,007 missing Customer ID rows identified and dropped
- [x] Handle missing Customer ID — drop policy
- [x] Handle cancelled transactions — drop `Invoice` starting with `C` (18,744 rows)
- [x] Clean transaction records — `src/preprocessing.py`
- [x] Check duplicates — 26,124 exact duplicates dropped
- [x] Handle invalid quantities/prices — 71 rows with qty≤0 or price≤0 dropped
- [x] Define observation period — 2010-01-01 → 2010-12-31
- [x] Define prediction period — 2011-01-01 → 2011-06-30
- [x] Define churn criteria — no purchase in prediction period among obs-active customers
- [x] Generate customer-level dataset — 4,231 customers
- [x] Validate churn labels — `all_passed: true`
- [x] Create preprocessing code/notebook — `src/preprocessing.py`, `notebooks/m1_preprocessing.ipynb`
- [x] Document preprocessing decisions — `docs/preprocessing_decisions.md`
- [x] Commit work to GitHub — `c9d5a74` on branch `Shasank`
- [x] Prepare evidence checklist for faculty — `docs/m1_faculty_evidence.md`

### In Progress

- [ ] None

### Blocked

- [ ] None

### Outputs

| Artifact | Path |
| -------- | ---- |
| Cleaned transactions | `data/processed/transactions_cleaned.parquet` |
| Customer churn labels | `data/processed/customer_churn_labels.parquet` |
| Customer churn labels (CSV) | `data/processed/customer_churn_labels.csv` |
| Validation report | `data/processed/m1_validation_report.json` |

### Evidence

- File: `src/preprocessing.py`, `data/processed/*`
- Commit: `c9d5a74` (`Data Preprocessing Done - by Shasank`)
- Branch: `Shasank`
- Screenshot: checklist in `docs/m1_faculty_evidence.md`
- Result: 4,231 customers; churn rate ~52.4%; validation passed

### Handoff to Member 2

- Status: **Accepted by M2** (handoff validated in `m2_validation_report.json`)

### Last Updated

2026-09-25

---

## Member 2 Progress — EDA & Feature Engineering

### Status

In Progress *(implementation + artifacts done; M2 git commit outstanding)*

### Completed

- [x] Load M1 customer-level dataset
- [x] Validate M1 output — matches M1 report; `churn_unchanged: true`
- [x] Analyze customer distribution — country top-10 figure
- [x] Analyze churn distribution — 2217 / 2014; figure saved
- [x] Generate EDA visualizations — `data/features/figures/`
- [x] Create RFM features — `recency_days`, `frequency`, `monetary`
- [x] Create behavioral features — AOV, purchase interval, product diversity, cancellation rate, spending/order trends
- [x] Check feature distributions — histograms + `feature_summary.csv`
- [x] Handle feature-level missing values — purchase-interval median imputation (1,418 customers)
- [x] Detect problematic outliers — IQR report in validation JSON (rows retained)
- [x] Validate features — `feature_validation.all_passed: true`
- [x] Document findings — `docs/feature_dictionary.md`, `docs/m2_eda_findings.md`
- [x] Prepare faculty evidence checklist — `docs/m2_faculty_evidence.md`

### In Progress

- [ ] Commit M2 work to GitHub
- [ ] Optional: create/use `feature/member-2-eda-features` branch naming

### Blocked

- [ ] None

### Outputs

| Artifact | Path |
| -------- | ---- |
| Feature table | `data/features/customer_features.parquet` |
| Feature table (CSV) | `data/features/customer_features.csv` |
| Feature summary | `data/features/feature_summary.csv` |
| Validation report | `data/features/m2_validation_report.json` |
| EDA figures | `data/features/figures/*.png` |

### Evidence

- File: `src/features.py`, `notebooks/m2_eda_features.ipynb`
- File: `docs/feature_dictionary.md`, `docs/m2_eda_findings.md`
- Commit: *pending*
- Branch: working on `Shasank` (uncommitted M2 files)
- Screenshot: figures under `data/features/figures/`
- Result: 4,231 rows; 0 nulls in core numerics; strongest |corr| with churn: recency (+0.31), product diversity (−0.29), frequency (−0.27)

### Handoff to Member 3

- Status: **Accepted by M3** (validated in `models/model_metrics.json`)

### Last Updated

2026-09-25

---

## Member 3 Progress — Machine Learning

### Status

In Progress *(training + artifacts done; M3 git commit outstanding)*

### Completed

- [x] Load M2 feature dataset
- [x] Validate feature integrity — `m2_handoff_validation.all_passed`
- [x] Define temporal train/validation/test split — by `obs_last_purchase`
- [x] Prevent temporal/data leakage — documented in metrics JSON
- [x] Analyze class imbalance — train 74.1% / val 56.2% / test 37.3% churn
- [x] Apply imbalance handling — `class_weight` / `scale_pos_weight`
- [x] Train Logistic Regression, Random Forest, XGBoost
- [x] Evaluate ROC-AUC, PR-AUC, Precision, Recall, F1, Confusion Matrix
- [x] Compare models — `models/model_comparison.json`
- [x] Select model — **random_forest** (best validation PR-AUC 0.725)
- [x] Save trained model — `models/final_model.joblib`
- [x] Save preprocessing pipeline — embedded in Pipeline + `final_bundle.joblib`
- [x] Document experiments — `docs/experiment_notes.md`
- [x] Prepare faculty evidence checklist — `docs/m3_faculty_evidence.md`

### In Progress

- [ ] Commit M3 work to GitHub

### Blocked

- [ ] None

### Outputs

| Artifact | Path |
| -------- | ---- |
| Final model | `models/final_model.joblib` |
| Bundle | `models/final_bundle.joblib` |
| Comparison | `models/model_comparison.json` |
| Full metrics | `models/model_metrics.json` |

**Selected test metrics (Random Forest):** ROC-AUC 0.755 · PR-AUC 0.625 · Precision 0.646 · Recall 0.494 · F1 0.560

### Evidence

- File: `src/modeling.py`, `notebooks/m3_modeling.ipynb`, `docs/experiment_notes.md`
- Commit: *pending*
- Branch: `Shasank` (uncommitted M3 files)
- Result: RF selected over LR and XGB by validation PR-AUC

### Handoff to Member 4

- Status: **Ready**
- Load: `models/final_model.joblib` (or `final_bundle.joblib`)
- Do not retrain a substitute without Decision Log entry

### Last Updated

2026-09-28

---

## Member 4 Progress — Explainable AI & Deployment

### Status

Not Started

### Completed

- [ ] *(none)*

### In Progress

- [ ] None

### Blocked

- [ ] Previously blocked on M3 model + pipeline — **blocker cleared** (`models/final_model.joblib` ready)


### Outputs

- None

### Evidence

- File: —
- Commit: —
- Branch: —
- Screenshot: —
- Result: —

### Last Updated

2026-09-25

---

## 3. Milestone Tracker

| Milestone                      | Owner | Status      | Evidence |
| ------------------------------ | ----- | ----------- | -------- |
| Dataset acquired               | M1    | Completed   | `DataSet/online_retail_II.xlsx` |
| Dataset documented             | M1    | Completed   | `docs/dataset_source.md` |
| Preprocessing completed        | M1    | Completed   | `src/preprocessing.py` + `transactions_cleaned.parquet` |
| Churn definition finalized     | M1    | Completed   | `docs/preprocessing_decisions.md` + report periods |
| Customer dataset generated     | M1    | Completed   | `data/processed/customer_churn_labels.parquet` (4,231 rows; validation passed) |
| EDA completed                  | M2    | Completed   | `data/features/figures/` + `docs/m2_eda_findings.md` |
| Feature engineering completed  | M2    | Completed   | `data/features/customer_features.parquet` (`all_passed`) |
| Temporal split implemented     | M3    | Completed   | `src/modeling.py` + `model_metrics.json` temporal_split |
| Models trained                 | M3    | Completed   | LR / RF / XGB pipelines under `models/` |
| Model evaluation completed     | M3    | Completed   | `models/model_comparison.json` |
| Final model saved              | M3    | Completed   | `models/final_model.joblib` (random_forest) |
| SHAP implemented               | M4    | Not Started | — |
| Statistical analysis completed | M4    | Not Started | — |
| Streamlit completed            | M4    | Not Started | — |
| Final integration completed    | M4    | Not Started | — |
| Final documentation completed  | All   | Not Started | Tracking docs + M1 docs only |

---

## 4. Git Contribution Log

| Date | Member | Branch | Commit | Description | Evidence |
| ---- | ------ | ------ | ------ | ----------- | -------- |
| 2026-09-25 | Member 1 (Shasank) | `Shasank` | `238adfb` | Plan, Progress and Readme Updated | `git log` |
| 2026-09-25 | Member 1 (Shasank) | `Shasank` | `c9d5a74` | Data Preprocessing Done - by Shasank | `git log`; M1 artifacts |
| 2026-09-25 | Member 2 | `Shasank` | — | M2 features/EDA implemented locally; not committed yet | `git status` shows untracked/modified M2 files |
| 2026-09-28 | Member 3 | `Shasank` | — | M3 modelling implemented locally; not committed yet | `models/final_model.joblib` present; untracked/modified |

---

## 5. Decision Log

## Decision: Repository layout adopted

Date: 2026-09-25  
Decision: Use the suggested layout from `PLAN.md`: raw data in `DataSet/`; outputs in `data/processed/`, `data/features/`, `models/`, `app/`; shared code in `src/`; notebooks in `notebooks/`; docs in `docs/`. Keep `PLAN.md` and `PROGRESS.md` at repository root.  
Reason: Align folder structure with sequential M1→M4 handoffs.  
Evidence: Directories and folder READMEs created; raw file at `DataSet/online_retail_II.xlsx`.  
Affected Modules: All  

## Decision: Missing Customer ID handling

Date: 2026-09-25  
Decision: Drop rows with missing `Customer ID`.  
Reason: Churn requires customer identity across time.  
Evidence: `docs/preprocessing_decisions.md`; 243,007 rows dropped (`m1_validation_report.json`).  
Affected Modules: M1, M2, M3  

## Decision: Cancellation handling

Date: 2026-09-25  
Decision: Drop invoices whose `Invoice` starts with `C`.  
Reason: Cancellations are not completed purchases.  
Evidence: 18,744 rows dropped; documented in `docs/preprocessing_decisions.md`.  
Affected Modules: M1, M2  

## Decision: Invalid quantity/price handling

Date: 2026-09-25  
Decision: Drop rows with `Quantity <= 0` or `Price <= 0`.  
Reason: Invalid sales lines / non-purchase adjustments.  
Evidence: 71 rows dropped; `docs/preprocessing_decisions.md`.  
Affected Modules: M1, M2  

## Decision: Observation period

Date: 2026-09-25  
Decision: 2010-01-01 through 2010-12-31.  
Reason: Full calendar year of activity inside dataset span with room for a future label window.  
Evidence: `docs/preprocessing_decisions.md`, `src/preprocessing.py` constants, validation report.  
Affected Modules: M1–M4  

## Decision: Prediction period

Date: 2026-09-25  
Decision: 2011-01-01 through 2011-06-30.  
Reason: Six-month forward window within available data.  
Evidence: same as observation period decision.  
Affected Modules: M1–M4  

## Decision: Churn definition

Date: 2026-09-25  
Decision: Eligible customers have ≥1 cleaned purchase in the observation period. `churn=1` if zero cleaned purchases in the prediction period; else `churn=0`.  
Reason: Temporal, leakage-aware label suitable for sequential modeling.  
Evidence: `docs/preprocessing_decisions.md`; 2,217 churn / 2,014 retained; validation `all_passed`.  
Affected Modules: M1–M4  

## Decision: Feature window (observation only)

Date: 2026-09-25  
Decision: All M2 features use 2010-01-01 → 2010-12-31 transactions only; M1 `churn` copied unchanged.  
Reason: Prevent target leakage into features.  
Evidence: `docs/feature_dictionary.md`; `m2_validation_report.json` → `churn_unchanged: true`.  
Affected Modules: M2, M3, M4  

## Decision: Purchase-interval imputation

Date: 2026-09-25  
Decision: For frequency = 1, impute `purchase_interval_days` with median of multi-purchase customers (48.75 days); flag via `purchase_interval_imputed`.  
Reason: Single-purchase customers have no inter-purchase gap; models need a numeric value without dropping ~1,418 customers.  
Evidence: `docs/feature_dictionary.md`; `m2_validation_report.json`.  
Affected Modules: M2, M3  

## Decision: Outliers retained

Date: 2026-09-25  
Decision: Report IQR outliers; do not delete outlier customers from the feature table.  
Reason: Preserve churn base rate; tree models tolerate skew; M3 may scale/winsorize.  
Evidence: `outlier_iqr_summary` in `m2_validation_report.json`.  
Affected Modules: M2, M3  

## Decision: Cancellation rate from raw data

Date: 2026-09-25  
Decision: Compute observation-period cancellation rate from raw invoices (`C`-prefix), not cleaned parquet.  
Reason: M1 cleaning removes cancellations; rate would otherwise be undefined/zero.  
Evidence: `src/features.py` `compute_cancellation_rates()`; feature dictionary.  
Affected Modules: M2, M3  

## Decision: Temporal split by obs_last_purchase

Date: 2026-09-28  
Decision: Train ≤ 2010-08-31; Val 2010-09-01..2010-10-31; Test ≥ 2010-11-01 (by last observation-period purchase).  
Reason: Calendar temporal/cohort split; avoids random mixing of early/late customers.  
Evidence: `docs/experiment_notes.md`; `models/model_metrics.json`.  
Affected Modules: M3, M4  

## Decision: Imbalance handling

Date: 2026-09-28  
Decision: LR/RF use `class_weight='balanced'`; XGBoost uses `scale_pos_weight=n_neg/n_pos` on train.  
Reason: Train churn rate (~74%) differs from test (~37%) under temporal split.  
Evidence: `models/model_metrics.json` → experiments.imbalance.  
Affected Modules: M3  

## Decision: Final model selection

Date: 2026-09-28  
Decision: Select **Random Forest** as final model.  
Reason: Highest validation PR-AUC (0.725) vs LR (0.691) and XGBoost (0.691); ties broken by ROC-AUC/F1 rule documented in code.  
Evidence: `models/model_comparison.json`; `docs/experiment_notes.md`.  
Affected Modules: M3, M4  


## 6. Experiment Log

| Experiment | Model/Method | Dataset | Parameters | Metrics | Result | Commit |
| ---------- | ------------ | ------- | ---------- | ------- | ------ | ------ |
| M3-1 | Logistic Regression | M2 features; temporal split | balanced, lbfgs | Val PR-AUC 0.691; Test PR-AUC 0.595 | Not selected (low recall under shift) | — |
| M3-2 | Random Forest | same | balanced, 300 trees, depth 10 | Val PR-AUC 0.725; Test ROC-AUC 0.755 | **Selected final** | — |
| M3-3 | XGBoost | same | scale_pos_weight, 300 est | Val PR-AUC 0.691; Test PR-AUC 0.573 | Not selected | — |

Selection criterion: highest validation PR-AUC. Details: `models/model_comparison.json`.

---

## 7. Problems & Resolutions

| Date       | Problem | Module | Cause | Resolution | Commit |
| ---------- | ------- | ------ | ----- | ---------- | ------ |
| 2026-09-25 | Git history / branches / commits cannot be used for faculty evidence yet | All | Git initialized on `master` but has zero commits, no remotes, no feature branches | **Resolved for M1:** commits exist on `Shasank` (`c9d5a74`). M2 commit still pending. | `c9d5a74` |
| 2026-09-25 | `to_parquet` failed on `StockCode` | M1 | Mixed int/str values in object column | Cast `Invoice`, `StockCode`, `Description`, `Country` to `str` before write | — |

---

## 8. Handoff Log

## M1 → M2

Status: **Completed / accepted**  
Date: 2026-09-25  
Input artifact: `DataSet/online_retail_II.xlsx`  
Output artifact: `data/processed/customer_churn_labels.parquet` (+ cleaned tx)  
Validation performed: M1 report + M2 `m1_handoff_validation.all_passed = true`  
Known limitations: Observation `obs_*` fields superseded by M2 engineered features for modelling  
Git commit: `c9d5a74`  
Receiving member: Member 2  

## M2 → M3

Status: **Completed / accepted**  
Date: 2026-09-28  
Input artifact: `data/features/customer_features.parquet`  
Output artifact consumed by M3: same + M1 dates for split  
Validation performed: M3 `m2_handoff_validation.all_passed = true`  
Known limitations: categorical `country` one-hot encoded in M3 pipeline  
Git commit: —  
Receiving member: Member 3  

## M3 → M4

Status: **Ready** (awaiting Member 4 acknowledgment)  
Date: 2026-09-28  
Input artifact: `data/features/customer_features.parquet`  
Output artifact: `models/final_model.joblib` (+ `final_bundle.joblib`, metrics JSON)  
Validation performed: comparison across LR/RF/XGB; RF selected on val PR-AUC; test ROC-AUC 0.755  
Known limitations:  
- M3 git commit not yet recorded  
- Default probability threshold 0.5; M4/business may retune threshold  
- Temporal cohort shift (train churn 74% vs test 37%)  
Git commit: —  
Receiving member: Member 4  

---

## 9. Faculty Demonstration Checklist

### Member 1

* [x] Can explain preprocessing — code + docs exist
* [x] Can explain dataset — `docs/dataset_source.md`
* [x] Can explain missing-value handling
* [x] Can explain cancellation handling
* [x] Can explain observation period
* [x] Can explain prediction period
* [x] Can explain churn definition
* [x] Can show code — `src/preprocessing.py`, notebook
* [x] Can show GitHub branch — `Shasank`
* [x] Can show commits — `c9d5a74`
* [x] Can show generated dataset — `data/processed/customer_churn_labels.*`

### Member 2

* [x] Can explain EDA — `docs/m2_eda_findings.md` + figures
* [x] Can explain RFM — feature dictionary
* [x] Can explain behavioral features — feature dictionary
* [x] Can explain visualizations — `data/features/figures/`
* [x] Can show code — `src/features.py`, `notebooks/m2_eda_features.ipynb`
* [ ] Can show GitHub commits — **M2 commit pending**

### Member 3

* [x] Can explain temporal split — by `obs_last_purchase`
* [x] Can explain class imbalance — rates + class_weight / scale_pos_weight
* [x] Can explain all three models — LR / RF / XGB trained
* [x] Can explain evaluation metrics — ROC-AUC, PR-AUC, P/R/F1, CM
* [x] Can show experimental results — `models/model_comparison.json`
* [x] Can show trained model — `models/final_model.joblib`
* [ ] Can show GitHub commits — **M3 commit pending**

### Member 4

* [ ] Can explain SHAP
* [ ] Can explain global explanation
* [ ] Can explain local explanation
* [ ] Can explain statistical analysis
* [ ] Can demonstrate Streamlit
* [ ] Can explain model integration
* [ ] Can show GitHub commits

---

## Progress Update Rules

1. Never claim completion without evidence.
2. Every completed task should reference a file, result, commit, or other verifiable artifact.
3. Record important decisions when they are made.
4. Record blockers immediately.
5. Record handoffs between members.
6. Do not delete historical progress.
7. Update the Git contribution log after meaningful commits.
8. Keep planned work in `PLAN.md` and actual work in `PROGRESS.md`.
