# M1 faculty evidence checklist

Use this checklist when preparing Member 1 demonstration materials.

## Work description

- [x] Documented in `docs/preprocessing_decisions.md` and `docs/dataset_source.md`
- [ ] Paste a short personal summary into your faculty submission (member-specific)

## Artifacts to show

- [ ] `DataSet/online_retail_II.xlsx` (raw)
- [ ] `src/preprocessing.py`
- [ ] `notebooks/m1_preprocessing.ipynb`
- [ ] `data/processed/transactions_cleaned.parquet`
- [ ] `data/processed/customer_churn_labels.csv` (or `.parquet`)
- [ ] `data/processed/m1_validation_report.json`

## Screenshots (capture locally)

- [ ] Raw schema / head of dataset
- [ ] Missing-value counts before cleaning
- [ ] Row counts after each cleaning step
- [ ] Churn class counts / rate
- [ ] Validation report `all_passed: true`

## Git evidence

- [ ] Branch `feature/member-1-preprocessing` (create when committing)
- [ ] Commits for preprocessing + docs + outputs
- [ ] Link commits in `PROGRESS.md` Git Contribution Log

## Demo talking points

1. Dataset source (UCI Online Retail II)
2. Why missing Customer IDs were dropped
3. How cancellations were identified (`Invoice` starts with `C`)
4. Observation vs prediction periods
5. Exact churn rule
6. How validation proves labels do not leak future purchases into `obs_*` fields
