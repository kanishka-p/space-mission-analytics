# 🚀 Space Mission Analytics

> **60+ years of human spaceflight — from Sputnik to SpaceX — analysed, transformed, and visualised.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://kanishka-p-space-mission-analytics.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![dbt](https://img.shields.io/badge/dbt-1.8-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://getdbt.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)

---

## Overview

An end-to-end **data analytics pipeline** covering **4,630 space missions** across 65 years. Raw mission data is ingested into PostgreSQL, transformed using **dbt** into analytical models, and surfaced through an interactive **Streamlit dashboard** with 10+ Plotly visualisations.

The project answers questions like:
- How has mission success rate evolved since the Space Race?
- When did commercial launches overtake government agencies?
- Which rockets are the most reliable, and which cost the most?
- How does SpaceX's cost-per-launch compare to NASA's?

---

## Live Dashboard

**[→ Open the dashboard](https://kanishka-p-space-mission-analytics.streamlit.app)**

![Dashboard Preview](assets/dashboard_preview.png)

---

## Key Findings

| Finding | Detail |
|---|---|
| 🇷🇺 USSR dominance | RVSN USSR launched 1,777 missions — more than any other agency in history |
| 💰 Commercial disruption | SpaceX avg cost: **$63M** vs NASA avg: **$512M** — an 8× reduction |
| 📈 Reliability surge | Global success rate rose from ~60% (1950s) to 95%+ (post-2000) |
| 🏆 Most reliable | ULA achieved **99.3% success rate** across 151 launches |
| 🔄 Sector shift | Commercial launches surpassed government launches around **2015** |

---

## Architecture

```
Kaggle CSV (raw data)
      ↓
PostgreSQL / Supabase      ← raw ingestion via Python + SQLAlchemy
      ↓
dbt Core                   ← cleaning, transformation, dimensional modelling
      ↓
  ┌─────────────────────────────────────────┐
  │  staging/     → stg_missions            │
  │  dimensions/  → dim_agencies            │
  │               → dim_rockets             │
  │  facts/       → fct_missions            │
  │               → agg_success_by_year     │
  │               → agg_sector_by_year      │
  │               → agg_country_launches    │
  └─────────────────────────────────────────┘
      ↓
Streamlit + Plotly         ← interactive dashboard
      ↓
Streamlit Community Cloud  ← public deployment
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Data Storage | PostgreSQL (Supabase) |
| Transformation | dbt Core 1.8 |
| Analysis | Python, Pandas, NumPy |
| Visualisation | Plotly Express, Plotly Graph Objects |
| Dashboard | Streamlit |
| Deployment | Streamlit Community Cloud |
| Version Control | Git, GitHub |

---

## Dashboard Features

- **Global sidebar filters** — filter all charts by year range, sector, and country simultaneously
- **4 tabs** — Overview, Agencies, Rockets, Mission Explorer
- **Interactive charts** — hover tooltips, range sliders, zoom, pan
- **Treemap** — country launch share with success rate on hover
- **Bubble chart** — agency launch volume vs reliability
- **Scatter plot** — mission cost over time, sized by cost
- **Mission Explorer** — live search + filter across 4,630 missions

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/Kanishka-p/space-mission-analytics.git
cd space-mission-analytics

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your database credentials
echo 'DB_URL=your_postgresql_connection_string' > .env

# Run the dashboard
streamlit run dashboard.py
```

---

## Data Source

- **Dataset:** [All Space Missions from 1957](https://www.kaggle.com/datasets/mysarahmadbhat/space-missions) — Kaggle
- **Coverage:** 1957–2022 · 4,630 missions · 28 agencies · 65 countries
