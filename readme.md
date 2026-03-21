# NS Pothole Freeze-Thaw Analysis Dashboard
## Government of Nova Scotia · Department of Public Works · NS TIR + ECCC · 2019–2025

> **One finding:** A freeze-thaw event today predicts a pothole complaint surge **exactly 5 days later** — consistent across every year 2019–2025. NS TIR has a reliable window to pre-stage crews before any citizen calls.

---

## Requirements

- Python 3.8 or higher — download from [python.org](https://www.python.org/downloads/)
- Git — download from [git-scm.com](https://git-scm.com/)
- A terminal / command prompt

---

## Clone & Run (First Time Setup)

```bash
# Step 1 — Clone the repository
git clone https://github.com/Krishna-Soni-Git/Pothole-V4.git
cd ns-pothole-analysis

# Step 2 — Create a virtual environment
python -m venv venv

# Step 3 — Activate it
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Step 4 — Install all dependencies
pip install pandas numpy openpyxl requests tqdm matplotlib seaborn scipy streamlit plotly
pip install statsmodels          # Recommended — enables Newey-West HAC standard errors

# Step 5 — Collect data  (first run only — takes 20–40 minutes)
python 01_collect_data.py

# Step 6 — Run the statistical analysis
python 02_analysis.py

# Step 7 — Launch the dashboard
streamlit run app.py
```

The dashboard opens automatically at **http://localhost:8501**

### Returning Users (already cloned)

```bash
cd ns-pothole-analysis
git pull                         # Get latest changes
source venv/bin/activate         # Mac / Linux  (or venv\Scripts\activate on Windows)
streamlit run app.py
```

> **Note:** If someone shares the files directly (no Git), skip Step 1 — just unzip the folder, open a terminal inside it, and start from Step 2.

---

## Project Files

| File | Purpose |
|------|---------|
| `01_collect_data.py` | Fetches ECCC weather data and merges with NS TIR records |
| `02_analysis.py` | Correlations, regression, regional breakdown — saves CSVs to `outputs/` |
| `app.py` | 13-slide interactive dashboard |
| `outputs/correlation_table.csv` | All lagged Spearman correlations with Bonferroni-corrected p-values |
| `outputs/regional_results.csv` | Regional correlation results by weather station |

---

## Dashboard — 13 Slides

| # | Slide | What It Shows |
|---|-------|--------------|
| 00 | Overview | Dataset summary, 4 headline KPIs, methodology |
| 01 | Summary Stats | All 12 key numbers at a glance |
| 02 | Plain English | Statistical terms explained for non-technical audiences |
| 03 | Case Analysis | Halifax Feb 2022 — the 5-day lag as a real event |
| 04 | The Problem | Annual complaint totals 2019–2025 |
| 05 | How Roads Break | 6-step physics process, formula definitions |
| 06 | Seasonal Pattern | Monthly FT days vs avg daily complaints |
| 07 | 5-Day Lag | Core statistical finding — lagged Spearman correlogram |
| 08 | Predictors | Weather variables ranked by predictive strength |
| 09 | By Region | Regional signal breakdown, hatched = not significant |
| 10 | Regression | OLS coefficient chart + significance table |
| 11 | Monthly Deep-Dive | Heatmap / trend+weather overlays / region×month / YoY comparison |
| 12 | Action Plan | 3-tier alert system, limitations, next steps |

**Presenter Notes** are on Slide 03 — full speaker scripts for every slide, visible only on your laptop while the projector shows any other slide.

---

## Key Results

| Metric | Value |
|--------|-------|
| Day 5 lag (all years) | r = −0.081 |
| Spring-only r (Mar–May) | r = −0.143 · p = 0.0003 · 3× stronger |
| Bonferroni correction | 42 tests · α = 0.00119 · 18 / 61 features significant |
| Full-model R² | 7.2% (includes Spring calendar dummy) |
| Weather-only R² | ~3–4% |
| Halifax priority | FTC r = −0.125 · 34% of all NS complaints |
| Peak month (every year) | July · 398–825 complaints depending on FT season severity |

### 3-Tier Alert System
| Alert | Trigger | Action |
|-------|---------|--------|
| 🔴 HIGH — Deploy | FTC_14d ≥ 5 days OR thaw after 3+ freezing days | Pre-stage crews within 5 days · Halifax first |
| 🟡 MEDIUM — Monitor | FTC_14d = 2–4 days OR 7-day precip > 25 mm | Schedule patrols · pre-stock materials |
| 🔵 LOW — Routine | Normal conditions | Standard reactive operations |

---

## Statistical Method

**Repeated lagged bivariate Spearman correlations** (not formal CCF/cross-correlation) — corrected for:
- **Weekday filter** — call-centre hours bias removed
- **Bonferroni correction** — prevents false positives across 42 simultaneous tests
- **Effective N** — p-values adjusted for autocorrelation via AR(1) approximation
- **Newey-West HAC SE** — regression standard errors corrected for serial autocorrelation

### Known Limitations
1. Seasonality not removed before correlating — shared winter trends may inflate r values
2. Province-wide weather averaging loses regional signal (5 stations → 1 series)
3. OLS used for count data — negative binomial regression more appropriate
4. Road age, PCI, and traffic volume not in the model
5. Yarmouth A (SW Nova Scotia) missing precipitation data — results inconclusive

---

## Suggested Improvements

| Priority | Enhancement | Expected Impact |
|----------|------------|----------------|
| High | Road Age + Pavement Condition Index (PCI) | Weather-only R² from ~3–4% → 10–15% |
| High | Connect live ECCC 7-day forecast API | Real-time alert generation |
| Medium | Traffic Volume (AADT) | Distinguish highway from side street damage |
| Medium | Negative Binomial Regression | More reliable p-values for count data |
| Low | STL Seasonal Decomposition | Isolate weather signal from shared seasonal trends |
| Low | Station-Level Panel Model | Preserve regional variation, increase power |

---

*Department of Public Works · MBAN 2026 · Group Project*