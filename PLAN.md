# PLAN.md — Customer Churn Prediction with Explainable AI

> Project roadmap and responsibility plan.
> Planned work lives here. Actual completion status lives in `PROGRESS.md`.

---

## 1. Project Overview

| Field | Description |
| ----- | ----------- |
| **Project title** | Customer Churn Prediction with Explainable AI |
| **Problem statement** | E-commerce businesses lose revenue when customers stop purchasing. Detecting likely churners early allows targeted retention. This project builds a predictive model on historical retail transactions and explains predictions so stakeholders can trust and act on them. |
| **Dataset** | UCI Online Retail II (`DataSet/online_retail_II.xlsx`) — transaction-level online retail data (sheets: Year 2009-2010, Year 2010-2011). Columns include Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country. |
| **Objective** | Build a temporally valid customer-churn classifier, evaluate multiple models, explain predictions with SHAP, and deploy an interactive Streamlit demo. |
| **Expected final system** | End-to-end pipeline: cleaned customer-level dataset → engineered features → trained models → SHAP explanations → Streamlit app showing churn probability, risk category, and top contributing factors. |
| **Academic purpose** | Demonstrate sequential, verifiable individual contribution across data engineering, EDA/features, ML, and XAI/deployment for faculty assessment. |
| **Team size** | 4 members |
| **Development model** | Sequential module-based development (M1 → M2 → M3 → M4) |
| **Primary tools** | Python, Jupyter/VS Code/Cursor, GitHub, Streamlit, SHAP, scikit-learn, XGBoost |

---

## 2. Complete Project Pipeline

```text
Online Retail II Dataset
        ↓
Data Collection
        ↓
Data Cleaning
        ↓
Transaction Filtering
        ↓
Observation / Prediction Period Definition
        ↓
Churn Label Generation
        ↓
Customer-Level Dataset
        ↓
EDA
        ↓
Feature Engineering
        ↓
Temporal Train/Validation/Test Split
        ↓
Class Imbalance Handling
        ↓
Model Training
        ↓
Model Evaluation
        ↓
SHAP Explainability
        ↓
Statistical Analysis
        ↓
Streamlit Deployment
        ↓
Final Documentation
```

---

## 3. Member Responsibilities

### Responsibility Matrix (Summary)

| Area | Member 1 | Member 2 | Member 3 | Member 4 |
| ---- | -------- | -------- | -------- | -------- |
| Raw data & preprocessing | Owner | Consumer | — | — |
| EDA & feature engineering | — | Owner | Consumer | — |
| ML training & evaluation | — | — | Owner | Consumer |
| SHAP, stats, Streamlit | — | — | — | Owner |
| Faculty evidence for own module | Required | Required | Required | Required |
| Git branch ownership | `feature/member-1-preprocessing` | `feature/member-2-eda-features` | `feature/member-3-machine-learning` | `feature/member-4-xai-deployment` |

---

### Member 1 — Data Collection & Preprocessing

| # | Task |
| - | ---- |
| 1 | Download Online Retail II dataset |
| 2 | Document source (UCI / URL / citation) |
| 3 | Inspect dataset structure |
| 4 | Identify columns and data types |
| 5 | Check missing values |
| 6 | Handle missing Customer ID |
| 7 | Handle cancelled transactions |
| 8 | Clean transaction records |
| 9 | Check duplicates |
| 10 | Handle invalid quantities/prices |
| 11 | Define observation period |
| 12 | Define prediction period |
| 13 | Define churn criteria |
| 14 | Generate customer-level dataset |
| 15 | Validate churn labels |
| 16 | Create preprocessing code/notebook |
| 17 | Document preprocessing decisions |
| 18 | Commit work to GitHub |
| 19 | Prepare evidence for faculty |

**Primary outputs (planned):** preprocessing notebook/script, cleaned transaction data, customer-level churn dataset, preprocessing decision notes, Git branch + commits.

---

### Member 2 — EDA & Feature Engineering

| # | Task |
| - | ---- |
| 1 | Load M1 customer-level dataset |
| 2 | Validate M1 output |
| 3 | Analyze customer distribution |
| 4 | Analyze churn distribution |
| 5 | Generate EDA visualizations |
| 6 | Create RFM features |
| 7 | Create behavioral features (see below) |
| 8 | Check feature distributions |
| 9 | Handle feature-level missing values |
| 10 | Detect problematic outliers |
| 11 | Validate features |
| 12 | Document findings |
| 13 | Commit work to GitHub |
| 14 | Prepare faculty evidence |

**Behavioral features to create:**

* Recency
* Frequency
* Monetary value
* Average order value
* Purchase interval
* Product diversity
* Cancellation rate
* Spending trend
* Order trend

**Primary outputs (planned):** EDA notebook, feature dataset, feature dictionary, visualizations, Git branch + commits.

**Constraint:** Must not silently redefine M1 churn labels. Any label change requires team decision + update in `PROGRESS.md`.

---

### Member 3 — Machine Learning

| # | Task |
| - | ---- |
| 1 | Load M2 feature dataset |
| 2 | Validate feature integrity |
| 3 | Define temporal train/validation/test split |
| 4 | Prevent temporal/data leakage |
| 5 | Analyze class imbalance |
| 6 | Apply appropriate imbalance handling |
| 7 | Train Logistic Regression |
| 8 | Train Random Forest |
| 9 | Train XGBoost |
| 10 | Evaluate ROC-AUC, PR-AUC, Precision, Recall, F1, Confusion Matrix |
| 11 | Compare models using actual experimental results |
| 12 | Select model based on documented experimental evidence |
| 13 | Save trained model |
| 14 | Save preprocessing pipeline if required |
| 15 | Document experiments |
| 16 | Commit work to GitHub |
| 17 | Prepare faculty evidence |

**Primary outputs (planned):** training scripts/notebooks, experiment log entries, saved model artifact(s), preprocessing pipeline artifact, evaluation report, Git branch + commits.

**Constraint:** Must not introduce temporal leakage. Prefer temporal split over random split when labels/features are time-dependent.

---

### Member 4 — Explainable AI & Deployment

| # | Task |
| - | ---- |
| 1 | Load final trained model |
| 2 | Implement SHAP |
| 3 | Generate global feature importance |
| 4 | Generate individual customer explanations |
| 5 | Perform statistical analysis / hypothesis testing |
| 6 | Document statistically significant relationships |
| 7 | Build Streamlit interface |
| 8 | Display customer information, churn probability, risk category, top factors, SHAP explanation |
| 9 | Integrate model and preprocessing pipeline |
| 10 | Test application |
| 11 | Document deployment |
| 12 | Commit work to GitHub |
| 13 | Prepare faculty evidence |

**Primary outputs (planned):** SHAP notebook/scripts, statistical analysis notes, Streamlit app, deployment docs, Git branch + commits.

**Constraint:** Must use the actual final trained model produced by M3 (not a substitute or re-trained ad-hoc model without recording the decision).

---

## 4. Dependency Map

```text
M1
 │
 └── customer-level churn dataset
          ↓
M2
 │
 └── engineered feature dataset
          ↓
M3
 │
 └── trained model + preprocessing pipeline
          ↓
M4
 │
 └── SHAP + Streamlit application
          ↓
FINAL PROJECT
```

### Explicit dependency rules

1. **M2 must not silently redefine M1's churn labels.** Label changes require a recorded decision in `PROGRESS.md` and re-validation of downstream work.
2. **M3 must not introduce temporal leakage.** Features and splits must respect observation vs prediction periods defined by M1.
3. **M4 must use the actual final trained model** saved by M3, plus any required preprocessing pipeline.
4. **Any change to an upstream artifact** (dataset schema, labels, features, model, pipeline) **must be recorded in `PROGRESS.md`** and may invalidate downstream handoffs until re-validated.

---

## 5. Git Workflow

### Expected branch structure

```text
main
│
├── feature/member-1-preprocessing
├── feature/member-2-eda-features
├── feature/member-3-machine-learning
└── feature/member-4-xai-deployment
```

### Expected commit style

```text
feat: implement transaction preprocessing
feat: create temporal churn labels
feat: add RFM features
feat: implement XGBoost training
feat: integrate SHAP explanations
```

### Contribution tracking fields

For each meaningful contribution, record in `PROGRESS.md`:

| Field | Meaning |
| ----- | ------- |
| Branch | Feature branch name |
| Commit hash | Full or short SHA |
| Pull request / merge status | Open / Merged / Not created |
| Files contributed | Paths changed |
| Date | Commit or merge date |
| Contributor | Member name / role |

### Suggested repository layout (planned; create as work proceeds)

```text
FDS_Project/
├── PLAN.md
├── PROGRESS.md
├── README.md
├── DataSet/
│   └── online_retail_II.xlsx
├── notebooks/          # or member-specific folders
├── src/
├── data/
│   ├── processed/
│   └── features/
├── models/
├── app/                # Streamlit
└── docs/
```

Exact folder names may be agreed by the team; record the agreed layout in `PROGRESS.md` when created.

---

## 6. Faculty Evidence Requirements

Every member must provide:

1. Work description
2. Screenshots
3. Results
4. Demo video if applicable
5. GitHub branch
6. GitHub commits
7. Final output files

### Member 1 — Evidence Checklist

* [ ] Written work description (preprocessing + churn definition)
* [ ] Screenshots of data inspection / cleaning steps
* [ ] Results (row counts before/after, churn rate, validation checks)
* [ ] Demo video (optional; walkthrough of notebook)
* [ ] GitHub branch: `feature/member-1-preprocessing`
* [ ] GitHub commits linked to preprocessing work
* [ ] Final output files: customer-level dataset + docs

### Member 2 — Evidence Checklist

* [ ] Written work description (EDA + features)
* [ ] Screenshots of visualizations
* [ ] Results (feature summary, distribution notes)
* [ ] Demo video (optional)
* [ ] GitHub branch: `feature/member-2-eda-features`
* [ ] GitHub commits linked to EDA/features
* [ ] Final output files: feature dataset + feature dictionary

### Member 3 — Evidence Checklist

* [ ] Written work description (models + evaluation)
* [ ] Screenshots of metrics / confusion matrices
* [ ] Results (comparison table of LR / RF / XGBoost)
* [ ] Demo video (optional; training or results walkthrough)
* [ ] GitHub branch: `feature/member-3-machine-learning`
* [ ] GitHub commits linked to ML work
* [ ] Final output files: trained model + pipeline + experiment notes

### Member 4 — Evidence Checklist

* [ ] Written work description (SHAP + stats + Streamlit)
* [ ] Screenshots of SHAP plots and Streamlit UI
* [ ] Results (global/local explanations, statistical test outcomes)
* [ ] Demo video of Streamlit application
* [ ] GitHub branch: `feature/member-4-xai-deployment`
* [ ] GitHub commits linked to XAI/deployment
* [ ] Final output files: app code + explanation artifacts + deployment docs

---

## 7. Quality-Control Requirements

### Data

* [ ] Dataset source documented
* [ ] Missing values checked
* [ ] Duplicate transactions checked
* [ ] Cancelled transactions handled
* [ ] Invalid records checked

### Churn

* [ ] Observation period documented
* [ ] Prediction period documented
* [ ] Churn definition documented
* [ ] No future information leaks into features

### Features

* [ ] Feature definitions documented
* [ ] Feature generation reproducible
* [ ] No target leakage

### Machine Learning

* [ ] Temporal split used
* [ ] No random split when it would cause temporal leakage
* [ ] Class imbalance addressed
* [ ] Multiple models evaluated
* [ ] Metrics recorded

### Explainability

* [ ] SHAP compatible with final model
* [ ] Global explanations produced
* [ ] Local explanations produced
* [ ] Statistical analysis documented

### Deployment

* [ ] Model loading tested
* [ ] Prediction pipeline tested
* [ ] Streamlit tested
* [ ] Input validation implemented

---

## 8. Definition of Done

Do not use vague statements such as "work completed." A module is done only when the criteria below are met **and** evidence is recorded in `PROGRESS.md`.

### M1 is complete only when:

* [ ] Preprocessing code/notebook exists in the repository
* [ ] Raw dataset is documented (source, citation, location)
* [ ] Cleaned data is generated and stored as a reproducible artifact
* [ ] Observation period, prediction period, and churn criteria are documented
* [ ] Churn labels are generated
* [ ] Validation checks on labels pass and are recorded
* [ ] Customer-level output artifact exists at a known path
* [ ] README or equivalent preprocessing documentation exists
* [ ] Git commit(s) exist for this work
* [ ] Feature branch exists (`feature/member-1-preprocessing` or recorded equivalent)
* [ ] Faculty evidence package is prepared

### M2 is complete only when:

* [ ] Code/notebook loads the actual M1 customer-level artifact
* [ ] M1 output validation is documented
* [ ] EDA visualizations and findings exist
* [ ] RFM and required behavioral features are generated
* [ ] Feature-level missing values and outliers are handled/documented
* [ ] Feature validation is recorded
* [ ] Engineered feature dataset artifact exists at a known path
* [ ] Feature definitions document exists
* [ ] Git commit(s) and feature branch exist
* [ ] Faculty evidence package is prepared
* [ ] Confirmed: churn labels were not silently redefined

### M3 is complete only when:

* [ ] Code loads the actual M2 feature artifact
* [ ] Temporal train/validation/test split is implemented and documented
* [ ] Leakage checks are documented
* [ ] Class imbalance analysis and handling are documented
* [ ] Logistic Regression, Random Forest, and XGBoost are trained
* [ ] ROC-AUC, PR-AUC, Precision, Recall, F1, and Confusion Matrix are recorded for each model
* [ ] Model comparison uses those actual experimental results
* [ ] Final model selection rationale is documented
* [ ] Trained model file is saved
* [ ] Preprocessing pipeline is saved if required for inference
* [ ] Experiment entries exist in `PROGRESS.md`
* [ ] Git commit(s) and feature branch exist
* [ ] Faculty evidence package is prepared

### M4 is complete only when:

* [ ] Final M3 model (and pipeline if required) loads successfully
* [ ] SHAP global and local explanations are generated
* [ ] Statistical analysis / hypothesis tests are documented
* [ ] Streamlit app displays customer info, churn probability, risk category, top factors, and SHAP explanation
* [ ] Model + preprocessing integration is tested
* [ ] Input validation is implemented
* [ ] Deployment documentation exists
* [ ] Git commit(s) and feature branch exist
* [ ] Faculty evidence package is prepared (including demo video if required)

### Final project is complete only when:

* [ ] All four modules meet their Definition of Done
* [ ] Handoffs M1→M2, M2→M3, M3→M4 are recorded and validated
* [ ] `PROGRESS.md` reflects final evidence
* [ ] Final documentation (README / report as required by faculty) exists
* [ ] Faculty demonstration checklists in `PROGRESS.md` can be completed by each member

---

## 9. How to Use This Plan

1. Keep **intent and ownership** in `PLAN.md`.
2. Record **facts, evidence, blockers, decisions, and handoffs** in `PROGRESS.md`.
3. Do not mark modules complete in either file without repository evidence.
4. After each meaningful commit or handoff, update `PROGRESS.md` the same day.
