# Customer Churn Prediction with Explainable AI

Academic team project (4 members) using the UCI Online Retail II dataset.

Roadmap and ownership: see [`PLAN.md`](PLAN.md).  
Factual progress and evidence: see [`PROGRESS.md`](PROGRESS.md).

## Repository layout

```text
FDS_Project/
├── PLAN.md                 # Project roadmap (root)
├── PROGRESS.md             # Evidence-based progress log (root)
├── README.md
├── DataSet/                # Raw dataset
│   └── online_retail_II.xlsx
├── notebooks/              # Jupyter notebooks (M1–M4)
├── src/                    # Reusable Python modules
├── data/
│   ├── processed/          # M1 cleaned / customer-level outputs
│   └── features/           # M2 engineered feature datasets
├── models/                 # M3 trained models & pipelines
├── app/                    # M4 Streamlit application
└── docs/                   # Module docs, decisions, faculty evidence notes
```

## Modules

| Module | Owner    | Directory focus                          |
| ------ | -------- | ---------------------------------------- |
| M1     | Shasank  | `DataSet/` → `data/processed/`, `notebooks/`, `src/` |
| M2     | Boni Ravi| `data/processed/` → `data/features/`, `notebooks/` |
| M3     | Vaishnavi| `data/features/` → `models/`, `notebooks/` |
| M4     | Bhavani  | `models/` → `app/`, SHAP / stats in `notebooks/` or `docs/` |

## Dataset

- **Location:** `DataSet/online_retail_II.xlsx`
- **Source:** UCI Online Retail II (document citation in M1 work)
- **Processed outputs:** write under `data/processed/` (do not overwrite the raw file)

## Development model

Sequential handoffs: **M1 → M2 → M3 → M4**.  
Do not redefine upstream labels/models without recording the decision in `PROGRESS.md`.
