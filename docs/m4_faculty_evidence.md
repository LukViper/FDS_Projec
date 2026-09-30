# M4 faculty evidence checklist

## Artifacts

- [ ] `src/explain.py`
- [ ] `app/streamlit_app.py`
- [ ] `notebooks/m4_shap_analysis.ipynb`
- [ ] `docs/shap_and_stats.md`
- [ ] `docs/deployment.md`
- [ ] `docs/xai/m4_xai_report.json`
- [ ] `docs/xai/figures/shap_global_importance.png`
- [ ] `docs/xai/figures/shap_summary.png`
- [ ] `models/final_model.joblib` (from M3 — show it is the one loaded)

## Screenshots / demo

- [ ] Global SHAP bar chart
- [ ] SHAP summary plot
- [ ] Streamlit: customer info + probability + risk
- [ ] Streamlit: top SHAP factors
- [ ] Statistical significance table (from JSON / notebook)

## Talking points

1. Loaded frozen M3 Random Forest — did not retrain
2. TreeExplainer for global vs local explanation
3. Significant RFM/behavioural associations (Mann–Whitney / chi-square)
4. Risk bands and input validation in the app
5. Observation-period-only inputs (no leakage)
