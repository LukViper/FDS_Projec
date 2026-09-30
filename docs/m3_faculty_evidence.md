# M3 faculty evidence checklist

## Artifacts

- [ ] `src/modeling.py`
- [ ] `notebooks/m3_modeling.ipynb`
- [ ] `docs/experiment_notes.md`
- [ ] `models/model_comparison.json`
- [ ] `models/model_metrics.json`
- [ ] `models/final_model.joblib`

## Screenshots

- [ ] Temporal split sizes / churn rates
- [ ] Validation comparison table (LR / RF / XGB)
- [ ] Selected model confusion matrix (val + test)
- [ ] File listing of `models/`

## Talking points

1. Why temporal split on `obs_last_purchase` (not random)
2. How leakage was prevented
3. Imbalance handling per model
4. Why Random Forest was selected (val PR-AUC)
5. What M4 must load (`final_model.joblib`)
