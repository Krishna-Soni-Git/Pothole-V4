"""
NS Pothole Project — Script 2: Statistical Analysis
=====================================================
Reads:  Data/NS_Project_Merged_FIXED.csv  (output of 01_collect_data.py)
Writes: outputs/  (9 figures + 2 CSV tables)

Analysis pipeline:
  1. Load & quality report
  2. Feature engineering  (freeze-thaw, rolling windows, HDD, lags, interactions)
  3. Spearman correlations (lag curve + rolling feature ranking)
  4. OLS regression        (weekdays, 7 predictors, HC3 robust SE)
  5. Regional analysis     (per-station Spearman for 3 key features)
  6. Nine publication-quality figures:
       01_lag_curve.png
       02_seasonal_pattern.png
       03_weekday_bias.png
       04_new_variables.png
       05_rolling_comparison.png
       06_ftc_boxplot.png
       07_snow_analysis.png
       08_regional_heatmap.png
       09_ols_coefficients.png

Run:
  pip install pandas numpy matplotlib seaborn scipy
  python 02_analysis.py
"""

import os, warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

INPUT_CSV = "Data/NS_Project_Merged_FIXED.csv"

# ── Colour palette (matches v2 style) ────────────────────────────────────────
P = {
    # chart colours — vivid enough to work on both white and dark backgrounds
    "bg":      "#F8F9FB",
    "panel":   "#FFFFFF",
    "text":    "#111827",
    "subtext": "#4B5563",
    "rain":    "#1D70B8",
    "ftc":     "#C0392B",
    "spring":  "#B45309",
    "neutral": "#6B7280",
    "snow":    "#0284C7",
    "green":   "#15803D",
    "gold":    "#D97706",
    "grid":    "#E5E7EB",
}


def apply_style():
    plt.rcParams.update({
        "figure.facecolor":  P["bg"],
        "axes.facecolor":    P["panel"],
        "axes.edgecolor":    P["grid"],
        "axes.labelcolor":   P["text"],
        "axes.titlecolor":   P["text"],
        "axes.titlesize":    14,
        "axes.titleweight":  "bold",
        "axes.labelsize":    11,
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.grid":         True,
        "grid.color":        P["grid"],
        "grid.linewidth":    0.6,
        "xtick.color":       P["subtext"],
        "ytick.color":       P["subtext"],
        "xtick.labelsize":   10,
        "ytick.labelsize":   10,
        "legend.fontsize":   10,
        "legend.frameon":    True,
        "legend.framealpha": 0.92,
        "font.family":       "DejaVu Sans",
        "text.color":        P["text"],
        "figure.dpi":        150,
        "savefig.dpi":       180,
        "axes.titlepad":     14,
        "axes.labelpad":     8,
    })


apply_style()


def caption(fig, txt, y=0.01):
    fig.text(0.5, y, txt, ha="center", va="bottom",
             fontsize=7.5, color=P["subtext"], style="italic")


def save(fig, name):
    fig.savefig(f"outputs/{name}", dpi=180, bbox_inches="tight", facecolor=P["bg"])
    print(f"  Saved: outputs/{name}")
    plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD & QUALITY REPORT
# ══════════════════════════════════════════════════════════════════════════════

def load(path: str) -> pd.DataFrame:
    print(f"Loading {path} ...")
    df = pd.read_csv(path, low_memory=False)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Coerce all weather numeric columns
    wx_cols = [c for c in df.columns if any(k in c for k in
               ["Temp", "Precip", "Rain", "Snow", "Gust", "Deg", "_Temp"])]
    for col in wx_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print(f"  {len(df):,} rows | {df['Date'].min().date()} – {df['Date'].max().date()}")
    return df


def quality_report(df: pd.DataFrame):
    print("\n" + "=" * 60)
    print("DATA QUALITY REPORT")
    print("=" * 60)
    total = len(df)
    pot   = df[df["Category Shortcode"] == "TCC-POTHOLE"]

    print(f"Total records    : {total:,}")
    print(f"Pothole records  : {len(pot):,}  ({100*len(pot)/total:.1f}%)")
    print(f"Date range       : {df['Date'].min().date()} to {df['Date'].max().date()}")

    print("\nTop 8 complaint types:")
    for cat, n in df["Category Shortcode"].value_counts().head(8).items():
        print(f"  {cat:<46} {n:>7,}  ({100*n/total:.1f}%)")

    print("\nWeekday reporting pattern (potholes):")
    pot2 = pot.copy()
    pot2["wd"] = pot2["Date"].dt.dayofweek
    day_names  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for d, n in pot2["wd"].value_counts().sort_index().items():
        print(f"  {day_names[d]}: {n:>5,}")

    print("\nWeather column availability (% null):")
    for col in ["Max_Temp", "Min_Temp", "Total_Precip", "Total_Rain",
                "Total_Snow", "Heat_Deg_Days", "Max_Gust_Speed", "Snow_on_Grnd"]:
        if col in df.columns:
            pct  = 100 * df[col].isna().sum() / total
            flag = "✓" if pct < 5 else ("~" if pct < 40 else "✗")
            print(f"  {flag} {col:<20} {pct:.1f}% null")

    print("\nStation breakdown:")
    for st, grp in df.groupby("Station_Label"):
        n_pot  = (grp["Category Shortcode"] == "TCC-POTHOLE").sum()
        p_null = 100 * grp["Total_Precip"].isna().sum() / len(grp) if "Total_Precip" in grp else 100
        print(f"  {st:<22} {len(grp):>7,} rows | potholes={n_pot:,} | precip null={p_null:.1f}%")

    print("=" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# 2. FEATURE ENGINEERING  (daily aggregate)
# ══════════════════════════════════════════════════════════════════════════════

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    print("\nBuilding daily feature matrix...")

    agg_dict = {
        "Pothole_Count": ("Category Shortcode", lambda x: (x == "TCC-POTHOLE").sum()),
    }
    for col in ["Total_Precip", "Total_Rain", "Total_Snow", "Snow_on_Grnd",
                "Max_Temp", "Min_Temp", "Mean_Temp", "Heat_Deg_Days", "Max_Gust_Speed"]:
        if col in df.columns:
            agg_dict[col] = (col, "mean")

    daily = (df.groupby("Date")
               .agg(**agg_dict)
               .reset_index()
               .sort_values("Date")
               .reset_index(drop=True))

    # Interpolate temperature gaps (short gaps only)
    for col in ["Max_Temp", "Min_Temp", "Mean_Temp", "Heat_Deg_Days"]:
        if col in daily.columns:
            daily[col] = daily[col].interpolate(method="linear", limit=5)

    # Fill missing precipitation with 0 (no precip reported = trace/none)
    for col in ["Total_Precip", "Total_Rain", "Total_Snow"]:
        if col in daily.columns:
            daily[col] = daily[col].fillna(0)

    # ── Calendar flags ────────────────────────────────────────────────────────
    daily["Month"]        = daily["Date"].dt.month
    daily["Weekday"]      = daily["Date"].dt.dayofweek
    daily["IsWeekday"]    = (daily["Weekday"] < 5).astype(int)
    daily["SpringSeason"] = daily["Month"].isin([3, 4, 5]).astype(int)
    daily["Year"]         = daily["Date"].dt.year

    # ── Freeze-Thaw Cycle flag ────────────────────────────────────────────────
    # A FTC day: Tmax > 0°C AND Tmin < 0°C (temperature crossed zero)
    if "Max_Temp" in daily.columns and "Min_Temp" in daily.columns:
        daily["Freeze_Thaw"] = (
            (daily["Max_Temp"] > 0) & (daily["Min_Temp"] < 0)
        ).astype(int)
    else:
        daily["Freeze_Thaw"] = 0

    # ── Rolling windows (shifted 1 day to prevent data leakage) ──────────────
    for w in [3, 5, 7, 14]:
        for col, prefix in [
            ("Total_Precip", "Precip"),
            ("Total_Rain",   "Rain"),
            ("Total_Snow",   "Snow"),
            ("Freeze_Thaw",  "FTC"),
        ]:
            if col in daily.columns:
                daily[f"{prefix}_Roll{w}d"] = (
                    daily[col].rolling(w, min_periods=1).sum().shift(1)
                )

    # Heating Degree Day rolling sum (proxy for frost depth / ground freeze)
    if "Heat_Deg_Days" in daily.columns:
        for w in [14, 30]:
            daily[f"HDD_Roll{w}d"] = (
                daily["Heat_Deg_Days"].rolling(w, min_periods=1).sum().shift(1)
            )

    # ── Single-day lags 1–21 (for lag-curve analysis) ─────────────────────────
    for lag in range(1, 22):
        if "Total_Precip" in daily.columns:
            daily[f"Precip_Lag_{lag}d"] = daily["Total_Precip"].shift(lag)
        daily[f"FTC_Lag_{lag}d"] = daily["Freeze_Thaw"].shift(lag)

    # ── Interaction term: precip occurring on a FTC day ───────────────────────
    if "Total_Precip" in daily.columns:
        daily["Precip_x_FTC"]       = daily["Total_Precip"] * daily["Freeze_Thaw"]
        daily["PrecipxFTC_Roll7d"]  = (
            daily["Precip_x_FTC"].rolling(7, min_periods=1).sum().shift(1)
        )

    print(f"  {len(daily)} days × {len(daily.columns)} features")
    return daily


# ══════════════════════════════════════════════════════════════════════════════
# 3. SPEARMAN CORRELATIONS
# ══════════════════════════════════════════════════════════════════════════════

def correlations(daily: pd.DataFrame) -> pd.DataFrame:
    print("\nSpearman correlations (all lag/rolling features)...")
    lag_cols = [c for c in daily.columns if
                any(k in c for k in ["Lag_", "Roll", "HDD", "PrecipxFTC"])]
    rows = []
    for col in lag_cols:
        sub = daily[["Pothole_Count", col]].dropna()
        if len(sub) < 30:
            continue
        r, p = stats.spearmanr(sub["Pothole_Count"], sub[col])
        rows.append({"Feature": col, "r": round(r, 4),
                     "p": round(p, 4), "N": len(sub)})

    corr_df = (pd.DataFrame(rows)
               .sort_values("r", ascending=False)
               .reset_index(drop=True))
    print("Top 12:")
    print(corr_df.head(12).to_string(index=False))
    return corr_df


# ══════════════════════════════════════════════════════════════════════════════
# 4. OLS REGRESSION
# ══════════════════════════════════════════════════════════════════════════════

def regression(daily: pd.DataFrame):
    print("\nOLS regression (weekdays only)...")

    # Select predictors — only include if the column exists
    candidate_preds = [
        "Precip_Roll7d", "Rain_Roll7d", "Snow_Roll7d",
        "FTC_Roll14d",   "HDD_Roll14d", "SpringSeason",
        "PrecipxFTC_Roll7d",
    ]
    preds = [p for p in candidate_preds if p in daily.columns]

    wd = daily[daily["IsWeekday"] == 1].dropna(subset=preds + ["Pothole_Count"]).copy()

    X = np.column_stack([np.ones(len(wd))] + [wd[p].values for p in preds])
    y = wd["Pothole_Count"].values

    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    yhat   = X @ beta
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2     = 1 - ss_res / ss_tot

    # Robust standard errors (HC3 sandwich estimator)
    n, k = X.shape
    e    = y - yhat
    h    = np.diag(X @ np.linalg.inv(X.T @ X) @ X.T)   # hat matrix diagonal
    e_hc3 = e / (1 - h)                                  # HC3 residuals
    meat  = (X * (e_hc3 ** 2)[:, None]).T @ X
    bread = np.linalg.inv(X.T @ X)
    cov   = bread @ meat @ bread
    se    = np.sqrt(np.diag(cov))
    tv    = beta / se
    pv    = [2 * (1 - stats.t.cdf(abs(t), df=n - k)) for t in tv]

    reg_df = pd.DataFrame({
        "Variable":    ["Intercept"] + preds,
        "Coefficient": np.round(beta, 4),
        "Std_Error":   np.round(se, 4),
        "T_Stat":      np.round(tv, 3),
        "P_Value":     np.round(pv, 4),
    })
    print(f"\n  R² = {r2:.4f}  (N={n:,})")
    print(reg_df.to_string(index=False))
    return reg_df, r2


# ══════════════════════════════════════════════════════════════════════════════
# 5. REGIONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

def regional(df: pd.DataFrame) -> pd.DataFrame:
    print("\nRegional analysis...")

    station_region_map = {
        "Halifax_Stanfield": "Halifax / Lunenburg",
        "Greenwood_A":       "Annapolis Valley",
        "Yarmouth_A":        "SW Nova Scotia",
        "Sydney_A":          "Cape Breton",
        "Truro":             "Central NS",
    }
    rows = []
    for label, region in station_region_map.items():
        sub = df[df["Station_Label"] == label].copy()
        if sub.empty:
            continue

        d = sub.groupby("Date").agg(
            Pothole_Count =("Category Shortcode", lambda x: (x == "TCC-POTHOLE").sum()),
            Total_Precip  =("Total_Precip",  "mean"),
            Max_Temp      =("Max_Temp",       "mean"),
            Min_Temp      =("Min_Temp",       "mean"),
            Heat_Deg_Days =("Heat_Deg_Days",  "mean") if "Heat_Deg_Days" in sub.columns else ("Max_Temp", "mean"),
        ).reset_index().sort_values("Date").reset_index(drop=True)

        d["Total_Precip"]  = d["Total_Precip"].fillna(0)
        d["Max_Temp"]      = d["Max_Temp"].interpolate(limit=5)
        d["Min_Temp"]      = d["Min_Temp"].interpolate(limit=5)
        d["Heat_Deg_Days"] = d["Heat_Deg_Days"].interpolate(limit=5)
        d["Freeze_Thaw"]   = ((d["Max_Temp"] > 0) & (d["Min_Temp"] < 0)).astype(int)

        d["PR7"]   = d["Total_Precip"].rolling(7,  min_periods=1).sum().shift(1)
        d["FT14"]  = d["Freeze_Thaw"].rolling(14,  min_periods=1).sum().shift(1)
        d["HDD14"] = d["Heat_Deg_Days"].rolling(14, min_periods=1).sum().shift(1)
        d = d.dropna(subset=["FT14", "HDD14"])

        if d["Pothole_Count"].sum() == 0:
            continue

        r_p, p_p = stats.spearmanr(d["Pothole_Count"], d["PR7"])
        r_f, p_f = stats.spearmanr(d["Pothole_Count"], d["FT14"])
        r_h, p_h = stats.spearmanr(d["Pothole_Count"], d["HDD14"])

        print(f"  {region:<24} Precip7d r={r_p:.3f}(p={p_p:.3f})  "
              f"FTC14d r={r_f:.3f}(p={p_f:.3f})  "
              f"HDD14d r={r_h:.3f}(p={p_h:.3f})  "
              f"potholes={int(d['Pothole_Count'].sum()):,}")

        rows.append({
            "Region":          region,
            "Station":         label,
            "Precip_Roll7d_r": round(r_p, 4), "Precip_Roll7d_p": round(p_p, 4),
            "FTC_14d_r":       round(r_f, 4), "FTC_14d_p":       round(p_f, 4),
            "HDD_14d_r":       round(r_h, 4), "HDD_14d_p":       round(p_h, 4),
            "Pothole_Total":   int(d["Pothole_Count"].sum()),
        })

    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# 6. FIGURES
# ══════════════════════════════════════════════════════════════════════════════

def plot_lag_curve(daily: pd.DataFrame):
    """Fig 01 — Spearman r at each 1–21 day lag for precip and FTC."""
    print("  Fig 01: lag curve")
    lags  = list(range(1, 22))
    cp, cf = [], []

    for lag in lags:
        for arr, out in [("Total_Precip", cp), ("Freeze_Thaw", cf)]:
            if arr not in daily.columns:
                out.append(np.nan); continue
            s = daily[["Pothole_Count", arr]].copy()
            s["sh"] = s[arr].shift(lag)
            s = s.dropna()
            r, _ = stats.spearmanr(s["Pothole_Count"], s["sh"])
            out.append(r)

    pp = int(np.nanargmax(cp)); pf = int(np.nanargmax(cf))

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.axhline(0, color=P["grid"], lw=1)
    ax.fill_between(lags, cp, alpha=.12, color=P["rain"])
    ax.fill_between(lags, cf, alpha=.10, color=P["ftc"])
    ax.plot(lags, cp, "o-",  lw=2.2, ms=5, color=P["rain"], label="Precipitation (single-day lag)")
    ax.plot(lags, cf, "s--", lw=2.2, ms=5, color=P["ftc"],  label="Freeze-Thaw (single-day lag)")
    ax.annotate(f"Peak Day {lags[pp]}\nr={cp[pp]:.3f}",
                xy=(lags[pp], cp[pp]), xytext=(lags[pp]+1.5, cp[pp]+.008),
                arrowprops=dict(arrowstyle="->", color=P["rain"], lw=1.2),
                fontsize=8, color=P["rain"])
    ax.annotate(f"Peak Day {lags[pf]}\nr={cf[pf]:.3f}",
                xy=(lags[pf], cf[pf]), xytext=(lags[pf]-4, cf[pf]+.012),
                arrowprops=dict(arrowstyle="->", color=P["ftc"], lw=1.2),
                fontsize=8, color=P["ftc"])
    ax.set_title("The Lag Effect: How Many Days After a Weather Event Do Potholes Spike?", pad=14)
    ax.set_xlabel("Days After Weather Event")
    ax.set_ylabel("Spearman r")
    ax.set_xticks(lags)
    ax.legend()
    caption(fig, "Source: NS TIR + Environment Canada | Spearman correlation 2019-2025 | All days")
    save(fig, "01_lag_curve.png")


def plot_seasonal(daily: pd.DataFrame):
    """Fig 02 — Average daily potholes per calendar month."""
    print("  Fig 02: seasonal pattern")
    m = (daily.groupby("Month")
               .agg(mean=("Pothole_Count", "mean"), total=("Pothole_Count", "sum"))
               .reset_index())
    m["pct"]  = 100 * m["total"] / m["total"].sum()
    mlabels   = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    colors    = [P["spring"] if x in [3, 4, 5] else P["rain"] for x in m["Month"]]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar([mlabels[x-1] for x in m["Month"]], m["mean"],
                  color=colors, width=.65, zorder=2, edgecolor=P["bg"])
    for bar, pct in zip(bars, m["pct"]):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+.15,
                f"{pct:.0f}%", ha="center", va="bottom", fontsize=7.5, color=P["subtext"])
    ax.legend(handles=[
        mpatches.Patch(color=P["spring"], label="Spring Thaw (Mar-May)"),
        mpatches.Patch(color=P["rain"],   label="Other Months"),
    ])
    ax.set_title("Average Daily Pothole Complaints by Month (2019-2025)", pad=14)
    ax.set_xlabel("Month"); ax.set_ylabel("Avg Complaints per Day")
    caption(fig, "Source: NS TIR Operations Contact Centre 2019-2025")
    save(fig, "02_seasonal_pattern.png")


def plot_weekday_bias(df: pd.DataFrame):
    """Fig 03 — Complaint volume by day of week (call-centre hours bias)."""
    print("  Fig 03: weekday bias")
    pot = df[df["Category Shortcode"] == "TCC-POTHOLE"].copy()
    pot["wd"] = pot["Date"].dt.dayofweek
    counts    = pot["wd"].value_counts().sort_index()
    dlabels   = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    colors    = [P["green"] if d < 5 else P["neutral"] for d in counts.index]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar([dlabels[d] for d in counts.index], counts.values,
                  color=colors, width=.6, zorder=2, edgecolor=P["bg"])
    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+35,
                f"{val:,}", ha="center", va="bottom", fontsize=8.5, color=P["subtext"])

    we_avg = counts[[5, 6]].mean()
    wd_avg = counts[[0, 1, 2, 3, 4]].mean()
    drop   = 100 * (1 - we_avg / wd_avg)
    ax.text(.97, .93, f"Weekend reporting\n{drop:.0f}% below weekday avg",
            transform=ax.transAxes, ha="right", va="top", fontsize=9, color=P["neutral"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor=P["bg"], edgecolor=P["grid"]))
    ax.legend(handles=[
        mpatches.Patch(color=P["green"],   label="Weekday"),
        mpatches.Patch(color=P["neutral"], label="Weekend"),
    ])
    ax.set_title("Pothole Complaints by Day of Week: Reporting Bias (2019-2025)", pad=14)
    ax.set_ylabel("Total Complaints")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    caption(fig, "Weekend drop reflects call-centre hours, not road conditions")
    save(fig, "03_weekday_bias.png")


def plot_new_variables(daily: pd.DataFrame):
    """Fig 04 — 4-panel scatter: new weather variables vs potholes."""
    print("  Fig 04: new variables")
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.patch.set_facecolor(P["bg"])
    fig.suptitle("Weather Predictors vs Daily Pothole Complaints",
                 fontsize=14, fontweight="bold", color=P["text"], y=1.01)

    wd = daily[daily["IsWeekday"] == 1].copy()

    panels = [
        ("Rain_Roll7d",       "7-day Cumulative Rain (mm)",   P["rain"],    axes[0, 0], "7-day Cumul. Rain vs Potholes"),
        ("Snow_Roll7d",       "7-day Cumulative Snowfall (cm)",P["snow"],   axes[0, 1], "7-day Cumul. Snowfall vs Potholes"),
        ("HDD_Roll14d",       "14-day Cumulative HDD",        P["ftc"],     axes[1, 0], "14-day Heating Degree Days vs Potholes\n(Frost-depth proxy)"),
        ("PrecipxFTC_Roll7d", "7-day Precip×FTC Sum",         P["spring"],  axes[1, 1], "Precip × Freeze-Thaw Interaction (7-day)\n(Wet + freeze = worst damage)"),
    ]
    for col, xlabel, color, ax, title in panels:
        if col not in wd.columns:
            ax.set_visible(False); continue
        sub = wd[["Pothole_Count", col]].dropna()
        ax.scatter(sub[col], sub["Pothole_Count"],
                   alpha=0.25, s=12, color=color, edgecolors="none")
        m, b   = np.polyfit(sub[col], sub["Pothole_Count"], 1)
        x_line = np.linspace(sub[col].min(), sub[col].max(), 100)
        ax.plot(x_line, m*x_line+b, color=P["ftc"], lw=2)
        r, p = stats.spearmanr(sub[col], sub["Pothole_Count"])
        ax.set_title(f"{title}\nSpearman r={r:.3f}  p={p:.4f}")
        ax.set_xlabel(xlabel); ax.set_ylabel("Daily Potholes")

    plt.tight_layout()
    caption(fig, "Source: NS TIR + Environment Canada | Weekdays only | Scatter + OLS trend line")
    save(fig, "04_new_variables.png")


def plot_rolling_comparison(daily: pd.DataFrame):
    """Fig 05 — Horizontal bar chart ranking all rolling features by Spearman r."""
    print("  Fig 05: rolling comparison")
    roll_cols = [c for c in daily.columns if "Roll" in c and any(
        k in c for k in ["Precip_Roll","Rain_Roll","Snow_Roll","FTC_Roll","HDD_Roll","PrecipxFTC"])]
    records = []
    for col in roll_cols:
        sub  = daily[["Pothole_Count", col]].dropna()
        r, _ = stats.spearmanr(sub["Pothole_Count"], sub[col])
        label = (col.replace("Precip_Roll","Precip ")
                    .replace("Rain_Roll",  "Rain ")
                    .replace("Snow_Roll",  "Snow ")
                    .replace("FTC_Roll",   "FTC ")
                    .replace("HDD_Roll",   "HDD ")
                    .replace("PrecipxFTC_Roll","Precip×FTC ")
                    .replace("d", "-day"))
        records.append({"Feature": label, "r": round(r, 4)})

    df_r   = pd.DataFrame(records).sort_values("r", ascending=False).head(14)
    colors = []
    for f in df_r["Feature"]:
        if "Rain" in f:       colors.append(P["rain"])
        elif "Snow" in f:     colors.append(P["snow"])
        elif "FTC" in f:      colors.append(P["ftc"])
        elif "HDD" in f:      colors.append(P["spring"])
        elif "Precip×FTC" in f: colors.append(P["gold"])
        else:                 colors.append(P["neutral"])

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(range(len(df_r)), df_r["r"],
                   color=colors, height=.6, zorder=2)
    for bar, r_val in zip(bars, df_r["r"]):
        ax.text(bar.get_width()+.001, bar.get_y()+bar.get_height()/2,
                f"{r_val:.3f}", va="center", fontsize=8.5, color=P["text"])
    ax.axvline(0, color=P["text"], lw=0.8)
    ax.set_yticks(range(len(df_r)))
    ax.set_yticklabels(df_r["Feature"], fontsize=9)
    ax.set_xlabel("Spearman r"); ax.invert_yaxis()
    ax.legend(handles=[
        mpatches.Patch(color=P["rain"],    label="Precipitation"),
        mpatches.Patch(color=P["snow"],    label="Snowfall"),
        mpatches.Patch(color=P["ftc"],     label="Freeze-Thaw Count"),
        mpatches.Patch(color=P["spring"],  label="Heating Degree Days"),
        mpatches.Patch(color=P["gold"],    label="Precip × FTC interaction"),
    ], loc="lower right")
    ax.set_title("All Rolling Weather Windows vs Daily Pothole Complaints\n"
                 "Spearman Correlation Ranked (top 14)", pad=14)
    caption(fig, "Source: NS TIR + Environment Canada | All days 2019-2025")
    save(fig, "05_rolling_comparison.png")


def plot_ftc_boxplot(daily: pd.DataFrame):
    """Fig 06 — Pothole distribution grouped by 14-day FTC count."""
    print("  Fig 06: FTC boxplot")
    wd = daily[daily["IsWeekday"] == 1].dropna(subset=["FTC_Roll14d"]).copy()
    wd["FTC_Group"] = pd.cut(
        wd["FTC_Roll14d"], bins=[-0.1, 0, 4, 14],
        labels=["None\n(0 FTC days)", "Moderate\n(1-4 FTC days)", "High\n(5+ FTC days)"]
    )
    glabels = ["None\n(0 FTC days)", "Moderate\n(1-4 FTC days)", "High\n(5+ FTC days)"]
    gdata   = [wd[wd["FTC_Group"] == g]["Pothole_Count"].dropna().values for g in glabels]
    bcolors = [P["rain"], P["gold"], P["ftc"]]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bp = ax.boxplot(gdata, tick_labels=glabels, patch_artist=True,
                    widths=.45,
                    medianprops=dict(color=P["text"], lw=2),
                    whiskerprops=dict(color=P["subtext"]),
                    capprops=dict(color=P["subtext"]),
                    flierprops=dict(marker=".", ms=3, alpha=.3, markerfacecolor=P["subtext"]))
    for patch, c in zip(bp["boxes"], bcolors):
        patch.set_facecolor(c); patch.set_alpha(.65)
    means = [g.mean() for g in gdata if len(g) > 0]
    ax.scatter(range(1, len(means)+1), means, marker="D",
               color=P["text"], zorder=5, s=40, label="Mean")
    for i, m in enumerate(means):
        ax.text(i+1.18, m, f"Mean: {m:.1f}", va="center", fontsize=8, color=P["subtext"])
    if len(gdata[0]) > 0 and len(gdata[2]) > 0:
        t, p = stats.ttest_ind(gdata[2], gdata[0])
        ax.text(.97, .97, f"None vs High:\nt={t:.2f}  p={p:.4f}",
                transform=ax.transAxes, ha="right", va="top", fontsize=8.5,
                bbox=dict(boxstyle="round,pad=0.4", facecolor=P["bg"], edgecolor=P["grid"]))
    ax.set_title("Freeze-Thaw Cycle Count vs Pothole Complaints\n"
                 "Weekdays only — grouped by FTC days in prior 14 days", pad=14)
    ax.set_ylabel("Daily Pothole Complaints")
    ax.legend(fontsize=9)
    caption(fig, "Source: NS TIR + Environment Canada | Weekdays only 2019-2025")
    save(fig, "06_ftc_boxplot.png")


def plot_snow_analysis(daily: pd.DataFrame):
    """Fig 07 — Snowfall vs potholes: boxplot groups + monthly dual-axis."""
    print("  Fig 07: snow analysis")
    wd = daily[daily["IsWeekday"] == 1].copy()
    if "Snow_Roll7d" not in wd.columns:
        print("    Skipped — Snow_Roll7d not available"); return

    wd["SnowGroup"] = pd.cut(
        wd["Snow_Roll7d"].fillna(0),
        bins=[-0.1, 0, 5, 20, 500],
        labels=["No Snow", "Light\n(1-5 cm)", "Moderate\n(5-20 cm)", "Heavy\n(20+ cm)"]
    )
    glabels = ["No Snow", "Light\n(1-5 cm)", "Moderate\n(5-20 cm)", "Heavy\n(20+ cm)"]
    gdata   = [wd[wd["SnowGroup"] == g]["Pothole_Count"].dropna().values for g in glabels]
    gcolors = [P["neutral"], P["snow"], P["rain"], P["ftc"]]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    fig.patch.set_facecolor(P["bg"])

    # Left: boxplot
    ax = axes[0]
    valid_data   = [g for g in gdata if len(g) > 0]
    valid_labels = [l for l, g in zip(glabels, gdata) if len(g) > 0]
    valid_colors = [c for c, g in zip(gcolors, gdata) if len(g) > 0]
    bp = ax.boxplot(valid_data, tick_labels=valid_labels, patch_artist=True,
                    widths=.45,
                    medianprops=dict(color=P["text"], lw=2),
                    whiskerprops=dict(color=P["subtext"]),
                    capprops=dict(color=P["subtext"]),
                    flierprops=dict(marker=".", ms=3, alpha=.3, markerfacecolor=P["subtext"]))
    for patch, c in zip(bp["boxes"], valid_colors):
        patch.set_facecolor(c); patch.set_alpha(.65)
    vm = [g.mean() for g in valid_data]
    ax.scatter(range(1, len(vm)+1), vm, marker="D", color=P["text"], zorder=5, s=40)
    for i, m in enumerate(vm):
        ax.text(i+1.1, m, f"{m:.1f}", va="center", fontsize=8, color=P["subtext"])
    ax.set_title("7-day Snowfall vs Pothole Complaints\n(Weekdays only)", pad=12)
    ax.set_ylabel("Daily Pothole Complaints")

    # Right: monthly snow vs potholes dual-axis
    ax = axes[1]
    if "Total_Snow" in daily.columns:
        m_snow = daily.groupby("Month")["Total_Snow"].mean().fillna(0)
    else:
        m_snow = pd.Series(0, index=range(1, 13))
    m_pot = daily.groupby("Month")["Pothole_Count"].mean()
    months  = list(range(1, 13))
    mlabels = list("JFMAMJJASOND")
    ax2 = ax.twinx(); ax2.set_facecolor("none")
    ax.bar(months, [m_snow.get(m, 0) for m in months],
           color=P["snow"], alpha=.7, label="Avg Daily Snow (cm)", zorder=2)
    ax2.plot(months, [m_pot.get(m, 0) for m in months],
             color=P["ftc"], lw=2.5, marker="o", ms=5, label="Avg Potholes/day")
    ax.set_xticks(months); ax.set_xticklabels(mlabels)
    ax.set_ylabel("Avg Daily Snowfall (cm)", color=P["snow"])
    ax2.set_ylabel("Avg Potholes per Day",   color=P["ftc"])
    ax.tick_params(axis="y", labelcolor=P["snow"])
    ax2.tick_params(axis="y", labelcolor=P["ftc"])
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2, loc="upper right", fontsize=8)
    ax.set_title("Monthly Snowfall vs Pothole Complaints\n"
                 "(Spring melt lag visible April)", pad=12)

    plt.tight_layout()
    caption(fig, "Source: NS TIR + Environment Canada | Snowfall available for all 5 stations")
    save(fig, "07_snow_analysis.png")


def plot_regional_heatmap(reg_df: pd.DataFrame):
    """Fig 08 — Heatmap of regional correlations with significance stars."""
    print("  Fig 08: regional heatmap")
    if reg_df.empty:
        print("    No regional data — skipping"); return

    plot_data = reg_df.set_index("Region")[
        ["Precip_Roll7d_r", "FTC_14d_r", "HDD_14d_r"]
    ].copy().astype(float)
    plot_data.columns = ["7-day Precip\n(r)", "14-day FTC\n(r)", "14-day HDD\n(r)"]
    p_cols = ["Precip_Roll7d_p", "FTC_14d_p", "HDD_14d_p"]

    fig, ax = plt.subplots(figsize=(7.5, len(plot_data)*1.1+2.2))
    fig.patch.set_facecolor(P["bg"])
    sns.heatmap(plot_data, annot=False, cmap="RdYlBu_r",
                vmin=-0.15, vmax=0.15, ax=ax, cbar=True,
                linewidths=1.5, linecolor=P["bg"])

    for i, region in enumerate(plot_data.index):
        for j, col_p in enumerate(p_cols):
            val  = plot_data.iloc[i, j]
            pv   = reg_df[reg_df["Region"] == region][col_p].values[0]
            stars= ("***" if pv<.001 else "**" if pv<.01 else "*" if pv<.05 else "ns")
            tc   = P["text"] if abs(val) < 0.08 else "white"
            ax.text(j+.5, i+.5, f"r={val:.3f}\n{stars}",
                    ha="center", va="center", fontsize=9, color=tc,
                    fontweight="bold" if stars != "ns" else "normal")

    ax.set_title("Regional Weather-Pothole Correlations\n"
                 "(* p<0.05  ** p<0.01  *** p<0.001  ns=not significant)", pad=14)
    ax.set_ylabel(""); ax.set_xlabel("")
    caption(fig, "HDD = Heating Degree Days (frost-depth proxy) | All 5 NS stations")
    save(fig, "08_regional_heatmap.png")


def plot_ols_coefficients(reg_df: pd.DataFrame, r2: float):
    """Fig 09 — OLS coefficient plot with 95% CI and significance colour."""
    print("  Fig 09: OLS coefficients")
    df_p = reg_df[reg_df["Variable"] != "Intercept"].copy().reset_index(drop=True)
    df_p["CI_low"]  = df_p["Coefficient"] - 1.96*df_p["Std_Error"]
    df_p["CI_high"] = df_p["Coefficient"] + 1.96*df_p["Std_Error"]
    df_p["Sig"]     = df_p["P_Value"] < .05

    labels = {
        "Precip_Roll7d":     "7-day Cumul. Precip",
        "Rain_Roll7d":       "7-day Cumul. Rain",
        "Snow_Roll7d":       "7-day Cumul. Snow",
        "FTC_Roll14d":       "14-day FTC Count",
        "HDD_Roll14d":       "14-day Heating Deg Days",
        "SpringSeason":      "Spring Season (Mar-May)",
        "PrecipxFTC_Roll7d": "Precip × FTC Interaction",
    }
    df_p["Label"] = df_p["Variable"].map(labels).fillna(df_p["Variable"])

    fig, ax = plt.subplots(figsize=(10, 5.5))
    y_pos  = range(len(df_p))
    colors = [P["ftc"] if s else P["neutral"] for s in df_p["Sig"]]
    ax.barh(y_pos, df_p["Coefficient"], height=.45, color=colors, alpha=.75, zorder=2)
    ax.errorbar(df_p["Coefficient"], y_pos,
                xerr=1.96*df_p["Std_Error"],
                fmt="none", color=P["text"], lw=1.4, capsize=5, zorder=3)
    ax.axvline(0, color=P["text"], lw=1)
    for i, row in df_p.iterrows():
        sign = "+" if row["Coefficient"] > 0 else ""
        ax.text(row["CI_high"]+.08, i,
                f"{sign}{row['Coefficient']:.2f}  (p={row['P_Value']:.3f})",
                va="center", fontsize=8.5,
                color=P["ftc"] if row["Sig"] else P["subtext"])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_p["Label"], fontsize=9.5)
    ax.set_xlabel("Regression Coefficient (extra complaints per unit increase)")
    ax.set_title(
        f"OLS Regression: Weather Effect on Daily Pothole Complaints\n"
        f"R² = {r2:.3f}  |  Model explains {r2*100:.1f}% of variance (weekdays only)",
        pad=14)
    ax.legend(handles=[
        mpatches.Patch(color=P["ftc"],     label="Significant (p<0.05)"),
        mpatches.Patch(color=P["neutral"], label="Not significant"),
    ], loc="lower right")
    caption(fig, "OLS with HC3 robust standard errors | Weekdays 2019-2025 | Bars show 95% CI")
    save(fig, "09_ols_coefficients.png")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 65)
    print("NS POTHOLE PROJECT — STEP 2: STATISTICAL ANALYSIS")
    print("=" * 65)

    if not os.path.exists(INPUT_CSV):
        print(f"\n✗  Input file not found: {INPUT_CSV}")
        print("   Run 01_collect_data.py first.")
        return

    df      = load(INPUT_CSV)
    quality_report(df)

    daily   = build_features(df)
    corr_df = correlations(daily)
    corr_df.to_csv("outputs/correlation_table.csv", index=False)

    reg_df, r2 = regression(daily)

    reg_results = regional(df)
    if not reg_results.empty:
        reg_results.to_csv("outputs/regional_results.csv", index=False)

    print("\nGenerating figures...")
    plot_lag_curve(daily)
    plot_seasonal(daily)
    plot_weekday_bias(df)
    plot_new_variables(daily)
    plot_rolling_comparison(daily)
    plot_ftc_boxplot(daily)
    plot_snow_analysis(daily)
    plot_regional_heatmap(reg_results)
    plot_ols_coefficients(reg_df, r2)

    print("\n" + "=" * 65)
    print("DONE — all outputs written to outputs/")
    print("=" * 65)
    print(f"""
RESULTS SUMMARY
───────────────────────────────────────────
OLS R²        : {r2:.4f}  ({r2*100:.1f}% of variance explained, weekdays)
Figures saved : outputs/01 – 09 PNG files
Tables saved  : outputs/correlation_table.csv
               outputs/regional_results.csv

Top 8 predictors (Spearman r):""")
    for _, row in corr_df.head(8).iterrows():
        print(f"  {row['Feature']:<30} r={row['r']:+.4f}  p={row['p']:.4f}")


if __name__ == "__main__":
    main()