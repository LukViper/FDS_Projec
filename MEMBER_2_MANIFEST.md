# Member 2 Package

**Project:** Customer Churn Prediction with Explainable AI

**Module:** Member 2 — EDA & Feature Engineering

**Source branch:** `Shasank` (HEAD at pack time: `c9d5a74` — Member 1 commit; M2 files were uncommitted)

**Base / previous module:** Member 1 — Data Collection & Preprocessing  
**Latest Member 1 commit:** `c9d5a74` — *Data Preprocessing Done - by Shasank*

## Purpose

Transfer **only Member 2 work** to another device for commit/push onto the Member 2 Git branch.

## Files included

```text
MEMBER_2_MANIFEST.md
requirements.txt
notebooks/m2_eda_features.ipynb
notebooks/README.md
src/features.py
src/__init__.py
docs/feature_dictionary.md
docs/m2_eda_findings.md
docs/m2_faculty_evidence.md
data/features/README.md
data/features/customer_features.parquet
data/features/customer_features.csv
data/features/feature_summary.csv
data/features/m2_validation_report.json
data/features/figures/churn_distribution.png
data/features/figures/country_top10.png
data/features/figures/box_recency_days_by_churn.png
data/features/figures/box_frequency_by_churn.png
data/features/figures/box_monetary_by_churn.png
data/features/figures/feature_histograms.png
data/features/figures/corr_with_churn.png
```

## Files intentionally excluded

```text
.git/                          # Git metadata
.github/
DataSet/online_retail_II.xlsx  # Raw dataset (large); not required to commit M2 outputs
data/processed/*               # Member 1 outputs — already on remote after M1 push; do not duplicate
src/preprocessing.py           # Member 1 source
notebooks/m1_preprocessing.ipynb
docs/dataset_source.md         # Member 1 docs
docs/preprocessing_decisions.md
docs/m1_faculty_evidence.md
app/ models/                   # Future M3/M4 placeholders
PLAN.md                        # Shared roadmap (not M2-specific)
PROGRESS.md                    # Shared tracker (modified locally for M2; commit separately if desired)
viva.tex                       # Shared viva notes (modified locally)
.gitignore
__pycache__/ *.pyc
.venv/ venv/ env/
.ipynb_checkpoints/
.cache/ tmp/ temp/
.env secrets
member2_eda_features.zip       # Prior ad-hoc zip if present
```

## Dependencies (not packaged — expect on target repo after Member 1)

Member 2 **consumes** these Member 1 artifacts already present in the repository / remote:

```text
data/processed/customer_churn_labels.parquet   # primary labelled customer table
data/processed/transactions_cleaned.parquet  # observation-period feature source
data/processed/m1_validation_report.json       # handoff validation
```

Optional for **re-running** cancellation-rate computation from scratch only:

```text
DataSet/online_retail_II.xlsx
```

Not required to commit the already-generated `customer_features.*` artifacts.

## Validation snapshot (at package time)

- Feature table rows: 4231
- RFM columns present: recency_days, frequency, monetary
- Behavioral columns present: avg_order_value, purchase_interval_days, product_diversity, cancellation_rate, spending_trend, order_trend
- `m2_validation_report.json`: m1_handoff `all_passed=true`, feature_validation `all_passed=true`, `churn_unchanged=true`
- EDA figures: 7 PNG files under `data/features/figures/`

## Suggested commit on other device

1. Extract this ZIP into the project root (merge paths).
2. Ensure Member 1 artifacts exist (pull `Shasank` / main as appropriate).
3. Create/checkout Member 2 feature branch.
4. `git add` the included paths (and optionally updated `PROGRESS.md` / `viva.tex` from the source machine if you sync those separately).
5. Commit and push from that device.

## Created

2026-09-25
