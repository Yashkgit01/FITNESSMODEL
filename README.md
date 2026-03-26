# 💚 HealthTrack Pro — Analytics Dashboard

> **MBA Data Analytics (MGB) — Individual Project**
> A professional Streamlit dashboard for the HealthTrack Pro synthetic business dataset.

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 Overview | Executive KPIs, sales funnel, revenue mix |
| 📣 Marketing & Channels | Channel ROI, conversion rates, ad spend |
| 👥 Customer Segments | Demographics, age/income tiers, geography |
| 📈 Conversion & Revenue | NPS vs usage, plan economics, revenue heatmap |
| 🔗 Correlation Analysis | Pearson heatmap, interactive variable explorer |
| ⚠️ Churn Intelligence | Retention analysis, churn risk quadrant map |

---

## 🚀 Deploy on Streamlit Cloud

### Step 1 — Push to GitHub
1. Create a new repository on [github.com](https://github.com) (public or private)
2. Upload all files from this zip (or clone and push):
```
healthtrack_dashboard/
├── app.py
├── healthtrack_clean.csv
├── requirements.txt
└── README.md
```

### Step 2 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository, branch (`main`), and set **Main file path** to `app.py`
5. Click **"Deploy"** — your app will be live in ~2 minutes! 🎉

---

## 🖥️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 File Structure

```
healthtrack_dashboard/
├── app.py                   ← Main Streamlit dashboard (6 pages)
├── healthtrack_clean.csv    ← Cleaned synthetic dataset (500 records)
├── requirements.txt         ← Python dependencies
└── README.md                ← This file
```

---

## 🔬 Dataset Overview

| Feature | Type | Description |
|---------|------|-------------|
| customer_id | String | Unique customer identifier |
| region | Categorical | North / South / East / West / Central |
| age | Integer | Customer age (18–65) |
| gender | Categorical | Male / Female / Non-binary |
| annual_income | Float | Annual income ($) |
| marketing_channel | Categorical | Social Media / Google Ads / Referral / Email / Organic |
| ad_spend_per_lead | Float | Cost per lead by channel |
| trial_signup | Boolean | Signed up for free trial |
| days_to_trial | Float | Days from lead to trial |
| usage_sessions | Float | Sessions during trial |
| nps_score | Float | Net Promoter Score (1–10) |
| purchased | Boolean | Converted to paid subscription |
| plan | Categorical | Basic / Standard / Premium / None |
| monthly_revenue | Float | Monthly subscription revenue |
| churned | Boolean | Cancelled subscription |
| age_group | Categorical | Age bracket (engineered) |
| income_segment | Categorical | Income tier (engineered) |
| revenue_per_session | Float | Monetisation efficiency (engineered) |

---

## 🛠️ Built With

- **[Streamlit](https://streamlit.io)** — Dashboard framework
- **[Plotly](https://plotly.com)** — Interactive visualisations
- **[Pandas](https://pandas.pydata.org)** — Data manipulation
- **[SciPy](https://scipy.org)** — Statistical analysis

---

*MBA Data Analytics · MGB · HealthTrack Pro Startup Analytics*
