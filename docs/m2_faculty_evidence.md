# M2 faculty evidence checklist

## Artifacts to show

- [ ] `src/features.py`
- [ ] `notebooks/m2_eda_features.ipynb`
- [ ] `data/features/customer_features.parquet` (or CSV)
- [ ] `docs/feature_dictionary.md`
- [ ] `docs/m2_eda_findings.md`
- [ ] `data/features/figures/` (EDA plots)
- [ ] `data/features/m2_validation_report.json`

## Screenshots (capture locally)

- [ ] Churn distribution bar chart
- [ ] RFM boxplots by churn
- [ ] Feature histograms
- [ ] Correlation-with-churn bar chart
- [ ] Validation `all_passed: true`

## Talking points

1. M1 handoff was validated; churn labels unchanged.
2. Features use observation period only (no leakage).
3. RFM definitions relative to 2010-12-31.
4. How cancellation rate was recovered from raw `C`-invoices.
5. Purchase-interval imputation for single-purchase customers.
6. Why outliers were reported but not deleted.
