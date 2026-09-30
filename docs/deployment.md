# M4 deployment notes

## Run locally

From repository root (with dependencies installed):

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Requires:

- `models/final_model.joblib`
- `models/model_comparison.json`
- `data/features/customer_features.parquet`

## Integration

1. App loads the **exact** M3 Pipeline (`preprocess` + Random Forest).
2. Prediction uses `predict_proba` → churn probability + risk band.
3. SHAP uses `TreeExplainer` on the forest with transformed features.
4. Manual inputs are validated before scoring.

## Testing checklist

- [x] Final model loads
- [x] M3 handoff validation passes
- [x] Prediction returns probability + risk
- [x] Local SHAP factors computed for a customer
- [x] Input validation rejects invalid recency/frequency/monetary/cancellation_rate
- [ ] Live Streamlit UI walkthrough (run locally for faculty demo)

## Risk categories

| Category | Probability |
| -------- | ----------- |
| Low | &lt; 0.33 |
| Medium | 0.33 – 0.66 |
| High | ≥ 0.66 |
