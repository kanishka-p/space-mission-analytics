import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_url = (
    st.secrets["DB_URL"]
    if "DB_URL" in st.secrets
    else os.getenv("DB_URL")
)
engine = create_engine(db_url)

st.set_page_config(
    page_title="Space Mission Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme constants ───────────────────────────────────────────────────────────
BG       = "#0d1117"
CARD_BG  = "#161b22"
BORDER   = "#30363d"
BLUE     = "#58a6ff"
PURPLE   = "#bc8cff"
GREEN    = "#3fb950"
AMBER    = "#d29922"
RED      = "#f85149"
CYAN     = "#39d0d8"

LAYOUT = dict(
    plot_bgcolor=BG, paper_bgcolor=BG,
    font=dict(color="#c9d1d9", family="Inter, sans-serif"),
    margin=dict(t=40, b=20, l=20, r=20),
    legend=dict(bgcolor=CARD_BG, bordercolor=BORDER, borderwidth=1),
    hoverlabel=dict(bgcolor=CARD_BG, bordercolor=BORDER, font_color="white"),
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG};
    color: #c9d1d9;
}}
[data-testid="stAppViewContainer"] {{ background-color: {BG}; }}
[data-testid="stSidebar"] {{
    background-color: {CARD_BG};
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{ color: #c9d1d9 !important; }}
.kpi-card {{
    background: linear-gradient(135deg, {CARD_BG} 0%, #1c2128 100%);
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    transition: border-color 0.2s;
}}
.kpi-card:hover {{ border-color: {BLUE}; }}
.kpi-value {{ font-size: 2rem; font-weight: 700; color: {BLUE}; margin: 0; }}
.kpi-label {{ font-size: 0.78rem; color: #8b949e; margin: 0; text-transform: uppercase; letter-spacing: 0.08em; }}
.insight-box {{
    background: linear-gradient(135deg, #1c2128 0%, #161b22 100%);
    border-left: 3px solid {BLUE};
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.88rem;
    color: #c9d1d9;
}}
.section-header {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid {BORDER};
}}
div[data-testid="stTabs"] button {{
    color: #8b949e !important;
    font-size: 0.95rem;
}}
div[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {BLUE} !important;
    border-bottom: 2px solid {BLUE} !important;
}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load(query):
    return pd.read_sql(query, engine)


missions   = load("SELECT * FROM analytics_facts.fct_missions")
by_year    = load("SELECT * FROM analytics_facts.agg_success_by_year ORDER BY launch_year")
by_sector  = load("SELECT * FROM analytics_facts.agg_sector_by_year ORDER BY launch_year")
agencies   = load("SELECT * FROM analytics_dimensions.dim_agencies ORDER BY total_launches DESC")
rockets    = load("SELECT * FROM analytics_dimensions.dim_rockets ORDER BY total_launches DESC")
by_country = load("SELECT * FROM analytics_facts.agg_country_launches ORDER BY total_launches DESC")


# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Filters")
    st.markdown("---")
    year_range = st.slider(
        "Year Range", 1957, 2022, (1957, 2022),
        help="Filter all charts by launch year"
    )
    sectors = st.multiselect(
        "Sector", ["Government", "Commercial"],
        default=["Government", "Commercial"]
    )
    countries = st.multiselect(
        "Country", by_country["country"].tolist(),
        default=by_country["country"].tolist(),
        help="Filter by launch country"
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#8b949e'>Data: Kaggle — All Space Missions 1957–2022<br>"
        "Transformed with dbt · Visualised with Plotly</small>",
        unsafe_allow_html=True
    )

m = missions[
    (missions["launch_year"] >= year_range[0]) &
    (missions["launch_year"] <= year_range[1]) &
    (missions["sector"].isin(sectors)) &
    (missions["country"].isin(countries))
]
yr = by_year[
    (by_year["launch_year"] >= year_range[0]) &
    (by_year["launch_year"] <= year_range[1])
]
sec = by_sector[
    (by_sector["launch_year"] >= year_range[0]) &
    (by_sector["launch_year"] <= year_range[1]) &
    (by_sector["sector"].isin(sectors))
]


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 1.5rem 0 0.5rem 0">
    <h1 style="margin:0; font-size:2.2rem; font-weight:700; color:#e6edf3">
        🚀 Space Mission Analytics
    </h1>
    <p style="margin:0.3rem 0 0 0; color:#8b949e; font-size:1rem">
        60+ years of human spaceflight &nbsp;·&nbsp; Sputnik to SpaceX &nbsp;·&nbsp; 4,630 missions analysed
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
k = st.columns(5)
kpis = [
    ("Total Missions",   f"{len(m):,}",                                           "🛸"),
    ("Success Rate",     f"{(m['is_success'].mean()*100):.1f}%",                  "✅"),
    ("Countries",        f"{m['country'].nunique()}",                              "🌍"),
    ("Unique Rockets",   f"{m['rocket'].nunique():,}",                             "🔭"),
    ("Year Span",        f"{year_range[1] - year_range[0]}y",                     "📅"),
]
for col, (label, value, icon) in zip(k, kpis):
    col.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">{icon} &nbsp; {label}</p>
        <p class="kpi-value">{value}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏢 Agencies", "🚀 Rockets", "🔍 Explorer"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-header">Mission Success Rate Over Time</p>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yr["launch_year"], y=yr["success_rate_pct"],
            mode="lines", fill="tozeroy",
            line=dict(color=GREEN, width=2.5),
            fillcolor="rgba(63,185,80,0.12)",
            hovertemplate="<b>%{x}</b><br>Success rate: %{y:.1f}%<extra></extra>",
        ))
        fig.add_hline(y=90, line_dash="dot", line_color=AMBER, opacity=0.5,
                      annotation_text="90% threshold", annotation_font_color=AMBER)
        fig.update_layout(**LAYOUT, yaxis_range=[0, 108],
                          xaxis=dict(rangeslider=dict(visible=True, thickness=0.05)))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">Total Launches Per Year</p>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=yr["launch_year"], y=yr["total_launches"],
            mode="lines", fill="tozeroy",
            line=dict(color=PURPLE, width=2.5),
            fillcolor="rgba(188,140,255,0.12)",
            hovertemplate="<b>%{x}</b><br>Launches: %{y}<extra></extra>",
        ))
        for vx, label, color in [
            (1957, "Sputnik", CYAN),
            (1969, "Moon Landing", AMBER),
            (1991, "USSR Collapse", RED),
            (2002, "SpaceX Founded", GREEN),
        ]:
            fig2.add_vline(x=vx, line_dash="dash", line_color=color, opacity=0.6,
                           annotation_text=label, annotation_font_color=color,
                           annotation_textangle=-90)
        fig2.update_layout(**LAYOUT, xaxis=dict(rangeslider=dict(visible=True, thickness=0.05)))
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<p class="section-header">Government vs Commercial Shift</p>', unsafe_allow_html=True)
        fig4 = px.area(
            sec, x="launch_year", y="total_launches", color="sector",
            color_discrete_map={"Commercial": AMBER, "Government": BLUE},
            labels={"total_launches": "Launches", "launch_year": "Year", "sector": ""},
            custom_data=["sector"],
        )
        fig4.update_traces(
            hovertemplate="<b>%{customdata[0]}</b><br>Year: %{x}<br>Launches: %{y}<extra></extra>"
        )
        fig4.update_layout(**LAYOUT)
        st.plotly_chart(fig4, use_container_width=True)

    with c4:
        st.markdown('<p class="section-header">Launch Share by Country</p>', unsafe_allow_html=True)
        top_c = by_country[by_country["country"].isin(countries)].head(10)
        fig6 = go.Figure(go.Treemap(
            labels=top_c["country"],
            parents=[""] * len(top_c),
            values=top_c["total_launches"],
            customdata=top_c[["success_rate_pct", "total_launches"]].values,
            hovertemplate="<b>%{label}</b><br>Launches: %{customdata[1]}<br>Success: %{customdata[0]}%<extra></extra>",
            marker=dict(
                colors=top_c["total_launches"],
                colorscale=[[0, "#1c2128"], [1, BLUE]],
                showscale=False,
            ),
            textfont=dict(size=14, color="white"),
        ))
        fig6.update_layout(**LAYOUT)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<p class="section-header">Mission Cost Over Time (USD Millions)</p>', unsafe_allow_html=True)
    priced = m.dropna(subset=["cost_usd_millions"])
    fig7 = px.scatter(
        priced, x="launch_year", y="cost_usd_millions",
        color="sector", size="cost_usd_millions", size_max=40,
        hover_name="mission_name",
        hover_data={"company": True, "rocket": True,
                    "cost_usd_millions": ":,.0f", "launch_year": False, "sector": False},
        labels={"cost_usd_millions": "Cost (USD M)", "launch_year": "Year", "sector": ""},
        color_discrete_map={"Commercial": AMBER, "Government": BLUE},
        opacity=0.8,
    )
    fig7.update_layout(**LAYOUT)
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown('<p class="section-header">Key Insights</p>', unsafe_allow_html=True)
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(f'<div class="insight-box">🇷🇺 <b>RVSN USSR</b> launched 1,777 missions — more than the entire rest of the world combined during the Cold War era.</div>', unsafe_allow_html=True)
    with i2:
        st.markdown(f'<div class="insight-box">💰 SpaceX reduced average mission cost to <b>$63M</b> vs NASA\'s <b>$512M</b> — an 8× cost reduction through reusability.</div>', unsafe_allow_html=True)
    with i3:
        st.markdown(f'<div class="insight-box">📈 Global success rate climbed from <b>~60%</b> in the 1950s to consistently <b>above 95%</b> post-2000.</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — AGENCIES
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    n_agencies = st.slider("Show top N agencies", 5, 30, 15)
    top_ag = agencies[agencies["sector"].isin(sectors)].head(n_agencies)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-header">Total Launches by Agency</p>', unsafe_allow_html=True)
        fig = px.bar(
            top_ag, x="total_launches", y="company", orientation="h",
            color="sector",
            color_discrete_map={"Commercial": AMBER, "Government": BLUE},
            labels={"total_launches": "Total Launches", "company": "", "sector": ""},
            hover_data={"success_rate_pct": True, "first_launch_year": True, "last_launch_year": True},
            custom_data=["success_rate_pct", "sector", "first_launch_year", "last_launch_year"],
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Launches: %{x}<br>Success: %{customdata[0]}%<br>Active: %{customdata[2]}–%{customdata[3]}<extra></extra>"
        )
        fig.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"}, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">Success Rate by Agency</p>', unsafe_allow_html=True)
        fig2 = px.bar(
            top_ag.sort_values("success_rate_pct", ascending=False),
            x="success_rate_pct", y="company", orientation="h",
            color="success_rate_pct",
            color_continuous_scale=[[0, RED], [0.5, AMBER], [1, GREEN]],
            labels={"success_rate_pct": "Success Rate (%)", "company": ""},
            custom_data=["total_launches", "sector"],
        )
        fig2.update_traces(
            hovertemplate="<b>%{y}</b><br>Success: %{x}%<br>Total launches: %{customdata[0]}<extra></extra>"
        )
        fig2.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"},
                           coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Launches vs Success Rate — Bubble View</p>', unsafe_allow_html=True)
    fig3 = px.scatter(
        top_ag,
        x="total_launches", y="success_rate_pct",
        size="total_launches", color="sector",
        text="company",
        color_discrete_map={"Commercial": AMBER, "Government": BLUE},
        labels={"total_launches": "Total Launches", "success_rate_pct": "Success Rate (%)", "sector": ""},
        size_max=60,
    )
    fig3.update_traces(textposition="top center", textfont=dict(size=10, color="white"))
    fig3.update_layout(**LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — ROCKETS
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    min_launches = st.slider("Minimum launches to qualify", 5, 50, 10)
    qualified = rockets[rockets["total_launches"] >= min_launches].copy()
    qualified["success_rate_pct"] = qualified["success_rate_pct"].astype(float)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<p class="section-header">Most Reliable Rockets</p>', unsafe_allow_html=True)
        top_reliable = qualified.sort_values("success_rate_pct", ascending=False).head(15)
        fig = px.bar(
            top_reliable, x="success_rate_pct", y="rocket", orientation="h",
            color="success_rate_pct",
            color_continuous_scale=[[0, RED], [0.7, AMBER], [1, GREEN]],
            labels={"success_rate_pct": "Success Rate (%)", "rocket": ""},
            custom_data=["total_launches", "rocket_status", "first_launch_year", "last_launch_year"],
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Success: %{x}%<br>Launches: %{customdata[0]}<br>Status: %{customdata[1]}<br>Active: %{customdata[2]}–%{customdata[3]}<extra></extra>"
        )
        fig.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"},
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<p class="section-header">Most Launched Rockets</p>', unsafe_allow_html=True)
        top_used = qualified.sort_values("total_launches", ascending=False).head(15)
        fig2 = px.bar(
            top_used, x="total_launches", y="rocket", orientation="h",
            color="rocket_status",
            color_discrete_map={"Retired": RED, "Active": GREEN},
            labels={"total_launches": "Total Launches", "rocket": "", "rocket_status": "Status"},
            custom_data=["success_rate_pct", "rocket_status"],
        )
        fig2.update_traces(
            hovertemplate="<b>%{y}</b><br>Launches: %{x}<br>Success: %{customdata[0]}%<br>Status: %{customdata[1]}<extra></extra>"
        )
        fig2.update_layout(**LAYOUT, yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">Launch Volume vs Reliability</p>', unsafe_allow_html=True)
    fig3 = px.scatter(
        qualified,
        x="total_launches", y="success_rate_pct",
        color="rocket_status", size="total_launches",
        hover_name="rocket",
        color_discrete_map={"Retired": RED, "Active": GREEN},
        labels={"total_launches": "Total Launches", "success_rate_pct": "Success Rate (%)", "rocket_status": "Status"},
        size_max=40, opacity=0.8,
    )
    fig3.add_hline(y=90, line_dash="dot", line_color=AMBER, opacity=0.5,
                   annotation_text="90% reliability line", annotation_font_color=AMBER)
    fig3.update_layout(**LAYOUT)
    st.plotly_chart(fig3, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — EXPLORER
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-header">Mission Explorer</p>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        search = st.text_input("Search mission or company", placeholder="e.g. Apollo, SpaceX...")
    with f2:
        status_filter = st.multiselect(
            "Mission Status", missions["mission_status"].unique().tolist(),
            default=missions["mission_status"].unique().tolist()
        )
    with f3:
        sort_col = st.selectbox("Sort by", ["launch_year", "cost_usd_millions", "company", "mission_status"])

    filtered = m[m["mission_status"].isin(status_filter)]
    if search:
        mask = (
            filtered["mission_name"].str.contains(search, case=False, na=False) |
            filtered["company"].str.contains(search, case=False, na=False) |
            filtered["rocket"].str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    filtered = filtered.sort_values(sort_col, ascending=(sort_col == "launch_year")).reset_index(drop=True)

    success_count = filtered["is_success"].sum()
    fail_count    = (~filtered["is_success"]).sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Filtered Missions", f"{len(filtered):,}")
    m2.metric("Successful", f"{success_count:,}")
    m3.metric("Failed / Partial", f"{fail_count:,}")

    st.dataframe(
        filtered[["mission_name", "company", "rocket", "country",
                  "launch_year", "sector", "mission_status", "cost_usd_millions"]]
        .rename(columns={
            "mission_name": "Mission", "company": "Company",
            "rocket": "Rocket", "country": "Country",
            "launch_year": "Year", "sector": "Sector",
            "mission_status": "Status", "cost_usd_millions": "Cost (USD M)",
        }),
        use_container_width=True,
        height=500,
    )
    st.caption(f"Showing {len(filtered):,} of {len(missions):,} total missions")
