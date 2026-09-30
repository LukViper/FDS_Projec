# Foundations of Data Science — Project Presentation

**Title:** Customer Churn Prediction with Explainable AI  
**Dataset:** UCI Online Retail II  
**Subject focus:** Foundations of Data Science (CO1–CO5)  
**Team:** 4 members · sequential pipeline M1 → M2 → M3 → M4

> How to use this file: each **Slide** block is what you show; the *Say this* paragraphs are natural speaking notes. Fill in Member 2–4 names where marked.

---

## Slide 1 — Title

**On screen**

- Customer Churn Prediction with Explainable AI  
- Foundations of Data Science  
- UCI Online Retail II · 4-member team project

**Say this**

Good morning. Today we will walk through our Foundations of Data Science project — not as a “machine learning demo,” but as a full data-science workflow: from messy retail transactions to clean labels, exploration, careful modelling, and finally checking how sure we can be about what we found.

---

## Slide 2 — Why this project? (Problem in plain words)

**On screen**

- Online retailers lose money when customers stop buying  
- Question we ask: *Among customers active in 2010, who does not return in early 2011?*  
- Goal: build a **trustworthy, time-aware** churn dataset and analysis — then predict and explain

**Say this**

The business problem is simple: if we can spot customers who are likely to disappear, the shop can try to keep them. The *data-science* challenge is harder. Our raw file is invoice lines — not “customer churn yes/no.” So most of our work was turning raw events into a statistically valid customer-level problem. That is exactly what Foundations of Data Science trains us to do before we even talk about fancy models.

---

## Slide 3 — How we organised the work

**On screen**

```text
M1 Data & Preprocessing  →  M2 EDA & Features  →  M3 Classification  →  M4 Certainty & Demo
   (Member 1)                  (Member 2)            (Member 3)            (Member 4)
```

| Member | Owns | Course Outcome weight |
| ------ | ---- | --------------------- |
| Member 1 — Shasank | Cleaning, periods, churn labels | CO1, CO2 |
| Member 2 — *[Name]* | EDA, visuals, RFM/behaviour features | CO2, CO3 |
| Member 3 — *[Name]* | Temporal split, LR / RF / XGBoost | CO4 |
| Member 4 — *[Name]* | Statistical tests, SHAP, Streamlit | CO1, CO5 |

**Say this**

We split the pipeline so each person owns a real stage of data science. Member 1 owns the foundation — without clean labels, nothing else is valid. Member 2 owns exploration and representation. Member 3 applies classification algorithms as one insight tool among others. Member 4 closes the loop with statistical certainty and explanations. Faculty can verify each stage with files and numbers, not only slides.

---

## Slide 4 — Dataset snapshot (common to all)

**On screen**

| Item | Detail |
| ---- | ------ |
| Source | UCI Online Retail II (Chen, 2019) |
| Raw size | ~1.07 million invoice lines |
| Columns | Invoice, StockCode, Quantity, InvoiceDate, Price, Customer ID, Country, … |
| Span | Dec 2009 → Dec 2011 |
| Our study design | Observe 2010 · Label repurchase Jan–Jun 2011 |

**Say this**

We did not invent a toy CSV. We started from a real public retail dataset. That matters for Foundations of Data Science: you learn how identity gaps, cancellations, duplicates, and time windows show up in practice — not only in textbook examples.

---

## Slide 5 — Course outcomes map (our “compass”)

**On screen**

| CO | Meaning | Where it lives in our project |
| -- | ------- | ----------------------------- |
| **CO1** | Statistical foundations | Churn as a binary outcome; distributions; significance tests; certainty language |
| **CO2** | Pre-processing raw data | Dropping invalid IDs/cancels/dupes; imputation policy; observation-only features |
| **CO3** | EDA & insightful visuals | Churn mix, country, RFM boxes/hists, correlation with churn |
| **CO4** | ML for classification / insight | Temporal split; LR vs RF vs XGBoost; metrics beyond accuracy |
| **CO5** | Degree of certainty | Mann–Whitney, point-biserial, chi-square; SHAP as model-side explanation |

**Say this**

Please keep this table in mind. Our presentation follows the COs in order. Machine learning appears, but only *after* statistics, cleaning, and exploration — and we treat models as one way to get insight, not the whole subject.

---

# PART A — Member 1 · Foundations & Pre-processing (CO1 + CO2)

## Slide 6 — Member 1 contribution (Shasank)

**On screen**

**Member 1 — Shasank · Data Collection & Preprocessing**

What I owned:

1. Acquire and cite the UCI dataset  
2. Inspect structure and data types  
3. Define cleaning rules and document *why*  
4. Define observation vs prediction periods  
5. Define churn scientifically  
6. Hand Member 2 a validated customer table  

Artifacts: `src/preprocessing.py`, `data/processed/*`, `docs/preprocessing_decisions.md`

**Say this**

I’m Member 1. My job was to make the *problem* valid. If churn labels are wrong, every chart and every model later is wrong — no matter how good the algorithm sounds.

---

## Slide 7 — From invoices to customers (CO2 in practice)

**On screen**

| Cleaning step | Rows affected | Why (human reason) |
| ------------- | ------------: | ------------------ |
| Missing Customer ID | 243,007 | Guests cannot be tracked over time → cannot define churn |
| Cancelled invoices (`C…`) | 18,744 | Cancellations are not completed purchases |
| Invalid qty / price ≤ 0 | 71 | Not reliable sales |
| Exact duplicates | 26,124 | Recording noise, not extra purchases |
| **Cleaned transactions** | **779,425** | Usable purchase events |

**Say this**

This is classic CO2 work. Pre-processing is not “delete inconvenient rows.” Each rule has a definitional reason. For example, without Customer ID we cannot follow the same person from 2010 into 2011 — so those rows cannot enter a customer-level study. We documented every decision so the next member does not silently change the meaning of the data.

---

## Slide 8 — Study design: time windows & churn (CO1)

**On screen**

```text
Observation period:  1 Jan 2010  ———  31 Dec 2010     ← behaviour we may use as inputs
Prediction period:   1 Jan 2011  ———  30 Jun 2011     ← used ONLY for the label
```

**Churn definition**

- Eligible: bought at least once in 2010  
- `churn = 1`: no cleaned purchase in Jan–Jun 2011  
- `churn = 0`: bought again in that window  

**Result:** 4,231 customers · 2,217 churned · 2,014 retained · ≈ **52.4%** churn

**Say this**

Here is the statistical foundation. Churn is a carefully defined binary outcome with a past window for features and a future window for labels. That separation is how we avoid *target leakage* — accidentally using future information to “predict” the future. In Foundations of Data Science terms: we designed the sampling frame and the response variable before modelling.

---

## Slide 9 — What Member 1 learned (practical FDS)

**On screen**

- Real data is messy; rules must be written down  
- Labels are a *research design* decision, not a column that arrives for free  
- Validation matters: our M1 report passed `all_passed = true` before handoff  

**Say this**

Practically, I learned that good data science starts with definitions and honesty about what you dropped. Faculty can ask “why six months?” — and our answer is: long enough to see repurchase, still inside the available calendar. That is CO1 thinking applied to a real file.

---

# PART B — Member 2 · Exploration & Features (CO2 + CO3)

## Slide 10 — Member 2 contribution (*[Name]*)

**On screen**

**Member 2 — *[Name]* · EDA & Feature Engineering**

What I owned:

1. Validate Member 1’s handoff (churn labels **unchanged**)  
2. Explore customer and churn distributions  
3. Build RFM + behavioural features from **2010 only**  
4. Handle feature missingness carefully  
5. Produce visuals and a feature dictionary for Member 3  

Artifacts: `src/features.py`, `data/features/*`, `docs/m2_eda_findings.md`

**Say this**

I’m Member 2. I take Member 1’s customer list and ask: what do these people *look like* in the data, and how do we summarise a year of shopping into numbers a model — and a human — can read?

---

## Slide 11 — Exploratory findings (CO3)

**On screen**

- Near-balanced churn: ~52% vs ~48% — useful for interpretation  
- UK dominates country mix (retail pattern visible in top-10 chart)  
- Monetary & frequency are **right-skewed** — typical retail, not “bad data”  
- Strongest simple associations with churn:

| Feature | Corr. with churn | Story |
| ------- | ---------------: | ----- |
| Recency (days since last buy) | **+0.31** | Longer silence → more churn |
| Product diversity | **−0.29** | Broader basket → less churn |
| Frequency | **−0.27** | More invoices → less churn |

**Say this**

This is CO3. Before any algorithm, the pictures already tell a story: people who have been quiet for a long time, who buy rarely, or who buy a narrow set of products, look more like churners. Exploration is not decoration — it guides which features deserve to exist and which hypotheses Member 4 will test later.

---

## Slide 12 — Feature engineering as pre-processing (CO2 continued)

**On screen**

**RFM (classic retail summary)**

- Recency · Frequency · Monetary — relative to 31 Dec 2010  

**Behavioural extras**

- Average order value · purchase interval · product diversity  
- Cancellation rate (from *raw* C-invoices — cleaned file has none)  
- Spending / order trends (H1 vs H2 of 2010 only)

**Hard rule:** no prediction-period fields in features · `churn_unchanged: true`

**Missingness decision:** single-purchase customers have no interval → median impute + flag (~1,418 rows). Outliers reported by IQR but **kept** so we do not distort the churn base rate.

**Say this**

Feature engineering is still Foundations work. We are transforming raw events into analysis-ready variables, with imputation that we can defend, and with leakage control. We kept outliers because deleting “weird” high spenders would quietly change who is in the study — another statistical integrity point.

---

## Slide 13 — What Member 2 learned (practical FDS)

**On screen**

- EDA first saves modelling from blind guessing  
- Correlation is a *clue*, not causation  
- Observation-only features are the line between science and cheating the future  

**Say this**

Practically, I learned that a feature dictionary and figures are as important as code. If Member 3 cannot explain what `recency_days` means, the model is a black box even before SHAP.

---

# PART C — Member 3 · Classification for insight (CO4)

## Slide 14 — Member 3 contribution (*[Name]*)

**On screen**

**Member 3 — *[Name]* · Machine Learning (kept secondary to FDS)**

What I owned:

1. Temporal train / validation / test split  
2. Class-imbalance awareness under time shift  
3. Train three classifiers: Logistic Regression, Random Forest, XGBoost  
4. Compare with ROC-AUC, PR-AUC, Precision, Recall, F1 — not accuracy alone  
5. Freeze the selected pipeline for Member 4  

Artifacts: `src/modeling.py`, `models/*`, `docs/experiment_notes.md`

**Say this**

I’m Member 3. My module maps to CO4 — identify algorithms for classification and extract insight. In this subject, the important part is *how* we evaluate under time, not who wins a Kaggle contest.

---

## Slide 15 — Temporal protocol & imbalance (still FDS thinking)

**On screen**

| Split | Rule (last purchase in 2010) | Role |
| ----- | ---------------------------- | ---- |
| Train | ≤ 31 Aug 2010 | Fit preprocess + model |
| Val | Sep–Oct 2010 | Select model |
| Test | ≥ 1 Nov 2010 | Honest final check |

Churn rate shifts across cohorts (train ~74% → test ~37%). We used class weights / scale_pos_weight — because the world changed over time, not because we “hacked accuracy.”

**Say this**

Random shuffle would mix early and late customers and give optimistic numbers. Temporal splitting is how Foundations of Data Science meets real sequential data. Imbalance handling is also statistical honesty: the positive rate is not constant across time.

---

## Slide 16 — Model comparison (insight, briefly)

**On screen**

| Model | Val PR-AUC | Test ROC-AUC | Selected? |
| ----- | ---------: | -----------: | --------- |
| Logistic Regression | 0.691 | 0.715 | No |
| **Random Forest** | **0.725** | **0.755** | **Yes** |
| XGBoost | 0.691 | 0.709 | No |

Selected test snapshot (RF): PR-AUC 0.625 · Precision 0.646 · Recall 0.494 · F1 0.560

**Say this**

We compared a linear baseline and two tree-based methods. Random Forest won on validation PR-AUC — a ranking metric that cares about the churn class under shift. Notice we do *not* sell these numbers as magic. They are tools to see whether the behavioural features carry predictive signal. That is CO4 used in service of insight, not as the centre of the course.

---

## Slide 17 — What Member 3 learned (practical FDS)

**On screen**

- Algorithm choice matters less than **split design** and **metric choice**  
- Accuracy alone would mislead under drifting base rates  
- Pipelines must freeze preprocessing with the model (fair handoff to Member 4)

**Say this**

The practical lesson: in Foundations of Data Science, modelling is the last mile of a careful experiment — not the first slide.

---

# PART D — Member 4 · Certainty, explanation, delivery (CO1 + CO5)

## Slide 18 — Member 4 contribution (*[Name]*)

**On screen**

**Member 4 — *[Name]* · Statistical analysis, XAI & Streamlit**

What I owned:

1. Load Member 3’s **frozen** Random Forest (no silent retrain)  
2. Run hypothesis tests: feature ↔ churn association  
3. Explain model predictions with SHAP (global + local)  
4. Deploy a Streamlit demo: probability, risk band, top factors  

Artifacts: `src/explain.py`, `app/streamlit_app.py`, `docs/xai/*`, `docs/shap_and_stats.md`

**Say this**

I’m Member 4. CO5 asks us to analyse the degree of certainty of predictions using statistical tests and models. My work sits on top of everyone else’s: same labels, same features, same frozen classifier.

---

## Slide 19 — Statistical certainty (CO5 / CO1)

**On screen**

| Test | Applied to | α |
| ---- | ---------- | - |
| Mann–Whitney U + point-biserial | 12 numeric features vs churn | 0.05 |
| Chi-square | Country (top groups + Other) | 0.05 |

**Result:** 12/12 numeric features significant; country also significant.

**Interpretation (spoken carefully)**

- Tests support that RFM/behaviour variables **differ by churn label in the data**  
- SHAP explains **what the trained model uses**  
- Together: data-level association + model-level attribution — not the same claim

**Say this**

This is where Foundations of Data Science shows maturity. We do not say “the model is right because AUC looks nice.” We ask: do the features we engineered actually separate churned and retained customers under standard nonparametric tests? Yes, at α = 0.05 for the features we checked. That is CO5 in practice.

---

## Slide 20 — SHAP in one minute (supporting insight)

**On screen**

- Global: monetary, frequency, average order value, spending trend among top drivers  
- Local: for one high-risk customer, show the few factors pushing probability up or down  
- Demo: Streamlit risk bands Low &lt; 0.33 · Medium · High ≥ 0.66  

**Say this**

SHAP helps a stakeholder hear *why this customer* looks risky. We keep it brief in an FDS presentation: explainability supports trust; the statistical tests support certainty language.

---

## Slide 21 — What Member 4 learned (practical FDS)

**On screen**

- “Significant” and “important to the model” are related but not identical  
- Freezing the pipeline prevents explanation theatre  
- A demo is useful only if inputs still respect the observation window

**Say this**

Practically, certainty means knowing the limits of your claims — and showing them.

---

# PART E — Team results & what we learned (CO wrap-up)

## Slide 22 — End-to-end result (one slide)

**On screen**

```text
1.07M raw lines
   → 779k cleaned purchases
   → 4,231 labelled customers (~52% churn)
   → RFM + behaviour features (observation-only)
   → Temporally evaluated RF (test ROC-AUC ~0.76)
   → Significant feature–churn tests + SHAP + Streamlit
```

**Say this**

That pipeline *is* the project. Models are one station on the line.

---

## Slide 23 — What we learned as a Foundations of Data Science class

**On screen — map each CO to a lived lesson**

| CO | Practical lesson from this project |
| -- | ---------------------------------- |
| **CO1** | Statistical foundations are study design: windows, binary outcomes, distributions, significance, and careful wording about certainty. |
| **CO2** | Pre-processing is reasoning under constraints — IDs, cancellations, duplicates, imputation, leakage — documented so others can reproduce. |
| **CO3** | EDA and visualisation surface patterns (recency, frequency, diversity) *before* algorithms; figures are evidence, not decoration. |
| **CO4** | Classification algorithms help when paired with temporal evaluation and proper metrics; insight > chasing a single accuracy number. |
| **CO5** | Degree of certainty comes from tests + transparent models/explanations; report what is significant and what remains uncertain under time shift. |

**Say this**

If faculty asks “what did you learn in this subject?”, this table is our answer. We practiced the whole foundation — not only fitting a classifier.

---

## Slide 24 — Individual accountability (quick viva matrix)

**On screen**

| Member | One sentence to own in viva |
| ------ | --------------------------- |
| **M1 Shasank** | “I made churn a valid, time-separated label from cleaned retail events.” |
| **M2 *[Name]*** | “I explored patterns and engineered observation-only RFM/behaviour features.” |
| **M3 *[Name]*** | “I compared classifiers under a temporal split and froze the best evidenced model.” |
| **M4 *[Name]*** | “I quantified feature–churn associations, explained predictions, and shipped the demo.” |

**Say this**

Each of us can point to files and numbers for that sentence. That is how we kept contribution clear.

---

## Slide 25 — Closing

**On screen**

- Foundations first → models second → certainty always  
- Thank you · Questions welcome  

**Say this**

Thank you. We are happy to take questions — especially on churn definition, leakage control, EDA findings, or how we talk about statistical certainty.

---

# Speaker tips (not a slide)

1. **Spend ~60% of time on M1 + M2 + stats (CO1–CO3, CO5).** Keep M3 to a few minutes.  
2. When showing figures, narrate the *story* (e.g. “longer silence → higher churn”), not the file name.  
3. If someone pushes “why Random Forest?”, answer with validation PR-AUC **and** remind them the FDS core is the temporal design and feature validity.  
4. Replace `*[Name]*` for Members 2–4 before the presentation day.  
5. Optional demo order: open Streamlit → pick one customer → show probability + top SHAP factors → mention the matching Mann–Whitney / correlation story from EDA.

---

# Optional Q&A bank (FDS-flavoured)

| Likely question | Short answer |
| --------------- | ------------ |
| Why drop missing Customer IDs? | Churn needs identity over time; guests are not trackable customers. |
| Why not use 2011 purchases as features? | That would leak the label period into the predictors. |
| Is 52% churn “imbalanced”? | Overall nearly balanced; *temporal cohorts* still shift — that is why M3 used weights. |
| Correlation vs SHAP vs Mann–Whitney? | Corr/EDA = exploratory association; Mann–Whitney = formal group difference; SHAP = model attribution. |
| Why PR-AUC for selection? | Emphasises ranking of the churn class under cohort shift better than raw accuracy. |
