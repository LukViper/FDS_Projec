# Project Progress

> This file records what has actually been completed.
> Do not mark work complete without repository evidence.

**Last repository inspection:** 2026-09-25

---

## Current Project Status

| Module                  | Owner    | Status      | Completion | Evidence |
| ----------------------- | -------- | ----------- | ---------: | -------- |
| M1 Data & Preprocessing | Member 1 | In Progress |         ~90% | Pipeline, docs, and artifacts exist; git branch/commits not created yet (DoD incomplete). See Member 1 section. |
| M2 EDA & Features       | Member 2 | Not Started |          — | Waiting on formal M1→M2 handoff acknowledgment; input artifact is ready. |
| M3 Machine Learning     | Member 3 | Not Started |          — | No training scripts, metrics, or model artifacts found. |
| M4 XAI & Deployment     | Member 4 | Not Started |          — | No SHAP code, statistical analysis, or Streamlit app found. |

**Status legend:** `Not Started` · `In Progress` · `Blocked` · `Needs Verification` · `Completed`

Completion % for M1 is approximate from the task checklist (git/faculty screenshots still open). Do not invent % for other modules.

---

## Repository State

Recorded from inspection on **2026-09-25**.

### Git

| Item | Value |
| ---- | ----- |
| Git repository initialized? | **Yes** (empty history — no commits yet) |
| Current branch | `master` (no commits) |
| Remote / GitHub | **Not configured / not verifiable** |
| Feature branches | **None** — `feature/member-1-preprocessing` not created yet |
| Commits | **None** |

### Important directories

| Path | Notes |
| ---- | ----- |
| Project root | `/home/luk_viper/FDS_Project` — `PLAN.md` and `PROGRESS.md` remain here |
| `DataSet/` | Raw dataset |
| `notebooks/` | Contains `m1_preprocessing.ipynb` |
| `src/` | Contains `preprocessing.py` |
| `data/processed/` | M1 outputs present |
| `data/features/` | Empty (M2) |
| `models/` | Empty (M3) |
| `app/` | Empty (M4) |
| `docs/` | M1 documentation present |

### Existing datasets

| Path | Size | Notes |
| ---- | ---- | ----- |
| `DataSet/online_retail_II.xlsx` | ~44 MB | Raw UCI Online Retail II |
| `data/processed/transactions_cleaned.parquet` | ~6.0 MB | 779,425 cleaned line items |
| `data/processed/customer_churn_labels.parquet` | ~160 KB | 4,231 customers |
| `data/processed/customer_churn_labels.csv` | ~550 KB | Same labels (CSV for easy inspection) |

### Existing notebooks

| Path | Notes |
| ---- | ----- |
| `notebooks/m1_preprocessing.ipynb` | M1 documentation / runnable notebook |

### Existing scripts

| Path | Notes |
| ---- | ----- |
| `src/preprocessing.py` | M1 load → clean → label → validate → write |
| `src/__init__.py` | Package marker |
| `requirements.txt` | pandas, openpyxl, pyarrow, jupyter |

### Existing models

*None found.*

### Existing documentation

| Path | Notes |
| ---- | ----- |
| `PLAN.md` | Roadmap |
| `PROGRESS.md` | This file |
| `README.md` | Layout overview |
| `viva.tex` | Viva / defence notes: what–how–why per member (M1 evidenced; M2–M4 planned) |
| `docs/dataset_source.md` | UCI source documentation |
| `docs/preprocessing_decisions.md` | Cleaning + churn decisions |
| `docs/m1_faculty_evidence.md` | Faculty evidence checklist |
| `data/processed/m1_validation_report.json` | Cleaning stats + validation |

### Existing tests

*No automated test suite.* Validation performed via `validate_customer_dataset()` (`all_passed: true` in report).

---

## Member 1 Progress — Data Collection & Preprocessing

### Status

In Progress *(implementation + artifacts done; git branch/commits outstanding for full DoD)*

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
- [x] Prepare evidence checklist for faculty — `docs/m1_faculty_evidence.md`

### In Progress

- [ ] Commit work to GitHub (no commits exist yet)
- [ ] Create / push `feature/member-1-preprocessing`
- [ ] Capture screenshots into faculty submission pack

### Blocked

- [ ] None for preprocessing logic

### Outputs

| Artifact | Path |
| -------- | ---- |
| Cleaned transactions | `data/processed/transactions_cleaned.parquet` |
| Customer churn labels | `data/processed/customer_churn_labels.parquet` |
| Customer churn labels (CSV) | `data/processed/customer_churn_labels.csv` |
| Validation report | `data/processed/m1_validation_report.json` |

**Key results (from validation report):**

| Metric | Value |
| ------ | ----- |
| Raw rows | 1,067,371 |
| Cleaned rows | 779,425 |
| Eligible customers | 4,231 |
| Churned (`churn=1`) | 2,217 |
| Retained (`churn=0`) | 2,014 |
| Churn rate | ~52.4% |
| Validation | `all_passed: true` |

### Evidence

- File: `src/preprocessing.py`
- File: `notebooks/m1_preprocessing.ipynb`
- File: `docs/dataset_source.md`
- File: `docs/preprocessing_decisions.md`
- File: `data/processed/customer_churn_labels.parquet`
- File: `data/processed/m1_validation_report.json`
- Commit: *none yet*
- Branch: current local branch `master` (empty history); planned `feature/member-1-preprocessing` **does not exist**
- Screenshot: *not stored in repo yet*
- Result: pipeline run succeeded 2026-09-25 (`python -m src.preprocessing`)

### Handoff to Member 2

- Status: **Ready for M2** (artifact available; awaiting M2 acknowledgment)
- Input for M2: `data/processed/customer_churn_labels.parquet` (and optionally cleaned transactions)
- Do **not** redefine `churn` without a Decision Log entry
- `obs_*` columns use observation-period data only

### Last Updated

2026-09-25

---

## Member 2 Progress — EDA & Feature Engineering

### Status

Not Started

### Completed

- [ ] *(none)*

### In Progress

- [ ] None

### Blocked

- [ ] Previously blocked on missing customer dataset — **blocker cleared** (artifact now exists). M2 may start after reading M1 docs.

### Outputs

- None

### Evidence

- File: —
- Commit: —
- Branch: —
- Screenshot: —
- Result: —

### Handoff to Member 3

- Status: **Not ready**

### Last Updated

2026-09-25

---

## Member 3 Progress — Machine Learning

### Status

Not Started

### Completed

- [ ] *(none)*

### In Progress

- [ ] None

### Blocked

- [ ] Blocked on M2 feature dataset

### Outputs

- None

### Evidence

- File: —
- Commit: —
- Branch: —
- Screenshot: —
- Result: —

### Handoff to Member 4

- Status: **Not ready**

### Last Updated

2026-09-25

---

## Member 4 Progress — Explainable AI & Deployment

### Status

Not Started

### Completed

- [ ] *(none)*

### In Progress

- [ ] None

### Blocked

- [ ] Blocked on M3 model + pipeline

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
| EDA completed                  | M2    | Not Started | — |
| Feature engineering completed  | M2    | Not Started | — |
| Temporal split implemented     | M3    | Not Started | — |
| Models trained                 | M3    | Not Started | — |
| Model evaluation completed     | M3    | Not Started | — |
| Final model saved              | M3    | Not Started | — |
| SHAP implemented               | M4    | Not Started | — |
| Statistical analysis completed | M4    | Not Started | — |
| Streamlit completed            | M4    | Not Started | — |
| Final integration completed    | M4    | Not Started | — |
| Final documentation completed  | All   | Not Started | Tracking docs + M1 docs only |

---

## 4. Git Contribution Log

| Date | Member | Branch | Commit | Description | Evidence |
| ---- | ------ | ------ | ------ | ----------- | -------- |
| —    | —      | `master` | — | No commits verifiable yet | `git status`: no commits; M1 files currently untracked |

Populate after the first meaningful commit.

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

---

## 6. Experiment Log

| Experiment | Model/Method | Dataset | Parameters | Metrics | Result | Commit |
| ---------- | ------------ | ------- | ---------- | ------- | ------ | ------ |
| —          | —            | —       | —          | —       | —      | —      |

No ML experiments yet (M3).

---

## 7. Problems & Resolutions

| Date       | Problem | Module | Cause | Resolution | Commit |
| ---------- | ------- | ------ | ----- | ---------- | ------ |
| 2026-09-25 | Git history / branches / commits cannot be used for faculty evidence yet | All | Git initialized on `master` but has zero commits, no remotes, no feature branches | Make initial commit(s), align to `main` if desired, add GitHub remote, create `feature/member-1-preprocessing` | — |
| 2026-09-25 | `to_parquet` failed on `StockCode` | M1 | Mixed int/str values in object column | Cast `Invoice`, `StockCode`, `Description`, `Country` to `str` before write | — |

---

## 8. Handoff Log

## M1 → M2

Status: **Ready** (awaiting Member 2 acknowledgment)  
Date: 2026-09-25  
Input artifact: `DataSet/online_retail_II.xlsx`  
Output artifact: `data/processed/customer_churn_labels.parquet` (+ CSV twin; cleaned tx in `transactions_cleaned.parquet`)  
Validation performed: `data/processed/m1_validation_report.json` → `validation.all_passed = true`  
Known limitations:  
- Git commit hash not yet available for provenance  
- Observation-period summary fields (`obs_*`) are for validation/handoff; M2 should engineer full RFM/behavioral features (may recompute from cleaned transactions)  
- Do not silently redefine `churn`  
Git commit: —  
Receiving member: Member 2  

## M2 → M3

Status: Not started  
Date: —  
Input artifact: —  
Output artifact: engineered feature dataset — **missing**  
Validation performed: —  
Known limitations: Waiting on M2  
Git commit: —  
Receiving member: Member 3  

## M3 → M4

Status: Not started  
Date: —  
Input artifact: —  
Output artifact: trained model + preprocessing pipeline — **missing**  
Validation performed: —  
Known limitations: Waiting on M3  
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
* [ ] Can show GitHub branch — **not created yet**
* [ ] Can show commits — **none yet**
* [x] Can show generated dataset — `data/processed/customer_churn_labels.*`

### Member 2

* [ ] Can explain EDA
* [ ] Can explain RFM
* [ ] Can explain behavioral features
* [ ] Can explain visualizations
* [ ] Can show code
* [ ] Can show GitHub commits

### Member 3

* [ ] Can explain temporal split
* [ ] Can explain class imbalance
* [ ] Can explain all three models
* [ ] Can explain evaluation metrics
* [ ] Can show experimental results
* [ ] Can show trained model
* [ ] Can show GitHub commits

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
