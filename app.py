"""
NS Pothole Freeze-Thaw Analysis · v5 — Professional Edition
Run: streamlit run app.py
Deps: pip install streamlit plotly
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
  min-width: 265px !important;
  max-width: 265px !important;
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
  padding: 9px 16px 9px 20px !important;
  width: 100% !important;
  text-align: left !important;
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
    ("Action Plan", "var(--red)"),
]
NUMS = ["01","02","03","04","05","06","07","08","09"]

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
        if st.button(f" {NUMS[i]} {label}", key=f"sb_{i}", use_container_width=True):
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
        'A 6-year analysis of <strong style="color:var(--text);font-weight:500">391,795 service '
        'records</strong> and daily weather from 5 ECCC stations reveals a consistent '
        '<strong style="color:var(--red);font-weight:500">5-day window</strong> between '
        'freeze-thaw events and pothole complaint surges.</p>'
        '<div style="width:48px;height:3px;background:#FDD54E;border-radius:2px;margin-top:4px"></div>'
        '</div>', unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1: kpi("Service Records", "391,795", "NS TIR · 2019–2025", border_color="var(--border)")
    with k2: kpi("Pothole Complaints","32,096", "8.2 % of all records", "var(--red)", "var(--red-bdr)")
    with k3: kpi("Freeze-Thaw Days", "647", "detected across NS", "var(--amber)","var(--amber-bdr)")
    with k4: kpi("Predictive Window", "5–7 days", "FT event → surge", "var(--blue)", "var(--blue-bdr)")

    divider()

    # Two-column content
    l, r = st.columns([1.08, 1], gap="large")
    with l:
        label("About this analysis")
        box("What We Did",
            "Every pothole complaint in the NS TIR Operations Contact Centre was linked to its "
            "nearest ECCC weather station. Spearman cross-correlation at 1–21 day lags was used "
            "to find whether freeze-thaw events reliably predict complaint surges — and by how many days.",
            "var(--red)")
        box("Why It Matters for NS TIR",
            "Maintenance crews are currently dispatched only <em>after</em> a citizen calls. "
            "A statistically significant 5-day lag means crews can be pre-staged before the "
            "phones start ringing — cutting response time and reducing per-pothole patching cost.",
            "var(--blue)")
    with r:
        label("Data")
        box("Dataset 1 — NS TIR OCC",
            "391,795 complaint records across 64 supervisor area codes. "
            "Provincial highways only. January 2019 – September 2025. "
            "Pothole complaints represent 8.2 % of all records (32,096).",
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
        years = ["2019","2020","2021","2022","2023","2024","2025"]
        vals = [4784, 4009, 4118, 5700, 3299, 4604, 5582]
        clrs = [C["red"] if y in ("2022","2025") else f"rgba(59,130,246,{0.38+i*0.08:.2f})"
                 for i, y in enumerate(years)]
        fig = go.Figure(go.Bar(
            x=years, y=vals,
            marker=dict(color=clrs, line=dict(width=0), cornerradius=5),
            text=[f"{v:,}" for v in vals], textposition="outside",
            textfont=dict(family="Roboto Mono", size=11, color=G["tick"]),
            hovertemplate="<b>%{x}</b> — %{y:,} complaints<extra></extra>",
        ))
        for yr, lbl in [("2022","Severe FT season"),("2025","Active FT season")]:
            fig.add_annotation(x=yr, y=vals[years.index(yr)], text=f"↑ {lbl}",
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
        box("The Lag in Plain English",
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
    slide_header("04", "Core Finding — The 5-Day Lag",
                 "Spearman cross-correlation computed at every lag from 1 to 21 days. "
                 "The minimum of the red curve at Day 5 is the central result of the entire analysis.")

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
        text="<b>Day 5 — Peak</b><br>r = −0.081",
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
    with c1: kpi("Peak Lag Day",        "Day 5",    "r = −0.081 across all 6 years",    "var(--red)",   "var(--red-bdr)")
    with c2: kpi("Spring-Only r",       "−0.143",   "p = 0.0003 — highly significant",  "var(--red)",   "var(--red-bdr)")
    with c3: kpi("Spring Amplification","3×",        "Stronger than the full-year signal","var(--amber)", "var(--amber-bdr)")
    with c4: kpi("Crew Action Window",  "5–7 days", "Pre-stage before phones ring",      "var(--green)", "var(--green-bdr)")

    # ── Reading guide — clean NS card style ───────────────────────────────
    divider()
    g1, g2, g3 = st.columns(3, gap="medium")
    for col, border, bg, title, body in [
        (g1, "#D30731", "rgba(211,7,49,0.05)",
         "What is the red shaded area?",
         "The red fill shows where freeze-thaw activity is suppressing same-day complaints. "
         "Roads are cracking but potholes are hidden under snow. "
         "Complaints are delayed — they arrive 5 days later."),
        (g2, "#C49A00", "rgba(196,154,0,0.07)",
         "What is the gold highlighted window?",
         "Days 5–7 is the operational window. When TIR detects a freeze-thaw event today, "
         "crews should be pre-staged within this window — before any citizen calls come in."),
        (g3, "#0045B8", "rgba(0,69,184,0.05)",
         "Why does the blue line look so different?",
         "Rain has no consistent lag pattern — it drives complaints on the same day. "
         "Freeze-thaw is unique: the damage is invisible for 5 days before complaints surge."),
    ]:
        col.markdown(
            f'<div style="background:{bg};border:1px solid rgba(0,35,102,0.12);'
            f'border-left:4px solid {border};border-radius:6px;padding:16px 15px">'
            f'<p style="font-family:Roboto Condensed,sans-serif;font-size:13px;'
            f'font-weight:700;color:{border};margin:0 0 8px">{title}</p>'
            f'<p style="font-size:12.5px;color:#3A4E72;line-height:1.7;font-weight:400;margin:0">{body}</p>'
            f'</div>', unsafe_allow_html=True)

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

    divider()
    rc1, rc2, rc3, rc4 = st.columns(4, gap="medium")
    for col, acc, rtitle, stat, body in [
        (rc1, "var(--red)",
         "Halifax / Lunenburg",
         "FTC r = -0.125 (p < 0.001)",
         "Strongest freeze-thaw signal in NS. 34% of all complaints come from here. "
         "Trigger: FTC_14d >= 5 days."),
        (rc2, "var(--blue)",
         "Annapolis Valley & Central NS",
         "Precip r = +0.09 to +0.10 (p < 0.001)",
         "Rainfall-driven — temperature cycling is less severe inland. "
         "Trigger: 7-day rain >= 25 mm."),
        (rc3, "var(--amber)",
         "Cape Breton",
         "FTC r = -0.041 (p < 0.05, weak)",
         "Atlantic Ocean moderates temperature swings — fewer complete freeze-thaw cycles. "
         "Trigger: Precip 7d >= 20 mm."),
        (rc4, "var(--slate)",
         "SW Nova Scotia",
         "No precipitation data available",
         "Yarmouth A lacks precipitation records. Results are inconclusive — likely a data "
         "gap, not an absence of the freeze-thaw effect."),
    ]:
        bg, bdr = ACC.get(acc, ("var(--surface2)", "var(--border)"))
        col.markdown(
            f'<div style="background:{bg};border:1px solid {bdr};border-left:3px solid {acc};'
            f'border-radius:10px;padding:16px 15px">'
            f'<p style="font-size:13px;font-weight:600;color:{acc};margin:0 0 5px">{rtitle}</p>'
            f'<p style="font-family:DM Mono,monospace;font-size:12px;color:var(--text);'
            f'margin:0 0 10px;font-weight:500">{stat}</p>'
            f'<p style="font-size:12px;color:var(--sub);line-height:1.7;font-weight:400;margin:0">{body}</p>'
            f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — REGRESSION
# ══════════════════════════════════════════════════════════════════════════════
elif S == 7:
    slide_header("07", "Five weather variables independently predict daily complaint counts.",
                 "OLS regression  ·  weekdays only 2019–2025  ·  R² = 7.2%")

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

    chart_col, table_col = st.columns([1.5, 1], gap="large")

    with chart_col:
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

    with table_col:
        # Clean NS government-style summary table
        st.markdown(
            '<p style="font-family:Roboto Condensed,sans-serif;font-size:10px;'
            'font-weight:700;letter-spacing:2px;text-transform:uppercase;'
            'color:#4A6490;margin:0 0 12px">Coefficient Summary</p>',
            unsafe_allow_html=True)

        rows_html = ""
        for name, val, sg, desc in predictors:
            sig_badge = (
                f'<span style="background:#D30731;color:#fff;font-size:10px;'
                f'font-weight:700;padding:2px 7px;border-radius:3px;'
                f'font-family:Roboto Condensed,sans-serif">significant</span>'
                if sg else
                f'<span style="background:#E5E9F0;color:#64748B;font-size:10px;'
                f'padding:2px 7px;border-radius:3px;'
                f'font-family:Roboto Condensed,sans-serif">not sig.</span>'
            )
            rows_html += (
                f'<tr style="border-bottom:1px solid #E8EDF5">'
                f'<td style="padding:10px 10px 10px 0;font-size:12.5px;'
                f'font-weight:{"600" if sg else "400"};color:{"#0D1B3E" if sg else "#64748B"}">'
                f'{name}</td>'
                f'<td style="font-family:Roboto Mono,monospace;font-size:13px;'
                f'color:{"#D30731" if sg else "#94A3B8"};text-align:right;'
                f'padding:10px 8px;font-weight:{"700" if sg else "400"}">'
                f'{val:+.2f}</td>'
                f'<td style="text-align:right;padding:10px 0 10px 4px">'
                f'{sig_badge}</td>'
                f'</tr>'
            )
        st.markdown(
            f'<div style="background:#FFFFFF;border:1px solid #D0D9E8;'
            f'border-top:3px solid #0045B8;border-radius:6px;padding:16px 18px">'
            f'<table style="width:100%;border-collapse:collapse">'
            f'<tr style="border-bottom:2px solid #0045B8">'
            f'<th style="font-family:Roboto Condensed,sans-serif;font-size:10px;'
            f'font-weight:700;color:#4A6490;text-transform:uppercase;letter-spacing:1.5px;'
            f'padding:0 10px 8px 0;text-align:left">Variable</th>'
            f'<th style="font-family:Roboto Condensed,sans-serif;font-size:10px;'
            f'font-weight:700;color:#4A6490;text-transform:uppercase;letter-spacing:1.5px;'
            f'padding:0 8px 8px;text-align:right">Effect</th>'
            f'<th style="font-family:Roboto Condensed,sans-serif;font-size:10px;'
            f'font-weight:700;color:#4A6490;text-transform:uppercase;letter-spacing:1.5px;'
            f'padding:0 0 8px;text-align:right">Status</th></tr>'
            f'{rows_html}'
            f'</table>'
            f'<p style="font-size:11px;color:#64748B;margin:12px 0 0;font-style:italic">'
            f'R² = 0.072 — weather explains 7.2% of daily variance</p>'
            f'</div>',
            unsafe_allow_html=True)

    divider()
    r1, r2, r3 = st.columns(3, gap="medium")
    for col, border_c, bg_c, rtitle, body in [
        (r1, "#D30731", "rgba(211,7,49,0.05)",
         "Spring dominates everything",
         "Just being in March–May adds +4.6 complaints per day. All winter damage "
         "becomes visible simultaneously — the single biggest predictor in the model."),
        (r2, "#C49A00", "rgba(196,154,0,0.06)",
         "Why does Freeze-Thaw show negative?",
         "During freezing, potholes form but stay hidden under snow. "
         "Calls drop temporarily. The surge arrives 5 days later — "
         "this is the lag effect, not a true inverse."),
        (r3, "#0045B8", "rgba(0,69,184,0.05)",
         "Why R² = 7.2% is acceptable",
         "Road age, traffic volume, and pavement condition explain most of the rest. "
         "Those data are not yet in the model. "
         "7.2% from weather alone is sufficient for an operational alert trigger."),
    ]:
        col.markdown(
            f'<div style="background:{bg_c};border:1px solid rgba(0,35,102,0.12);'
            f'border-left:4px solid {border_c};border-radius:6px;padding:16px 15px">'
            f'<p style="font-family:Roboto Condensed,sans-serif;font-size:13px;'
            f'font-weight:700;color:{border_c};margin:0 0 8px">{rtitle}</p>'
            f'<p style="font-size:12.5px;color:#3A4E72;line-height:1.7;font-weight:400;margin:0">{body}</p>'
            f'</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — ACTION PLAN
# ══════════════════════════════════════════════════════════════════════════════
elif S == 8:
    slide_header("08", "Three findings. One early-warning system.",
                 "The analysis supports a weather-triggered, regionally-differentiated maintenance "
                 "alert that converts NS TIR from reactive to proactive operations.")

    cl, cr = st.columns(2, gap="large")
    with cl:
        label("Core findings")
        findings = [
            ("var(--red)", "1", "A measurable 5-day lag exists",
             "Spearman r = −0.081 at Day 5. Spring-only: r = −0.143, p = 0.0003. "
             "Consistent and statistically significant across all 6 years."),
            ("var(--blue)", "2", "Weather explains 7.2% of daily variance",
             "Spring Season (+4.59), FTC 14d (−0.67), and Snow 7d (+0.23) are the dominant "
             "significant OLS predictors under HC3 robust standard errors."),
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
    c1, c2 = st.columns(2, gap="large")
    with c1:
        box("Data Limitations",
            "Yarmouth A has no precipitation data. Greenwood A has no rain/snow split. "
            "Weather explains only 7.2% of variance — road age and traffic volume are "
            "the dominant unmeasured confounders.", "var(--amber)")
    with c2:
        box("Expected Impact",
            "Early-warning deployment could reduce average pothole response time from "
            "5–7 days (reactive) to 1–2 days (proactive). Fewer complaints, lower "
            "patching cost, measurably better citizen service.", "var(--blue)")


# """
# NS Pothole Freeze-Thaw Analysis · v5 — Professional Edition
# Run: streamlit run app.py
# Deps: pip install streamlit plotly
# """
# import streamlit as st
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# st.set_page_config(
# page_title="NS Pothole Analysis",
# page_icon="",
# layout="wide",
# initial_sidebar_state="expanded",
# )

# # ══════════════════════════════════════════════════════════════════════════════
# # DESIGN SYSTEM · Instrument Serif + DM Mono · auto dark / light
# # ══════════════════════════════════════════════════════════════════════════════
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Sora:wght@300;400;500;600;700&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

# /* ─── LIGHT ──────────────────────────────── */
# :root {
# --bg: #F2F4F8;
# --surface: #FFFFFF;
# --surface2: #F7F8FC;
# --surface3: #EFF1F7;
# --border: #E0E4EF;
# --border2: #C8CFDF;
# --text: #080E1F;
# --text2: #1A2540;
# --sub: #4A5578;
# --faint: #8A94B0;
# --divider: rgba(0,0,0,0.07);

# --red: #B91C1C;
# --red-v: #DC2626;
# --red-bg: rgba(185,28,28,0.07);
# --red-bdr: rgba(185,28,28,0.2);

# --blue: #1D4ED8;
# --blue-v: #2563EB;
# --blue-bg: rgba(29,78,216,0.07);
# --blue-bdr: rgba(29,78,216,0.2);

# --amber: #B45309;
# --amber-v: #B8930A;
# --amber-bg: rgba(180,83,9,0.07);
# --amber-bdr: rgba(180,83,9,0.2);

# --green: #15803D;
# --green-v: #15803D;
# --green-bg: rgba(21,128,61,0.07);
# --green-bdr: rgba(21,128,61,0.2);

# --slate: #334155;
# --slate-bg: rgba(51,65,85,0.06);
# --slate-bdr: rgba(51,65,85,0.18);

# /* sidebar */
# --sb: #111827;
# --sb2: #1F2937;
# --sb-txt: #F9FAFB;
# --sb-sub: #9CA3AF;
# --sb-faint: #4B5563;
# --sb-line: rgba(255,255,255,0.07);
# --sb-hover: rgba(255,255,255,0.05);
# --sb-dot: #EF4444;
# }

# /* ─── DARK ───────────────────────────────── */
# @media (prefers-color-scheme: dark) {
# :root {
# --bg: #060A14;
# --surface: #0D1525;
# --surface2: #121D30;
# --surface3: #0A1020;
# --border: #1A2840;
# --border2: #243350;
# --text: #F0F4FF;
# --text2: #C0CCED;
# --sub: #7A8EBB;
# --faint: #3D5070;
# --divider: rgba(255,255,255,0.06);

# --red: #F87171;
# --red-v: #FCA5A5;
# --red-bg: rgba(248,113,113,0.1);
# --red-bdr: rgba(248,113,113,0.28);

# --blue: #60A5FA;
# --blue-v: #93C5FD;
# --blue-bg: rgba(96,165,250,0.09);
# --blue-bdr: rgba(96,165,250,0.26);

# --amber: #FBBF24;
# --amber-v: #FDE68A;
# --amber-bg: rgba(251,191,36,0.09);
# --amber-bdr: rgba(251,191,36,0.26);

# --green: #34D399;
# --green-v: #6EE7B7;
# --green-bg: rgba(52,211,153,0.09);
# --green-bdr: rgba(52,211,153,0.24);

# --slate: #94A3B8;
# --slate-bg: rgba(148,163,184,0.08);
# --slate-bdr: rgba(148,163,184,0.2);

# --sb: #060A14;
# --sb2: #0D1525;
# --sb-txt: #F0F4FF;
# --sb-sub: #64748B;
# --sb-faint: #1E2D40;
# --sb-line: rgba(255,255,255,0.05);
# --sb-hover: rgba(255,255,255,0.04);
# --sb-dot: #F87171;
# }
# }

# /* ─── BASE ───────────────────────────────── */
# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
# html, body, [class*="css"] {
# font-family: 'Sora', system-ui, sans-serif !important;
# color: var(--text) !important;
# -webkit-font-smoothing: antialiased;
# -moz-osx-font-smoothing: grayscale;
# }
# .stApp { background: var(--bg) !important; }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container {
# padding: 2.5rem 3rem 6rem !important;
# max-width: 1180px !important;
# }

# /* ─── SIDEBAR ────────────────────────────── */
# [data-testid="stSidebar"] {
# background: var(--sb) !important;
# border-right: 1px solid var(--sb-line) !important;
# min-width: 230px !important;
# max-width: 230px !important;
# }
# [data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
# [data-testid="collapsedControl"] { display: none !important; }

# /* Sidebar nav buttons */
# [data-testid="stSidebar"] .stButton > button {
# background: transparent !important;
# border: none !important;
# border-radius: 0 !important;
# color: var(--sb-sub) !important;
# font-family: 'Sora', sans-serif !important;
# font-size: 12.5px !important;
# font-weight: 400 !important;
# padding: 10px 20px 10px 24px !important;
# width: 100% !important;
# text-align: left !important;
# white-space: nowrap !important;
# overflow: hidden !important;
# text-overflow: ellipsis !important;
# transition: color .13s, background .13s !important;
# letter-spacing: 0.01em !important;
# position: relative !important;
# }
# [data-testid="stSidebar"] .stButton > button:hover {
# background: var(--sb-hover) !important;
# color: var(--sb-txt) !important;
# }

# /* ─── CHARTS ─────────────────────────────── */
# [data-testid="stPlotlyChart"] > div {
# border-radius: 14px !important;
# border: 1px solid var(--border) !important;
# overflow: hidden !important;
# background: var(--surface) !important;
# box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
# }

# /* ─── SCROLLBAR ──────────────────────────── */
# ::-webkit-scrollbar { width: 4px; height: 4px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
# </style>
# """, unsafe_allow_html=True)

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE REGISTRY
# # ══════════════════════════════════════════════════════════════════════════════
# SLIDES = [
# ("Overview", "var(--red)"),
# ("The Problem", "var(--red)"),
# ("How Roads Break", "var(--blue)"),
# ("Seasonal Pattern","var(--amber)"),
# ("5-Day Lag ", "var(--red)"),
# ("Predictors", "var(--blue)"),
# ("By Region", "var(--amber)"),
# ("Regression", "var(--green)"),
# ("Action Plan", "var(--red)"),
# ]
# NUMS = ["01","02","03","04","05","06","07","08","09"]

# if "s" not in st.session_state:
# st.session_state.s = 0

# # ══════════════════════════════════════════════════════════════════════════════
# # SIDEBAR
# # ══════════════════════════════════════════════════════════════════════════════
# with st.sidebar:
# # Brand block
# st.markdown(
# '<div style="padding:32px 24px 24px;border-bottom:1px solid var(--sb-line)">'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11.5px;font-weight:500;'
# 'color:var(--sb-dot);letter-spacing:3.5px;margin:0 0 8px">NS · POTHOLE</p>'
# '<p style="font-family:\'Instrument Serif\',serif;font-size:16px;'
# 'color:var(--sb-txt);margin:0 0 4px;font-style:italic;line-height:1.3">'
# 'Freeze-Thaw Analysis</p>'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11.5px;color:var(--sb-sub);'
# 'margin:0;letter-spacing:.5px">2019 – 2025</p>'
# '</div>',
# unsafe_allow_html=True)

# st.markdown(
# '<p style="font-family:\'DM Mono\',monospace;font-size:11px;letter-spacing:2.5px;'
# 'text-transform:uppercase;color:var(--sb-faint);padding:20px 24px 6px;'
# 'border-bottom:none">Navigation</p>',
# unsafe_allow_html=True)

# S = st.session_state.s
# for i, (label, _color) in enumerate(SLIDES):
# if st.button(f" {NUMS[i]} {label}", key=f"sb_{i}", use_container_width=True):
# st.session_state.s = i
# st.rerun()

# # Active highlight
# st.markdown(f"""
# <style>
# [data-testid="stSidebar"] .stButton:nth-of-type({S+1}) > button {{
# background: rgba(255,255,255,0.06) !important;
# color: var(--sb-txt) !important;
# font-weight: 600 !important;
# border-right: 2px solid var(--sb-dot) !important;
# }}
# </style>""", unsafe_allow_html=True)

# # Footer
# st.markdown(
# f'<div style="position:absolute;bottom:0;left:0;right:0;'
# f'padding:20px 24px;border-top:1px solid var(--sb-line)">'
# f'<div style="display:flex;justify-content:space-between;align-items:center;'
# f'margin-bottom:6px">'
# f'<span style="font-family:\'DM Mono\',monospace;font-size:11px;'
# f'color:var(--sb-faint);letter-spacing:.5px">{NUMS[S]}&nbsp;of&nbsp;{NUMS[-1]}</span>'
# f'<div style="display:flex;gap:4px">'
# + "".join(
# f'<div style="width:{14 if j==S else 5}px;height:3px;'
# f'border-radius:2px;background:{"var(--sb-dot)" if j==S else "var(--sb-faint)"};'
# f'transition:all .2s"></div>'
# for j in range(len(SLIDES))
# )
# + f'</div></div>'
# f'<p style="font-size:11.5px;color:var(--sb-faint);font-weight:400">'
# f'MBAN 2026 · Nova Scotia TIR + ECCC</p>'
# f'</div>',
# unsafe_allow_html=True)

# S = st.session_state.s

# # ══════════════════════════════════════════════════════════════════════════════
# # CHART PALETTE (explicit hex — Plotly can't read CSS vars)
# # ══════════════════════════════════════════════════════════════════════════════
# C = dict(
# red = "#EF4444",
# blue = "#3B82F6",
# amber = "#F59E0B",
# green = "#10B981",
# slate = "#94A3B8",
# indigo = "#6366F1",
# )
# G = dict(
# bg = "rgba(0,0,0,0)",
# grid = "rgba(110,120,150,0.12)",
# tick = "#6B7A99",
# line = "rgba(110,120,150,0.2)",
# zero = "rgba(100,110,140,0.45)",
# )

# def pset(fig, h=400, l=56, r=32, t=46, b=54):
# fig.update_layout(
# height=h, plot_bgcolor=G["bg"], paper_bgcolor=G["bg"],
# font=dict(family="Sora", size=12, color=G["tick"]),
# margin=dict(l=l, r=r, t=t, b=b),
# legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0,
# font=dict(size=11.5, color=G["tick"]),
# orientation="h", y=1.07, x=0, itemsizing="constant"),
# hoverlabel=dict(bgcolor="rgba(8,14,31,0.94)",
# bordercolor="rgba(255,255,255,0.12)",
# font=dict(family="Sora", size=12, color="#F0F4FF")),
# )
# fig.update_xaxes(gridcolor=G["grid"], zeroline=False,
# tickfont=dict(size=11, color=G["tick"]),
# title_font=dict(size=12, color=G["tick"]),
# linecolor=G["line"], showline=True,
# ticks="outside", ticklen=3, tickcolor=G["line"])
# fig.update_yaxes(gridcolor=G["grid"], zeroline=False,
# tickfont=dict(size=11, color=G["tick"]),
# title_font=dict(size=12, color=G["tick"]),
# linecolor="rgba(0,0,0,0)")
# return fig

# # ── UI HELPERS ────────────────────────────────────────────────────────────────
# ACC = {
# "var(--red)": ("var(--red-bg)", "var(--red-bdr)"),
# "var(--blue)": ("var(--blue-bg)", "var(--blue-bdr)"),
# "var(--amber)": ("var(--amber-bg)", "var(--amber-bdr)"),
# "var(--green)": ("var(--green-bg)", "var(--green-bdr)"),
# "var(--slate)": ("var(--slate-bg)", "var(--slate-bdr)"),
# }

# def slide_header(num, title, sub=""):
# """Professional slide header with number badge."""
# st.markdown(
# f'<div style="margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid var(--divider)">'
# f'<div style="display:flex;align-items:baseline;gap:14px;margin-bottom:12px">'
# f'<span style="font-family:\'DM Mono\',monospace;font-size:11px;font-weight:500;'
# f'color:var(--faint);letter-spacing:1.5px">{num}</span>'
# f'<h1 style="font-family:\'Instrument Serif\',serif;font-size:clamp(1.6rem,3.2vw,2.2rem);'
# f'font-weight:400;font-style:italic;color:var(--text);line-height:1.18;'
# f'letter-spacing:-0.3px">{title}</h1>'
# f'</div>'
# + (f'<p style="font-size:14px;color:var(--sub);line-height:1.8;max-width:820px;'
# f'font-weight:400">{sub}</p>' if sub else "")
# + '</div>', unsafe_allow_html=True)


# def box(title, body, accent="var(--blue)"):
# bg, bdr = ACC.get(accent, ("var(--surface2)", "var(--border)"))
# st.markdown(
# f'<div style="background:{bg};border:1px solid {bdr};border-left:3px solid {accent};'
# f'border-radius:10px;padding:15px 17px;margin-bottom:11px">'
# f'<p style="font-size:12px;font-weight:600;color:{accent};margin:0 0 7px;'
# f'letter-spacing:.03em">{title}</p>'
# f'<p style="font-size:13px;color:var(--text2);line-height:1.75;margin:0;'
# f'font-weight:400">{body}</p>'
# f'</div>', unsafe_allow_html=True)


# def kpi(label, value, sub="", color="var(--text)", border_color=None):
# bc = border_color or "var(--border)"
# st.markdown(
# f'<div style="background:var(--surface);border:1px solid {bc};'
# f'border-radius:12px;padding:22px 16px;text-align:center">'
# f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;font-weight:500;'
# f'color:var(--faint);text-transform:uppercase;letter-spacing:2.5px;margin:0 0 11px">{label}</p>'
# f'<p style="font-family:\'Instrument Serif\',serif;font-size:clamp(1.5rem,2.8vw,1.9rem);'
# f'font-style:italic;color:{color};line-height:1;margin:0 0 7px">{value}</p>'
# + (f'<p style="font-size:11.5px;color:var(--sub);margin:0;font-weight:400">{sub}</p>' if sub else "")
# + '</div>', unsafe_allow_html=True)


# def divider():
# st.markdown('<hr style="border:none;border-top:1px solid var(--divider);margin:24px 0">', unsafe_allow_html=True)


# def label(text):
# st.markdown(
# f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;font-weight:500;'
# f'color:var(--faint);text-transform:uppercase;letter-spacing:2.5px;margin:0 0 16px">{text}</p>',
# unsafe_allow_html=True)

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 0 — OVERVIEW
# # ══════════════════════════════════════════════════════════════════════════════
# if S == 0:
# # Hero headline
# st.markdown(
# '<div style="padding:8px 0 36px">'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11.5px;font-weight:500;'
# 'letter-spacing:2.5px;color:#0045B8;margin:0 0 20px">NOVA SCOTIA · TIR + ECCC · 2019–2025</p>'
# '<h1 style="font-family:\'Instrument Serif\',serif;'
# 'font-size:clamp(2.2rem,5vw,3.6rem);font-weight:400;font-style:italic;'
# 'color:var(--text);line-height:1.08;letter-spacing:-1px;margin:0 0 18px">'
# 'Can we predict potholes<br>'
# '<span style="color:var(--red)">before</span> they appear?'
# '</h1>'
# '<p style="font-size:15px;color:var(--sub);line-height:1.85;max-width:620px;'
# 'font-weight:400;margin:0 0 30px">'
# 'A 6-year analysis of <strong style="color:var(--text);font-weight:500">391,795 service '
# 'records</strong> and daily weather from 5 ECCC stations reveals a consistent '
# '<strong style="color:var(--red);font-weight:500">5-day window</strong> between '
# 'freeze-thaw events and pothole complaint surges.</p>'
# '<div style="width:48px;height:3px;background:#FDD54E;border-radius:2px;margin-top:4px"></div>'
# '</div>', unsafe_allow_html=True)

# # KPI row
# k1, k2, k3, k4 = st.columns(4, gap="medium")
# with k1: kpi("Service Records", "391,795", "NS TIR · 2019–2025", border_color="var(--border)")
# with k2: kpi("Pothole Complaints","32,096", "8.2 % of all records", "var(--red)", "var(--red-bdr)")
# with k3: kpi("Freeze-Thaw Days", "647", "detected across NS", "var(--amber)","var(--amber-bdr)")
# with k4: kpi("Predictive Window", "5–7 days", "FT event → surge", "var(--blue)", "var(--blue-bdr)")

# divider()

# # Two-column content
# l, r = st.columns([1.08, 1], gap="large")
# with l:
# label("About this analysis")
# box("What We Did",
# "Every pothole complaint in the NS TIR Operations Contact Centre was linked to its "
# "nearest ECCC weather station. Spearman cross-correlation at 1–21 day lags was used "
# "to find whether freeze-thaw events reliably predict complaint surges — and by how many days.",
# "var(--red)")
# box("Why It Matters for NS TIR",
# "Maintenance crews are currently dispatched only <em>after</em> a citizen calls. "
# "A statistically significant 5-day lag means crews can be pre-staged before the "
# "phones start ringing — cutting response time and reducing per-pothole patching cost.",
# "var(--blue)")
# with r:
# label("Data")
# box("Dataset 1 — NS TIR OCC",
# "391,795 complaint records across 64 supervisor area codes. "
# "Provincial highways only. January 2019 – September 2025. "
# "Pothole complaints represent 8.2 % of all records (32,096).",
# "var(--amber)")
# box("Dataset 2 — Environment Canada (ECCC)",
# "Daily climate data from 5 verified weather stations: Halifax Stanfield, "
# "Greenwood A, Truro, Sydney A, and Yarmouth A. Merged to complaints by "
# "geographic region and date.", "var(--green)")
# box("Use the sidebar to navigate",
# "Each slide covers one finding — a chart and a plain-English explanation. "
# "Read in order for the full story, or jump to any slide directly.", "var(--slate)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 1 — THE PROBLEM
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 1:
# slide_header("01", "Potholes cost money. Right now, we fix them too late.",
# "NS TIR dispatches repair crews only after citizens file complaints — "
# "weather data already available in real time could allow proactive deployment instead.")

# cl, cr = st.columns([1.45, 1], gap="large")
# with cl:
# years = ["2019","2020","2021","2022","2023","2024","2025"]
# vals = [4784, 4009, 4118, 5700, 3299, 4604, 5582]
# clrs = [C["red"] if y in ("2022","2025") else f"rgba(59,130,246,{0.38+i*0.08:.2f})"
# for i, y in enumerate(years)]
# fig = go.Figure(go.Bar(
# x=years, y=vals,
# marker=dict(color=clrs, line=dict(width=0), cornerradius=5),
# text=[f"{v:,}" for v in vals], textposition="outside",
# textfont=dict(family="Roboto Mono", size=11, color=G["tick"]),
# hovertemplate="<b>%{x}</b> — %{y:,} complaints<extra></extra>",
# ))
# for yr, lbl in [("2022","Severe FT season"),("2025","Active FT season")]:
# fig.add_annotation(x=yr, y=vals[years.index(yr)], text=f"↑ {lbl}",
# showarrow=False, yshift=27,
# font=dict(family="Sora", size=10.5, color=C["red"]))
# fig = pset(fig, h=380, l=52, r=24, t=42, b=46)
# fig.update_layout(
# title=dict(text="Annual Pothole Complaints · 2019–2025",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# showlegend=False,
# yaxis=dict(title="Complaints", tickformat=","),
# bargap=0.30)
# st.plotly_chart(fig, use_container_width=True)

# with cr:
# box("The Reactive Problem",
# "By the time a citizen calls TIR, the pothole has often existed for days. "
# "Reactive patching means crews mobilise after damage is visible and citizen "
# "frustration has already accumulated.", "var(--red)")
# box("The Opportunity",
# "ECCC weather data is freely available 24/7. A consistent 5-day lag between "
# "freeze-thaw events and complaint surges means crews can be pre-staged before "
# "any call is made.", "var(--blue)")
# box("Why 2022 and 2025 Peak",
# "Both years had unusually severe freeze-thaw seasons — more temperature cycling "
# "events, greater cumulative pavement stress, and correspondingly larger complaint "
# "waves in the weeks that followed.", "var(--amber)")
# box("The Business Case",
# "CAA estimates NS drivers pay $137 per year in extra costs due to poor roads. "
# "Proactive maintenance converts $1 in preservation spend into $6–10 of avoided "
# "repair expenditure.", "var(--green)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 2 — HOW ROADS BREAK
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 2:
# slide_header("02", "A freeze-thaw cycle cracks roads — but complaints arrive days later.",
# "The physics explains why the 5-day lag is consistent across all 6 years "
# "and all 5 regions of Nova Scotia.")

# steps = [
# ("var(--blue)", "01", "Water Enters", "Rain or snowmelt seeps into micro-cracks in the asphalt and sub-base layer."),
# ("var(--slate)", "02", "Night Freeze", "Tmin < 0°C — water expands 9%, permanently widening the crack walls."),
# ("var(--amber)", "03", "Day Thaw", "Tmax > 0°C — ice melts, but the crack is now wider than before. Permanent."),
# ("var(--red)", "04", "Repeat Cycles", "Each additional FT cycle compounds stress. Five or more causes structural failure."),
# ("var(--slate)", "05", "Surface Fails", "Traffic breaks through weakened pavement. A pothole forms and grows."),
# ("var(--red)", "06", "Complaint Filed", "Citizen notices the pothole and calls TIR — typically 5–7 days post-event."),
# ]
# step_cols = st.columns(6, gap="small")
# for col, (color, num, title, desc) in zip(step_cols, steps):
# col.markdown(
# f'<div style="background:var(--surface);border:1px solid var(--border);'
# f'border-top:2px solid {color};border-radius:10px;padding:18px 11px;'
# f'text-align:center;min-height:190px">'
# f'<p style="font-family:\'DM Mono\',monospace;font-size:1.15rem;font-weight:500;'
# f'color:{color};margin-bottom:12px">{num}</p>'
# f'<p style="font-size:12.5px;font-weight:600;color:var(--text);margin-bottom:8px">{title}</p>'
# f'<p style="font-size:11.5px;color:var(--sub);line-height:1.65;font-weight:400">{desc}</p>'
# f'</div>', unsafe_allow_html=True)

# divider()
# cl, cr = st.columns(2, gap="large")
# with cl:
# box("Freeze-Thaw Day Definition",
# '<code style="background:var(--red-bg);padding:3px 10px;border-radius:5px;'
# 'font-family:DM Mono,monospace;font-size:12px;color:var(--red)">'
# 'FT_day = 1 &nbsp;if&nbsp; Tmax &gt; 0°C &nbsp;AND&nbsp; Tmin &lt; 0°C</code><br><br>'
# 'Temperature must cross the freezing point in <em>both directions</em> within 24 hours. '
# '<strong style="color:var(--text)">647 such days</strong> detected across NS, 2019–2025. '
# 'Concentrated January through April.', "var(--red)")
# box("Why the 14-Day Rolling Window",
# "A single FT day causes minor damage. Multiple consecutive FT days destroy a road. "
# "<strong style='color:var(--text)'>FTC_14d</strong> sums FT events over the prior 14 days — "
# "capturing accumulated pavement stress. Strongest single predictor at Spearman r = −0.087.",
# "var(--amber)")
# with cr:
# st.markdown(
# '<div style="background:var(--surface);border:1px solid var(--border);'
# 'border-radius:12px;padding:24px">'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11px;letter-spacing:2.5px;'
# 'color:var(--faint);text-transform:uppercase;margin-bottom:18px">Key Formulas</p>'
# '<div style="background:var(--red-bg);border:1px solid var(--red-bdr);'
# 'border-radius:8px;padding:18px 20px;margin-bottom:18px">'
# '<code style="font-family:\'DM Mono\',monospace;font-size:13px;color:var(--amber);'
# 'line-height:2.25;display:block">'
# 'FT_day(t) = 1<br>'
# '&nbsp;&nbsp;if Tmax(t) &gt; 0°C<br>'
# '&nbsp;&nbsp;AND Tmin(t) &lt; 0°C<br><br>'
# 'FTC_14d(t) = Σ FT_day(t−14 … t−1)</code>'
# '</div>'
# '<p style="font-size:13px;color:var(--sub);line-height:1.8;font-weight:400">'
# 'The window is shifted one day forward to prevent data leakage. Only weather '
# 'information available <em>before</em> the complaint date is used as a predictor.</p>'
# '</div>',
# unsafe_allow_html=True)
# box("The Lag in Plain English",
# "Road cracks on the FT event day. The pothole develops over subsequent days. "
# "The citizen discovers it and calls TIR — consistently 5–7 days after the event.",
# "var(--blue)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 3 — SEASONAL PATTERN
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 3:
# slide_header("03", "Winter breaks roads. Summer gets the complaints.",
# "FT damage accumulates across winter and surfaces as visible complaints in summer — "
# "a macro-scale version of the same 5-day daily lag.")

# months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
# ft_days = [126, 105, 150, 71, 4, 0, 0, 0, 3, 8, 71, 112]
# ph_avg = [11.0, 15.4, 12.2, 13.7, 15.5, 16.2, 18.3, 12.9, 11.3, 10.4, 8.2, 9.8]

# fig = make_subplots(specs=[[{"secondary_y": True}]])
# bar_c = [f"rgba(59,130,246,{max(0.15, ft/155*0.82):.2f})" for ft in ft_days]
# fig.add_trace(go.Bar(x=months, y=ft_days, name="Freeze-Thaw Days",
# marker=dict(color=bar_c, line=dict(width=0), cornerradius=4),
# hovertemplate="<b>%{x}</b> FT days: %{y}<extra></extra>"), secondary_y=False)
# fig.add_trace(go.Scatter(x=months, y=ph_avg, name="Avg Potholes / Day",
# line=dict(color=C["red"], width=3, shape="spline"),
# marker=dict(size=[14 if m=="Jul" else 6 for m in months],
# color=[C["red"] if m=="Jul" else "rgba(239,68,68,0.5)" for m in months],
# line=dict(color="rgba(0,0,0,0.15)", width=1.5)),
# fill="tozeroy", fillcolor="rgba(211,7,49,0.06)",
# hovertemplate="<b>%{x}</b> %{y:.1f} complaints/day<extra></extra>"), secondary_y=True)
# fig.add_annotation(x="Jul", y=18.3, text="Peak 18.3 / day",
# showarrow=False, yshift=22, yref="y2",
# font=dict(family="Roboto Mono", size=10.5, color=C["red"]))
# fig.add_annotation(x="Mar", y=150, text="Peak FT month",
# showarrow=False, yshift=22, yref="y",
# font=dict(family="Roboto Mono", size=10.5, color=C["blue"]))
# fig = pset(fig, h=400, l=60, r=68, t=44, b=48)
# fig.update_layout(
# title=dict(text="Monthly Freeze-Thaw Days · vs Avg Daily Pothole Complaints",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# bargap=0.18)
# fig.update_yaxes(title="Freeze-Thaw Days", secondary_y=False,
# title_font=dict(color="#1D4ED8"),
# tickfont=dict(color="#1D4ED8"))
# fig.update_yaxes(title="Avg Potholes / Day", secondary_y=True,
# title_font=dict(color="#B91C1C"),
# tickfont=dict(color="#B91C1C"))
# st.plotly_chart(fig, use_container_width=True)

# c1, c2, c3 = st.columns(3, gap="large")
# with c1:
# box("Peak FT Month: March",
# "<strong style='color:var(--text)'>150 freeze-thaw days</strong> in March across "
# "6 years — highest of any month. Yet March complaints are only moderate: the lag "
# "hasn't expired and potholes haven't yet surfaced.", "var(--blue)")
# with c2:
# box("Peak Complaint Month: July",
# "<strong style='color:var(--text)'>18.3 avg complaints/day</strong> in July — "
# "despite zero FT events that month. All accumulated winter damage is now visible "
# "on dry summer roads and being actively reported.", "var(--red)")
# with c3:
# box("The Macro Lag: 4–5 Months",
# "FT damage peaks in March. Complaints peak in July. The 4–5 month annual offset "
# "is the same physical mechanism as the 5-day daily lag — same cause, same physics, "
# "different timescale.", "var(--amber)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 4 — THE 5-DAY LAG 
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 4:
# slide_header("04", "Core Finding — The 5-Day Lag",
# "Spearman cross-correlation computed at every lag from 1 to 21 days. "
# "The minimum of the red curve at Day 5 is the central result of the entire analysis.")

# lags = list(range(1, 22))
# ftc_r = [-0.0437,-0.0461,-0.0572,-0.0742,-0.0810,-0.0541,-0.0482,
# -0.0376,-0.0601,-0.0600,-0.0452,-0.0347,-0.0630,-0.0705,
# -0.0453,-0.0430,-0.0504,-0.0401,-0.0252,-0.0291,-0.0427]
# pre_r = [ 0.0223, 0.0038,-0.0013, 0.0371, 0.0126, 0.0117,-0.0042,
# -0.0062, 0.0016, 0.0230, 0.0160, 0.0053,-0.0210,-0.0107,
# -0.0203, 0.0196, 0.0198, 0.0021,-0.0101,-0.0029,-0.0164]

# fig = go.Figure()
# fig.add_vrect(x0=4.5, x1=7.5, fillcolor="rgba(245,158,11,0.06)",
# line=dict(color="rgba(245,158,11,0.45)", width=1, dash="dash"),
# annotation_text="5–7 Day window", annotation_position="top",
# annotation_font=dict(family="Roboto Mono", size=10, color=C["amber"]))
# fig.add_hline(y=0, line_color=G["zero"], line_width=1.2)
# fig.add_trace(go.Scatter(
# x=lags, y=ftc_r, name="Freeze-Thaw Count (FTC)",
# mode="lines+markers",
# line=dict(color=C["red"], width=2.8, shape="spline"),
# marker=dict(size=[18 if i==4 else 6 for i in range(21)],
# color=[C["red"] if i==4 else "rgba(239,68,68,0.38)" for i in range(21)],
# symbol=["star" if i==4 else "circle" for i in range(21)],
# line=dict(color="rgba(0,0,0,0.1)", width=1)),
# fill="tozeroy", fillcolor="rgba(239,68,68,0.06)",
# hovertemplate="Day %{x} lag — FTC r = %{y:.4f}<extra></extra>"))
# fig.add_trace(go.Scatter(
# x=lags, y=pre_r, name="Precipitation",
# mode="lines+markers",
# line=dict(color=C["blue"], width=1.8, dash="dot", shape="spline"),
# marker=dict(size=5, color="rgba(59,130,246,0.5)",
# line=dict(color="rgba(0,0,0,0.08)", width=1)),
# hovertemplate="Day %{x} lag — Precip r = %{y:.4f}<extra></extra>"))
# fig.add_annotation(x=5, y=-0.081,
# text=" Day 5 · r = −0.081",
# showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor=C["red"],
# ax=88, ay=-62,
# font=dict(family="Sora", size=12, color=C["red"]),
# bgcolor="rgba(8,14,31,0.9)", bordercolor="rgba(239,68,68,0.5)",
# borderwidth=1, borderpad=8)
# fig = pset(fig, h=420, l=65, r=30, t=46, b=54)
# fig.update_layout(
# title=dict(text="Spearman Cross-Correlation: Freeze-Thaw Events → Pothole Complaints · Lags 1–21 Days",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# xaxis=dict(title="Days After the Weather Event", tickvals=lags, tickfont=dict(size=10.5)),
# yaxis=dict(title="Spearman r", range=[-0.105, 0.065]))
# st.plotly_chart(fig, use_container_width=True)

# c1, c2, c3, c4 = st.columns(4, gap="small")
# with c1: kpi("FTC Peak Lag", "Day 5", "r = −0.081 (all years)", "var(--red)", "var(--red-bdr)")
# with c2: kpi("Spring-Only r", "−0.143", "p = 0.0003 ", "var(--red)", "var(--red-bdr)")
# with c3: kpi("Spring Amplification","3×", "stronger than full year", "var(--amber)", "var(--amber-bdr)")
# with c4: kpi("Action Window", "5–7 days", "pre-stage on FT day 0", "var(--blue)", "var(--blue-bdr)")

# divider()
# cl, cr = st.columns(2, gap="large")
# with cl:
# box("How to Read This Chart",
# "Each point on the X-axis is the number of days between a weather event and the "
# "daily complaint count being measured. The FTC line dips "
# "<strong style='color:var(--text)'>negative</strong> because during active freeze "
# "seasons, citizens haven't yet discovered the potholes — complaints are temporarily "
# "suppressed. Day 5 is where the delayed surge peaks.", "var(--blue)")
# with cr:
# box("Why the Spring Signal Is 3× Stronger",
# "The all-year r of −0.081 triples to −0.143 (p = 0.0003) when restricted to "
# "March–May. All accumulated winter damage becomes visible simultaneously in spring, "
# "making the FT → complaint relationship its tightest and most operationally useful.",
# "var(--red)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 5 — PREDICTORS
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 5:
# slide_header("05", "Weather Predictor Ranking",
# "Rolling weather features ranked by Spearman r against daily pothole counts. "
# "Negative r = active-freeze suppression. Positive r = rain-driven surge.")

# cl, cr = st.columns([1.42, 1], gap="large")
# with cl:
# features = [
# ("FTC 14-day", -0.0870, C["red"], True),
# ("Precip × FTC 7-day", -0.0461, "rgba(239,68,68,0.52)", True),
# ("Snow 7-day", -0.0369, C["slate"]),
# ("Snow 14-day", -0.0338, "rgba(148,163,184,0.68)"),
# ("Snow 5-day", -0.0310, "rgba(148,163,184,0.54)"),
# ("HDD 30-day", -0.0255, C["amber"], True),
# ("Snow 3-day", -0.0145, "rgba(148,163,184,0.38)"),
# ("Rain 3-day", 0.0132, "rgba(59,130,246,0.36)"),
# ("Rain 14-day", 0.0262, "rgba(59,130,246,0.50)"),
# ("Precip 3-day", 0.0451, "rgba(59,130,246,0.62)"),
# ("Rain 7-day", 0.0489, "rgba(59,130,246,0.72)"),
# ("Rain 5-day", 0.0496, "rgba(59,130,246,0.82)"),
# ("Precip 14-day", 0.0534, "#1D4ED8"),
# ("Precip 5-day", 0.0727, "rgba(59,130,246,0.94)"),
# ("Precip 7-day", 0.0734, C["blue"], True),
# ]
# fig = go.Figure(go.Bar(
# x=[f[1] for f in features], y=[f[0] for f in features],
# orientation="h",
# marker=dict(color=[f[2] for f in features], line=dict(width=0), cornerradius=3),
# text=[f"{f[1]:+.4f}" for f in features],
# textposition="outside",
# textfont=dict(family="Roboto Mono", size=10.5, color=G["tick"]),
# hovertemplate="<b>%{y}</b> r = %{x:.4f}<extra></extra>"))
# fig.add_vline(x=0, line_color=G["zero"], line_width=1.5)
# # Quadrant labels
# fig.add_annotation(x=-0.05, y=14.7, text="← Freeze-season suppression",
# showarrow=False, xanchor="right",
# font=dict(family="Roboto Mono", size=9, color="#B91C1C"))
# fig.add_annotation(x=0.05, y=14.7, text="Rain-driven surge →",
# showarrow=False, xanchor="left",
# font=dict(family="Roboto Mono", size=9, color="#1D4ED8"))
# fig = pset(fig, h=530, l=142, r=86, t=44, b=46)
# fig.update_layout(
# title=dict(text="Spearman r · Rolling Weather Features vs Daily Pothole Complaints",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# showlegend=False,
# xaxis=dict(title="Spearman r", range=[-0.112, 0.107]),
# yaxis=dict(tickfont=dict(size=11, color=G["tick"])))
# st.plotly_chart(fig, use_container_width=True)

# with cr:
# st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
# box("FTC 14-day — Strongest Overall",
# "r = −0.087. High FTC periods = active freeze season where same-day complaints "
# "are suppressed. The surge arrives 5 days later — this variable captures the "
# "entire lag mechanism.", "var(--red)")
# box("Precipitation 7-day — Best Positive",
# "r = +0.073. More rain in the past week → more complaints today. Rain "
# "infiltrates existing cracks and directly accelerates both erosion and "
# "freeze-thaw damage.", "var(--blue)")
# box("Snow — Negative for a Different Reason",
# "Heavy snow masks potholes from view. Complaints are suppressed during active "
# "snowfall periods — the surge comes after the snow clears and damage is exposed.",
# "var(--slate)")
# box("Precip × FTC Interaction",
# "r = −0.046. Wet pavement that subsequently freezes creates maximum cracking "
# "stress. The interaction term is 3× stronger in spring — capturing the worst "
# "combination: saturated roads hit by a sudden cold snap.", "var(--amber)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 6 — REGIONAL BREAKDOWN
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 6:
# slide_header("06", "Halifax leads. The signal varies significantly by region.",
# "Region-specific triggers outperform a province-wide blanket alert. "
# "Some regions respond to freeze-thaw; others to rainfall accumulation.")

# regions = ["Halifax /\nLunenburg","Annapolis\nValley","Central NS","Cape Breton","SW Nova\nScotia"]
# reg_flat = ["Halifax / Lunenburg","Annapolis Valley","Central NS","Cape Breton","SW Nova Scotia"]
# n_vals = [10866, 8623, 6148, 4639, 1340]
# p_r = [0.014, 0.094, 0.101, -0.041, 0.000]
# f_r = [-0.125, -0.057, -0.044, -0.029, -0.033]
# h_r = [-0.112, -0.020, -0.011, 0.011, -0.018]
# p_sig = ["ns", "***", "***", "*", "ns"]
# f_sig = ["***", "***", "*", "ns", "ns"]
# h_sig = ["***", "ns", "ns", "ns", "ns"]
# r_accent = ["var(--red)","var(--blue)","var(--amber)","var(--green)","var(--slate)"]

# # Region cards — clean design with strength bar
# pct_map = {"var(--red)":"var(--red-bdr)","var(--blue)":"var(--blue-bdr)",
# "var(--amber)":"var(--amber-bdr)","var(--green)":"var(--green-bdr)",
# "var(--slate)":"var(--slate-bdr)"}
# kpi_cols = st.columns(5, gap="small")
# for col, name, n, ftc, fsig, acc in zip(kpi_cols, regions, n_vals, f_r, f_sig, r_accent):
# sc = "var(--red)" if fsig=="***" else "var(--amber)" if fsig in ("**","*") else "var(--faint)"
# bar_w = int(min(100, abs(ftc) / 0.125 * 100)) # scale to Halifax max
# bdr = pct_map.get(acc, "var(--border)")
# col.markdown(
# f'<div style="background:var(--surface);border:1px solid var(--border);'
# f'border-top:3px solid {acc};border-radius:12px;padding:18px 12px 14px;text-align:center">'
# f'<p style="font-size:11px;font-weight:500;color:var(--sub);margin:0 0 12px;'
# f'white-space:pre-line;line-height:1.4;letter-spacing:0.01em">{name}</p>'
# f'<p style="font-family:\'Instrument Serif\',serif;font-size:1.55rem;font-style:italic;'
# f'color:{acc};margin:0 0 2px;letter-spacing:-0.3px">{n:,}</p>'
# f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--faint);'
# f'text-transform:uppercase;letter-spacing:1px;font-size:11px;margin:0 0 14px">Potholes</p>'
# f'<div style="border-top:1px solid var(--border);padding-top:12px">'
# f'<p style="font-family:\'DM Mono\',monospace;font-size:11px;'
# f'color:var(--sub);margin:0 0 8px">'
# f'FTC&nbsp;r&nbsp;=&nbsp;<strong style="color:{sc};font-size:12px">{ftc:+.3f}</strong>'
# f'&nbsp;<span style="color:{sc};font-size:11.5px;font-weight:600">{fsig}</span></p>'
# f'<div style="background:var(--surface3);border-radius:3px;height:4px;overflow:hidden">'
# f'<div style="width:{bar_w}%;height:4px;background:{acc};border-radius:3px;'
# f'transition:width .6s ease"></div></div>'
# f'<p style="font-size:11px;color:var(--faint);margin:4px 0 0;font-weight:400">'
# f'Signal strength</p>'
# f'</div></div>', unsafe_allow_html=True)

# divider()
# cl, cr = st.columns([1.55, 1], gap="large")
# with cl:
# fig = go.Figure()
# fig.add_hline(y=0, line_color=G["zero"], line_width=1)
# fig.add_hrect(y0=-0.05, y1=0.05, fillcolor="rgba(100,110,140,0.04)", line_width=0,
# annotation_text="weak / not significant zone",
# annotation_position="right",
# annotation_font=dict(family="Roboto Mono", size=9, color=G["tick"]))
# for metric, vals, sigs_list, color, sym in [
# ("7-day Precip r", p_r, p_sig, C["blue"], "circle"),
# ("14-day FTC r", f_r, f_sig, C["red"], "diamond"),
# ("14-day HDD r", h_r, h_sig, C["amber"], "square"),
# ]:
# for rx, ry in zip(reg_flat, vals):
# fig.add_shape(type="line", x0=rx, x1=rx, y0=0, y1=ry,
# line=dict(color=color, width=1.5, dash="dot"), opacity=0.3)
# r_, g_, b_ = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
# # Split into significant and non-significant dots
# # (Plotly marker.line must be a single dict, not a list)
# for is_sig, line_clr, line_w, opacity in [
# (True, color, 2, 0.92),
# (False, G["tick"], 1, 0.32),
# ]:
# mask = [s in ("*","**","***") for s in sigs_list]
# xs = [x for x, m in zip(reg_flat, mask) if m == is_sig]
# ys = [y for y, m in zip(vals, mask) if m == is_sig]
# ss = [s for s, m in zip(sigs_list,mask) if m == is_sig]
# if not xs:
# continue
# sizes = [max(10, abs(v)*290) for v in ys]
# fig.add_trace(go.Scatter(
# x=xs, y=ys, mode="markers+text",
# name=metric if is_sig else None,
# showlegend=is_sig,
# marker=dict(
# symbol=sym, size=sizes,
# color=f"rgba({r_},{g_},{b_},{opacity:.2f})",
# line=dict(color=line_clr, width=line_w),
# ),
# text=[f"{v:+.3f}{s}" for v, s in zip(ys, ss)],
# textposition=["top center" if v >= 0 else "bottom center" for v in ys],
# textfont=dict(family="Roboto Mono", size=9.5, color=color),
# hovertemplate="<b>%{x}</b><br>" + metric + " = %{y:+.3f}<extra></extra>",
# ))
# fig = pset(fig, h=420, l=52, r=75, t=50, b=50)
# fig.update_layout(
# title=dict(text="Spearman r by Region · Three weather drivers compared",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# legend=dict(orientation="h", y=1.08, x=0, font=dict(size=11.5)),
# xaxis=dict(tickfont=dict(size=11.5)),
# yaxis=dict(title="Spearman r", range=[-0.168, 0.155]))
# st.plotly_chart(fig, use_container_width=True)

# # Reading guide
# st.markdown(
# '<div style="background:var(--surface2);border:1px solid var(--border);'
# 'border-radius:8px;padding:14px 18px">'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11px;letter-spacing:2px;'
# 'color:var(--faint);text-transform:uppercase;margin-bottom:10px">Chart guide</p>'
# '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px">'
# '<div><p style="font-size:12px;font-weight:600;color:var(--text);margin:0 0 3px">Dot size</p>'
# '<p style="font-size:11.5px;color:var(--sub);font-weight:400">Larger = stronger |r|</p></div>'
# '<div><p style="font-size:12px;font-weight:600;color:var(--text);margin:0 0 3px">Opacity</p>'
# '<p style="font-size:11.5px;color:var(--sub);font-weight:400">Bright = significant (p&lt;0.05)</p></div>'
# '<div><p style="font-size:12px;font-weight:600;color:var(--text);margin:0 0 3px">Direction</p>'
# '<p style="font-size:11.5px;color:var(--sub);font-weight:400">Above zero = rain-driven; below = freeze-lag suppression</p></div>'
# '</div></div>', unsafe_allow_html=True)

# with cr:
# box("Halifax / Lunenburg — Priority",
# "FTC r = −0.125 (***). Strongest freeze-thaw signal province-wide. "
# "33.9% of all pothole complaints originate here — the highest ROI region for "
# "an early-alert deployment.", "var(--red)")
# box("Annapolis Valley & Central NS",
# "Precipitation dominates: r ≈ +0.09–0.10 (***). These inland regions respond "
# "to rainfall rather than temperature cycling. Use a 7-day cumulative rainfall "
# "threshold as the alert trigger — not FTC count.", "var(--blue)")
# box("Cape Breton — Maritime Effect",
# "The Atlantic Ocean moderates temperature extremes, producing fewer complete "
# "freeze-thaw cycles. FTC signal is weak and non-significant, though "
# "precipitation remains marginally significant (r = −0.041*).", "var(--amber)")
# box("SW Nova Scotia — Data Gap",
# "Yarmouth A has no precipitation data in the ECCC archive for this period. "
# "Non-significant results almost certainly reflect the missing data, not a "
# "genuine absence of the freeze-thaw effect.", "var(--slate)")
# st.markdown(
# '<div style="background:var(--surface);border:1px solid var(--border);'
# 'border-radius:10px;padding:18px;margin-top:4px">'
# '<p style="font-family:\'DM Mono\',monospace;font-size:11px;font-weight:500;'
# 'color:var(--faint);text-transform:uppercase;letter-spacing:2px;margin:0 0 14px">'
# 'Recommended trigger by region</p>'
# '<table style="width:100%;border-collapse:collapse">'
# + "".join(
# f'<tr style="border-bottom:1px solid var(--border)">'
# f'<td style="padding:9px 8px 9px 0;font-size:12.5px;font-weight:{"400" if r!="SW Nova Scotia" else "300"};'
# f'color:{"var(--text2)" if r!="SW Nova Scotia" else "var(--faint)"}">{r}</td>'
# f'<td style="font-family:DM Mono,monospace;font-size:11px;color:{c};text-align:right;padding:9px 0">{t}</td>'
# f'</tr>'
# for r, c, t in [
# ("Halifax", "var(--red)", "FTC 14d ≥ 5"),
# ("Annapolis / Central", "var(--blue)", "Precip 7d ≥ 25mm"),
# ("Cape Breton", "var(--amber)", "Precip 7d ≥ 20mm"),
# ("SW Nova Scotia", "var(--faint)", "No data"),
# ])
# + '</table></div>', unsafe_allow_html=True)

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 7 — REGRESSION
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 7:
# slide_header("07", "Five weather variables independently predict daily complaint counts.",
# "OLS with HC3 robust standard errors. Weekdays only, 2019–2025. R² = 0.072.")

# cl, cr = st.columns([1.32, 1], gap="large")
# with cl:
# predictors = [
# ("7-day Total Precip", 0.05, False),
# ("7-day Rain", -0.02, False),
# ("14-day Heating Degree Days",-0.02, True),
# ("Precip × FTC (7-day)", 0.11, True),
# ("7-day Cumulative Snow", 0.23, True),
# ("14-day FTC Count", -0.67, True),
# ("Spring Season (Mar–May)", 4.59, True),
# ]
# ci = [0.07, 0.09, 0.008, 0.04, 0.09, 0.08, 0.60]
# p_c = [C["red"] if p[2] else "rgba(148,163,184,0.26)" for p in predictors]

# fig = go.Figure()
# fig.add_trace(go.Bar(
# x=[p[1] for p in predictors], y=[p[0] for p in predictors],
# orientation="h",
# marker=dict(color=p_c, line=dict(width=0), cornerradius=4),
# hovertemplate="<b>%{y}</b> coeff = %{x:+.2f}<extra></extra>",
# showlegend=False))
# fig.add_trace(go.Scatter(
# x=[p[1] for p in predictors], y=[p[0] for p in predictors],
# mode="markers",
# marker=dict(symbol="line-ns", size=12,
# color="rgba(100,110,140,0.65)",
# line=dict(color=G["tick"], width=1.8)),
# error_x=dict(type="data", array=ci, color=G["tick"], thickness=1.5, width=5),
# showlegend=False, hoverinfo="skip"))
# for i, (name, val, sig) in enumerate(predictors):
# xpos = val + ci[i] + 0.18
# fig.add_annotation(x=xpos, y=name, text=f"{val:+.2f} {'' if sig else 'ns'}",
# showarrow=False, xanchor="left",
# font=dict(family="Roboto Mono", size=10.5,
# color=C["red"] if sig else G["tick"]))
# fig.add_vline(x=0, line_color=G["zero"], line_width=1.5)
# fig = pset(fig, h=368, l=218, r=26, t=42, b=50)
# fig.update_layout(
# title=dict(text="OLS Coefficients · R² = 0.072 · HC3 Robust SE",
# font=dict(family="Sora", size=13.5, color=G["tick"])),
# showlegend=False,
# xaxis=dict(title="Extra daily complaints per unit increase", range=[-1.1, 7.8]),
# yaxis=dict(tickfont=dict(size=12)))
# st.plotly_chart(fig, use_container_width=True)

# ca, cb_ = st.columns(2, gap="small")
# with ca:
# box("5 Significant ",
# "Spring Season, FTC 14d, Snow 7d, Precip×FTC, HDD 14d — all pass "
# "p < 0.05 with HC3 robust standard errors.", "var(--red)")
# with cb_:
# box("2 Non-Significant",
# "Rain 7d (p = 0.807) and Precip 7d (p = 0.439) are absorbed by "
# "collinear predictors in the full model.", "var(--slate)")

# with cr:
# rows = [
# ("Spring Season", "+4.59", "<0.001", True),
# ("FTC 14d", "−0.67", "<0.001", True),
# ("Snow 7d", "+0.23", "0.009", True),
# ("Precip×FTC", "+0.11", "0.006", True),
# ("HDD 14d", "−0.02", "0.007", True),
# ("Rain 7d", "−0.02", "0.807", False),
# ("Precip 7d", "+0.05", "0.439", False),
# ]
# hdr = (
# '<tr style="border-bottom:1px solid var(--border2)">'
# '<th style="font-family:DM Mono,monospace;font-size:11px;color:var(--faint);'
# 'text-transform:uppercase;letter-spacing:1.5px;padding:10px 10px 10px 0;'
# 'font-weight:400;text-align:left">Predictor</th>'
# '<th style="font-family:DM Mono,monospace;font-size:11px;color:var(--faint);'
# 'text-transform:uppercase;letter-spacing:1.5px;padding:10px;'
# 'font-weight:400;text-align:right">Coef.</th>'
# '<th style="font-family:DM Mono,monospace;font-size:11px;color:var(--faint);'
# 'text-transform:uppercase;letter-spacing:1.5px;padding:10px 0;'
# 'font-weight:400;text-align:right">p-value</th></tr>'
# )
# bdy = "".join(
# f'<tr style="border-bottom:1px solid var(--border)">'
# f'<td style="padding:10px 10px 10px 0;font-size:13px;'
# f'font-weight:{"500" if sig else "300"};'
# f'color:{"var(--text)" if sig else "var(--faint)"}">{name}</td>'
# f'<td style="font-family:DM Mono,monospace;font-size:12px;'
# f'color:{"var(--amber)" if sig else "var(--faint)"};'
# f'padding:10px;text-align:right">{coef}</td>'
# f'<td style="font-family:DM Mono,monospace;font-size:11px;'
# f'color:{"var(--green)" if sig else "var(--faint)"};'
# f'text-align:right">{pval}</td>'
# f'</tr>'
# for name, coef, pval, sig in rows
# )
# st.markdown(
# f'<div style="background:var(--surface);border:1px solid var(--border);'
# f'border-radius:10px;padding:20px;margin-bottom:13px">'
# f'<p style="font-family:DM Mono,monospace;font-size:11px;font-weight:500;'
# f'color:var(--faint);text-transform:uppercase;letter-spacing:2px;margin:0 0 13px">'
# f'Coefficient Table</p>'
# f'<table style="width:100%;border-collapse:collapse">{hdr}{bdy}</table>'
# f'</div>', unsafe_allow_html=True)
# box("Why R² = 7.2% Is Acceptable",
# "Weather explains 7.2% of daily variance. Road age, traffic volume, and pavement "
# "condition account for the rest — none of which are in this dataset. 7.2% is still "
# "sufficient to build a reliable operational alert trigger.", "var(--amber)")
# box("Why FTC Has a Negative Coefficient",
# "High FTC = active winter freeze season where same-day complaints are suppressed. "
# "The Spring Season dummy (+4.59) captures the full delayed wave once the lag expires.",
# "var(--red)")

# # ══════════════════════════════════════════════════════════════════════════════
# # SLIDE 8 — ACTION PLAN
# # ══════════════════════════════════════════════════════════════════════════════
# elif S == 8:
# slide_header("08", "Three findings. One early-warning system.",
# "The analysis supports a weather-triggered, regionally-differentiated maintenance "
# "alert that converts NS TIR from reactive to proactive operations.")

# cl, cr = st.columns(2, gap="large")
# with cl:
# label("Core findings")
# findings = [
# ("var(--red)", "1", "A measurable 5-day lag exists",
# "Spearman r = −0.081 at Day 5. Spring-only: r = −0.143, p = 0.0003. "
# "Consistent and statistically significant across all 6 years."),
# ("var(--blue)", "2", "Weather explains 7.2% of daily variance",
# "Spring Season (+4.59), FTC 14d (−0.67), and Snow 7d (+0.23) are the dominant "
# "significant OLS predictors under HC3 robust standard errors."),
# ("var(--amber)", "3", "Halifax requires priority alert triage",
# "FTC r = −0.125 (***). Annapolis and Central NS are precipitation-driven. "
# "Region-differentiated alerts outperform province-wide blanket warnings."),
# ]
# items = ""
# for i, (color, num, title, body) in enumerate(findings):
# sep = "padding-bottom:20px;border-bottom:1px solid var(--divider);margin-bottom:20px;" if i < 2 else ""
# items += (
# f'<div style="display:flex;gap:18px;align-items:flex-start;{sep}">'
# f'<div style="font-family:\'Instrument Serif\',serif;font-size:1.6rem;font-style:italic;'
# f'color:{color};line-height:1;flex-shrink:0;width:28px;padding-top:2px">{num}</div>'
# f'<div>'
# f'<p style="font-size:14px;font-weight:600;color:var(--text);margin:0 0 5px">{title}</p>'
# f'<p style="font-size:13px;color:var(--sub);line-height:1.75;font-weight:400">{body}</p>'
# f'</div></div>')
# st.markdown(
# f'<div style="background:var(--surface);border:1px solid var(--border);'
# f'border-radius:12px;padding:26px">{items}</div>', unsafe_allow_html=True)

# with cr:
# label("Proposed 3-tier alert system")
# for acc, title, body in [
# ("var(--red)", "HIGH ALERT — Deploy Now",
# "≥5 FT days in rolling 14d, OR thaw after 3+ consecutive freezing days. "
# "Pre-stage full patching crews within 5 days. Prioritise Halifax."),
# ("var(--amber)", "MEDIUM ALERT — Monitor",
# "2–4 FT days in 14d window, OR 7-day precip > 25 mm. "
# "Schedule patrols and pre-stock materials at priority depots."),
# ("var(--blue)", "LOW ALERT — Routine",
# "0–1 FT days, normal precipitation. Standard reactive complaint-response."),
# ]:
# bg, bdr = ACC.get(acc, ("var(--surface2)", "var(--border)"))
# st.markdown(
# f'<div style="background:{bg};border:1px solid {bdr};border-left:3px solid {acc};'
# f'border-radius:10px;padding:15px 17px;margin-bottom:10px">'
# f'<p style="font-size:12px;font-weight:600;color:{acc};margin:0 0 6px">{title}</p>'
# f'<p style="font-size:13px;color:var(--text2);line-height:1.72;font-weight:400">{body}</p>'
# f'</div>', unsafe_allow_html=True)

# divider()
# c1, c2, c3 = st.columns(3, gap="large")
# with c1:
# box("Data Limitations",
# "Yarmouth A has no precipitation data. Greenwood A has no rain/snow split. "
# "Weather explains only 7.2% of variance — road age and traffic volume are "
# "the dominant unmeasured confounders.", "var(--amber)")
# with c2:
# box("Recommended Next Steps",
# "① Connect live ECCC forecast API for real-time FTC monitoring.<br>"
# "② Add road age and Pavement Condition Index as model covariates.<br>"
# "③ Pilot the alert system with Halifax depot for one full spring season.",
# "var(--green)")
# with c3:
# box("Expected Impact",
# "Early-warning deployment could reduce average pothole response time from "
# "5–7 days (reactive) to 1–2 days (proactive). Fewer complaints, lower "
# "patching cost, measurably better citizen service.", "var(--blue)")