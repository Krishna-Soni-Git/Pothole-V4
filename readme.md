# 🚧 NS Pothole Freeze-Thaw Analysis

A data analysis project that uses weather data to predict pothole complaint surges in Nova Scotia — up to 5 days before they happen.

**Data sources:** NS TIR Operations Contact Centre (391,795 records, 2019–2025) + Environment Canada (ECCC) daily weather from 5 stations

---

## 📁 Project Files

```
project/
│
├── 01_collect_data.py           ← Step 1: Download weather + merge with complaints
├── 02_analysis.py               ← Step 2: Run all statistics and generate charts
├── app.py                       ← Step 3: Launch the interactive dashboard
│
├── Data/
│   ├── Operations_Contact_Centre_Call_Summary_20260120.csv.xlsx   ← You provide this
│   ├── NS_Project_Merged_FIXED.csv                                ← Created by Step 1
│   └── raw_weather/                                               ← Weather cache (auto-created)
│
└── outputs/                     ← Charts and tables (created by Step 2)
    ├── 01_lag_curve.png
    ├── 02_seasonal_pattern.png
    ├── 03_weekday_bias.png
    ├── 04_new_variables.png
    ├── 05_rolling_comparison.png
    ├── 06_ftc_boxplot.png
    ├── 07_snow_analysis.png
    ├── 08_regional_heatmap.png
    ├── 09_ols_coefficients.png
    ├── correlation_table.csv
    └── regional_results.csv
```

---

## ⚙️ Setup — Do This Once

### 1. Make sure Python is installed
You need **Python 3.10 or higher**. Check your version:
```bash
python --version
```

### 2. Install required packages

**For data collection and analysis:**
```bash
pip install pandas numpy openpyxl requests tqdm matplotlib seaborn scipy
```

**For the dashboard:**
```bash
pip install streamlit plotly
```

### 3. Place the OCC data file
Put the NS TIR complaints file in the same folder as the scripts:
```
Operations_Contact_Centre_Call_Summary_20260120.csv.xlsx
```
> ⚠️ The filename must match exactly. The script will tell you if it can't find it.

---

## 🚀 How to Run — Three Steps in Order

### Step 1 — Collect & Merge Data
```bash
python 01_collect_data.py
```
**What it does:**
- Downloads daily weather data from Environment Canada for 5 NS stations (2019–2025)
- Loads the OCC complaints file
- Matches each complaint to the nearest weather station by region
- Saves the merged dataset to `Data/NS_Project_Merged_FIXED.csv`

**How long it takes:** 20–40 minutes on first run (downloads ~6 years of weather data). Subsequent runs are instant — it uses the cached files in `Data/raw_weather/`.

**Expected output:**
```
✅  Weather collected: 10,950 station-day rows
✅  Merged dataset saved → Data/NS_Project_Merged_FIXED.csv
    Shape: 391,795 rows × 18 columns
```

---

### Step 2 — Run the Analysis
```bash
python 02_analysis.py
```
**What it does:**
- Engineers features: freeze-thaw days, rolling weather windows, heating degree days, interaction terms
- Runs Spearman cross-correlations at 1–21 day lags
- Fits an OLS regression model with 7 weather predictors
- Runs regional breakdowns for all 5 NS weather stations
- Saves 9 chart images and 2 summary CSV tables to `outputs/`

**How long it takes:** 1–3 minutes.

**Expected output:**
```
✅  09 figures saved to outputs/
✅  correlation_table.csv  →  outputs/
✅  regional_results.csv   →  outputs/
```

---

### Step 3 — Launch the Dashboard
```bash
streamlit run app.py
```
**What it does:**
- Opens an interactive 9-slide presentation in your browser
- Covers all major findings with charts and plain-language explanations

**A browser tab will open automatically** at `http://localhost:8501`. If it doesn't, open that URL manually.

**To stop the dashboard:** Press `Ctrl + C` in the terminal.

---

## 🗺️ What the Dashboard Covers

| Slide | Title | What You'll Learn |
|-------|-------|-------------------|
| 01 | Overview | The research question and dataset summary |
| 02 | The Problem | Why reactive patching is too slow and costly |
| 03 | How Roads Break | The physics of freeze-thaw damage |
| 04 | Seasonal Pattern | Why July gets the most complaints despite no winter weather |
| 05 | 5-Day Lag ★ | The core finding — complaints peak 5 days after freeze-thaw events |
| 06 | Predictors | Which weather variables best predict complaint counts |
| 07 | By Region | How the signal differs across Halifax, Annapolis Valley, Cape Breton, etc. |
| 08 | Regression | OLS model results and what the coefficients mean in plain English |
| 09 | Action Plan | A proposed 3-tier weather alert system for NS TIR operations |

---

## 🌡️ Weather Stations Used

| Station | Region Covered | ECCC ID |
|---------|---------------|---------|
| Halifax Stanfield | HRM & Lunenburg | 50620 |
| Greenwood A | Annapolis Valley & Kings | 50839 |
| Truro | Colchester & Cumberland | 6354 |
| Sydney A | Cape Breton | 50308 |
| Yarmouth A | SW Nova Scotia & Shelburne | 43405 |

> Note: Yarmouth A has limited precipitation data. Sydney A uses a fallback station (Glace Bay) if the primary is unavailable.

---

## 📊 Key Findings (Summary)

- **5-day lag:** Freeze-thaw events reliably predict a surge in pothole complaints 5 days later (Spearman r = −0.081; spring only: r = −0.143, p < 0.001)
- **Spring amplification:** The signal is 3× stronger during March–May than the full-year average
- **Top predictors:** Spring season (+4.59 complaints/day), FTC 14-day (−0.67), 7-day snowfall (+0.23)
- **Regional variation:** Halifax has the strongest freeze-thaw signal; Annapolis Valley and Central NS are precipitation-driven
- **Model fit:** OLS R² = 7.2% — weather explains 7.2% of daily variance; road age and traffic volume account for most of the rest

---

## ❓ Common Issues

**"OCC file not found"**
> Make sure `Operations_Contact_Centre_Call_Summary_20260120.csv.xlsx` is in the same folder as the scripts. Check the filename matches exactly (including the date).

**"Module not found" error**
> You're missing a package. Run the pip install commands in the Setup section again.

**Dashboard won't open**
> Make sure you ran `pip install streamlit plotly` first. Then try opening `http://localhost:8501` manually in your browser.

**Weather download is slow or fails**
> The ECCC API can be slow. If a station fails, the script automatically tries fallback station IDs. Previously downloaded stations are cached and won't be re-downloaded.

**Analysis script fails with "file not found"**
> Step 1 must be completed first. Run `python 01_collect_data.py` before `python 02_analysis.py`.

---

## 📝 Notes

- All analysis uses **weekdays only** for the OLS regression to remove the call-centre reporting bias (weekend complaints are ~75% lower simply because the phone lines have reduced hours)
- The freeze-thaw day definition is: `Tmax > 0°C AND Tmin < 0°C` on the same calendar day
- Rolling weather windows are computed with a **1-day forward shift** to prevent data leakage (only weather before the complaint date is used as a predictor)
- Data covers January 2019 through September 2025

---

*MBAN 2026 · NS TIR Operations Contact Centre + Environment and Climate Change Canada*