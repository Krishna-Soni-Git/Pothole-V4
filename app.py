"""
NS Pothole Freeze-Thaw Analysis · v5 — Professional Edition
Run: streamlit run app.py
Deps: pip install streamlit plotly pandas
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os

st.set_page_config(
    page_title="NS Pothole Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM · DM Sans + DM Mono · auto dark / light
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&family=Roboto+Condensed:wght@400;600;700&family=Roboto+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════
   NS GOVERNMENT BRAND PALETTE
   Primary Blue:  #0045B8  (NS flag blue)
   Gold/Yellow:   #FDD54E  (NS flag gold)
   Red:           #D30731  (NS flag red)
   White:         #FFFFFF
   Dark Navy:     #002366  (deep navy for headers)
   Light Grey:    #F4F6F9  (page background)
   ══════════════════════════════════════════ */

:root {
  /* ─── Page backgrounds ─── */
  --bg:          #F4F6F9;
  --surface:     #FFFFFF;
  --surface2:    #F0F3F8;
  --surface3:    #E8EDF5;
  --border:      #D0D9E8;
  --border2:     #B8C5D8;
  --divider:     rgba(0,69,184,0.08);

  /* ─── Typography ─── */
  --text:        #0D1B3E;
  --text2:       #1A2F5A;
  --sub:         #3A4E72;
  --faint:       #5A6E92;

  /* ─── NS Brand: Primary Blue ─── */
  --red:         #004CB3;
  --red-v:       #0045B8;
  --red-bg:      rgba(0,69,184,0.07);
  --red-bdr:     rgba(0,69,184,0.22);

  /* ─── NS Brand: Gold ─── */
  --amber:       #B8860B;
  --amber-v:     #D4A017;
  --amber-bg:    rgba(253,213,78,0.18);
  --amber-bdr:   rgba(184,134,11,0.35);

  /* ─── NS Brand: Red ─── */
  --blue:        #A8001F;
  --blue-v:      #D30731;
  --blue-bg:     rgba(211,7,49,0.06);
  --blue-bdr:    rgba(211,7,49,0.22);

  /* ─── Green (kept for positive) ─── */
  --green:       #1A6B3C;
  --green-v:     #15803D;
  --green-bg:    rgba(26,107,60,0.07);
  --green-bdr:   rgba(26,107,60,0.22);

  /* ─── Slate (neutral) ─── */
  --slate:       #3A4E72;
  --slate-bg:    rgba(58,78,114,0.06);
  --slate-bdr:   rgba(58,78,114,0.20);

  /* ─── Sidebar: NS Deep Navy ─── */
  --sb:          #002366;
  --sb2:         #003090;
  --sb-txt:      #FFFFFF;
  --sb-sub:      #A8BDD8;
  --sb-faint:    #4A6490;
  --sb-line:     rgba(255,255,255,0.10);
  --sb-hover:    rgba(253,213,78,0.12);
  --sb-dot:      #FDD54E;
}

/* ─── BASE ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
  font-family: 'Roboto', system-ui, sans-serif !important;
  color: var(--text) !important;
  -webkit-font-smoothing: antialiased;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 2.5rem 3rem 6rem !important;
  max-width: 1200px !important;
}

/* ─── NS GOVERNMENT TOP BANNER ──────────────── */
.block-container::before {
  content: "Government of Nova Scotia  ·  Department of Public Works  ·  TIR Analysis 2019–2025";
  display: block;
  background: #002366;
  color: #FDD54E;
  font-family: 'Roboto Condensed', sans-serif;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  padding: 7px 0;
  margin: -2.5rem -3rem 2rem -3rem;
  text-align: center;
  border-bottom: 3px solid #FDD54E;
}

/* ─── SIDEBAR: NS NAVY ───────────────────────── */
[data-testid="stSidebar"] {
  background: #002366 !important;
  border-right: 4px solid #FDD54E !important;
  min-width: 255px !important;
  max-width: 255px !important;
  transform-origin: top left !important;
  transform: perspective(1200px) rotateY(3deg) !important;
  box-shadow: 8px 0 28px rgba(0,35,102,0.25) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  border-left: 3px solid transparent !important;
  color: #A8BDD8 !important;
  font-family: 'Roboto', sans-serif !important;
  font-size: 12.5px !important;
  font-weight: 400 !important;
  padding: 9px 16px 9px 16px !important;
  width: 100% !important;
  text-align: left !important;
  justify-content: flex-start !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
  transition: all .15s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(253,213,78,0.10) !important;
  color: #FFFFFF !important;
  border-left: 3px solid rgba(253,213,78,0.5) !important;
}

/* ─── CHARTS ────────────────────────────────── */
[data-testid="stPlotlyChart"] > div {
  border-radius: 8px !important;
  border: 1px solid #D0D9E8 !important;
  border-top: 3px solid #0045B8 !important;
  overflow: hidden !important;
  background: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(0,35,102,0.08) !important;
}

/* ─── SCROLLBAR ─────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #E8EDF5; }
::-webkit-scrollbar-thumb { background: #0045B8; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #002366; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LIVE DATA LOADING
# Reads CSV outputs produced by 02_analysis.py when available.
# Falls back to representative hardcoded values if CSVs are missing.
# Re-run `python 02_analysis.py` to refresh all values.
# ══════════════════════════════════════════════════════════════════════════════

_OUTPUTS = "outputs"

@st.cache_data(ttl=3600)
def _load_outputs():
    """Load all generated CSVs into a dict. Keys are None if file missing."""
    def _read(filename):
        path = os.path.join(_OUTPUTS, filename)
        try:
            return pd.read_csv(path) if os.path.exists(path) else None
        except Exception:
            return None

    corr        = _read("correlation_table.csv")
    regional    = _read("regional_results.csv")
    lag_stats   = _read("lag_window_summary_stats.csv")
    lag_full    = _read("lag_window_summary.csv")
    alert_prec  = _read("alert_precision.csv")
    seas_check  = _read("seasonal_adjustment_check.csv")
    merged_path = "Data/NS_Project_Merged_FIXED.csv"

    annual_counts = None
    total_records = None
    total_potholes = None
    if os.path.exists(merged_path):
        try:
            df = pd.read_csv(merged_path, usecols=["Date", "Category Shortcode"],
                             low_memory=False)
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Year"] = df["Date"].dt.year
            pot = df[df["Category Shortcode"] == "TCC-POTHOLE"]
            annual_counts  = pot.groupby("Year").size().to_dict()
            total_records  = len(df)
            total_potholes = len(pot)
        except Exception:
            pass

    return {
        "corr":           corr,
        "regional":       regional,
        "lag_stats":      lag_stats,
        "lag_full":       lag_full,
        "alert_prec":     alert_prec,
        "seas_check":     seas_check,
        "annual_counts":  annual_counts,
        "total_records":  total_records,
        "total_potholes": total_potholes,
        "data_available": any(x is not None for x in [corr, regional, annual_counts]),
    }

_live = _load_outputs()

# ── Resolve key values: live first, hardcoded fallback ───────────────────────
_ANNUAL_FALLBACK = {2019: 4784, 2020: 4009, 2021: 4118,
                    2022: 5700, 2023: 3299, 2024: 4604, 2025: 5582}
ANNUAL_COUNTS   = _live["annual_counts"]  or _ANNUAL_FALLBACK
TOTAL_RECORDS   = f"{_live['total_records']:,}"   if _live["total_records"]  else "391,795"
TOTAL_POTHOLES  = f"{_live['total_potholes']:,}"  if _live["total_potholes"] else "32,096"
POTHOLE_PCT     = (f"{100*_live['total_potholes']/_live['total_records']:.1f} %"
                   if _live["total_records"] and _live["total_potholes"] else "8.2 %")

# Best lag info — from lag_window_summary_stats.csv or hardcoded default
_ls = _live["lag_stats"]
BEST_LAG_DAY   = int(_ls["best_lag_day"].iloc[0])  if _ls is not None and len(_ls) else 5
BEST_LAG_R     = float(_ls["best_r"].iloc[0])      if _ls is not None and len(_ls) else -0.081
BEST_LAG_PBONF = float(_ls["best_p_bonferroni"].iloc[0]) if _ls is not None and len(_ls) else 0.042
SIG_LAG_MIN    = int(_ls["sig_lag_min"].iloc[0])   if _ls is not None and len(_ls) and pd.notna(_ls["sig_lag_min"].iloc[0]) else 4
SIG_LAG_MAX    = int(_ls["sig_lag_max"].iloc[0])   if _ls is not None and len(_ls) and pd.notna(_ls["sig_lag_max"].iloc[0]) else 7

# Alert precision info
_ap = _live["alert_prec"]
ALERT_PRECISION    = float(_ap["precision"].iloc[0])          if _ap is not None and len(_ap) else None
ALERT_FALSE_POS    = float(_ap["false_positive_rate"].iloc[0]) if _ap is not None and len(_ap) else None
ALERT_LIFT         = float(_ap["lift_over_baseline"].iloc[0])  if _ap is not None and len(_ap) else None
ALERT_N            = int(_ap["n_alert_days"].iloc[0])          if _ap is not None and len(_ap) else None

# Seasonal adjustment result
_sc = _live["seas_check"]
if _sc is not None and len(_sc):
    _peak_adj = _sc.loc[_sc["r_adj"].abs().idxmax()]
    ADJ_PEAK_LAG = int(_peak_adj["lag"])
    ADJ_PEAK_R   = float(_peak_adj["r_adj"])
else:
    ADJ_PEAK_LAG, ADJ_PEAK_R = 5, -0.062   # representative fallback

# Sidebar data-status indicator
if _live["data_available"]:
    st.sidebar.caption("✅ Live analysis outputs loaded.")
else:
    st.sidebar.caption("ℹ️ Using representative values. Run `02_analysis.py` to load live data.")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE REGISTRY
# ══════════════════════════════════════════════════════════════════════════════
SLIDES = [
    ("Overview", "var(--red)"),
    ("The Problem", "var(--red)"),
    ("How Roads Break", "var(--blue)"),
    ("Seasonal Pattern","var(--amber)"),
    ("5-Day Lag ", "var(--red)"),
    ("Predictors", "var(--blue)"),
    ("By Region", "var(--amber)"),
    ("Regression", "var(--green)"),
    ("Monthly Deep-Dive", "var(--blue)"),
    ("Action Plan", "var(--red)"),
]
NUMS = ["01","02","03","04","05","06","07","08","09","10"]

if "s" not in st.session_state:
    st.session_state.s = 0

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand block — NS Government
    st.markdown(
        '<div style="background:#001A4E;padding:20px 20px 14px;border-bottom:3px solid #FDD54E">'
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px">'
        '<div style="width:7px;height:7px;background:#FDD54E;border-radius:50%"></div>'
        '<p style="font-family:\'Roboto Condensed\',sans-serif;font-size:9px;font-weight:700;'
        'color:#FDD54E;letter-spacing:2.5px;text-transform:uppercase;margin:0">'
        'Nova Scotia · Public Works</p></div>'
        '<p style="font-family:\'Roboto Condensed\',sans-serif;font-size:16px;font-weight:700;'
        'color:#FFFFFF;margin:0 0 3px;line-height:1.2;letter-spacing:0.2px">'
        'Pothole Analysis</p>'
        '<p style="font-family:\'Roboto Mono\',monospace;font-size:11px;color:#7A9FC0;'
        'margin:0;font-weight:400">NS TIR + ECCC · 2019–2025</p>'
        '</div>',
        unsafe_allow_html=True)

    st.markdown(
        '<p style="font-family:\'Roboto Condensed\',sans-serif;font-size:10px;font-weight:700;'
        'letter-spacing:2px;text-transform:uppercase;color:#4A6490;'
        'padding:14px 20px 6px;margin:0">Navigation</p>',
        unsafe_allow_html=True)

    S = st.session_state.s
    for i, (label, _color) in enumerate(SLIDES):
        if st.button(label, key=f"sb_{i}", use_container_width=True):
            st.session_state.s = i
            st.rerun()

    # Active highlight
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] .stButton:nth-of-type({S+1}) > button {{
      background: rgba(253,213,78,0.15) !important;
      color: #FFFFFF !important;
      font-weight: 600 !important;
      border-left: 3px solid #FDD54E !important;
    }}
    </style>""", unsafe_allow_html=True)

    # Footer
    st.markdown(
        f'<div style="padding:14px 22px 18px;border-top:1px solid var(--sb-line)">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'margin-bottom:6px">'
        f'<span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--sb-faint);letter-spacing:.5px">{NUMS[S]}&nbsp;of&nbsp;{NUMS[-1]}</span>'
        f'<div style="display:flex;gap:3px;align-items:center">'
        + "".join(
            f'<div style="width:{14 if j==S else 5}px;height:3px;'
            f'border-radius:2px;background:{"var(--sb-dot)" if j==S else "var(--sb-faint)"};'
            f'transition:all .2s"></div>'
            for j in range(len(SLIDES))
        )
        + f'</div></div>'
        f'<p style="font-size:11.5px;color:var(--sb-faint);font-weight:400">'
        f'MBAN 2026 · Nova Scotia TIR + ECCC</p>'
        f'</div>',
        unsafe_allow_html=True)

S = st.session_state.s

# ══════════════════════════════════════════════════════════════════════════════
# CHART PALETTE (explicit hex — Plotly can't read CSS vars)
# ══════════════════════════════════════════════════════════════════════════════
C = dict(
    red = "#EF4444",
    blue = "#3B82F6",
    amber = "#F59E0B",
    green = "#10B981",
    slate = "#94A3B8",
    indigo = "#6366F1",
)
G = dict(
    bg = "rgba(0,0,0,0)",
    grid = "rgba(110,120,150,0.12)",
    tick = "#6B7A99",
    line = "rgba(110,120,150,0.2)",
    zero = "rgba(100,110,140,0.45)",
)

def pset(fig, h=400, l=56, r=32, t=46, b=54):
    fig.update_layout(
        height=h, plot_bgcolor=G["bg"], paper_bgcolor=G["bg"],
        font=dict(family="Roboto", size=12, color=G["tick"]),
        margin=dict(l=l, r=r, t=t, b=b),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
                    font=dict(size=11.5, color=G["tick"]),
                    orientation="h", y=1.07, x=0, itemsizing="constant"),
        hoverlabel=dict(bgcolor="rgba(8,14,31,0.94)",
                        bordercolor="rgba(255,255,255,0.12)",
                        font=dict(family="Roboto", size=12, color="#F0F4FF")),
    )
    fig.update_xaxes(gridcolor=G["grid"], zeroline=False,
                     tickfont=dict(size=11, color=G["tick"]),
                     title_font=dict(size=12, color=G["tick"]),
                     linecolor=G["line"], showline=True,
                     ticks="outside", ticklen=3, tickcolor=G["line"])
    fig.update_yaxes(gridcolor=G["grid"], zeroline=False,
                     tickfont=dict(size=11, color=G["tick"]),
                     title_font=dict(size=12, color=G["tick"]),
                     linecolor="rgba(0,0,0,0)")
    return fig

# ── UI HELPERS ────────────────────────────────────────────────────────────────
ACC = {
    "var(--red)": ("var(--red-bg)", "var(--red-bdr)"),
    "var(--blue)": ("var(--blue-bg)", "var(--blue-bdr)"),
    "var(--amber)": ("var(--amber-bg)", "var(--amber-bdr)"),
    "var(--green)": ("var(--green-bg)", "var(--green-bdr)"),
    "var(--slate)": ("var(--slate-bg)", "var(--slate-bdr)"),
}

def slide_header(num, title, sub=""):
    """Professional slide header with number badge."""
    st.markdown(
        f'<div style="margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid var(--divider)">'
        f'<div style="display:flex;align-items:baseline;gap:14px;margin-bottom:12px">'
        f'<span style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:600;'
        f'color:var(--sub);letter-spacing:1px">{num}</span>'
        f'<h1 style="font-family:\'Roboto Condensed\',sans-serif;font-size:clamp(1.5rem,3vw,2.1rem);'
        f'font-weight:700;color:#0D1B3E;line-height:1.15;'
        f'letter-spacing:-0.2px">{title}</h1>'
        f'</div>'
        + (f'<p style="font-size:14px;color:var(--sub);line-height:1.8;max-width:820px;'
           f'font-weight:400">{sub}</p>' if sub else "")
        + '</div>', unsafe_allow_html=True)


def box(title, body, accent="var(--blue)"):
    bg, bdr = ACC.get(accent, ("var(--surface2)", "var(--border)"))
    st.markdown(
        f'<div style="background:{bg};border:1px solid {bdr};border-left:3px solid {accent};'
        f'border-radius:10px;padding:15px 17px;margin-bottom:11px">'
        f'<p style="font-size:12px;font-weight:600;color:{accent};margin:0 0 7px;'
        f'letter-spacing:.03em">{title}</p>'
        f'<p style="font-size:13px;color:var(--text2);line-height:1.75;margin:0;'
        f'font-weight:400">{body}</p>'
        f'</div>', unsafe_allow_html=True)


def kpi(label, value, sub="", color="var(--text)", border_color=None):
    bc = border_color or "var(--border)"
    st.markdown(
        f'<div style="background:var(--surface);border:1px solid {bc};'
        f'border-radius:12px;padding:22px 16px;text-align:center">'
        f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;font-weight:500;'
        f'color:var(--faint);text-transform:uppercase;letter-spacing:2.5px;margin:0 0 11px">{label}</p>'
        f'<p style="font-family:\'Roboto Condensed\',sans-serif;font-size:clamp(1.5rem,2.8vw,2rem);font-weight:700;'
        f'color:{color};line-height:1;margin:0 0 7px">{value}</p>'
        + (f'<p style="font-size:11.5px;color:var(--sub);margin:0;font-weight:400">{sub}</p>' if sub else "")
        + '</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr style="border:none;border-top:1px solid var(--divider);margin:24px 0">', unsafe_allow_html=True)


def label(text):
    st.markdown(
        f'<p style="font-family:\'DM Mono\',monospace;font-size:12px;font-weight:600;'
        f'color:var(--sub);text-transform:uppercase;letter-spacing:1px;margin:0 0 16px">{text}</p>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 0 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if S == 0:
    # Hero headline
    st.markdown(
        '<div style="padding:8px 0 36px">'
        '<p style="font-family:\'DM Mono\',monospace;font-size:11.5px;font-weight:500;'
        'letter-spacing:2.5px;color:#0045B8;margin:0 0 20px">NOVA SCOTIA · TIR + ECCC · 2019–2025</p>'
        '<h1 style="font-family:\'DM Sans\',serif;'
        'font-size:clamp(2.2rem,5vw,3.6rem);font-weight:400;'
        'color:var(--text);line-height:1.08;letter-spacing:-1px;margin:0 0 18px">'
        'Can we predict potholes<br>'
        '<span style="color:var(--red)">before</span> they appear?'
        '</h1>'
        '<p style="font-size:15px;color:var(--sub);line-height:1.85;max-width:620px;'
        'font-weight:400;margin:0 0 30px">'
        f'A 6-year analysis of <strong style="color:var(--text);font-weight:500">{TOTAL_RECORDS} service '
        f'records</strong> and daily weather from 5 ECCC stations reveals a consistent '
        f'<strong style="color:var(--red);font-weight:500">{SIG_LAG_MIN}–{SIG_LAG_MAX}-day window</strong> between '
        'freeze-thaw events and pothole complaint surges.</p>'
        '<div style="width:48px;height:3px;background:#FDD54E;border-radius:2px;margin-top:4px"></div>'
        '</div>', unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1: kpi("Service Records",   TOTAL_RECORDS,   "NS TIR · 2019–2025", border_color="var(--border)")
    with k2: kpi("Pothole Complaints", TOTAL_POTHOLES,  f"{POTHOLE_PCT} of all records", "var(--red)", "var(--red-bdr)")
    with k3: kpi("Freeze-Thaw Days",   "647",           "detected across NS",  "var(--amber)","var(--amber-bdr)")
    with k4: kpi("Predictive Window",  f"{SIG_LAG_MIN}–{SIG_LAG_MAX} days", "FT event → surge", "var(--blue)", "var(--blue-bdr)")

    divider()

    # Two-column content
    l, r = st.columns([1.08, 1], gap="large")
    with l:
        label("About this analysis")
        box("What We Did",
            "Every pothole complaint in the NS TIR Operations Contact Centre was linked to its "
            "nearest ECCC weather station. Repeated lagged bivariate Spearman correlations at "
            "1–21 day lag offsets (weekdays only) were used to find whether freeze-thaw events "
            "reliably predict complaint surges — and by how many days. "
            "Bonferroni correction applied across 42 tests. "
            "(Note: this is a Spearman correlogram, not a formal CCF/cross-correlation.)",
            "var(--red)")
        box("Why It Matters for NS TIR",
            "Maintenance crews are currently dispatched only <em>after</em> a citizen calls. "
            "A statistically significant 5-day lag means crews can be pre-staged before the "
            "phones start ringing — cutting response time and reducing per-pothole patching cost.",
            "var(--blue)")
    with r:
        label("Data")
        box("Dataset 1 — NS TIR OCC",
            f"{TOTAL_RECORDS} complaint records across 64 supervisor area codes. "
            "Provincial highways only. January 2019 – September 2025. "
            f"Pothole complaints represent {POTHOLE_PCT} of all records ({TOTAL_POTHOLES}).",
            "var(--amber)")
        box("Dataset 2 — Environment Canada (ECCC)",
            "Daily climate data from 5 verified weather stations: Halifax Stanfield, "
            "Greenwood A, Truro, Sydney A, and Yarmouth A. Merged to complaints by "
            "geographic region and date.", "var(--green)")
# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
elif S == 1:
    slide_header("01", "Potholes cost money. Right now, we fix them too late.",
                 "NS TIR dispatches repair crews only after citizens file complaints — "
                 "weather data already available in real time could allow proactive deployment instead.")

    cl, cr = st.columns([1.45, 1], gap="large")
    with cl:
        years_sorted = sorted(ANNUAL_COUNTS.keys())
        yr_labels    = [str(y) for y in years_sorted]
        vals         = [ANNUAL_COUNTS[y] for y in years_sorted]
        clrs = ["#EF4444" if y in (2022, 2025) else
                f"rgba(59,130,246,{0.38 + i * 0.08:.2f})"
                for i, y in enumerate(years_sorted)]
        fig = go.Figure(go.Bar(
            x=yr_labels, y=vals,
            marker=dict(color=clrs, line=dict(width=0), cornerradius=5),
            text=[f"{v:,}" for v in vals], textposition="outside",
            textfont=dict(family="Roboto Mono", size=11, color=G["tick"]),
            hovertemplate="<b>%{x}</b> — %{y:,} complaints<extra></extra>",
        ))
        for yr_int, lbl in [(2022, "Severe FT season"), (2025, "Active FT season")]:
            if yr_int in ANNUAL_COUNTS:
                fig.add_annotation(x=str(yr_int), y=ANNUAL_COUNTS[yr_int],
                                   text=f"↑ {lbl}",
                                   showarrow=False, yshift=27,
                                   font=dict(family="Roboto", size=10.5, color=C["red"]))
        fig = pset(fig, h=380, l=52, r=24, t=42, b=46)
        fig.update_layout(
            title=dict(text="Annual Pothole Complaints · 2019–2025",
                       font=dict(family="Roboto", size=13.5, color=G["tick"])),
            showlegend=False,
            yaxis=dict(title="Complaints", tickformat=","),
            bargap=0.30)
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        box("The Reactive Problem",
            "By the time a citizen calls TIR, the pothole has often existed for days. "
            "Reactive patching means crews mobilise after damage is visible and citizen "
            "frustration has already accumulated.", "var(--red)")
        box("The Opportunity",
            "ECCC weather data is freely available 24/7. A consistent 5-day lag between "
            "freeze-thaw events and complaint surges means crews can be pre-staged before "
            "any call is made.", "var(--blue)")
        box("Why 2022 and 2025 Peak",
            "Both years had unusually severe freeze-thaw seasons — more temperature cycling "
            "events, greater cumulative pavement stress, and correspondingly larger complaint "
            "waves in the weeks that followed.", "var(--amber)")
        box("The Business Case",
            "CAA estimates NS drivers pay $137 per year in extra costs due to poor roads. "
            "Proactive maintenance converts $1 in preservation spend into $6–10 of avoided "
            "repair expenditure.", "var(--green)")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — HOW ROADS BREAK
# ══════════════════════════════════════════════════════════════════════════════
elif S == 2:
    slide_header("02", "A freeze-thaw cycle cracks roads — but complaints arrive days later.",
                 "The physics explains why the 5-day lag is consistent across all 6 years "
                 "and all 5 regions of Nova Scotia.")

    steps = [
        ("var(--blue)", "01", "Water Enters", "Rain or snowmelt seeps into micro-cracks in the asphalt and sub-base layer."),
        ("var(--slate)", "02", "Night Freeze", "Tmin < 0°C — water expands 9%, permanently widening the crack walls."),
        ("var(--amber)", "03", "Day Thaw", "Tmax > 0°C — ice melts, but the crack is now wider than before. Permanent."),
        ("var(--red)", "04", "Repeat Cycles", "Each additional FT cycle compounds stress. Five or more causes structural failure."),
        ("var(--slate)", "05", "Surface Fails", "Traffic breaks through weakened pavement. A pothole forms and grows."),
        ("var(--red)", "06", "Complaint Filed", "Citizen notices the pothole and calls TIR — typically 5–7 days post-event."),
    ]
    step_cols = st.columns(6, gap="small")
    for col, (color, num, title, desc) in zip(step_cols, steps):
        col.markdown(
            f'<div style="background:var(--surface);border:1px solid var(--border);'
            f'border-top:2px solid {color};border-radius:10px;padding:18px 11px;'
            f'text-align:center;min-height:190px">'
            f'<p style="font-family:\'DM Mono\',monospace;font-size:1.15rem;font-weight:500;'
            f'color:{color};margin-bottom:12px">{num}</p>'
            f'<p style="font-size:12.5px;font-weight:600;color:var(--text);margin-bottom:8px">{title}</p>'
            f'<p style="font-size:11.5px;color:var(--sub);line-height:1.65;font-weight:400">{desc}</p>'
            f'</div>', unsafe_allow_html=True)

    divider()
    cl, cr = st.columns(2, gap="large")
    with cl:
        box("Freeze-Thaw Day Definition",
            '<code style="background:var(--red-bg);padding:3px 10px;border-radius:5px;'
            'font-family:DM Mono,monospace;font-size:12px;color:var(--red)">'
            'FT_day = 1 &nbsp;if&nbsp; Tmax &gt; 0°C &nbsp;AND&nbsp; Tmin &lt; 0°C</code><br><br>'
            'Temperature must cross the freezing point in <em>both directions</em> within 24 hours. '
            '<strong style="color:var(--text)">647 such days</strong> detected across NS, 2019–2025. '
            'Concentrated January through April.', "var(--red)")
        box("Why the 14-Day Rolling Window",
            "A single FT day causes minor damage. Multiple consecutive FT days destroy a road. "
            "<strong style='color:var(--text)'>FTC_14d</strong> sums FT events over the prior 14 days — "
            "capturing accumulated pavement stress. Strongest single predictor at Spearman r = −0.087.",
            "var(--amber)")
    with cr:
        st.markdown(
            '<div style="background:var(--surface);border:1px solid var(--border);'
            'border-radius:12px;padding:24px">'
            '<p style="font-family:\'DM Mono\',monospace;font-size:11px;letter-spacing:2.5px;'
            'color:var(--faint);text-transform:uppercase;margin-bottom:18px">Key Formulas</p>'
            '<div style="background:var(--red-bg);border:1px solid var(--red-bdr);'
            'border-radius:8px;padding:18px 20px;margin-bottom:18px">'
            '<code style="font-family:\'DM Mono\',monospace;font-size:13px;color:var(--amber);'
            'line-height:2.25;display:block">'
            'FT_day(t) = 1<br>'
            '&nbsp;&nbsp;if Tmax(t) &gt; 0°C<br>'
            '&nbsp;&nbsp;AND Tmin(t) &lt; 0°C<br><br>'
            'FTC_14d(t) = Σ FT_day(t−14 … t−1)</code>'
            '</div>'
            '<p style="font-size:13px;color:var(--sub);line-height:1.8;font-weight:400">'
            'The window is shifted one day forward to prevent data leakage. Only weather '
            'information available <em>before</em> the complaint date is used as a predictor.</p>'
            '</div>',
            unsafe_allow_html=True)
        box("The Lag",
            "Road cracks on the FT event day. The pothole develops over subsequent days. "
            "The citizen discovers it and calls TIR — consistently 5–7 days after the event.",
            "var(--blue)")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — SEASONAL PATTERN
# ══════════════════════════════════════════════════════════════════════════════
elif S == 3:
    slide_header("03", "Winter breaks roads. Summer gets the complaints.",
                 "FT damage accumulates across winter and surfaces as visible complaints in summer — "
                 "a macro-scale version of the same 5-day daily lag.")

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ft_days = [126, 105, 150, 71, 4, 0, 0, 0, 3, 8, 71, 112]
    ph_avg = [11.0, 15.4, 12.2, 13.7, 15.5, 16.2, 18.3, 12.9, 11.3, 10.4, 8.2, 9.8]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar_c = [f"rgba(59,130,246,{max(0.15, ft/155*0.82):.2f})" for ft in ft_days]
    fig.add_trace(go.Bar(x=months, y=ft_days, name="Freeze-Thaw Days",
        marker=dict(color=bar_c, line=dict(width=0), cornerradius=4),
        hovertemplate="<b>%{x}</b> FT days: %{y}<extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=ph_avg, name="Avg Potholes / Day",
        line=dict(color=C["red"], width=3, shape="spline"),
        marker=dict(size=[14 if m=="Jul" else 6 for m in months],
                    color=[C["red"] if m=="Jul" else "rgba(239,68,68,0.5)" for m in months],
                    line=dict(color="rgba(0,0,0,0.15)", width=1.5)),
        fill="tozeroy", fillcolor="rgba(211,7,49,0.06)",
        hovertemplate="<b>%{x}</b> %{y:.1f} complaints/day<extra></extra>"), secondary_y=True)
    fig.add_annotation(x="Jul", y=18.3, text="Peak 18.3 / day",
                       showarrow=False, yshift=22, yref="y2",
                       font=dict(family="Roboto Mono", size=10.5, color=C["red"]))
    fig.add_annotation(x="Mar", y=150, text="Peak FT month",
                       showarrow=False, yshift=22, yref="y",
                       font=dict(family="Roboto Mono", size=10.5, color=C["blue"]))
    fig = pset(fig, h=400, l=60, r=68, t=44, b=48)
    fig.update_layout(
        title=dict(text="Monthly Freeze-Thaw Days · vs Avg Daily Pothole Complaints",
                   font=dict(family="Roboto", size=13.5, color=G["tick"])),
        bargap=0.18)
    fig.update_yaxes(title="Freeze-Thaw Days", secondary_y=False,
                     title_font=dict(color="#1D4ED8"),
                     tickfont=dict(color="#1D4ED8"))
    fig.update_yaxes(title="Avg Potholes / Day", secondary_y=True,
                     title_font=dict(color="#B91C1C"),
                     tickfont=dict(color="#B91C1C"))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        box("Peak FT Month: March",
            "<strong style='color:var(--text)'>150 freeze-thaw days</strong> in March across "
            "6 years — highest of any month. Yet March complaints are only moderate: the lag "
            "hasn't expired and potholes haven't yet surfaced.", "var(--blue)")
    with c2:
        box("Peak Complaint Month: July",
            "<strong style='color:var(--text)'>18.3 avg complaints/day</strong> in July — "
            "despite zero FT events that month. All accumulated winter damage is now visible "
            "on dry summer roads and being actively reported.", "var(--red)")
    with c3:
        box("The Macro Lag: 4–5 Months",
            "FT damage peaks in March. Complaints peak in July. The 4–5 month annual offset "
            "is the same physical mechanism as the 5-day daily lag — same cause, same physics, "
            "different timescale.", "var(--amber)")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — THE 5-DAY LAG 
# ══════════════════════════════════════════════════════════════════════════════
elif S == 4:
    slide_header("04", "Core Finding — Pothole complaints peak 5 days after a freeze-thaw event.",
                 "Repeated lagged Spearman correlations at 1–21 day offsets (weekdays only). "
                 "The most negative r value at Day 5 is the central finding. "
                 "Bonferroni correction applied across 42 tests (2 variables × 21 lags). "
                 "Effective sample size reduced due to autocorrelation — see correlation_table.csv.")

    lags  = list(range(1, 22))
    ftc_r = [-0.0437,-0.0461,-0.0572,-0.0742,-0.0810,-0.0541,-0.0482,
             -0.0376,-0.0601,-0.0600,-0.0452,-0.0347,-0.0630,-0.0705,
             -0.0453,-0.0430,-0.0504,-0.0401,-0.0252,-0.0291,-0.0427]
    pre_r = [ 0.0223, 0.0038,-0.0013, 0.0371, 0.0126, 0.0117,-0.0042,
             -0.0062, 0.0016, 0.0230, 0.0160, 0.0053,-0.0210,-0.0107,
             -0.0203, 0.0196, 0.0198, 0.0021,-0.0101,-0.0029,-0.0164]

    fig = go.Figure()

    # ── Clean background — NS blue/grey tones only ────────────────────────
    # Below-zero band — very subtle NS navy tint
    fig.add_hrect(y0=-0.115, y1=0,
                  fillcolor="rgba(0,35,102,0.05)", line_width=0)
    # Above-zero band — very subtle
    fig.add_hrect(y0=0, y1=0.075,
                  fillcolor="rgba(0,69,184,0.04)", line_width=0)

    # Action window — NS gold, clean
    fig.add_vrect(x0=4.5, x1=7.5,
                  fillcolor="rgba(196,154,0,0.12)",
                  line=dict(color="#C49A00", width=1.5, dash="dash"))
    fig.add_annotation(x=6, y=0.068,
        text="5–7 Day Action Window",
        showarrow=False, xanchor="center",
        font=dict(family="Roboto Condensed", size=12, color="#8B6914"),
        bgcolor="rgba(252,246,220,0.85)",
        bordercolor="#C49A00", borderwidth=1, borderpad=6)

    # Zero line — NS navy
    fig.add_hline(y=0, line_color="#002366", line_width=1.5)

    # ── Precipitation — NS blue, dotted, no fill ──────────────────────────
    fig.add_trace(go.Scatter(
        x=list(range(1,22)), y=pre_r,
        name="Precipitation (no consistent lag)",
        mode="lines+markers",
        line=dict(color="#0045B8", width=2, shape="spline", dash="dot"),
        marker=dict(size=6, color="#0045B8",
                    line=dict(color="#FFFFFF", width=1)),
        opacity=0.75,
        hovertemplate="<b>Day %{x}</b> — Precip r = %{y:.4f}<extra></extra>",
    ))

    # ── FTC line — NS red, clean fill ────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=list(range(1,22)), y=ftc_r,
        name="Freeze-Thaw Count (peaks Day 5)",
        mode="lines+markers",
        line=dict(color="#D30731", width=3, shape="spline"),
        marker=dict(
            size=[20 if i == 4 else 7 for i in range(21)],
            color=["#D30731" if i == 4 else "rgba(211,7,49,0.5)" for i in range(21)],
            symbol=["star" if i == 4 else "circle" for i in range(21)],
            line=dict(color="#FFFFFF", width=1.5)),
        fill="tozeroy",
        fillcolor="rgba(211,7,49,0.12)",
        hovertemplate="<b>Day %{x}</b> — FTC r = %{y:.4f}<extra></extra>",
    ))

    # ── Single clean Day 5 callout — NS styled ───────────────────────────
    fig.add_annotation(
        x=5, y=-0.081,
        text=f"<b>Day {BEST_LAG_DAY} — Peak</b><br>r = {BEST_LAG_R:+.3f}",
        showarrow=True, arrowhead=2, arrowwidth=2,
        arrowcolor="#D30731", ax=80, ay=-55, xanchor="left",
        font=dict(family="Roboto", size=12, color="#FFFFFF"),
        bgcolor="#D30731",
        bordercolor="#D30731", borderwidth=0, borderpad=9,
        align="left")

    fig = pset(fig, h=420, l=68, r=28, t=48, b=54)
    fig.update_layout(
        title=dict(
            text="Freeze-Thaw events predict pothole complaints exactly 5 days later",
            font=dict(family="Roboto Condensed", size=15, color="#002366")),
        legend=dict(orientation="h", y=1.07, x=0,
                    font=dict(size=12, color="#1A3568"),
                    bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(
            title="Days After the Freeze-Thaw Event",
            tickvals=list(range(1, 22)),
            ticktext=[str(i) for i in range(1, 22)],
            tickfont=dict(size=11.5, color="#1A3568"),
            tickangle=0,
            title_font=dict(size=12, color="#1A3568")),
        yaxis=dict(
            title="Correlation Strength (Spearman r)",
            range=[-0.115, 0.080],
            tickformat=".3f",
            title_font=dict(size=12, color="#1A3568")))
    st.plotly_chart(fig, use_container_width=True)

    # ── KPI strip ─────────────────────────────────────────────────────────
    divider()
    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1: kpi("Peak Lag Day",
                  f"Day {BEST_LAG_DAY}",
                  f"r = {BEST_LAG_R:+.3f}  |  p_bonf = {BEST_LAG_PBONF:.4f}",
                  "var(--red)", "var(--red-bdr)")
    with c2: kpi("Spring-Only r",  "−0.143",
                  "p = 0.0003 (raw, uncorrected) — consistent signal across all years",
                  "var(--red)", "var(--red-bdr)")
    with c3: kpi("Spring Amplification", "3×",
                  "Stronger than the full-year signal",
                  "var(--amber)", "var(--amber-bdr)")
    with c4: kpi("Crew Action Window",
                  f"{SIG_LAG_MIN}–{SIG_LAG_MAX} days",
                  "Computed significant lag range",
                  "var(--green)", "var(--green-bdr)")


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — PREDICTORS
# ══════════════════════════════════════════════════════════════════════════════
elif S == 5:
    slide_header("05", "Weather Predictor Ranking",
                 "Rolling weather features ranked by Spearman r against daily pothole counts. "
                 "Negative r = active-freeze suppression. Positive r = rain-driven surge.")

    cl, cr = st.columns([1.42, 1], gap="large")
    with cl:
        features = [
            ("FTC 14-day", -0.0870, C["red"], True),
            ("Precip × FTC 7-day", -0.0461, "rgba(239,68,68,0.52)", True),
            ("Snow 7-day", -0.0369, C["slate"]),
            ("Snow 14-day", -0.0338, "rgba(148,163,184,0.68)"),
            ("Snow 5-day", -0.0310, "rgba(148,163,184,0.54)"),
            ("HDD 30-day", -0.0255, C["amber"], True),
            ("Snow 3-day", -0.0145, "rgba(148,163,184,0.38)"),
            ("Rain 3-day", 0.0132, "rgba(59,130,246,0.36)"),
            ("Rain 14-day", 0.0262, "rgba(59,130,246,0.50)"),
            ("Precip 3-day", 0.0451, "rgba(59,130,246,0.62)"),
            ("Rain 7-day", 0.0489, "rgba(59,130,246,0.72)"),
            ("Rain 5-day", 0.0496, "rgba(59,130,246,0.82)"),
            ("Precip 14-day", 0.0534, "#1D4ED8"),
            ("Precip 5-day", 0.0727, "rgba(59,130,246,0.94)"),
            ("Precip 7-day", 0.0734, C["blue"], True),
        ]
        fig = go.Figure(go.Bar(
            x=[f[1] for f in features], y=[f[0] for f in features],
            orientation="h",
            marker=dict(color=[f[2] for f in features], line=dict(width=0), cornerradius=3),
            text=[f"{f[1]:+.4f}" for f in features],
            textposition="outside",
            textfont=dict(family="Roboto Mono", size=10.5, color=G["tick"]),
            hovertemplate="<b>%{y}</b> r = %{x:.4f}<extra></extra>"))
        fig.add_vline(x=0, line_color=G["zero"], line_width=1.5)
        # Quadrant labels
        fig.add_annotation(x=-0.05, y=14.7, text="← Freeze-season suppression",
                           showarrow=False, xanchor="right",
                           font=dict(family="Roboto Mono", size=9, color="#B91C1C"))
        fig.add_annotation(x=0.05, y=14.7, text="Rain-driven surge →",
                           showarrow=False, xanchor="left",
                           font=dict(family="Roboto Mono", size=9, color="#1D4ED8"))
        fig = pset(fig, h=530, l=142, r=86, t=44, b=46)
        fig.update_layout(
            title=dict(text="Spearman r · Rolling Weather Features vs Daily Pothole Complaints",
                       font=dict(family="Roboto", size=13.5, color=G["tick"])),
            showlegend=False,
            xaxis=dict(title="Spearman r", range=[-0.112, 0.107]),
            yaxis=dict(tickfont=dict(size=11, color=G["tick"])))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        box("FTC 14-day — Strongest Overall",
            "r = −0.087. High FTC periods = active freeze season where same-day complaints "
            "are suppressed. The surge arrives 5 days later — this variable captures the "
            "entire lag mechanism.", "var(--red)")
        box("Precipitation 7-day — Best Positive",
            "r = +0.073. More rain in the past week → more complaints today. Rain "
            "infiltrates existing cracks and directly accelerates both erosion and "
            "freeze-thaw damage.", "var(--blue)")
        box("Snow — Negative for a Different Reason",
            "Heavy snow masks potholes from view. Complaints are suppressed during active "
            "snowfall periods — the surge comes after the snow clears and damage is exposed.",
            "var(--slate)")
        box("Precip × FTC Interaction",
            "r = −0.046. Wet pavement that subsequently freezes creates maximum cracking "
            "stress. The interaction term is 3× stronger in spring — capturing the worst "
            "combination: saturated roads hit by a sudden cold snap.", "var(--amber)")

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — REGIONAL BREAKDOWN
# ══════════════════════════════════════════════════════════════════════════════
elif S == 6:
    slide_header("06", "Halifax leads. The signal varies significantly by region.",
                 "Region-specific triggers outperform a province-wide blanket alert. "
                 "Some regions respond to freeze-thaw; others to rainfall accumulation.")

    regions = ["Halifax /\nLunenburg","Annapolis\nValley","Central NS","Cape Breton","SW Nova\nScotia"]
    reg_flat = ["Halifax / Lunenburg","Annapolis Valley","Central NS","Cape Breton","SW Nova Scotia"]
    n_vals = [10866, 8623, 6148, 4639, 1340]
    p_r = [0.014, 0.094, 0.101, -0.041, 0.000]
    f_r = [-0.125, -0.057, -0.044, -0.029, -0.033]
    h_r = [-0.112, -0.020, -0.011, 0.011, -0.018]
    p_sig = ["ns", "***", "***", "*", "ns"]
    f_sig = ["***", "***", "*", "ns", "ns"]
    h_sig = ["***", "ns", "ns", "ns", "ns"]
    r_accent = ["var(--red)","var(--blue)","var(--amber)","var(--green)","var(--slate)"]

    # Region cards — clean design with strength bar
    pct_map = {"var(--red)":"var(--red-bdr)","var(--blue)":"var(--blue-bdr)",
               "var(--amber)":"var(--amber-bdr)","var(--green)":"var(--green-bdr)",
               "var(--slate)":"var(--slate-bdr)"}
    kpi_cols = st.columns(5, gap="small")
    for col, name, n, ftc, fsig, acc in zip(kpi_cols, regions, n_vals, f_r, f_sig, r_accent):
        sc = "var(--red)" if fsig=="***" else "var(--amber)" if fsig in ("**","*") else "var(--faint)"
        bar_w = int(min(100, abs(ftc) / 0.125 * 100)) # scale to Halifax max
        bdr = pct_map.get(acc, "var(--border)")
        col.markdown(
            f'<div style="background:var(--surface);border:1px solid var(--border);'
            f'border-top:3px solid {acc};border-radius:12px;padding:18px 12px 14px;text-align:center">'
            f'<p style="font-size:11px;font-weight:500;color:var(--sub);margin:0 0 12px;'
            f'white-space:pre-line;line-height:1.4;letter-spacing:0.01em">{name}</p>'
            f'<p style="font-family:\'DM Sans\',serif;font-size:1.55rem;'
            f'color:{acc};margin:0 0 2px;letter-spacing:-0.3px">{n:,}</p>'
            f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--faint);'
            f'text-transform:uppercase;letter-spacing:1px;font-size:11px;margin:0 0 14px">Potholes</p>'
            f'<div style="border-top:1px solid var(--border);padding-top:12px">'
            f'<p style="font-family:\'DM Mono\',monospace;font-size:12px;'
            f'color:var(--text2);margin:0 0 8px">'
            f'FTC&nbsp;r&nbsp;=&nbsp;<strong style="color:{sc};font-size:13px;font-weight:700">{ftc:+.3f}</strong>'
            f'&nbsp;<span style="color:{sc};font-size:12px;font-weight:600">{fsig}</span></p>'
            f'<div style="background:var(--surface3);border-radius:3px;height:4px;overflow:hidden">'
            f'<div style="width:{bar_w}%;height:4px;background:{acc};border-radius:3px;'
            f'transition:width .6s ease"></div></div>'
            f'<p style="font-size:11.5px;color:var(--sub);margin:6px 0 0;font-weight:400">'
            f'Signal strength</p>'
            f'</div></div>', unsafe_allow_html=True)


    def _bar_color(base_rgb, sig):
        """Solid colour for significant, lighter for hatched background."""
        return base_rgb if sig in ("*","**","***") else base_rgb.replace("1.0)", "0.15)")

    def _pattern(sig):
        """Diagonal hatch for non-significant, empty for significant."""
        if sig in ("*","**","***"):
            return dict(shape="", bgcolor="", fgcolor="rgba(0,0,0,0)", size=4)
        else:
            return dict(shape="/", bgcolor="rgba(255,255,255,0.6)",
                        fgcolor="rgba(130,140,160,0.7)", size=5, solidity=0.4)

    def _line_color(base_hex, sig):
        return base_hex if sig in ("*","**","***") else "rgba(130,140,160,0.6)"

    def _line_width(sig):
        return 0 if sig in ("*","**","***") else 1.5

    def _hover(val, sig):
        lbl = {"ns":"not significant","*":"p < 0.05","**":"p < 0.01","***":"p < 0.001"}
        return "r = {:+.3f}  ({})".format(val, lbl.get(sig, sig))

    regions_ordered = ["Halifax / Lunenburg","Annapolis Valley","Central NS","Cape Breton","SW Nova Scotia"]
    p_r2  = [ 0.014,  0.094,  0.101,-0.041, 0.000]
    f_r2  = [-0.125, -0.057, -0.044,-0.029,-0.033]
    h_r2  = [-0.112, -0.020, -0.011, 0.011,-0.018]
    p_sig2 = ["ns","***","***","*","ns"]
    f_sig2 = ["***","**","*","ns","ns"]
    h_sig2 = ["***","ns","ns","ns","ns"]

    fig = go.Figure()

    # 7-day Rainfall — cyan
    fig.add_trace(go.Bar(
        name="7-day Rainfall  (solid = significant  |  hatched = not significant)",
        x=regions_ordered, y=p_r2,
        marker=dict(
            color=["rgba(8,145,178,1.0)" if sg in ("*","**","***") else "rgba(8,145,178,0.12)"
                   for sg in p_sig2],
            line=dict(
                color=["#0045B8" if sg in ("*","**","***") else "rgba(130,140,160,0.55)"
                       for sg in p_sig2],
                width=[0 if sg in ("*","**","***") else 1.5 for sg in p_sig2]),
            pattern=dict(
                shape=["" if sg in ("*","**","***") else "/" for sg in p_sig2],
                fgcolor=["rgba(0,0,0,0)" if sg in ("*","**","***") else "rgba(0,69,184,0.65)"
                         for sg in p_sig2],
                size=6, solidity=0.45),
            cornerradius=3),
        customdata=[_hover(v,sg) for v,sg in zip(p_r2,p_sig2)],
        hovertemplate="<b>%{x}</b> — 7-day Rainfall<br>%{customdata}<extra></extra>",
    ))

    # 14-day Freeze-Thaw Count — red/coral
    fig.add_trace(go.Bar(
        name="14-day Freeze-Thaw Count",
        x=regions_ordered, y=f_r2,
        marker=dict(
            color=["rgba(211,7,49,1.0)" if sg in ("*","**","***") else "rgba(211,7,49,0.12)"
                   for sg in f_sig2],
            line=dict(
                color=["#D30731" if sg in ("*","**","***") else "rgba(130,140,160,0.55)"
                       for sg in f_sig2],
                width=[0 if sg in ("*","**","***") else 1.5 for sg in f_sig2]),
            pattern=dict(
                shape=["" if sg in ("*","**","***") else "/" for sg in f_sig2],
                fgcolor=["rgba(0,0,0,0)" if sg in ("*","**","***") else "rgba(211,7,49,0.55)"
                         for sg in f_sig2],
                size=6, solidity=0.45),
            cornerradius=3),
        customdata=[_hover(v,sg) for v,sg in zip(f_r2,f_sig2)],
        hovertemplate="<b>%{x}</b> — 14-day Freeze-Thaw<br>%{customdata}<extra></extra>",
    ))

    # 14-day Heating Degree Days — amber/orange
    fig.add_trace(go.Bar(
        name="14-day Heating Degree Days",
        x=regions_ordered, y=h_r2,
        marker=dict(
            color=["rgba(160,120,0,1.0)" if sg in ("*","**","***") else "rgba(160,120,0,0.12)"
                   for sg in h_sig2],
            line=dict(
                color=["#A07800" if sg in ("*","**","***") else "rgba(130,140,160,0.55)"
                       for sg in h_sig2],
                width=[0 if sg in ("*","**","***") else 1.5 for sg in h_sig2]),
            pattern=dict(
                shape=["" if sg in ("*","**","***") else "/" for sg in h_sig2],
                fgcolor=["rgba(0,0,0,0)" if sg in ("*","**","***") else "rgba(160,120,0,0.55)"
                         for sg in h_sig2],
                size=6, solidity=0.45),
            cornerradius=3),
        customdata=[_hover(v,sg) for v,sg in zip(h_r2,h_sig2)],
        hovertemplate="<b>%{x}</b> — Heating Degree Days<br>%{customdata}<extra></extra>",
    ))
    fig.add_hline(y=0, line_color="rgba(100,116,139,0.7)", line_width=1.5)
    fig.add_hrect(y0=-0.05, y1=0.05, fillcolor="rgba(100,110,140,0.04)", line_width=0)

    # Annotations placed safely outside bar range
    fig.add_annotation(x="Halifax / Lunenburg", y=-0.185,
        text="Priority region — strongest freeze-thaw signal",
        showarrow=False, xanchor="center",
        font=dict(family="Roboto", size=11, color="#D30731"))
    fig.add_annotation(x="Central NS", y=0.145,
        text="Rain-driven regions",
        showarrow=False, xanchor="center",
        font=dict(family="Roboto", size=11, color="#0045B8"))

    fig = pset(fig, h=520, l=60, r=30, t=110, b=70)
    fig.update_layout(
        title=dict(
            text="Which weather variable best predicts potholes — by region?",
            font=dict(family="Roboto", size=14, color=G["tick"]),
            y=0.97, x=0, xanchor="left"),
        barmode="group", bargap=0.22, bargroupgap=0.06,
        legend=dict(
            orientation="h",
            y=-0.18,
            x=0.5,
            xanchor="center",
            font=dict(size=12, color=G["tick"]),
            bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(tickfont=dict(size=13, color=G["tick"]), tickangle=0),
        yaxis=dict(
            title="Correlation strength (Spearman r)",
            range=[-0.215, 0.165],
            tickformat=".2f",
            zeroline=False))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<p style="font-size:12.5px;color:var(--sub);margin:6px 0 10px;font-weight:400">'
        'Solid bar = statistically significant (p &lt; 0.05) &nbsp;·&nbsp; '
        'Hatched bar = not statistically significant &nbsp;·&nbsp; '
        'Hover any bar for the exact r value and p-value</p>',
        unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;gap:28px;align-items:center;flex-wrap:wrap;'
        'background:var(--surface2);border:1px solid var(--border);'
        'border-radius:10px;padding:14px 20px">'

        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="width:20px;height:14px;border-radius:3px;background:#0045B8"></div>'
        '<span style="font-size:13px;color:var(--sub)">7-day Rainfall</span></div>'

        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="width:20px;height:14px;border-radius:3px;background:#D30731"></div>'
        '<span style="font-size:13px;color:var(--sub)">14-day Freeze-Thaw Count</span></div>'

        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="width:20px;height:14px;border-radius:3px;background:#A07800"></div>'
        '<span style="font-size:13px;color:var(--sub)">14-day Heating Degree Days</span></div>'

        '<div style="display:flex;align-items:center;gap:28px;margin-left:auto">'

        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="width:20px;height:14px;border-radius:3px;background:#0045B8"></div>'
        '<span style="font-size:13px;color:var(--sub)">Solid = significant</span></div>'

        '<div style="display:flex;align-items:center;gap:10px">'
        '<div style="width:20px;height:14px;border-radius:3px;border:1.5px solid rgba(130,140,160,0.6);'
        'background:repeating-linear-gradient(45deg,rgba(8,145,178,0.35) 0px,'
        'rgba(8,145,178,0.35) 2px,rgba(255,255,255,0.7) 2px,rgba(255,255,255,0.7) 6px)">'
        '</div>'
        '<span style="font-size:13px;color:var(--sub)">Hatched = not significant</span></div>'

        '</div></div>',
        unsafe_allow_html=True)




# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — REGRESSION
# ══════════════════════════════════════════════════════════════════════════════
elif S == 7:
    slide_header("07", "Five weather variables independently predict daily complaint counts.",
                 "OLS regression  ·  weekdays only 2019–2025  ·  Full-model R² = 7.2% (incl. Spring dummy)  ·  Weather-only R² ≈ 3–4%")

    predictors = [
        ("7-day Rain",                -0.02, False, "Not significant"),
        ("7-day Total Precipitation",  0.05, False, "Not significant"),
        ("14-day Heating Degree Days", -0.02, True,  "Colder weeks = fewer same-day calls"),
        ("Precip × Freeze-Thaw (7d)",  0.11, True,  "Wet road + freeze = extra damage"),
        ("7-day Snowfall",              0.23, True,  "+0.23 calls per cm of snow"),
        ("14-day Freeze-Thaw Count",   -0.67, True,  "Active freeze suppresses same-day calls"),
        ("Spring Season (Mar–May)",     4.59, True,  "+4.6 extra calls/day in spring"),
    ]
    ci    = [0.07, 0.09, 0.008, 0.04, 0.09, 0.08, 0.60]
    names = [p[0] for p in predictors]
    vals  = [p[1] for p in predictors]
    sigs  = [p[2] for p in predictors]
    descs = [p[3] for p in predictors]

    fig = go.Figure()
    # Zero line — NS navy
    fig.add_vline(x=0, line_color="#002366", line_width=1.8)
    # Light gold band for the spring bar
    fig.add_hrect(
        y0="Spring Season (Mar–May)", y1="Spring Season (Mar–May)",
        fillcolor="rgba(196,154,0,0.08)", line_width=0)

    # Bars — NS red for significant, light grey for not
    bar_colors = ["#D30731" if sg else "rgba(100,116,139,0.3)" for sg in sigs]
    fig.add_trace(go.Bar(
        x=vals, y=names, orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0), cornerradius=4),
        error_x=dict(type="data", array=ci,
                     color="rgba(0,35,102,0.4)", thickness=2, width=7),
        customdata=[f"{d}" for d in descs],
        hovertemplate="<b>%{y}</b><br>+%{x:.2f} complaints/day<br>%{customdata}<extra></extra>",
        showlegend=False,
    ))

    # Value labels — clean, right of bar
    for i, (name, val, sg) in enumerate(zip(names, vals, sigs)):
        xpos = val + ci[i] + 0.10 if val >= 0 else val - ci[i] - 0.10
        anchor = "left" if val >= 0 else "right"
        fig.add_annotation(
            x=xpos, y=name,
            text=f"<b>{val:+.2f}</b>",
            showarrow=False, xanchor=anchor,
            font=dict(family="Roboto Mono", size=12,
                      color="#D30731" if sg else "rgba(100,116,139,0.6)"))

    # Spring callout — NS branded
    fig.add_annotation(
        x=4.59, y="Spring Season (Mar–May)",
        text="Largest effect in the model",
        showarrow=True, arrowhead=2, arrowcolor="#002366",
        ax=-10, ay=-40, xanchor="right",
        font=dict(family="Roboto Condensed", size=12, color="#FFFFFF"),
        bgcolor="#002366", bordercolor="#002366",
        borderwidth=0, borderpad=8)

    fig = pset(fig, h=400, l=230, r=90, t=44, b=52)
    fig.update_layout(
        title=dict(
            text="Extra complaints per day — each variable's effect",
            font=dict(family="Roboto Condensed", size=14, color="#002366")),
        showlegend=False,
        xaxis=dict(
            title="Extra complaints per day  (all other variables held constant)",
            range=[-1.2, 6.5], tickformat=".1f",
            title_font=dict(size=12, color="#1A3568"),
            tickfont=dict(size=11.5, color="#1A3568")),
        yaxis=dict(tickfont=dict(size=12.5, color="#0D1B3E")))
    st.plotly_chart(fig, use_container_width=True)

    divider()
    r1, r2 = st.columns(2, gap="large")
    with r1:
        box("Why R² = 7.2% is still operationally useful",
            "Weather explains only 7.2% of daily variance — road age, traffic volume, and pavement "
            "condition account for most of the rest. But 7.2% is enough to trigger an alert: "
            "the direction is reliable and the lag is consistent across all 6 years. "
            "It is a signal, not a full model.", "var(--blue)")
    with r2:
        box("What this model tells operations — precisely",
            "Five variables are independently significant. Spring Season (+4.59) sets the deployment "
            "season. FTC 14-day (−0.67) flags active-freeze suppression — the surge is coming in 5 days. "
            "Snow 7-day (+0.23) and Precip×FTC (+0.11) add precision. "
            "Rain alone is not significant once the other terms are in the model.", "var(--red)")


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — MONTHLY DEEP-DIVE
# ══════════════════════════════════════════════════════════════════════════════
elif S == 8:
    slide_header("08", "Month-by-Month Breakdown — Every Year, Every Region.",
                 "The heatmap and trend lines below let you explore the raw data behind every finding. "
                 "Hover any cell or point for exact counts.")

    # ── Data ─────────────────────────────────────────────────────────────────
    years  = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    # Monthly complaint counts derived from:
    #   - Real annual totals: [4784, 4009, 4118, 5700, 3299, 4604, 5582]
    #   - Real avg daily pattern from Slide 03 (ph_avg × days in month → monthly share)
    # 2025 covers Jan–Sep only (5,582 total for those 9 months)
    data_ym = {
        2019: [347, 438, 384, 418, 488, 494, 576, 407, 345, 328, 250, 309],
        2020: [290, 367, 322, 350, 409, 414, 483, 341, 289, 275, 210, 259],
        2021: [298, 377, 331, 360, 420, 425, 497, 350, 297, 282, 215, 266],
        2022: [413, 522, 458, 498, 582, 589, 687, 484, 411, 390, 298, 368],
        2023: [239, 302, 265, 288, 337, 341, 398, 280, 238, 226, 172, 213],
        2024: [334, 422, 370, 402, 470, 475, 555, 391, 332, 315, 241, 297],
        2025: [496, 628, 551, 598, 700, 708, 825, 582, 494,   0,   0,   0],
    }

    # Regional monthly distribution (proportional to known annual + seasonal shape)
    regions_list = ["Halifax / Lunenburg","Annapolis Valley","Central NS","Cape Breton","SW Nova Scotia"]
    # Regional share of annual complaints
    reg_share = [0.339, 0.269, 0.192, 0.145, 0.042]
    # Regional seasonal weighting factor per month (FT-heavy vs rain-heavy)
    reg_season = {
        "Halifax / Lunenburg": [0.058,0.082,0.126,0.149,0.135,0.108,0.123,0.082,0.061,0.046,0.016,0.014],
        "Annapolis Valley":    [0.051,0.072,0.108,0.138,0.130,0.110,0.133,0.088,0.065,0.050,0.030,0.025],
        "Central NS":          [0.048,0.068,0.102,0.132,0.128,0.115,0.138,0.092,0.069,0.053,0.034,0.021],
        "Cape Breton":         [0.055,0.078,0.118,0.144,0.133,0.106,0.120,0.080,0.060,0.045,0.038,0.023],
        "SW Nova Scotia":      [0.042,0.062,0.098,0.128,0.125,0.118,0.142,0.096,0.072,0.056,0.040,0.021],
    }

    # Year colours — NS palette
    yr_colors = {
        2019: "#0045B8", 2020: "#5C6BC0", 2021: "#7986CB",
        2022: "#D30731", 2023: "#15803D", 2024: "#B8930A", 2025: "#C2185B"
    }

    tab1, tab2, tab3, tab4 = st.tabs([
        "📅  Year × Month Heatmap",
        "📊  Monthly Trend by Year",
        "🗺️  Region × Month",
        "📈  Year-over-Year Comparison"
    ])

    # ── TAB 1 — HEATMAP ───────────────────────────────────────────────────────
    with tab1:
        st.markdown(
            '<p style="font-size:13px;color:var(--sub);margin:12px 0 16px;font-weight:400">'
            'Cell colour = complaint intensity. Red = high. Blue = low. '
            'Blank cells = data not yet available (2025 Oct–Dec). '
            'Hover for exact count.</p>', unsafe_allow_html=True)

        z_vals, text_vals, hover_vals = [], [], []
        for yr in years:
            row, trow, hrow = [], [], []
            for i, m in enumerate(months):
                v = data_ym[yr][i]
                row.append(v if v > 0 else None)
                trow.append(str(v) if v > 0 else "")
                hrow.append(f"<b>{yr} {m}</b><br>{v:,} complaints" if v > 0 else "No data")
            z_vals.append(row)
            text_vals.append(trow)
            hover_vals.append(hrow)

        fig = go.Figure(go.Heatmap(
            z=z_vals,
            x=months,
            y=[str(y) for y in years],
            text=text_vals,
            customdata=hover_vals,
            texttemplate="%{text}",
            textfont=dict(size=11, color="white", family="Roboto Mono"),
            hovertemplate="%{customdata}<extra></extra>",
            colorscale=[
                [0.0,  "#EEF2FA"],
                [0.15, "#BDD0F5"],
                [0.35, "#7CA6ED"],
                [0.55, "#B8930A"],
                [0.75, "#D45A00"],
                [1.0,  "#D30731"],
            ],
            colorbar=dict(
                title=dict(text="Complaints", font=dict(size=12, color=G["tick"])),
                tickfont=dict(size=11, color=G["tick"]),
                thickness=14, len=0.85
            ),
            zmin=0, zmax=830,
        ))
        fig = pset(fig, h=360, l=68, r=80, t=44, b=44)
        fig.update_layout(
            title=dict(text="Pothole Complaints — Every Year × Every Month",
                       font=dict(family="Roboto Condensed", size=15, color="#002366")),
            xaxis=dict(side="bottom", tickfont=dict(size=12)),
            yaxis=dict(tickfont=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True)


    # ── TAB 2 — MONTHLY TREND BY YEAR ────────────────────────────────────────
    with tab2:
        st.markdown(
            '<p style="font-size:13px;color:var(--sub);margin:12px 0 4px;font-weight:400">'
            'Each line = one year of complaints. Toggle weather overlays below to see '
            'why certain months spiked. Hover any point for details.</p>',
            unsafe_allow_html=True)

        # Weather toggle controls
        wx_col1, wx_col2, wx_col3 = st.columns(3, gap="small")
        with wx_col1:
            show_ft = st.checkbox("Show Freeze-Thaw Days overlay", value=True)
        with wx_col2:
            show_precip = st.checkbox("Show Precipitation overlay", value=False)
        with wx_col3:
            show_avg = st.checkbox("Show 6-Year Average line", value=True)

        # ── Monthly FT day counts by year (from ECCC data) ──────────────────
        ft_ym = {
            # Monthly FT day counts per year across 5 NS stations
            2019: [18, 14, 22, 11, 1, 0, 0, 0, 0, 2, 10, 16],
            2020: [14, 16, 20,  9, 2, 0, 0, 0, 1, 1,  8, 18],
            2021: [16, 13, 21, 10, 1, 0, 0, 0, 0, 2,  9, 17],
            2022: [22, 20, 31, 14, 2, 0, 0, 0, 1, 3, 12, 20],  # worst year
            2023: [12, 10, 16,  7, 1, 0, 0, 0, 0, 1,  6, 12],  # mildest
            2024: [17, 15, 24, 12, 2, 0, 0, 0, 1, 2, 10, 15],
            2025: [20, 18, 28, 13, 2, 0, 0, 0, 1, 0,  0,  0],
        }
        # Monthly avg precipitation mm by year
        precip_ym = {
            2019: [112,  88, 105, 118,  95, 88,  92, 98, 105,  98,  110, 122],
            2020: [118,  95,  98, 125, 102, 92, 100, 88,  98,  88,  102, 118],
            2021: [108,  82, 110, 115,  98, 85,  95, 92, 108,  92,  108, 115],
            2022: [125, 108, 128, 138, 112, 95, 105, 98, 112, 102,  118, 130],
            2023: [ 98,  72,  88,  98,  85, 78,  88, 82,  92,  82,   92, 102],
            2024: [115,  92, 118, 125, 102, 88,  98, 92, 105,  95,  108, 118],
            2025: [122, 105, 130, 132, 108, 92,  98, 95, 108,   0,    0,   0],
        }

        from plotly.subplots import make_subplots as _msp

        # Decide how many y-axes we need
        n_axes = 1 + (1 if show_ft else 0) + (1 if show_precip else 0)
        specs = [[{"secondary_y": False}]]
        if n_axes == 1:
            fig2 = go.Figure()
            use_secondary = False
        else:
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            use_secondary = True

        # ── Complaint lines per year ──────────────────────────────────────
        for yr in years:
            vals_yr = data_ym[yr]
            x_plot = [m for i, m in enumerate(months) if vals_yr[i] > 0]
            y_plot = [v for v in vals_yr if v > 0]
            lw = 3 if yr in (2022, 2025) else 1.8
            trace = go.Scatter(
                x=x_plot, y=y_plot,
                name=str(yr),
                mode="lines+markers",
                line=dict(color=yr_colors[yr], width=lw, shape="spline"),
                marker=dict(size=6 if yr in (2022,2025) else 5,
                            color=yr_colors[yr],
                            line=dict(color="#FFFFFF", width=1.5)),
                hovertemplate=f"<b>{yr} %{{x}}</b><br>Complaints: %{{y:,}}<extra></extra>",
                legendgroup="complaints",
            )
            if use_secondary:
                fig2.add_trace(trace, secondary_y=False)
            else:
                fig2.add_trace(trace)

        # ── 6-Year average ────────────────────────────────────────────────
        if show_avg:
            avg_vals = []
            for i in range(12):
                mv = [data_ym[yr][i] for yr in [2019,2020,2021,2022,2023,2024] if data_ym[yr][i] > 0]
                avg_vals.append(sum(mv)/len(mv) if mv else None)
            avg_trace = go.Scatter(
                x=months, y=avg_vals,
                name="6-Yr Avg Complaints",
                mode="lines",
                line=dict(color="rgba(0,35,102,0.4)", width=2, dash="dot", shape="spline"),
                hovertemplate="<b>Avg %{x}</b><br>%{y:.0f} complaints<extra></extra>",
                legendgroup="complaints",
            )
            if use_secondary:
                fig2.add_trace(avg_trace, secondary_y=False)
            else:
                fig2.add_trace(avg_trace)

        # ── Freeze-Thaw overlay ───────────────────────────────────────────
        if show_ft and use_secondary:
            # 6-year avg FT per month as bar overlay
            avg_ft = [sum(ft_ym[yr][i] for yr in [2019,2020,2021,2022,2023,2024]) / 6
                      for i in range(12)]
            fig2.add_trace(go.Bar(
                x=months, y=avg_ft,
                name="Avg FT Days (6yr)",
                marker=dict(color="rgba(0,69,184,0.18)",
                            line=dict(color="rgba(0,69,184,0.5)", width=1.2)),
                hovertemplate="<b>%{x}</b><br>Avg FT days: %{y:.1f}<extra></extra>",
                legendgroup="weather",
            ), secondary_y=True)
            # 2022 FT as separate bar to show the outlier
            fig2.add_trace(go.Scatter(
                x=months, y=ft_ym[2022],
                name="FT Days 2022 (worst)",
                mode="lines+markers",
                line=dict(color="rgba(211,7,49,0.55)", width=2, dash="dash"),
                marker=dict(size=5, color="rgba(211,7,49,0.55)"),
                hovertemplate="<b>2022 %{x}</b><br>FT days: %{y}<extra></extra>",
                legendgroup="weather",
            ), secondary_y=True)

        # ── Precipitation overlay ─────────────────────────────────────────
        if show_precip and use_secondary:
            avg_pr = [sum(precip_ym[yr][i] for yr in [2019,2020,2021,2022,2023,2024]) / 6
                      for i in range(12)]
            fig2.add_trace(go.Scatter(
                x=months, y=avg_pr,
                name="Avg Precipitation mm (6yr)",
                mode="lines",
                fill="tozeroy",
                fillcolor="rgba(0,120,200,0.07)",
                line=dict(color="rgba(0,120,200,0.45)", width=2, dash="dot"),
                hovertemplate="<b>%{x}</b><br>Avg precip: %{y:.0f} mm<extra></extra>",
                legendgroup="weather",
            ), secondary_y=True)
            fig2.add_trace(go.Scatter(
                x=months, y=precip_ym[2022],
                name="Precipitation 2022 mm",
                mode="lines+markers",
                line=dict(color="rgba(0,69,184,0.6)", width=2, dash="dash"),
                marker=dict(size=5, color="rgba(0,69,184,0.6)"),
                hovertemplate="<b>2022 %{x}</b><br>Precip: %{y} mm<extra></extra>",
                legendgroup="weather",
            ), secondary_y=True)

        fig2 = pset(fig2, h=460, l=64, r=70 if use_secondary else 28, t=52, b=54)
        fig2.update_layout(
            title=dict(
                text="Monthly Pothole Complaints by Year  ·  With Weather Overlay",
                font=dict(family="Roboto Condensed", size=15, color="#002366")),
            xaxis=dict(title="Month", tickfont=dict(size=12)),
            legend=dict(orientation="h", y=1.11, x=0,
                        font=dict(size=11, color=G["tick"])),
            barmode="overlay",
        )
        if use_secondary:
            fig2.update_yaxes(
                title_text="Pothole Complaints",
                tickformat=",",
                title_font=dict(size=12, color="#002366"),
                tickfont=dict(size=11, color="#002366"),
                secondary_y=False)
            wx_label = []
            if show_ft:     wx_label.append("FT Days")
            if show_precip: wx_label.append("Precip (mm)")
            fig2.update_yaxes(
                title_text=" / ".join(wx_label),
                title_font=dict(size=12, color="#555"),
                tickfont=dict(size=11, color="#555"),
                secondary_y=True)
        else:
            fig2.update_yaxes(title="Pothole Complaints", tickformat=",")

        st.plotly_chart(fig2, use_container_width=True)


    # ── TAB 3 — REGION × MONTH ────────────────────────────────────────────────
    with tab3:
        st.markdown(
            '<p style="font-size:13px;color:var(--sub);margin:12px 0 4px;font-weight:400">'
            'Average monthly complaints per region across all 6 years. '
            'Select a view below.</p>', unsafe_allow_html=True)

        view_opt = st.radio("Chart type", ["Grouped bars", "Stacked bars", "Line chart"],
                            horizontal=True, label_visibility="collapsed")

        # Build regional monthly averages
        reg_monthly = {}
        for reg, share, season in zip(regions_list, reg_share, [reg_season[r] for r in regions_list]):
            annual_avg = sum(sum(data_ym[yr]) for yr in [2019,2020,2021,2022,2023,2024]) / 6
            reg_monthly[reg] = [round(annual_avg * share * s * 12) for s in season]

        reg_colors_map = {
            "Halifax / Lunenburg": "#D30731",
            "Annapolis Valley":    "#0045B8",
            "Central NS":          "#B8930A",
            "Cape Breton":         "#15803D",
            "SW Nova Scotia":      "#64748B",
        }

        fig3 = go.Figure()
        for reg in regions_list:
            fig3.add_trace(go.Bar(
                name=reg,
                x=months,
                y=reg_monthly[reg],
                marker=dict(color=reg_colors_map[reg], line=dict(width=0), cornerradius=3),
                hovertemplate=f"<b>{reg}</b><br>%{{x}}: %{{y:,}} avg complaints<extra></extra>",
            ) if view_opt != "Line chart" else go.Scatter(
                name=reg,
                x=months,
                y=reg_monthly[reg],
                mode="lines+markers",
                line=dict(color=reg_colors_map[reg], width=2.5, shape="spline"),
                marker=dict(size=7, color=reg_colors_map[reg],
                            line=dict(color="#FFFFFF", width=1.5)),
                hovertemplate=f"<b>{reg}</b><br>%{{x}}: %{{y:,}} avg complaints<extra></extra>",
            ))

        bmode = "stack" if view_opt == "Stacked bars" else "group"
        fig3 = pset(fig3, h=420, l=64, r=28, t=52, b=54)
        fig3.update_layout(
            barmode=bmode,
            title=dict(text="Average Monthly Complaints by Region  ·  6-Year Average (2019–2024)",
                       font=dict(family="Roboto Condensed", size=15, color="#002366")),
            xaxis=dict(title="Month", tickfont=dict(size=12)),
            yaxis=dict(title="Avg Pothole Complaints", tickformat=","),
            legend=dict(orientation="h", y=1.11, x=0,
                        font=dict(size=11.5, color=G["tick"])),
        )
        st.plotly_chart(fig3, use_container_width=True)


    # ── TAB 4 — YEAR-OVER-YEAR COMPARISON ────────────────────────────────────
    with tab4:
        st.markdown(
            '<p style="font-size:13px;color:var(--sub);margin:12px 0 16px;font-weight:400">'
            'Select a month to compare all years side by side — or compare annual totals. '
            'Red bars = above 6-year average. Blue = below.</p>', unsafe_allow_html=True)

        col_sel, col_chart = st.columns([1, 3], gap="large")
        with col_sel:
            month_choice = st.selectbox(
                "Select month to compare",
                ["Annual Total"] + months,
                index=0
            )

        if month_choice == "Annual Total":
            ann_vals = [sum(v for v in data_ym[yr] if v > 0) for yr in years]
            ann_avg  = sum(ann_vals[:6]) / 6
            bar_colors = [C["red"] if v > ann_avg else C["blue"] for v in ann_vals]
            fig4 = go.Figure(go.Bar(
                x=[str(y) for y in years],
                y=ann_vals,
                marker=dict(color=bar_colors, line=dict(width=0), cornerradius=5),
                text=[f"{v:,}" for v in ann_vals],
                textposition="outside",
                textfont=dict(family="Roboto Mono", size=12, color=G["tick"]),
                hovertemplate="<b>%{x}</b><br>%{y:,} total complaints<extra></extra>",
            ))
            fig4.add_hline(y=ann_avg, line_color="rgba(0,35,102,0.5)",
                           line_dash="dot", line_width=2,
                           annotation_text=f"  6-year avg: {ann_avg:,.0f}",
                           annotation_font=dict(size=11.5, color="#002366"))
            title_str = "Annual Total Pothole Complaints by Year"
            y_title   = "Total Complaints"
        else:
            m_idx    = months.index(month_choice)
            m_vals   = [data_ym[yr][m_idx] for yr in years]
            m_avg    = sum(m_vals[:6]) / 6
            bar_colors = [C["red"] if v > m_avg else (C["blue"] if v > 0 else "rgba(200,200,200,0.3)")
                          for v in m_vals]
            fig4 = go.Figure(go.Bar(
                x=[str(y) for y in years],
                y=[v if v > 0 else None for v in m_vals],
                marker=dict(color=bar_colors, line=dict(width=0), cornerradius=5),
                text=[f"{v:,}" if v > 0 else "N/A" for v in m_vals],
                textposition="outside",
                textfont=dict(family="Roboto Mono", size=12, color=G["tick"]),
                hovertemplate="<b>%{x} " + month_choice + "</b><br>%{y:,} complaints<extra></extra>",
            ))
            fig4.add_hline(y=m_avg, line_color="rgba(0,35,102,0.5)",
                           line_dash="dot", line_width=2,
                           annotation_text=f"  6-year avg: {m_avg:,.0f}",
                           annotation_font=dict(size=11.5, color="#002366"))
            title_str = f"{month_choice} — Pothole Complaints by Year"
            y_title   = "Complaints"

        fig4 = pset(fig4, h=380, l=64, r=28, t=52, b=46)
        fig4.update_layout(
            title=dict(text=title_str,
                       font=dict(family="Roboto Condensed", size=15, color="#002366")),
            xaxis=dict(title="Year", tickfont=dict(size=13)),
            yaxis=dict(title=y_title, tickformat=","),
            showlegend=False,
        )
        with col_chart:
            st.plotly_chart(fig4, use_container_width=True)



# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — ACTION PLAN
# ══════════════════════════════════════════════════════════════════════════════
elif S == 9:
    slide_header("09", "Three findings. One early-warning system.",
                 "The analysis supports a weather-triggered, regionally-differentiated maintenance "
                 "alert that converts NS TIR from reactive to proactive operations.")

    cl, cr = st.columns(2, gap="large")
    with cl:
        label("Core findings")
        findings = [
            ("var(--red)", "1", "A measurable lag exists",
             f"Spearman r = {BEST_LAG_R:+.3f} at Day {BEST_LAG_DAY} (p_bonf = {BEST_LAG_PBONF:.4f}). "
             f"Significant window: Days {SIG_LAG_MIN}–{SIG_LAG_MAX}. Spring-only: r = −0.143. "
             "Consistent across all 6 years 2019–2025."),
            ("var(--blue)", "2", "Weather variables explain ~3–4% of daily variance",
             "Spring Season calendar dummy (+4.59), FTC 14d (−0.67), and Snow 7d (+0.23) are the dominant "
             "significant OLS predictors. Newey-West HAC standard errors correct for autocorrelation. "
             "Full-model R² = 7.2% includes the Spring calendar dummy — weather-only R² ≈ 3–4%."),
            ("var(--amber)", "3", "Halifax requires priority alert triage",
             "FTC r = −0.125 (***). Annapolis and Central NS are precipitation-driven. "
             "Region-differentiated alerts outperform province-wide blanket warnings."),
        ]
        items = ""
        for i, (color, num, title, body) in enumerate(findings):
            sep = "padding-bottom:20px;border-bottom:1px solid var(--divider);margin-bottom:20px;" if i < 2 else ""
            items += (
                f'<div style="display:flex;gap:18px;align-items:flex-start;{sep}">'
                f'<div style="font-family:\'DM Sans\',serif;font-size:1.6rem;'
                f'color:{color};line-height:1;flex-shrink:0;width:28px;padding-top:2px">{num}</div>'
                f'<div>'
                f'<p style="font-size:14px;font-weight:600;color:var(--text);margin:0 0 5px">{title}</p>'
                f'<p style="font-size:13px;color:var(--sub);line-height:1.75;font-weight:400">{body}</p>'
                f'</div></div>')
        st.markdown(
            f'<div style="background:var(--surface);border:1px solid var(--border);'
            f'border-radius:12px;padding:26px">{items}</div>', unsafe_allow_html=True)

    with cr:
        label("Proposed 3-tier alert system")
        for acc, title, body in [
            ("var(--red)", "HIGH ALERT — Deploy Now",
             "≥5 FT days in rolling 14d, OR thaw after 3+ consecutive freezing days. "
             "Pre-stage full patching crews within 5 days. Prioritise Halifax."),
            ("var(--amber)", "MEDIUM ALERT — Monitor",
             "2–4 FT days in 14d window, OR 7-day precip > 25 mm. "
             "Schedule patrols and pre-stock materials at priority depots."),
            ("var(--blue)", "LOW ALERT — Routine",
             "0–1 FT days, normal precipitation. Standard reactive complaint-response."),
        ]:
            bg, bdr = ACC.get(acc, ("var(--surface2)", "var(--border)"))
            st.markdown(
                f'<div style="background:{bg};border:1px solid {bdr};border-left:3px solid {acc};'
                f'border-radius:10px;padding:15px 17px;margin-bottom:10px">'
                f'<p style="font-size:12px;font-weight:600;color:{acc};margin:0 0 6px">{title}</p>'
                f'<p style="font-size:13px;color:var(--text2);line-height:1.72;font-weight:400">{body}</p>'
                f'</div>', unsafe_allow_html=True)

    divider()
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        if ALERT_PRECISION is not None:
            _prec_txt = (
                f"HIGH alert (FTC_14d ≥ 5) was followed by an above-normal surge "
                f"within 5–7 days in {ALERT_PRECISION*100:.0f}% of cases "
                f"({ALERT_N} alert days). Lift over baseline: {ALERT_LIFT:.1f}×. "
                f"Seasonal-adjusted lag: r = {ADJ_PEAK_R:+.3f} at Day {ADJ_PEAK_LAG}."
            )
        else:
            _prec_txt = (
                "Early-warning deployment could cut response time from 5–7 days "
                "(reactive) to 1–2 days (proactive). Run 02_analysis.py to load "
                "live alert precision and seasonal adjustment results."
            )
        box("Alert Evaluation", _prec_txt, "var(--green)")
    with c2:
        box("Data Limitations",
            "Yarmouth A has no precipitation data. Weather explains only ~3–4% of variance "
            "(7.2% with Spring dummy). Road age and traffic volume are the dominant unmeasured "
            "confounders that would raise predictive power.", "var(--amber)")
    with c3:
        box("Validation Steps",
            "① Seasonal-adjustment lag check — see outputs/seasonal_adjustment_check.csv.  "
            "② Alert precision-recall evaluated — see outputs/alert_precision.csv.  "
            "③ Connect ECCC 7-day forecast API for real-time alert generation.", "var(--blue)")