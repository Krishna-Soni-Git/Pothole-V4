# NS Pothole & Weather Analysis

**MBAN 5510 — Foundation of Professional Analytics**  
**Saint Mary's University**

---

## Research Question

**Can freeze-thaw weather events predict pothole complaint surges in Nova Scotia, and by how many days?**

---

## Project Structure

```
5510-V4/
├── 01_collect_data.py          # Data collection: ECCC weather + NS TIR OCC complaints
├── 02_analysis.py              # Statistical analysis: correlations, OLS, neg-binomial,
│                               #   seasonal adjustment, alert precision evaluation
├── app.py                      # Streamlit dashboard (reads live CSV outputs from outputs/)
├── README.md                   # This file
├── Requirements.txt            # Python dependencies
├── Data/
│   ├── raw_weather/            # Cached per-station daily CSVs (created on first run)
│   └── NS_Project_Merged_FIXED.csv   # Final merged dataset (output of Step 1)
└── outputs/                    # Figures and tables (output of Step 2)
    ├── 01_lag_curve.png  …  09_ols_coefficients.png
    ├── correlation_table.csv          # Lagged Spearman r + Bonferroni p-values
    ├── regional_results.csv           # Per-station correlations
    ├── negbin_results.csv             # Negative binomial regression (IRR)
    ├── seasonal_adjustment_check.csv  # Month-demeaned lag comparison
    ├── alert_precision.csv            # HIGH alert precision-recall
    ├── lag_window_summary.csv         # Full Bonferroni significance table
    └── lag_window_summary_stats.csv   # Best lag, significant range, median
```

---

## How to Run

### Step 0 — Install dependencies

```bash
pip install pandas openpyxl requests tqdm matplotlib seaborn scipy statsmodels
pip install streamlit plotly
```

### Step 1 — Collect data

**Required source file:** Place `Operations_Contact_Centre_Call_Summary_20260120.csv.xlsx`  
in the same folder as `01_collect_data.py`, then run:

```bash
python 01_collect_data.py
```

Downloads ~80 station-years of daily weather from ECCC (~20–40 min on first run).  
Subsequent runs load from cache in `Data/raw_weather/`.  
Outputs `Data/NS_Project_Merged_FIXED.csv`.

A **completeness check** compares expected vs actual calendar days per station and prints a warning if more than 5% of days are missing.

### Step 2 — Run statistical analysis

```bash
python 02_analysis.py
```

Produces 9 figures + 7 CSV tables in `outputs/`, including:
- Seasonal adjustment validation (month-demeaned lag comparison)
- Alert precision-recall evaluation of the HIGH threshold
- Full lag significance window summary

### Step 3 — Launch dashboard

```bash
streamlit run app.py
```

The dashboard reads all CSVs from `outputs/` automatically (`@st.cache_data`). KPI tiles, lag p-values, alert precision, and annual counts update whenever `02_analysis.py` is re-run. Falls back to representative values if outputs are missing — sidebar shows which mode is active.

---

## Data Sources

| Source | Description | Coverage |
|--------|-------------|----------|
| NS TIR Operations Contact Centre | ~391,795 complaint records, 64 supervisor area codes | Jan 2019 – Sep 2025 |
| Environment & Climate Change Canada (ECCC) | Daily temperature, precipitation, snow, gust speed | Jan 2019 – Sep 2025 |

### Weather Stations

| Station | ECCC ID | Region Covered | Notes |
|---------|---------|----------------|-------|
| Halifax Stanfield | 50620 | HRM / Lunenburg | — |
| Greenwood A | 27141 (fallback) | Annapolis Valley / Kings | Primary 50839 null temps |
| Sydney A | 50308 | Cape Breton | Old ID 6526 decommissioned |
| Truro | 6354 | Colchester / Cumberland / Pictou / Antigonish | — |
| Yarmouth A | 43405 | SW Nova Scotia / Shelburne | **No precipitation sensor** |

**Yarmouth A precipitation:** Zero-filled. Companion flag columns (`Total_Precip_imputed`, `Total_Rain_imputed`, `Total_Snow_imputed` = 1) mark imputed rows throughout the analysis.

---

## Methodology

### Feature Engineering
- **FTC day:** `Tmax > 0°C AND Tmin < 0°C` — 647 detected 2019–2025
- **Rolling windows:** 3, 5, 7, 14-day cumulative sums (shifted 1 day to prevent leakage)
- **Interaction:** `Precip × FTC` — saturated pavement hitting a freeze
- **Imputation flags:** Missing precip filled with 0; `*_imputed = 1` columns mark fills

### Weekday Filter
All correlations and regression use weekdays only (Mon–Fri). Weekend volumes are ~70% lower due to call-centre hours, not road conditions.

### Lagged Spearman Correlations
Repeated lagged bivariate Spearman correlations at 1–21 day offsets (Spearman correlogram, NOT formal CCF). Corrections: Bonferroni (`α / n_tests`) and effective sample size Nₑ via AR(1) adjustment.

### OLS Regression
Seven predictors; weekdays only; `statsmodels.OLS` with Newey-West HAC standard errors (maxlags=5). Full-model R² and weather-only R² reported separately.

### Negative Binomial Regression
Fitted alongside OLS — preferred for overdispersed count data. Incidence Rate Ratios saved to `outputs/negbin_results.csv`.

### Seasonal Adjustment Validation *(implemented)*
Lag correlogram re-run on month-demeaned series to check whether shared seasonal trends inflate the raw finding. Results in `outputs/seasonal_adjustment_check.csv`.

### Alert Precision Evaluation *(implemented)*
HIGH alert (FTC_14d ≥ 5) evaluated against complaint surges (>75th weekday percentile within 5–7 days). Precision, false-positive rate, and lift over baseline saved to `outputs/alert_precision.csv`.

### Lag Window Summary *(implemented)*
Full Bonferroni-corrected significance table for FTC lags 1–21 days. Best lag day, significant range, and median in `outputs/lag_window_summary_stats.csv`.

---

## Key Results

| Finding | Value |
|---------|-------|
| Peak lag day | Day 5 (r = −0.081, Bonferroni-significant) |
| Spring-only lag (Day 5) | r = −0.143 (p = 0.0003 raw) |
| Full-model OLS R² (incl. Spring dummy) | 7.2% |
| Weather-only OLS R² | ~3–4% |
| Strongest rolling predictor | FTC 14-day count (r = −0.087) |
| Strongest regional signal | Halifax / Lunenburg (FTC r = −0.125, p < 0.001) |

### 3-Tier Alert System

| Level | Trigger | Action |
|-------|---------|--------|
| **HIGH** | ≥5 FT days in rolling 14d | Pre-stage crews within 5 days. Prioritise Halifax. |
| **MEDIUM** | 2–4 FT days in 14d, OR 7-day precip > 25 mm | Schedule patrols, pre-stock materials. |
| **LOW** | 0–1 FT days, normal precip | Standard reactive response. |

See `outputs/alert_precision.csv` for computed precision of the HIGH threshold.

---

## Known Limitations

- **Yarmouth A** has no precipitation sensor — precip results for SW NS are unreliable
- **Greenwood A** fallback ID (27141) lacks rain/snow split
- **OLS on count data** can predict negatives — negative binomial is preferred (`negbin_results.csv`)
- **Seasonality check** implemented — see `seasonal_adjustment_check.csv` to assess confounding
- **Alert precision** evaluated — see `alert_precision.csv` before operational deployment
- **Weather explains ~7.2% of variance** — road age, PCI, and traffic volume are unmeasured

---

## Requirements.txt

```
pandas>=2.0
openpyxl>=3.1
requests>=2.31
tqdm>=4.65
matplotlib>=3.7
seaborn>=0.12
scipy>=1.11
statsmodels>=0.14
streamlit>=1.28
plotly>=5.17
numpy>=1.24
```

---

## Quick Test Checklist

```bash
# 1. Collect (uses cache if already downloaded)
python 01_collect_data.py

# 2. Analyse — verify 7 CSVs appear in outputs/
python 02_analysis.py
ls outputs/*.csv
# Expected: correlation_table, regional_results, negbin_results,
#           seasonal_adjustment_check, alert_precision,
#           lag_window_summary, lag_window_summary_stats

# 3. Dashboard — sidebar should say "Live analysis outputs loaded"
streamlit run app.py
```

**Verify in dashboard after running analysis:**
- Slide 00: KPIs show live totals and computed sig. lag window
- Slide 01: Bar chart shows actual annual counts
- Slide 04: Peak lag day, p_bonf, and action window are computed values
- Slide 09: "Alert Evaluation" box shows precision % and lift over baseline