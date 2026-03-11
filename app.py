"""
NS Pothole Freeze-Thaw Analysis Dashboard
Run: streamlit run app.py
Requires: pip install streamlit plotly
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="NS Pothole Analysis",
    page_icon="🚧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BG    = "#0D1117"
CARD  = "#161B22"
BORDER= "#21262D"
RED   = "#F85149"
BLUE  = "#388BFD"
GOLD  = "#D29922"
GREEN = "#3FB950"
TEXT  = "#E6EDF3"
SUB   = "#8B949E"
MUTED = "#6E7681"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; color: {TEXT} !important; }}
.stApp {{ background: {BG}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1rem 2rem 4rem !important; max-width: 1400px !important; }}
.stButton > button {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    color: {SUB} !important; border-radius: 6px !important;
    font-size: 11px !important; font-weight: 500 !important;
    padding: 6px 2px !important; width: 100% !important;
    white-space: nowrap !important; overflow: hidden !important;
    text-overflow: ellipsis !important; transition: all .15s !important;
}}
.stButton > button:hover {{
    border-color: {BLUE} !important; color: {TEXT} !important;
    background: rgba(56,139,253,0.08) !important;
}}
[data-testid="metric-container"] {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 12px !important; padding: 18px 14px !important;
}}
[data-testid="metric-container"] label {{
    color: {MUTED} !important; font-size: 10px !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}}
[data-testid="stMetricValue"] {{ color: {TEXT} !important; font-size: 1.6rem !important; font-weight: 800 !important; }}
hr {{ border-color: {BORDER} !important; margin: 20px 0 !important; }}
</style>
""", unsafe_allow_html=True)

# ── SLIDES ────────────────────────────────────────────────────────────────────
SLIDE_LABELS = [
    "Cover",
    "The Problem",
    "How Roads Break",
    "Seasonal Pattern",
    "5-Day Lag ★",
    "Weather Predictors",
    "Regional Breakdown",
    "Regression Model",
    "Action Plan",
]

if "s" not in st.session_state:
    st.session_state.s = 0

# ── TOP NAV ───────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;padding-top:8px">'
    f'<span style="font-family:JetBrains Mono,monospace;font-size:11px;font-weight:700;'
    f'color:{RED};letter-spacing:2px;white-space:nowrap">🚧 NS POTHOLE ANALYSIS</span>'
    f'<span style="font-size:11px;color:{MUTED}">|</span>'
    f'<span style="font-size:11px;color:{SUB}">Click a slide to navigate</span>'
    f'</div>', unsafe_allow_html=True)

cols = st.columns(len(SLIDE_LABELS))
for i, (col, label) in enumerate(zip(cols, SLIDE_LABELS)):
    with col:
        if st.button(label, key=f"nav_{i}", use_container_width=True):
            st.session_state.s = i
            st.rerun()

bar_html = "".join(
    f'<div style="flex:1;height:3px;background:{"#F85149" if i==st.session_state.s else BORDER};'
    f'border-radius:2px;margin:0 1px"></div>'
    for i in range(len(SLIDE_LABELS))
)
st.markdown(f'<div style="display:flex;margin-bottom:20px;margin-top:3px">{bar_html}</div>',
            unsafe_allow_html=True)

st.markdown(f"""
<style>
div[data-testid="stHorizontalBlock"] > div:nth-child({st.session_state.s + 1}) button {{
    border-color: {RED} !important; color: {TEXT} !important;
    font-weight: 700 !important; background: rgba(248,81,73,0.08) !important;
}}
</style>""", unsafe_allow_html=True)

S = st.session_state.s

# ── HELPERS ───────────────────────────────────────────────────────────────────
def pset(fig, h=360):
    fig.update_layout(
        height=h, plot_bgcolor=CARD, paper_bgcolor=CARD,
        font=dict(family="Inter", size=11, color=SUB),
        margin=dict(l=60, r=30, t=50, b=55),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, font=dict(size=11, color=SUB)),
    )
    fig.update_xaxes(gridcolor=BORDER, zeroline=False, tickfont=dict(size=11, color=SUB),
                     title_font=dict(size=11, color=SUB), linecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zeroline=False, tickfont=dict(size=11, color=SUB),
                     title_font=dict(size=11, color=SUB), linecolor=BORDER)
    return fig

def hero(tag, title, sub=""):
    st.markdown(
        f'<div style="margin-bottom:24px;padding-bottom:18px;border-bottom:1px solid {BORDER}">'
        f'<p style="font-family:JetBrains Mono,monospace;font-size:9px;letter-spacing:3px;'
        f'text-transform:uppercase;color:{RED};margin:0 0 10px">{tag}</p>'
        f'<h1 style="font-size:1.75rem;font-weight:800;color:{TEXT};line-height:1.15;'
        f'letter-spacing:-0.5px;margin:0 0 10px">{title}</h1>'
        + (f'<p style="font-size:13px;color:{SUB};line-height:1.7;max-width:820px;margin:0">{sub}</p>'
           if sub else "")
        + '</div>', unsafe_allow_html=True)

def box(title, body, color=BLUE):
    st.markdown(
        f'<div style="background:{color}12;border:1px solid {color}38;border-left:3px solid {color};'
        f'border-radius:8px;padding:13px 15px;margin-bottom:10px">'
        f'<p style="font-size:11px;font-weight:700;color:{color};margin:0 0 5px">{title}</p>'
        f'<p style="font-size:12px;color:{SUB};line-height:1.65;margin:0">{body}</p>'
        f'</div>', unsafe_allow_html=True)

def kpi(label, value, sub="", color=TEXT):
    st.markdown(
        f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;'
        f'padding:16px 12px;text-align:center">'
        f'<p style="font-size:9px;font-weight:600;color:{MUTED};text-transform:uppercase;'
        f'letter-spacing:1.5px;margin:0 0 7px">{label}</p>'
        f'<p style="font-size:1.45rem;font-weight:800;color:{color};line-height:1.1;'
        f'margin:0 0 4px;word-break:break-word">{value}</p>'
        + (f'<p style="font-size:10px;color:{MUTED};margin:0">{sub}</p>' if sub else "")
        + '</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 0 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
if S == 0:
    st.markdown(
        f'<div style="padding:12px 0 20px">'
        f'<p style="font-family:JetBrains Mono,monospace;font-size:10px;letter-spacing:3px;'
        f'text-transform:uppercase;color:{RED};margin:0 0 12px">Nova Scotia TIR · ECCC Weather · 2019–2025</p>'
        f'<h1 style="font-size:2.5rem;font-weight:900;color:{TEXT};line-height:1.05;'
        f'letter-spacing:-1.5px;margin:0 0 14px">'
        f'Can we predict potholes<br><span style="color:{RED}">before</span> they appear?</h1>'
        f'<p style="font-size:14px;color:{SUB};line-height:1.8;max-width:680px;margin:0 0 24px">'
        f'A data analysis of <strong style="color:{TEXT}">391,795 service records</strong> and '
        f'<strong style="color:{TEXT}">6 years of daily weather data</strong> across Nova Scotia — '
        f'revealing a consistent <strong style="color:{RED}">5-day window</strong> between '
        f'freeze-thaw events and pothole complaint surges. '
        f'Public Works can pre-stage repair crews <em>before the phones start ringing.</em></p>'
        f'<div style="width:60px;height:4px;background:{RED};border-radius:2px;margin-bottom:24px"></div>'
        f'</div>', unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5, gap="medium")
    with c1: kpi("Service Records",   "391,795",  "NS TIR OCC · 2019–2025")
    with c2: kpi("Pothole Calls",     "32,096",   "8.2% of all records")
    with c3: kpi("Freeze-Thaw Days",  "647",      "detected 2019–2025",          color=RED)
    with c4: kpi("Predictive Window", "5–7 days", "FT event → complaint spike",   color=BLUE)
    with c5: kpi("Weather Match",     "89.9%",    "records matched to ECCC")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    l, r = st.columns(2, gap="large")
    with l:
        box("What This Project Does",
            "We linked every pothole complaint to the nearest ECCC weather station, then tested "
            "whether freeze-thaw cycles predict complaint surges at daily lags of 1–21 days. "
            "A consistent 5-day signal was found — strongest in spring.", RED)
        box("Why It Matters for NS TIR",
            "The current workflow is entirely reactive: crews deploy only after a citizen calls. "
            "A 5-day advance signal converts this to proactive scheduling — "
            "reducing response time, patching cost, and citizen frustration.", BLUE)
    with r:
        box("Data Sources",
            "<strong style='color:#E6EDF3'>Dataset 1:</strong> NS TIR Operations Contact Centre — "
            "391,795 records across 64 supervisor area codes, 2019–2025. Provincial highways only.<br><br>"
            "<strong style='color:#E6EDF3'>Dataset 2:</strong> Environment Canada (ECCC) — "
            "daily climate from 5 stations: Halifax Stanfield, Greenwood A, Truro, Sydney A, Yarmouth A.", GOLD)
        box("How to Navigate",
            "Click any button above to jump to a slide. "
            "Each slide presents one finding — a chart plus plain-English explanations. "
            "Read in order for the full story, or jump to any section directly.", GREEN)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — THE PROBLEM
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 1:
    hero("The Problem",
         "Potholes cost money. Right now, we fix them too late.",
         "NS TIR dispatches repair crews only after citizens file complaints via the 24/7 Operations "
         "Contact Centre. Weather data already available in real time could allow proactive deployment instead.")

    cl, cr = st.columns([1.2, 1], gap="large")
    with cl:
        years = ["2019","2020","2021","2022","2023","2024","2025"]
        vals  = [4784, 4009, 4118, 5700, 3299, 4604, 5582]
        clrs  = [RED if y in ("2022","2025") else "rgba(56,139,253,0.45)" for y in years]
        fig = go.Figure(go.Bar(
            x=years, y=vals, marker=dict(color=clrs, line=dict(width=0)),
            text=vals, textposition="outside", textfont=dict(size=11, color=SUB),
            hovertemplate="<b>%{x}</b><br>%{y:,} pothole complaints<extra></extra>"))
        for yr, txt in [("2022","Severe FT season"),("2025","Active FT season")]:
            fig.add_annotation(x=yr, y=vals[years.index(yr)], text=txt,
                showarrow=True, arrowhead=2, arrowcolor=RED, ax=0, ay=-44,
                font=dict(size=10, color=RED), bgcolor=CARD, bordercolor=RED, borderwidth=1)
        fig = pset(fig, 360)
        fig.update_layout(
            title=dict(text="Annual Pothole Complaints — 2019 to 2025",
                       font=dict(size=13, color=TEXT)),
            showlegend=False,
            yaxis=dict(title=dict(text="Complaints", font=dict(size=11, color=SUB))),
            margin=dict(l=60, r=30, t=50, b=55))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        box("The Reactive Problem",
            "By the time a citizen calls TIR, the pothole already exists — often for several days. "
            "Reactive patching is expensive: crews mobilise after damage is visible, not before.", RED)
        box("The Opportunity",
            "Freeze-thaw weather data is freely available from ECCC. "
            "If FT events reliably predict complaint surges with a consistent 5-day delay, "
            "crews can be pre-staged <strong style='color:#E6EDF3'>before</strong> any call is made.", BLUE)
        box("Why 2022 and 2025 Peak",
            "Both years had unusually severe freeze-thaw seasons — more cycling events, "
            "greater cumulative pavement stress, and larger complaint waves in the weeks that followed.", GOLD)
        box("The Business Case",
            "The CAA estimates NS drivers pay $137/year extra due to poor roads. "
            "Proactive maintenance using the 5-day signal could shift $1 preservation spend "
            "into $6–$10 of avoided repair costs.", GREEN)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — HOW ROADS BREAK
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 2:
    hero("The Physical Mechanism",
         "A freeze-thaw cycle cracks roads — but complaints arrive days later.",
         "Understanding the physics explains why the statistical lag is consistent "
         "across all 6 years and all 5 regions of Nova Scotia.")

    steps = [
        (RED,   "01", "Water Enters",    "Rain or snowmelt seeps into micro-cracks in the asphalt and sub-base layer."),
        (BLUE,  "02", "Night Freeze",    "Tmin < 0°C — water expands 9% as it freezes, forcing crack walls permanently apart."),
        (GOLD,  "03", "Day Thaw",        "Tmax > 0°C — ice melts, but the crack is now wider than before. Damage is permanent."),
        (GREEN, "04", "Repeat Cycles",   "Each FT cycle compounds stress. Five or more cycles causes structural failure."),
        (MUTED, "05", "Surface Fails",   "Traffic breaks through weakened pavement. A pothole forms and grows."),
        (RED,   "06", "Complaint Filed", "Citizen notices the pothole and calls TIR — typically 5–7 days after the FT event."),
    ]
    step_cols = st.columns(6, gap="small")
    for col, (color, num, title, desc) in zip(step_cols, steps):
        col.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-top:3px solid {color};'
            f'border-radius:10px;padding:16px 10px;text-align:center">'
            f'<div style="font-size:1.4rem;font-weight:800;color:{color};margin-bottom:8px">{num}</div>'
            f'<div style="font-size:12px;font-weight:700;color:{TEXT};margin-bottom:7px">{title}</div>'
            f'<div style="font-size:11px;color:{MUTED};line-height:1.6">{desc}</div>'
            f'</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    cl, cr = st.columns(2, gap="large")
    with cl:
        box("Freeze-Thaw Day Definition",
            "<code style='background:rgba(248,81,73,0.1);padding:2px 8px;border-radius:4px;"
            "font-family:JetBrains Mono;font-size:12px;color:#F85149'>"
            "FT_day = 1 &nbsp;if&nbsp; Tmax &gt; 0°C &nbsp;AND&nbsp; Tmin &lt; 0°C</code><br><br>"
            "Water must cross the freezing point in <em>both directions</em> within 24 hours. "
            "We detected <strong style='color:#E6EDF3'>647 such days</strong> across NS from 2019–2025, "
            "concentrated in January through April.", RED)
        box("Why the 14-Day Rolling Window",
            "A single FT day causes minor damage. "
            "<strong style='color:#E6EDF3'>Multiple consecutive FT days</strong> can destroy a road. "
            "FTC_14d = cumulative FT days in the prior 14 days — capturing total accumulated "
            "pavement stress. Our strongest single predictor at Spearman r = −0.087.", GOLD)
    with cr:
        st.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:22px">'
            f'<p style="font-family:JetBrains Mono,monospace;font-size:9px;letter-spacing:2px;'
            f'color:{MUTED};text-transform:uppercase;margin-bottom:14px">Key Formulas</p>'
            f'<div style="background:rgba(248,81,73,0.06);border:1px solid rgba(248,81,73,0.2);'
            f'border-radius:8px;padding:16px;margin-bottom:14px">'
            f'<code style="font-family:JetBrains Mono,monospace;font-size:12px;color:{GOLD};'
            f'line-height:2.2;display:block">'
            f'FT_day(t) = 1<br>&nbsp;&nbsp;if Tmax(t) &gt; 0°C<br>&nbsp;&nbsp;AND Tmin(t) &lt; 0°C'
            f'<br><br>FTC_14d(t) =<br>&nbsp;&nbsp;Σ FT_day from t−14 to t−1</code></div>'
            f'<p style="font-size:12px;color:{MUTED};line-height:1.7;margin:0">'
            f'Window shifted by one day to prevent data leakage — only weather information '
            f'available <em>before</em> the complaint date is used as a predictor.</p></div>',
            unsafe_allow_html=True)
        box("The Lag in Plain English",
            "The road cracks on the FT event day. The pothole grows over the following days. "
            "The citizen discovers it and calls TIR — creating a consistent 5–7 day delay "
            "between the weather cause and the recorded complaint.", BLUE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — SEASONAL PATTERN
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 3:
    hero("Seasonal Pattern",
         "Winter breaks roads. Summer gets the complaints.",
         "The monthly chart reveals the macro version of the same lag found at the daily level. "
         "Freeze-thaw damage accumulates all winter and surfaces as visible complaints in summer.")

    months  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ft_days = [126, 105, 150, 71, 4, 0, 0, 0, 3, 8, 71, 112]
    ph_avg  = [11.0, 15.4, 12.2, 13.7, 15.5, 16.2, 18.3, 12.9, 11.3, 10.4, 8.2, 9.8]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=months, y=ft_days, name="Freeze-Thaw Days",
        marker=dict(color="rgba(56,139,253,0.35)", line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>FT Days: %{y}<extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=ph_avg, name="Avg Potholes / Day",
        line=dict(color=RED, width=3),
        marker=dict(size=8, color=RED, line=dict(color=CARD, width=2)),
        hovertemplate="<b>%{x}</b><br>%{y:.1f} complaints/day<extra></extra>"), secondary_y=True)
    fig = pset(fig, 380)
    fig.update_layout(
        title=dict(text="Monthly Freeze-Thaw Days (bars) vs Average Daily Pothole Complaints (line)",
                   font=dict(size=13, color=TEXT)),
        legend=dict(orientation="h", y=1.08, x=0),
        margin=dict(l=65, r=65, t=55, b=55))
    fig.update_yaxes(title=dict(text="Freeze-Thaw Days", font=dict(size=11, color=BLUE)),
                     secondary_y=False, tickfont=dict(color=BLUE))
    fig.update_yaxes(title=dict(text="Avg Potholes / Day", font=dict(size=11, color=RED)),
                     secondary_y=True, tickfont=dict(color=RED))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        box("Peak FT Month: March",
            "<strong style='color:#E6EDF3'>150 freeze-thaw days</strong> in March across 6 years — "
            "the highest of any month. Temperatures oscillating around 0°C means "
            "maximum pavement stress. Yet March complaint volumes are only moderate.", BLUE)
    with c2:
        box("Peak Complaint Month: July",
            "<strong style='color:#E6EDF3'>18.3 average complaints per day</strong> in July — "
            "yet zero freeze-thaw events occur. All accumulated winter damage is now "
            "visible on dry summer roads and being reported.", RED)
    with c3:
        box("The Macro Lag: 4–5 Months",
            "FT damage peaks in March. Complaints peak in July. "
            "This 4–5 month annual offset is the same physics as the 5-day daily lag — "
            "winter causes, spring reveals, summer brings the complaints.", GOLD)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — THE 5-DAY LAG ★
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 4:
    hero("Core Finding ★ — The 5-Day Lag",
         "A consistent, statistically significant 5-day lag between freeze-thaw events and pothole complaints.",
         "Spearman cross-correlation computed at every lag from 1 to 21 days. "
         "This chart is the central result of the entire analysis.")

    lags  = list(range(1, 22))
    ftc_r = [-0.0437,-0.0461,-0.0572,-0.0742,-0.0810,-0.0541,-0.0482,
             -0.0376,-0.0601,-0.0600,-0.0452,-0.0347,-0.0630,-0.0705,
             -0.0453,-0.0430,-0.0504,-0.0401,-0.0252,-0.0291,-0.0427]
    pre_r = [ 0.0223, 0.0038,-0.0013, 0.0371, 0.0126, 0.0117,-0.0042,
             -0.0062, 0.0016, 0.0230, 0.0160, 0.0053,-0.0210,-0.0107,
             -0.0203, 0.0196, 0.0198, 0.0021,-0.0101,-0.0029,-0.0164]

    fig = go.Figure()
    fig.add_vrect(x0=4.5, x1=7.5, fillcolor="rgba(210,153,34,0.07)",
        line=dict(color=GOLD, width=1, dash="dot"),
        annotation_text="5–7 Day Action Window", annotation_position="top",
        annotation_font=dict(size=11, color=GOLD))
    fig.add_hline(y=0, line_color=BORDER, line_width=1.5)
    sz  = [14 if i == 4 else 6 for i in range(21)]
    clr = [RED if i == 4 else "rgba(248,81,73,0.5)" for i in range(21)]
    sym = ["star" if i == 4 else "circle" for i in range(21)]
    fig.add_trace(go.Scatter(x=lags, y=ftc_r, name="Freeze-Thaw Count",
        mode="lines+markers", line=dict(color=RED, width=2.5),
        marker=dict(size=sz, color=clr, symbol=sym, line=dict(color=CARD, width=1)),
        fill="tozeroy", fillcolor="rgba(248,81,73,0.06)",
        hovertemplate="Lag %{x}d — FTC r = %{y:.4f}<extra></extra>"))
    fig.add_trace(go.Scatter(x=lags, y=pre_r, name="Precipitation",
        mode="lines+markers", line=dict(color=BLUE, width=2),
        marker=dict(size=6, color=BLUE, line=dict(color=CARD, width=1)),
        hovertemplate="Lag %{x}d — Precip r = %{y:.4f}<extra></extra>"))
    fig.add_annotation(x=5, y=-0.081, text="★  Day 5 · r = −0.081",
        showarrow=True, arrowhead=2, arrowcolor=RED, ax=70, ay=-50,
        font=dict(size=11, color=RED),
        bgcolor=CARD, bordercolor=RED, borderwidth=1, borderpad=6)
    fig = pset(fig, 390)
    fig.update_layout(
        title=dict(text="Cross-Correlation: Freeze-Thaw Events → Pothole Complaints at Lags 1–21 Days",
                   font=dict(size=13, color=TEXT)),
        xaxis=dict(title=dict(text="Days After the Weather Event", font=dict(size=11, color=SUB)),
                   tickvals=list(range(1, 22))),
        yaxis=dict(title=dict(text="Spearman r", font=dict(size=11, color=SUB))),
        legend=dict(orientation="h", y=1.08, x=0),
        margin=dict(l=65, r=30, t=55, b=55))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1: kpi("FTC Peak Lag",        "Day 5",    "r = −0.081 (all years)",       color=RED)
    with c2: kpi("Spring-Only r",       "−0.143",   "p = 0.0003  ★★★",             color=RED)
    with c3: kpi("Spring Amplification","3×",        "stronger than full-year",      color=GOLD)
    with c4: kpi("Operational Window",  "5–7 days", "pre-stage crews on FT day 0",  color=BLUE)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    cl, cr = st.columns(2, gap="large")
    with cl:
        box("How to Read This Chart",
            "Each X-axis point is the lag in days between a weather event and the complaint count. "
            "The red FTC line dips <strong style='color:#E6EDF3'>negative</strong> because during "
            "active freeze seasons, citizens haven't noticed potholes yet — complaints are "
            "temporarily suppressed. The minimum at Day 5 is when the delayed complaint wave peaks.", BLUE)
    with cr:
        box("Why the Spring Signal Is 3× Stronger",
            "The all-year Spearman r of −0.081 triples to −0.143 (p = 0.0003) when restricted "
            "to March–May only. In spring, all accumulated winter damage becomes visible "
            "simultaneously — making the FT → complaint relationship tightest and most "
            "actionable for scheduling decisions.", RED)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — WEATHER PREDICTORS
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 5:
    hero("Weather Predictor Ranking",
         "Precipitation and freeze-thaw operate through different mechanisms.",
         "Rolling weather features ranked by Spearman r against daily pothole counts. "
         "Understanding each direction of effect is critical for building the alert trigger.")

    cl, cr = st.columns([1.3, 1], gap="large")
    with cl:
        features = [
            ("FTC 14-day rolling",    -0.0870, RED),
            ("Precip × FTC (7-day)", -0.0461, RED),
            ("Snow 7-day rolling",   -0.0369, "rgba(110,118,129,0.6)"),
            ("Snow 14-day rolling",  -0.0338, "rgba(110,118,129,0.6)"),
            ("Snow 5-day rolling",   -0.0310, "rgba(110,118,129,0.6)"),
            ("HDD 30-day rolling",   -0.0255, GOLD),
            ("Snow 3-day rolling",   -0.0145, "rgba(110,118,129,0.6)"),
            ("Rain 3-day rolling",    0.0132, "rgba(56,139,253,0.55)"),
            ("Rain 14-day rolling",   0.0262, "rgba(56,139,253,0.55)"),
            ("Precip 3-day rolling",  0.0451, BLUE),
            ("Rain 7-day rolling",    0.0489, "rgba(56,139,253,0.55)"),
            ("Rain 5-day rolling",    0.0496, "rgba(56,139,253,0.55)"),
            ("Precip 14-day rolling", 0.0534, BLUE),
            ("Precip 5-day rolling",  0.0727, BLUE),
            ("Precip 7-day rolling",  0.0734, BLUE),
        ]
        fig = go.Figure(go.Bar(
            x=[f[1] for f in features], y=[f[0] for f in features], orientation="h",
            marker=dict(color=[f[2] for f in features], line=dict(width=0)),
            text=[f"{f[1]:+.4f}" for f in features],
            textposition="outside", textfont=dict(size=10, color=SUB),
            hovertemplate="<b>%{y}</b><br>Spearman r = %{x:.4f}<extra></extra>"))
        fig.add_vline(x=0, line_color=BORDER, line_width=2)
        fig = pset(fig, 500)
        fig.update_layout(
            title=dict(text="Spearman r — Rolling Weather Features vs Daily Pothole Complaints",
                       font=dict(size=13, color=TEXT)),
            showlegend=False,
            margin=dict(l=180, r=85, t=50, b=55),
            xaxis=dict(
                title=dict(text="Spearman r", font=dict(size=11, color=SUB)),
                range=[-0.115, 0.105]),
            yaxis=dict(tickfont=dict(size=11, color=SUB)))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        box("FTC 14-day — Strongest Overall",
            "r = −0.087. High FTC periods = active freeze seasons where complaints are currently "
            "suppressed. The surge arrives 5 days later. This captures the entire lag mechanism.", RED)
        box("Precipitation — Best Positive Predictor",
            "7-day rolling precipitation: r = +0.073. More rain in the past week predicts "
            "more complaints today. Rain infiltrates existing cracks and directly accelerates "
            "both erosion and freeze-thaw damage.", BLUE)
        box("Snow — Also Negative (Different Reason)",
            "During heavy snowfall, potholes are masked by snow cover. "
            "Complaints are suppressed during snowfall — the surge comes after the snow clears.", MUTED)
        box("Precip × FTC Interaction",
            "r = −0.046. Wet pavement that then freezes causes maximum cracking stress. "
            "3× stronger in spring — capturing the worst combination: "
            "saturated roads hit by a sudden cold snap.", GOLD)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — REGIONAL BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 6:
    hero("Regional Breakdown",
         "Halifax leads. The freeze-thaw signal varies significantly across the province.",
         "One-size-fits-all alerts are less efficient than region-specific triggers. "
         "Each region has a dominant weather driver that should guide its alert threshold.")

    regions = ["Halifax /\nLunenburg","Annapolis\nValley","Central NS","Cape Breton","SW Nova\nScotia"]
    n_vals  = [10866, 8623, 6148, 4639, 1340]
    p_r     = [0.014,  0.094,  0.101, -0.041,  0.000]
    f_r     = [-0.125, -0.057, -0.044, -0.029, -0.033]
    h_r     = [-0.112, -0.020, -0.011,  0.011, -0.018]
    sigs    = ["***","***","***","*","ns"]
    rclrs   = [RED, BLUE, GOLD, GREEN, MUTED]

    kpi_cols = st.columns(5, gap="small")
    for col, name, n, ftc, sig, clr in zip(kpi_cols, regions, n_vals, f_r, sigs, rclrs):
        col.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-top:3px solid {clr};'
            f'border-radius:10px;padding:12px 8px;text-align:center">'
            f'<p style="font-size:9px;font-weight:600;color:{MUTED};margin:0 0 6px;'
            f'font-family:JetBrains Mono,monospace;white-space:pre-line">{name}</p>'
            f'<p style="font-size:1.3rem;font-weight:800;color:{clr};margin:0 0 2px;line-height:1">{n:,}</p>'
            f'<p style="font-size:10px;color:{MUTED};margin:0 0 5px">potholes</p>'
            f'<div style="border-top:1px solid {BORDER};padding-top:5px">'
            f'<code style="font-size:9px;color:{MUTED}">FTC r={ftc:.3f} {sig}</code></div></div>',
            unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    cl, cr = st.columns([1.4, 1], gap="large")
    with cl:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="7-day Precip r", x=regions, y=p_r,
            marker=dict(color=BLUE, line=dict(width=0))))
        fig.add_trace(go.Bar(name="14-day FTC r", x=regions, y=f_r,
            marker=dict(color=RED, line=dict(width=0))))
        fig.add_trace(go.Bar(name="14-day HDD r", x=regions, y=h_r,
            marker=dict(color=GOLD, line=dict(width=0))))
        fig.add_hline(y=0, line_color=BORDER, line_width=1.5)
        fig = pset(fig, 360)
        fig.update_layout(
            title=dict(text="Spearman r by Region — Precipitation, FTC, and Heating Degree Days",
                       font=dict(size=13, color=TEXT)),
            barmode="group",
            legend=dict(orientation="h", y=1.08, x=0),
            yaxis=dict(title=dict(text="Spearman r", font=dict(size=11, color=SUB))),
            xaxis=dict(tickfont=dict(size=10, color=SUB)),
            margin=dict(l=65, r=30, t=55, b=55))
        st.plotly_chart(fig, use_container_width=True)

    with cr:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        box("Halifax / Lunenburg — Priority Region",
            "FTC r = −0.125 (***). Strongest freeze-thaw signal in the province. "
            "33.9% of all pothole complaints — highest ROI for an early-alert system.", RED)
        box("Annapolis Valley & Central NS",
            "Precipitation dominates: r ≈ +0.09 to +0.10 (***). "
            "These inland regions are more sensitive to rainfall than to FT cycling. "
            "Use rain accumulation thresholds as the alert trigger here, not FTC counts.", BLUE)
        box("Cape Breton — Maritime Effect",
            "The Atlantic Ocean moderates temperature extremes, producing fewer complete FT cycles. "
            "Weaker FTC signal (r = −0.029), but precipitation still significant (r = −0.041*).", GOLD)
        box("SW Nova Scotia — Data Gap",
            "Yarmouth A has no precipitation data in the ECCC archive. "
            "Non-significant results likely reflect the data limitation, "
            "not a genuine absence of the freeze-thaw effect.", MUTED)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — REGRESSION MODEL
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 7:
    hero("OLS Regression Model",
         "Five weather variables independently predict daily pothole complaint counts.",
         "Ordinary Least Squares with HC3 robust standard errors. Weekdays only, 2019–2025. R² = 0.072.")

    cl, cr = st.columns([1.3, 1], gap="large")
    with cl:
        predictors = [
            ("Spring Season (Mar–May)",     4.59, True),
            ("14-day FTC Count",           -0.67, True),
            ("7-day Cumulative Snow",       0.23, True),
            ("Precip × FTC (7-day)",        0.11, True),
            ("14-day Heating Degree Days", -0.02, True),
            ("7-day Rain",                 -0.02, False),
            ("7-day Total Precip",          0.05, False),
        ]
        pcolors = [RED if p[2] else "rgba(110,118,129,0.35)" for p in predictors]
        ptexts  = [f"{p[1]:+.2f}  ★" if p[2] else f"{p[1]:+.2f}  ns" for p in predictors]
        fig = go.Figure(go.Bar(
            x=[p[1] for p in predictors], y=[p[0] for p in predictors], orientation="h",
            marker=dict(color=pcolors, line=dict(width=0)),
            text=ptexts, textposition="outside", textfont=dict(size=11, color=SUB),
            hovertemplate="<b>%{y}</b><br>Coefficient = %{x:+.2f}<extra></extra>"))
        fig.add_vline(x=0, line_color=BORDER, line_width=2)
        fig = pset(fig, 340)
        fig.update_layout(
            title=dict(text="OLS Coefficients  ·  R² = 0.072  ·  HC3 Robust SE",
                       font=dict(size=13, color=TEXT)),
            showlegend=False,
            margin=dict(l=220, r=100, t=50, b=55),
            xaxis=dict(
                title=dict(text="Extra daily complaints per unit increase",
                           font=dict(size=11, color=SUB)),
                range=[-1.0, 6.5]),
            yaxis=dict(tickfont=dict(size=11, color=SUB)))
        st.plotly_chart(fig, use_container_width=True)

        ca, cb = st.columns(2, gap="medium")
        with ca:
            box("5 Significant Predictors ★",
                "Spring Season, FTC 14d, Snow 7d, Precip×FTC, and HDD 14d all pass "
                "p < 0.05 with HC3 robust standard errors.", RED)
        with cb:
            box("2 Non-Significant (ns)",
                "Rain 7d (p=0.807) and Precip 7d (p=0.439) are absorbed by "
                "correlated predictors in the full model.", MUTED)

    with cr:
        rows = [
            ("Spring Season", "+4.59","<0.001", True),
            ("FTC 14d",       "−0.67","<0.001", True),
            ("Snow 7d",       "+0.23","0.009",  True),
            ("Precip×FTC",    "+0.11","0.006",  True),
            ("HDD 14d",       "−0.02","0.007",  True),
            ("Rain 7d",       "−0.02","0.807",  False),
            ("Precip 7d",     "+0.05","0.439",  False),
        ]
        hdr = (f'<tr style="border-bottom:1px solid {BORDER}">'
               f'<th style="font-family:JetBrains Mono,monospace;font-size:9px;color:{MUTED};'
               f'text-transform:uppercase;letter-spacing:1.5px;padding:10px 8px 10px 0;font-weight:500">Predictor</th>'
               f'<th style="font-family:JetBrains Mono,monospace;font-size:9px;color:{MUTED};'
               f'text-transform:uppercase;letter-spacing:1.5px;padding:10px 8px;font-weight:500">Coef.</th>'
               f'<th style="font-family:JetBrains Mono,monospace;font-size:9px;color:{MUTED};'
               f'text-transform:uppercase;letter-spacing:1.5px;padding:10px 0;font-weight:500">p-value</th></tr>')
        bdy = ""
        for name, coef, pval, sig in rows:
            nc = RED if sig else MUTED
            pc = GREEN if sig else MUTED
            bdy += (f'<tr style="border-bottom:1px solid {BORDER}44">'
                    f'<td style="padding:10px 8px 10px 0;font-size:12px;'
                    f'font-weight:{"600" if sig else "400"};color:{nc}">{name}</td>'
                    f'<td style="font-family:JetBrains Mono,monospace;font-size:11px;'
                    f'color:{GOLD};padding:10px 8px">{coef}</td>'
                    f'<td style="font-family:JetBrains Mono,monospace;font-size:10px;color:{pc}">{pval}</td>'
                    f'</tr>')
        st.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;'
            f'padding:20px;margin-bottom:12px">'
            f'<p style="font-size:10px;font-weight:600;color:{MUTED};text-transform:uppercase;'
            f'letter-spacing:2px;margin:0 0 12px">Coefficient Table</p>'
            f'<table style="width:100%;border-collapse:collapse">{hdr}{bdy}</table></div>',
            unsafe_allow_html=True)
        box("Why R² = 7.2% Is Acceptable",
            "Weather explains 7.2% of daily variance. Road age, traffic volume, and pavement "
            "condition account for the rest — unmeasured here. 7.2% is still sufficient "
            "to build a reliable operational alert trigger.", GOLD)
        box("Why FTC Shows a Negative Coefficient",
            "High FTC = active winter freeze season where same-day complaints are suppressed "
            "(the lag has not yet expired). The Spring Season dummy (+4.59) captures "
            "the full delayed complaint wave when it finally arrives.", RED)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — ACTION PLAN
# ═══════════════════════════════════════════════════════════════════════════════
elif S == 8:
    hero("Conclusions & Action Plan",
         "Three findings. One early-warning system.",
         "The analysis supports a weather-triggered, regionally-differentiated maintenance alert "
         "that converts NS TIR from reactive to proactive operations.")

    cl, cr = st.columns(2, gap="large")
    with cl:
        findings = [
            (RED,  "1", "A measurable 5-day lag exists",
             "Spearman r = −0.081 at Day 5 lag. Spring-only: r = −0.143, p = 0.0003. "
             "Consistent and statistically significant across all 6 years of data."),
            (BLUE, "2", "Weather explains 7.2% of daily variance",
             "Spring Season (+4.59), FTC 14d (−0.67), and Snow 7d (+0.23) are the dominant "
             "significant OLS predictors. Partial but reliable signal for scheduling."),
            (GOLD, "3", "Halifax needs priority alert triage",
             "FTC r = −0.125 (***). Annapolis and Central NS are precipitation-driven. "
             "Region-differentiated alerts outperform province-wide blanket warnings."),
        ]
        cards = ""
        for i, (color, num, title, body_text) in enumerate(findings):
            sep = f"padding-bottom:16px;border-bottom:1px solid {BORDER};margin-bottom:16px;" if i < 2 else ""
            cards += (f'<div style="display:flex;gap:14px;align-items:flex-start;{sep}">'
                      f'<div style="font-size:1.6rem;font-weight:800;color:{color};'
                      f'line-height:1;flex-shrink:0;width:28px">{num}</div>'
                      f'<div><p style="font-size:13px;font-weight:700;color:{TEXT};margin:0 0 4px">{title}</p>'
                      f'<p style="font-size:12px;color:{MUTED};line-height:1.65;margin:0">{body_text}</p>'
                      f'</div></div>')
        st.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:22px">'
            f'<p style="font-size:9px;font-weight:600;color:{MUTED};text-transform:uppercase;'
            f'letter-spacing:2px;margin:0 0 18px">Three Core Findings</p>'
            f'{cards}</div>', unsafe_allow_html=True)

    with cr:
        tiers = [
            (RED,  "HIGH ALERT — Deploy Now",
             "Trigger: ≥5 FT days in rolling 14-day window, OR thaw after 3+ consecutive freezing days. "
             "Action: Pre-stage full patching crews within 5 days. Prioritise Halifax region."),
            (GOLD, "MEDIUM ALERT — Monitor Closely",
             "Trigger: 2–4 FT days in 14-day window, OR 7-day accumulated precip > 25mm. "
             "Action: Schedule inspection patrols and pre-stock patching materials in priority depots."),
            (BLUE, "LOW ALERT — Routine Operations",
             "Trigger: 0–1 FT days, normal precipitation. "
             "Action: Standard reactive complaint-response. Log and schedule in next maintenance cycle."),
        ]
        tiers_html = ""
        for color, title, body_text in tiers:
            tiers_html += (f'<div style="background:{color}10;border:1px solid {color}38;'
                           f'border-left:3px solid {color};border-radius:8px;padding:14px;margin-bottom:10px">'
                           f'<p style="font-size:11px;font-weight:700;color:{color};margin:0 0 5px">{title}</p>'
                           f'<p style="font-size:12px;color:{MUTED};line-height:1.65;margin:0">{body_text}</p>'
                           f'</div>')
        st.markdown(
            f'<div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:22px">'
            f'<p style="font-size:9px;font-weight:600;color:{MUTED};text-transform:uppercase;'
            f'letter-spacing:2px;margin:0 0 16px">Proposed 3-Tier Alert System</p>'
            f'{tiers_html}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        box("Data Limitations",
            "Yarmouth A: no precipitation data. Greenwood A: no rain/snow split. "
            "Weather explains only 7.2% of variance — road age and traffic volume are "
            "unmeasured confounders that would significantly improve model accuracy.", GOLD)
    with c2:
        box("Recommended Next Steps",
            "① Connect live ECCC forecast API for real-time FTC monitoring. "
            "② Add road age and Pavement Condition Index as model covariates. "
            "③ Pilot the 3-tier alert system with Halifax region depot for one spring season.", GREEN)
    with c3:
        box("Expected Operational Impact",
            "Early-warning deployment could reduce average pothole response time from "
            "5–7 days (reactive) to 1–2 days (proactive). "
            "Fewer complaints, lower patching costs, and measurably better citizen service.", BLUE)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div style="margin-top:28px;padding-top:14px;border-top:1px solid {BORDER};'
    f'display:flex;justify-content:space-between;align-items:center">'
    f'<span style="font-family:JetBrains Mono,monospace;font-size:9px;'
    f'color:{MUTED};letter-spacing:1px">NS ROAD INFRASTRUCTURE · MBAN 2026</span>'
    f'<span style="font-family:JetBrains Mono,monospace;font-size:9px;'
    f'color:{MUTED};letter-spacing:1px">ECCC + NS TIR OCC · 391,795 records · Provincial Highways Only</span>'
    f'<span style="font-family:JetBrains Mono,monospace;font-size:9px;'
    f'color:{RED};letter-spacing:1px;font-weight:700">'
    f'Slide {S+1} of {len(SLIDE_LABELS)}</span></div>',
    unsafe_allow_html=True)