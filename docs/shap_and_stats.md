# M4 — SHAP, statistical analysis, and deployment

Date: 2026-09-28  
Module: Member 4  
Code: `src/explain.py`, `app/streamlit_app.py`  
Notebook: `notebooks/m4_shap_analysis.ipynb`

## Model loaded (frozen M3)

- Path: `models/final_model.joblib`
- Selected model: **random_forest** (`RandomForestClassifier` inside sklearn Pipeline)
- M3 handoff validation: `all_passed: true` (see `docs/xai/m4_xai_report.json`)
- **Model was not retrained**

## SHAP method

- Explainer: `shap.TreeExplainer` on the Random Forest
- Features explained in **preprocessed** space (same transform as training)
- Global importance: mean |SHAP| over a sample of 500 customers
- Local explanations: top-|SHAP| factors for high-risk example customers

### Top global drivers (mean |SHAP|)

See `docs/xai/shap_global_importance.csv`. Leading features include monetary, frequency, avg_order_value, spending_trend, and related behavioural fields.

Figures:

- `docs/xai/figures/shap_global_importance.png`
- `docs/xai/figures/shap_summary.png`

## Statistical analysis

Tests on the full customer feature table (data-level associations with churn):

| Test | Features | Alpha |
| ---- | -------- | ----- |
| Mann–Whitney U + point-biserial | All numeric engineered features | 0.05 |
| Chi-square | `country` (top-8 + Other) | 0.05 |

**Result:** All 12 numeric features were significant at α=0.05; country also significant.  
Details: `docs/xai/statistical_tests.json`.

Interpretation: SHAP explains *the model*; these tests support that key RFM/behavioural variables also differ by churn label in the data.

## Streamlit deployment

```bash
streamlit run app/streamlit_app.py
```

UI shows:

- Customer information
- Churn probability
- Risk category (Low &lt; 0.33, Medium, High ≥ 0.66)
- Top SHAP contributing factors
- Input validation (non-negative recency, frequency ≥ 1, etc.)

Modes: select existing Customer ID, or manual observation-period feature entry.

## Artifacts

| Path | Role |
| ---- | ---- |
| `docs/xai/m4_xai_report.json` | Validation + summary |
| `docs/xai/shap_global_importance.csv` | Global SHAP table |
| `docs/xai/shap_local_examples.json` | Example local explanations |
| `docs/xai/statistical_tests.json` | Hypothesis test results |
| `app/streamlit_app.py` | Interactive demo |

## Handoff completeness

Final integration requires M2 features + M3 `final_model.joblib` present. M4 consumes both; does not redefine labels or retrain the classifier.
