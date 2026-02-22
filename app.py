"""
U.R.I.E — Urban Resilience Intelligence Engine
All 6 Windows: Live Heat, Behaviour Simulator, Cooling ROI, Job Risk, Livelihood Pivot, Thermal Equity
Run: streamlit run urie_app.py
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import time
import streamlit as st
import streamlit.components.v1 as components
import os

html_path = os.path.join("templates", "urie_all_6_windows.html")

with open(html_path, "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1200, scrolling=True)

try:
    import pydeck as pdkstreamlit
    PYDECK_AVAILABLE = True
except ImportError:
    PYDECK_AVAILABLE = False

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="U.R.I.E — Urban Resilience Intelligence Engine",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;0,9..40,700;0,9..40,900;1,9..40,400&family=Space+Mono:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #060a12;
        color: #dde4f0;
    }
    .stApp { background-color: #060a12; }

    /* ── Horizontal Window Nav ── */
    .window-nav {
        display: flex;
        gap: 6px;
        padding: 4px 0 20px 0;
        overflow-x: auto;
        scrollbar-width: none;
    }
    .window-nav::-webkit-scrollbar { display: none; }

    .win-tab {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 18px;
        border-radius: 10px;
        border: 1px solid #1a2535;
        background: #0a1018;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        white-space: nowrap;
    }
    .win-tab:hover {
        border-color: #2a3a55;
        background: #0d1520;
    }
    .win-tab.active {
        background: #0f1f38;
        border-color: #1e4a8a;
        box-shadow: 0 0 20px rgba(30,74,138,0.25);
    }
    .win-tab-num {
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        color: #3a5070;
        font-weight: 700;
    }
    .win-tab.active .win-tab-num { color: #4a9eff; }
    .win-tab-icon { font-size: 16px; }
    .win-tab-label { font-size: 12px; font-weight: 600; color: #5a7090; }
    .win-tab.active .win-tab-label { color: #c8deff; }

    /* ── General cards ── */
    .card {
        background: #0a1220;
        border: 1px solid #162030;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .card-accent-blue  { border-color: #1e4a8a44; }
    .card-accent-green { border-color: #1a5a3044; }
    .card-accent-red   { border-color: #5a1a2044; }

    /* ── Risk banner ── */
    .risk-banner {
        display: flex;
        align-items: center;
        gap: 24px;
        background: #070c15;
        border: 1px solid #1a2a40;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
    }
    .risk-score { font-size: 64px; font-weight: 900; line-height: 1; font-family: 'Space Mono', monospace; }
    .risk-label { font-size: 20px; font-weight: 800; }
    .risk-detail { font-size: 12px; color: #4a6080; margin-top: 4px; }

    /* ── Career cards ── */
    .career-card {
        background: #080f1c;
        border: 1px solid #162030;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        transition: border-color 0.2s;
    }
    .career-card:hover { border-color: #1e4a8a; }
    .career-title  { font-size: 15px; font-weight: 700; color: #e8f0ff; }
    .career-salary { font-size: 13px; color: #2ecc71; font-weight: 700; font-family: 'Space Mono', monospace; }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 5px;
    }
    .badge-green  { background: #0a2a1a; color: #2ecc71; border: 1px solid #1a4a2a; }
    .badge-blue   { background: #0a1a30; color: #4a9eff; border: 1px solid #1a3a60; }
    .badge-purple { background: #1a0a30; color: #a78bfa; border: 1px solid #3a1a60; }
    .badge-red    { background: #2a0a10; color: #ff4466; border: 1px solid #5a1a2a; }
    .badge-orange { background: #2a1500; color: #ff8c35; border: 1px solid #5a3000; }

    /* ── Skill chips ── */
    .skill-chip {
        display: inline-block;
        background: #0f1a2a;
        color: #6a90b8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin: 3px;
        border: 1px solid #1a2a40;
    }
    .green-skill-chip {
        display: inline-block;
        background: #061810;
        color: #2ecc71;
        border: 1px solid #1a4a2a;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        margin: 3px;
    }

    /* ── Section labels ── */
    .section-label {
        font-size: 10px;
        font-weight: 700;
        color: #3a5070;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    /* ── Live chip ── */
    .live-chip {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #080f1c;
        border: 1px solid #162030;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 12px;
        color: #6a90b8;
    }
    .live-dot {
        width: 7px; height: 7px;
        background: #2ecc71;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #2ecc71;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── Zone boxes ── */
    .zone-box-hi {
        background: #080f1c;
        border: 1px solid #1a3a6044;
        border-radius: 14px;
        padding: 20px;
    }
    .zone-box-lo {
        background: #080f1c;
        border: 1px solid #5a1a2044;
        border-radius: 14px;
        padding: 20px;
    }
    .vs-box {
        background: #060a12;
        border: 1px solid #1a2535;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .gap-num { font-size: 24px; font-weight: 900; color: #ff4466; font-family: 'Space Mono', monospace; }
    .inequality-score { font-size: 52px; font-weight: 900; font-family: 'Space Mono', monospace; }

    /* ── Narrative box ── */
    .narrative-box {
        background: #070c15;
        border: 1px solid #ff443520;
        border-left: 3px solid #ff4435;
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        color: #8a9ab8;
        font-size: 14px;
        line-height: 1.75;
    }

    /* ── AI box ── */
    .ai-box {
        background: #07080f;
        border: 1px solid #6366f125;
        border-radius: 12px;
        padding: 18px;
        margin-top: 14px;
    }
    .ai-title {
        font-size: 10px;
        font-weight: 700;
        color: #6366f1;
        letter-spacing: 2px;
        margin-bottom: 12px;
        text-transform: uppercase;
    }

    /* ── Window header ── */
    .win-header {
        display: flex;
        align-items: flex-start;
        gap: 20px;
        margin-bottom: 24px;
    }
    .win-num {
        font-family: 'Space Mono', monospace;
        font-size: 80px;
        font-weight: 700;
        color: #0e1825;
        line-height: 1;
        letter-spacing: -4px;
        flex-shrink: 0;
    }
    .win-title-wrap { padding-top: 12px; }
    .win-title { font-size: 28px; font-weight: 800; color: #e8f0ff; letter-spacing: -0.5px; }
    .win-sub   { font-size: 14px; color: #4a6080; margin-top: 4px; }

    /* ── Risk cards ── */
    .risk-card {
        background: linear-gradient(135deg, rgba(255,60,0,0.1), rgba(255,0,60,0.04));
        border: 1px solid rgba(255,60,0,0.35);
        border-radius: 10px;
        padding: 14px;
        margin: 6px 0;
        font-family: 'Space Mono', monospace;
    }
    .risk-card-green {
        background: linear-gradient(135deg, rgba(0,200,100,0.08), rgba(0,180,80,0.03));
        border: 1px solid rgba(0,200,100,0.25);
        border-radius: 10px;
        padding: 14px;
        margin: 6px 0;
    }
    .risk-card-orange {
        background: linear-gradient(135deg, rgba(255,140,0,0.1), rgba(255,100,0,0.04));
        border: 1px solid rgba(255,140,0,0.35);
        border-radius: 10px;
        padding: 14px;
        margin: 6px 0;
    }
    .zone-header {
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        letter-spacing: 3px;
        color: #4a6080;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .graph-label {
        font-size: 11px;
        letter-spacing: 1px;
        color: #4a6080;
        text-transform: uppercase;
        margin: 10px 0 5px 0;
        border-left: 3px solid #1e4a8a;
        padding-left: 10px;
        line-height: 1.5;
        font-family: 'Space Mono', monospace;
    }

    /* ── Metrics ── */
    div[data-testid="stMetricValue"] { color: #4a9eff !important; font-family: 'Space Mono', monospace; }
    div[data-testid="stMetricDelta"] { font-size: 11px !important; }
    .stProgress > div > div { background: linear-gradient(90deg, #1e4a8a, #4a9eff) !important; }
    .stSelectbox label, .stSlider label, .stTextInput label { color: #6a90b8 !important; font-size: 13px !important; }

    /* ── Divider ── */
    hr { border-color: #0f1825; }

    /* ── Result card ── */
    .result-card {
        background: rgba(255,255,255,0.02);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }

    /* ── Info banner ── */
    .info-banner {
        background: #070c15;
        border: 1px solid #162030;
        border-radius: 10px;
        padding: 12px 18px;
        font-size: 13px;
        color: #6a90b8;
        margin-bottom: 16px;
        font-family: 'Space Mono', monospace;
    }

    /* ── Sidebar ── */
    div[data-testid="stSidebar"] {
        background: #050810 !important;
        border-right: 1px solid #0f1825;
    }
    div[data-testid="stSidebar"] .stMarkdown { color: #6a90b8; }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #0f1f38, #162a50) !important;
        border: 1px solid #1e4a8a !important;
        color: #c8deff !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #162a50, #1e3a6a) !important;
        box-shadow: 0 0 20px rgba(30,74,138,0.3) !important;
    }
    [data-testid="baseButton-primary"] > button, button[kind="primary"] {
        background: linear-gradient(135deg, #1e4a8a, #2a6abf) !important;
        border-color: #2a6abf !important;
    }
    .stSelectbox > div > div {
        background: #080f1c !important;
        border-color: #162030 !important;
        color: #dde4f0 !important;
    }
    .stTextInput > div > div > input {
        background: #080f1c !important;
        border-color: #162030 !important;
        color: #dde4f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── DATA DEFINITIONS ─────────────────────────────────────────────────────────

OWM_API_KEY = "fbbfdfb1aff4c893505cf9f9e1731d11"

CITIES = {
    "Bengaluru":  {"lat": 12.9716, "lon": 77.5946, "pop": 13_193_000, "elec": 7.80},
    "Mumbai":     {"lat": 19.0760, "lon": 72.8777, "pop": 20_667_000, "elec": 8.50},
    "Delhi":      {"lat": 28.7041, "lon": 77.1025, "pop": 32_941_000, "elec": 7.00},
    "Chennai":    {"lat": 13.0827, "lon": 80.2707, "pop": 11_503_000, "elec": 6.50},
    "Hyderabad":  {"lat": 17.3850, "lon": 78.4867, "pop": 10_534_000, "elec": 7.20},
    "Kolkata":    {"lat": 22.5726, "lon": 88.3639, "pop": 15_333_000, "elec": 6.80},
    "Pune":       {"lat": 18.5204, "lon": 73.8567, "pop":  7_276_000, "elec": 8.00},
    "Ahmedabad":  {"lat": 23.0225, "lon": 72.5714, "pop":  8_450_000, "elec": 5.50},
}

JOB_DATA_W4 = {
    "Construction Worker": {
        "base_risk": 78, "heat_exposure": 85, "automation_risk": 40, "outdoor_hours": 9,
        "skills": ["Manual labour", "Equipment operation", "Site safety"],
        "pivot": [
            {"title": "Solar Panel Installer",         "skills": "Electrical + rooftop work", "stability": 82, "risk": "Low"},
            {"title": "Green Building Inspector",       "skills": "Safety audit + certification", "stability": 75, "risk": "Low"},
            {"title": "EV Charging Infrastructure",     "skills": "Electrical wiring", "stability": 78, "risk": "Low"},
        ]
    },
    "Street Vendor": {
        "base_risk": 70, "heat_exposure": 90, "automation_risk": 20, "outdoor_hours": 10,
        "skills": ["Customer service", "Sales", "Inventory management"],
        "pivot": [
            {"title": "Indoor Market Operator",  "skills": "Sales + cold-chain logistics", "stability": 68, "risk": "Moderate"},
            {"title": "Online Reseller",          "skills": "E-commerce + packaging", "stability": 72, "risk": "Low"},
            {"title": "Food Processing Unit",     "skills": "Food safety + packaging", "stability": 65, "risk": "Low"},
        ]
    },
    "Delivery Rider": {
        "base_risk": 65, "heat_exposure": 80, "automation_risk": 55, "outdoor_hours": 8,
        "skills": ["Navigation", "Time management", "Customer handling"],
        "pivot": [
            {"title": "EV Delivery Fleet Manager",  "skills": "Route optimisation + EV ops", "stability": 74, "risk": "Low"},
            {"title": "Warehouse Coordinator",       "skills": "Logistics + inventory", "stability": 70, "risk": "Low"},
            {"title": "Last-Mile Tech Support",      "skills": "App support + delivery ops", "stability": 76, "risk": "Low"},
        ]
    },
    "Farmer / Agri Worker": {
        "base_risk": 82, "heat_exposure": 92, "automation_risk": 45, "outdoor_hours": 10,
        "skills": ["Crop management", "Water management", "Machinery operation"],
        "pivot": [
            {"title": "Precision Agri Technician",     "skills": "Drone ops + soil sensors", "stability": 80, "risk": "Low"},
            {"title": "Greenhouse Manager",             "skills": "Indoor farming + hydroponics", "stability": 77, "risk": "Low"},
            {"title": "Agri-Supply Chain Analyst",      "skills": "Logistics + crop forecasting", "stability": 72, "risk": "Low"},
        ]
    },
    "Waste Picker": {
        "base_risk": 85, "heat_exposure": 88, "automation_risk": 30, "outdoor_hours": 8,
        "skills": ["Material sorting", "Route knowledge", "Physical endurance"],
        "pivot": [
            {"title": "Recycling Plant Operator",       "skills": "Indoor sorting + machinery", "stability": 70, "risk": "Low"},
            {"title": "Urban Mining Specialist",         "skills": "E-waste + precious metals", "stability": 75, "risk": "Low"},
            {"title": "Green Logistics Coordinator",     "skills": "Waste logistics + data entry", "stability": 68, "risk": "Moderate"},
        ]
    },
    "Traffic Police": {
        "base_risk": 72, "heat_exposure": 82, "automation_risk": 25, "outdoor_hours": 8,
        "skills": ["Traffic management", "Law enforcement", "Emergency response"],
        "pivot": [
            {"title": "Smart Traffic System Operator",   "skills": "AI traffic + control room", "stability": 80, "risk": "Low"},
            {"title": "Drone Surveillance Operator",     "skills": "UAV monitoring + GIS", "stability": 76, "risk": "Low"},
            {"title": "Urban Mobility Consultant",       "skills": "Transport planning + policy", "stability": 78, "risk": "Low"},
        ]
    },
}

JOB_DATA_W5 = {
    "🏗️ Construction Worker": {
        "key": "construction", "heat_exposure": 92, "automation_risk": 38, "outdoor_hours": 8,
        "skills": ["physical endurance", "material handling", "equipment operation", "structural knowledge"],
    },
    "🚴 Delivery / Logistics": {
        "key": "delivery", "heat_exposure": 85, "automation_risk": 65, "outdoor_hours": 7,
        "skills": ["navigation", "time management", "customer interaction", "vehicle operation"],
    },
    "🛒 Street Vendor": {
        "key": "vendor", "heat_exposure": 88, "automation_risk": 20, "outdoor_hours": 9,
        "skills": ["sales", "cash handling", "inventory", "customer service"],
    },
    "💼 Office Worker": {
        "key": "office", "heat_exposure": 18, "automation_risk": 55, "outdoor_hours": 0.5,
        "skills": ["data processing", "communication", "spreadsheets", "reporting"],
    },
    "🌿 Green Sector Worker": {
        "key": "green", "heat_exposure": 45, "automation_risk": 12, "outdoor_hours": 4,
        "skills": ["environmental knowledge", "maintenance", "planting", "monitoring"],
    },
    "🌾 Agricultural Worker": {
        "key": "agriculture", "heat_exposure": 95, "automation_risk": 42, "outdoor_hours": 10,
        "skills": ["crop management", "irrigation", "soil knowledge", "harvesting"],
    },
}

GREEN_CAREERS = {
    "construction": [
        {"title": "Solar Panel Installer",             "stability": 88, "risk": "Low",    "salary": "₹3.5–6L/yr",  "skills": ["electrical basics", "roof safety", "panel mounting"]},
        {"title": "Sustainable Building Retrofitter",  "stability": 82, "risk": "Low",    "salary": "₹4–7L/yr",   "skills": ["energy auditing", "insulation", "green materials"]},
        {"title": "Urban Green Infrastructure Worker", "stability": 79, "risk": "Low",    "salary": "₹3–5L/yr",   "skills": ["landscaping", "stormwater systems", "plant care"]},
    ],
    "delivery": [
        {"title": "EV Fleet Technician",               "stability": 85, "risk": "Low",    "salary": "₹4–8L/yr",   "skills": ["EV mechanics", "battery systems", "diagnostics"]},
        {"title": "Green Logistics Coordinator",       "stability": 80, "risk": "Low",    "salary": "₹3.5–6L/yr", "skills": ["route optimization", "carbon tracking", "data entry"]},
        {"title": "Drone Delivery Operator",           "stability": 75, "risk": "Medium", "salary": "₹4–7L/yr",   "skills": ["drone piloting", "GPS systems", "safety protocols"]},
    ],
    "vendor": [
        {"title": "Community Urban Farmer",            "stability": 76, "risk": "Low",    "salary": "₹2.5–5L/yr", "skills": ["hydroponics", "sales", "community engagement"]},
        {"title": "Sustainable Products Retailer",     "stability": 72, "risk": "Low",    "salary": "₹3–5.5L/yr", "skills": ["eco-product knowledge", "marketing", "customer care"]},
        {"title": "Green Market Organizer",            "stability": 78, "risk": "Low",    "salary": "₹3–6L/yr",   "skills": ["event planning", "vendor coordination", "promotion"]},
    ],
    "office": [
        {"title": "Climate Data Analyst",              "stability": 91, "risk": "Low",    "salary": "₹6–14L/yr",  "skills": ["data analysis", "Python/R", "climate modeling"]},
        {"title": "ESG Reporting Specialist",          "stability": 87, "risk": "Low",    "salary": "₹7–15L/yr",  "skills": ["sustainability reporting", "compliance", "writing"]},
        {"title": "Green Finance Advisor",             "stability": 84, "risk": "Low",    "salary": "₹8–18L/yr",  "skills": ["finance", "carbon credits", "ESG frameworks"]},
    ],
    "green": [
        {"title": "Biodiversity Monitor",              "stability": 80, "risk": "Low",    "salary": "₹4–8L/yr",   "skills": ["ecology", "GIS mapping", "field surveys"]},
        {"title": "Urban Forestry Specialist",         "stability": 85, "risk": "Low",    "salary": "₹5–10L/yr",  "skills": ["arboriculture", "city planning", "tree care"]},
        {"title": "Climate Resilience Consultant",     "stability": 90, "risk": "Low",    "salary": "₹8–16L/yr",  "skills": ["risk assessment", "policy", "community planning"]},
    ],
    "agriculture": [
        {"title": "Climate-Smart Agriculture Advisor", "stability": 83, "risk": "Low",    "salary": "₹4–9L/yr",   "skills": ["agronomy", "water conservation", "crop diversification"]},
        {"title": "Vertical Farming Technician",       "stability": 87, "risk": "Low",    "salary": "₹4–8L/yr",   "skills": ["hydroponics", "climate control", "crop monitoring"]},
        {"title": "Agroforestry Specialist",           "stability": 81, "risk": "Low",    "salary": "₹3.5–7L/yr", "skills": ["tree-crop systems", "soil management", "carbon sequestration"]},
    ],
}

# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_weather_ometeio(city: str) -> dict:
    coords = CITIES[city]
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={coords['lat']}&longitude={coords['lon']}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m"
        f"&timezone=auto"
    )
    try:
        r = requests.get(url, timeout=6)
        d = r.json()["current"]
        return {
            "temp":       round(d["temperature_2m"], 1),
            "humidity":   d["relative_humidity_2m"],
            "feels_like": round(d["apparent_temperature"], 1),
            "wind":       d["wind_speed_10m"],
            "city":       city,
        }
    except Exception:
        return {"temp": 34, "humidity": 65, "feels_like": 38, "wind": 12, "city": city}


def get_weather_data(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OWM_API_KEY}&units=metric"
    return requests.get(url).json()


def fetch_live_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
        r = requests.get(url, timeout=8).json()
        if r.get("cod") == 200:
            return {
                "temp":       round(r["main"]["temp"], 1),
                "feels_like": round(r["main"]["feels_like"], 1),
                "humidity":   r["main"]["humidity"],
                "wind":       round(r["wind"]["speed"] * 3.6, 1),
                "source":     "openweathermap",
            }
    except Exception:
        pass
    try:
        url2 = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&current_weather=true&hourly=relativehumidity_2m,apparent_temperature")
        r2 = requests.get(url2, timeout=8).json()
        cw = r2.get("current_weather", {})
        return {"temp": round(cw.get("temperature", 30), 1), "feels_like": round(cw.get("temperature", 30)+2, 1),
                "humidity": 55, "wind": round(cw.get("windspeed", 10), 1), "source": "open-meteo"}
    except Exception:
        return {"temp": 32, "feels_like": 36, "humidity": 60, "wind": 12, "source": "fallback"}


def fetch_air_quality_openmeteo(lat, lon):
    try:
        url = (f"https://air-quality-api.open-meteo.com/v1/air-quality?"
               f"latitude={lat}&longitude={lon}&hourly=pm2_5,uv_index&timezone=auto")
        r = requests.get(url, timeout=8).json()
        hourly = r.get("hourly", {})
        pm25_vals = [v for v in hourly.get("pm2_5", []) if v is not None]
        uv_vals   = [v for v in hourly.get("uv_index", []) if v is not None]
        pm25 = round(pm25_vals[0], 1) if pm25_vals else 45.0
        uv   = round(uv_vals[0],   1) if uv_vals   else 5.0
        aqi  = min(500, int(pm25 * 4.5))
        return {"aqi": aqi, "pm25": pm25, "uv": uv}
    except Exception:
        return {"aqi": 85, "pm25": 35.0, "uv": 6.0}


def fetch_temperature_trend(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&hourly=temperature_2m&past_days=7&forecast_days=0&timezone=auto")
        r = requests.get(url, timeout=8).json()
        df = pd.DataFrame({"time": pd.to_datetime(r["hourly"]["time"]), "temp": r["hourly"]["temperature_2m"]}).dropna()
        df["date"] = df["time"].dt.date
        return df.groupby("date")["temp"].mean().reset_index().rename(columns={"date":"time"})
    except Exception:
        return pd.DataFrame()


def fetch_forecast_hourly(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
               f"&hourly=apparent_temperature&forecast_days=2&timezone=auto")
        r = requests.get(url, timeout=8).json()
        df = pd.DataFrame({"time": pd.to_datetime(r["hourly"]["time"][:24]),
                           "feels": r["hourly"]["apparent_temperature"][:24]}).dropna()
        return df
    except Exception:
        return pd.DataFrame()


def get_aqi_label(aqi):
    if aqi <= 50:    return "Good",            "#4ade80"
    elif aqi <= 100: return "Moderate",        "#ffd700"
    elif aqi <= 150: return "Unhealthy*",      "#ff8c00"
    elif aqi <= 200: return "Unhealthy",       "#ff4444"
    elif aqi <= 300: return "Very Unhealthy",  "#9b59b6"
    else:            return "Hazardous",       "#7f0000"


def get_risk_label(score):
    if score >= 75:  return "🔴 HIGH RISK",  "#ff4444"
    elif score >= 50: return "🟠 MODERATE",  "#ff8c00"
    else:             return "🟢 LOW RISK",  "#4ade80"


def format_inr(val):
    val = int(val)
    if val >= 1_00_00_000: return f"₹{val/1_00_00_000:.2f} Cr"
    elif val >= 1_00_000:  return f"₹{val/1_00_000:.2f} L"
    else:                  return f"₹{val:,}"


def plotly_dark_theme(fig, title="", height=300):
    fig.update_layout(
        title=dict(text=title, font=dict(size=11, color="#4a6080", family="Space Mono"), x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dde4f0", family="DM Sans"),
        height=height,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", color="#4a6080"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", color="#4a6080"),
    )


def result_card_html(icon, label, value, sub, color):
    return f"""
    <div style="background:rgba(255,255,255,0.02);border:1px solid {color}33;
                border-radius:12px;padding:16px;margin-bottom:10px;">
        <div style="font-size:22px;">{icon}</div>
        <div style="font-size:10px;color:#3a5070;text-transform:uppercase;letter-spacing:1.5px;">{label}</div>
        <div style="font-size:22px;font-weight:800;color:{color};margin:4px 0;font-family:'Space Mono',monospace;">{value}</div>
        <div style="font-size:11px;color:#3a5070;">{sub}</div>
    </div>"""


def compute_job_risk_w5(job_data: dict, feels_like: float) -> dict:
    heat_stress = min(100, max(0, (feels_like - 25) * 2.5))
    risk_score  = round(job_data["heat_exposure"] * 0.5 + job_data["automation_risk"] * 0.3 + heat_stress * 0.2)
    stability   = max(10, 100 - risk_score)
    return {"risk_score": risk_score, "stability": stability, "heat_stress": round(heat_stress)}


def risk_meta_w5(score: int) -> dict:
    if score >= 75: return {"label": "🔴 CRITICAL", "color": "#ff2d55"}
    if score >= 55: return {"label": "🟠 HIGH",     "color": "#ff8c35"}
    if score >= 35: return {"label": "🟡 MODERATE", "color": "#ffd60a"}
    return             {"label": "🟢 LOW",       "color": "#2ecc71"}


def compute_zone(tree_cover, ac_access, building_age, green_spaces, base_temp, rise, income_type):
    tree_cool  = tree_cover   * 0.08
    ac_benefit = ac_access    * 0.04
    age_heat   = building_age * 0.05
    green_cool = green_spaces * 0.30
    multiplier = 1.12 if income_type == "low" else 1.05
    eff_temp   = round(base_temp + rise * multiplier - tree_cool - ac_benefit - green_cool + age_heat * 0.5, 1)
    vuln       = min(100, round((100 - tree_cover) * 0.3 + (100 - ac_access) * 0.3 + building_age * 0.2 + rise * 5))
    energy     = min(100, round(
        ((100 - ac_access) * 0.4 + rise * 8) if income_type == "low"
        else ((100 - ac_access) * 0.15 + rise * 3)
    ))
    health = min(100, round(vuln * 0.7 + (100 - tree_cover) * 0.3))
    return {"eff_temp": eff_temp, "vulnerability": vuln, "energy_burden": energy, "health_risk": health}


def call_claude(prompt: str, api_key: str) -> str:
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-opus-4-5", "max_tokens": 400, "messages": [{"role": "user", "content": prompt}]},
            timeout=30,
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return f"⚠️ Could not reach Claude API: {e}"


def generate_uhi_zones(lat, lon, base_temp, tree_cover=30, traffic=50, ac_usage=60, population=70):
    np.random.seed(42)
    districts = {
        "CBD / Downtown":    {"offset": (0, 0),        "radius": 0.03,  "heat_mult": 1.4,  "n": 60},
        "Industrial Zone":   {"offset": (0.04, -0.03), "radius": 0.025, "heat_mult": 1.6,  "n": 50},
        "Residential Dense": {"offset": (-0.03, 0.04), "radius": 0.03,  "heat_mult": 1.2,  "n": 55},
        "Suburban":          {"offset": (0.06, 0.05),  "radius": 0.04,  "heat_mult": 0.85, "n": 50},
        "Green Park Zone":   {"offset": (-0.05,-0.04), "radius": 0.025, "heat_mult": 0.65, "n": 40},
        "Mixed Commercial":  {"offset": (0.01, 0.06),  "radius": 0.035, "heat_mult": 1.15, "n": 45},
    }
    all_points = []
    for dname, cfg in districts.items():
        dlat, dlon = cfg["offset"]
        for _ in range(cfg["n"]):
            angle = np.random.uniform(0, 2 * np.pi)
            r     = np.random.uniform(0, cfg["radius"])
            pt_lat = lat + dlat + r * np.cos(angle)
            pt_lon = lon + dlon + r * np.sin(angle)
            base_score = (
                (100 - tree_cover) * 0.20 + traffic * 0.20 +
                ac_usage * 0.15 + population * 0.15 + 50 * 0.10 + 30 * 0.10 + 40 * 0.10
            )
            heat_score = min(max(base_score * cfg["heat_mult"] * np.random.uniform(0.85, 1.15), 0), 100)
            all_points.append({"lat": pt_lat, "lon": pt_lon, "heat_score": heat_score,
                                "district": dname, "weight": heat_score / 100})
    return pd.DataFrame(all_points), districts


def get_district_risk_level(heat_mult):
    if heat_mult >= 1.4:   return "🔴 EXTREME", "risk-card"
    elif heat_mult >= 1.1: return "🟠 MODERATE", "risk-card-orange"
    else:                  return "🟢 LOW",      "risk-card-green"


def generate_heat_forecast(base_score, days=7):
    np.random.seed(7)
    forecast, score = [], base_score
    for _ in range(days):
        score = max(0, min(100, score + np.random.normal(0.5, 2.5)))
        forecast.append(round(score, 2))
    return forecast


def progress_bar_w4(label, value, color):
    st.markdown(f"""
    <div style="margin-bottom:10px;">
        <div style="font-size:11px;color:#4a6080;margin-bottom:4px;font-family:'Space Mono',monospace;">
            {label} — <b style="color:{color};">{value}</b>
        </div>
        <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:6px;">
            <div style="width:{min(value,100)}%;background:{color};height:6px;border-radius:4px;
                        box-shadow:0 0 8px {color}66;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:4px;'>
        <div style='font-family:"Space Mono",monospace; font-size:22px; font-weight:700; color:#4a9eff; letter-spacing:-1px;'>U.R.I.E</div>
        <div style='font-size:10px; color:#3a5070; letter-spacing:2px; text-transform:uppercase;'>Urban Resilience Intelligence Engine</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected_city = st.selectbox("🏙️ City", list(CITIES.keys()), index=0)

    if st.button("🔄 Refresh Weather", use_container_width=True):
        fetch_weather_ometeio.clear()
        st.rerun()

    weather_sidebar = fetch_weather_ometeio(selected_city)

    st.markdown("---")
    st.markdown('<div class="section-label">Live Weather</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("Temp", f"{weather_sidebar['temp']}°C")
    c2.metric("Feels", f"{weather_sidebar['feels_like']}°C")
    c1.metric("Humidity", f"{weather_sidebar['humidity']}%")
    c2.metric("Wind", f"{weather_sidebar['wind']} km/h")

    st.markdown("---")
    st.markdown('<div class="section-label">Claude AI (optional)</div>', unsafe_allow_html=True)
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.caption("Enables AI career & policy insights")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:10px; color:#2a3a50; text-align:center; line-height:1.8;'>
        Live data via Open-Meteo<br>
        AI via Claude · Made for India
    </div>
    """, unsafe_allow_html=True)

# ─── HORIZONTAL WINDOW NAVIGATION ─────────────────────────────────────────────

WINDOWS = [
    {"num": "01", "icon": "🔥", "label": "Live Heat Dashboard"},
    {"num": "02", "icon": "🌍", "label": "Behaviour Simulator"},
    {"num": "03", "icon": "💰", "label": "Cooling ROI"},
    {"num": "04", "icon": "👷", "label": "Job Risk Analyzer"},
    {"num": "05", "icon": "🌱", "label": "Livelihood Pivot"},
    {"num": "06", "icon": "⚖️", "label": "Thermal Equity"},
]

if "active_window" not in st.session_state:
    st.session_state.active_window = 0

# Render nav tabs using columns
cols = st.columns(len(WINDOWS))
for i, (col, w) in enumerate(zip(cols, WINDOWS)):
    with col:
        is_active = st.session_state.active_window == i
        btn_style = (
            "background:linear-gradient(135deg,#0f1f38,#1a3060)!important;"
            "border:1px solid #1e4a8a!important;"
            "box-shadow:0 0 15px rgba(30,74,138,0.3)!important;"
        ) if is_active else ""
        if st.button(f"{w['icon']} {w['num']}\n{w['label']}", key=f"nav_{i}", use_container_width=True):
            st.session_state.active_window = i
            st.rerun()

st.markdown("<hr style='border-color:#0d1825; margin:8px 0 24px 0;'>", unsafe_allow_html=True)

window = st.session_state.active_window
city_cfg = CITIES[selected_city]

# ─── WINDOW 1: LIVE HEAT DASHBOARD ────────────────────────────────────────────

if window == 0:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">01</div>
        <div class="win-title-wrap">
            <div class="win-title">Live Heat Dashboard</div>
            <div class="win-sub">Real-time climate & behaviour intelligence</div>
        </div>
    </div>""", unsafe_allow_html=True)

    city_input = st.text_input("Enter City Name", placeholder="e.g. Mumbai, Delhi, London...")

    if city_input:
        data = get_weather_data(city_input)
        if data.get("cod") != 200:
            st.error("City not found. Please try again.")
            st.stop()

        live_temp  = data["main"]["temp"]
        humidity   = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        condition  = data["weather"][0]["main"]
        lat        = data["coord"]["lat"]
        lon        = data["coord"]["lon"]
        heat_index = live_temp + (humidity * 0.05)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌡 Temperature (°C)", live_temp)
        c2.metric("💧 Humidity (%)", humidity)
        c3.metric("💨 Wind Speed (m/s)", wind_speed)
        c4.metric("🌤 Condition", condition)

        st.markdown("---")
        st.markdown("#### 🏙 Urban Behaviour Inputs")

        col_l, col_r = st.columns(2)
        with col_l:
            tree_cover       = st.slider("🌳 Tree Cover %",            0, 100, 30)
            traffic          = st.slider("🚗 Traffic Level %",          0, 100, 50)
            ac_usage         = st.slider("❄ AC Usage %",                0, 100, 60)
            population       = st.slider("👥 Population Density %",     0, 100, 70)
        with col_r:
            albedo           = st.slider("☀ Surface Albedo %",          0, 100, 20)
            green_roof       = st.slider("🏢 Green Roof Coverage %",    0, 100, 15)
            public_transport = st.slider("🚆 Public Transport Usage %", 0, 100, 40)

        if st.button("🚀 Calculate Heat Score", use_container_width=True, type="primary"):
            sim_score = (
                (100 - tree_cover) * 0.20 + traffic * 0.20 +
                ac_usage * 0.15 + population * 0.15 +
                (100 - albedo) * 0.10 + (100 - green_roof) * 0.10 +
                (100 - public_transport) * 0.10
            )
            final_score = (sim_score * 0.6) + (heat_index * 0.4)

            st.markdown("---")
            st.progress(int(min(final_score, 100)))
            st.metric("Final Heat Score", round(final_score, 2))

            if final_score < 40:   st.success("🟢 Low Heat Risk")
            elif final_score < 70: st.warning("🟠 Moderate Heat Risk")
            else:                  st.error("🔴 Extreme Heat Risk")

            cg, cr = st.columns(2)
            with cg:
                st.markdown('<div class="graph-label">Urban Heat Vulnerability Gauge</div>', unsafe_allow_html=True)
                gauge = go.Figure(go.Indicator(
                    mode="gauge+number", value=final_score,
                    title={'text': "Heat Score", 'font': {'color': '#4a6080', 'size': 12}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickcolor': '#3a5070'},
                        'bar': {'color': '#4a9eff'},
                        'bgcolor': 'rgba(0,0,0,0)',
                        'steps': [
                            {'range': [0,  40], 'color': "rgba(46,204,113,0.2)"},
                            {'range': [40, 70], 'color': "rgba(255,140,53,0.2)"},
                            {'range': [70,100], 'color': "rgba(255,68,0,0.2)"}
                        ]
                    }
                ))
                gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#dde4f0', height=250)
                st.plotly_chart(gauge, use_container_width=True)

            with cr:
                st.markdown('<div class="graph-label">Urban Factor Radar</div>', unsafe_allow_html=True)
                radar_df = pd.DataFrame({
                    "Factor": ["Tree Cover","Traffic","AC Usage","Population","Albedo","Green Roof","Public Transport"],
                    "Value":  [tree_cover, traffic, ac_usage, population, albedo, green_roof, public_transport]
                })
                radar = px.line_polar(radar_df, r="Value", theta="Factor", line_close=True)
                radar.update_traces(fill="toself", line_color="#4a9eff", fillcolor="rgba(74,158,255,0.15)")
                radar.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#dde4f0',
                                    polar=dict(bgcolor='rgba(0,0,0,0)'), height=250)
                st.plotly_chart(radar, use_container_width=True)

            forecast = generate_heat_forecast(final_score)
            days_labels = ["Today","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"]
            ff = go.Figure()
            ff.add_trace(go.Scatter(x=days_labels, y=forecast, mode='lines+markers',
                line=dict(color='#4a9eff', width=3), marker=dict(size=7),
                fill='tozeroy', fillcolor='rgba(74,158,255,0.08)', name="Projected"))
            ff.add_hline(y=70, line_dash="dot", line_color="#ff4444", annotation_text="Extreme (70)")
            ff.add_hline(y=40, line_dash="dot", line_color="#ff8c35", annotation_text="Moderate (40)")
            plotly_dark_theme(ff, "7-DAY HEAT SCORE FORECAST", 280)
            st.plotly_chart(ff, use_container_width=True)

# ─── WINDOW 2: BEHAVIOUR SIMULATOR ────────────────────────────────────────────

elif window == 1:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">02</div>
        <div class="win-title-wrap">
            <div class="win-title">Behaviour Simulator & UHI Explorer</div>
            <div class="win-sub">Urban scenario projection & district-level heat island mapping</div>
        </div>
    </div>""", unsafe_allow_html=True)

    city_input = st.text_input("Enter City for Simulation", placeholder="e.g. Chennai, Tokyo, Berlin...")

    if city_input:
        data = get_weather_data(city_input)
        if data.get("cod") != 200:
            st.error("City not found.")
            st.stop()

        temp     = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        lat      = data["coord"]["lat"]
        lon      = data["coord"]["lon"]

        c1, c2 = st.columns(2)
        c1.metric("Temperature (°C)", temp)
        c2.metric("Humidity (%)", humidity)

        st.markdown("---")
        sc_col, map_col = st.columns([1, 1])
        with sc_col:
            scenario = st.selectbox("Urban Scenario", ["Green Smart City", "Industrial Expansion", "High Traffic City"])
        with map_col:
            layer_type = st.selectbox("Map Layer Type", ["Heatmap", "Scatter Bubbles", "Both"])

        presets = {"Green Smart City": (75, 40, 35), "Industrial Expansion": (25, 70, 65), "High Traffic City": (35, 60, 85)}
        default_tree, default_ac, default_traffic = presets[scenario]

        sc1, sc2 = st.columns(2)
        with sc1:
            tree_cover = st.slider("🌳 Tree Cover %",          0, 100, default_tree,    key="sim_tree")
            traffic_s  = st.slider("🚗 Traffic Level %",       0, 100, default_traffic, key="sim_traffic")
        with sc2:
            ac_usage   = st.slider("❄ AC Usage %",             0, 100, default_ac,      key="sim_ac")
            population = st.slider("👥 Population Density %",  0, 100, 70,              key="sim_pop")

        if st.button("🚀 Run Simulation & Generate Zone Map", use_container_width=True, type="primary"):
            baseline_heat   = temp + (humidity * 0.05)
            impact          = (100 - tree_cover) * 0.3 + ac_usage * 0.3 + traffic_s * 0.4
            projected_score = (baseline_heat * 0.5) + (impact * 0.5)
            sustainability  = tree_cover * 0.5 + (100 - traffic_s) * 0.3 + (100 - ac_usage) * 0.2

            m1, m2 = st.columns(2)
            m1.metric("🔥 Projected Heat Score", round(projected_score, 2))
            m2.metric("🌱 Sustainability Score",  round(sustainability,  2))

            scenarios_list = ["Green Smart City", "Industrial Expansion", "High Traffic City"]
            params = [(75, 40, 35), (25, 70, 65), (35, 60, 85)]
            scores = [round((baseline_heat * 0.5) + (((100-t)*0.3 + a*0.3 + tr*0.4) * 0.5), 2) for t, a, tr in params]

            bar_fig = go.Figure(go.Bar(
                x=scenarios_list, y=scores,
                marker_color=["rgba(46,204,113,0.8)","rgba(255,68,0,0.8)","rgba(255,140,53,0.8)"],
                text=[f"{s:.1f}" for s in scores], textposition="outside"
            ))
            bar_fig.add_hline(y=projected_score, line_dash="dash", line_color="#4a9eff",
                              annotation_text=f"Selected: {projected_score:.1f}")
            plotly_dark_theme(bar_fig, "SCENARIO COMPARISON — PROJECTED HEAT SCORE", 280)
            st.plotly_chart(bar_fig, use_container_width=True)

            with st.spinner("Analysing urban zones..."):
                zone_df, districts = generate_uhi_zones(lat, lon, temp, tree_cover, traffic_s, ac_usage, population)

            st.markdown("#### 🏘️ District Risk Assessment")
            dist_cols = st.columns(3)
            for idx, (dname, cfg) in enumerate(districts.items()):
                risk_label, card_class = get_district_risk_level(cfg["heat_mult"])
                avg_score = zone_df[zone_df["district"] == dname]["heat_score"].mean()
                with dist_cols[idx % 3]:
                    st.markdown(f"""
                    <div class="{card_class}">
                        <div style="font-size:10px;letter-spacing:2px;opacity:0.6;">{risk_label}</div>
                        <div style="font-size:14px;font-weight:700;margin:4px 0;">{dname}</div>
                        <div style="font-size:12px;color:#4a6080;">Score: <span style="color:#4a9eff;font-weight:bold;">{avg_score:.1f}/100</span></div>
                        <div style="font-size:11px;color:#3a5070;">UHI: {cfg['heat_mult']}x</div>
                    </div>""", unsafe_allow_html=True)

            if PYDECK_AVAILABLE:
                import pydeck as pdk
                layers = []
                if layer_type in ["Heatmap", "Both"]:
                    layers.append(pdk.Layer("HeatmapLayer", zone_df, get_position="[lon, lat]",
                        get_weight="weight", opacity=0.85, radius_pixels=60,
                        color_range=[[0,100,200,50],[0,200,100,100],[255,220,0,150],[255,100,0,200],[255,30,0,255]]))
                if layer_type in ["Scatter Bubbles", "Both"]:
                    zone_df["color"] = zone_df["heat_score"].apply(
                        lambda s: [255,30,0,180] if s>70 else [255,140,53,160] if s>40 else [46,204,113,150])
                    layers.append(pdk.Layer("ScatterplotLayer", zone_df, get_position="[lon, lat]",
                        get_radius=1200, get_fill_color="color", pickable=True, opacity=0.7))

                st.pydeck_chart(pdk.Deck(layers=layers,
                    initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=11, pitch=45),
                    map_style="mapbox://styles/mapbox/dark-v10",
                    tooltip={"html": "<b>{district}</b><br/>Heat Score: {heat_score:.1f}",
                             "style": {"backgroundColor":"rgba(6,10,18,0.9)","color":"#4a9eff"}}))
            else:
                st.info("Install pydeck for interactive maps: `pip install pydeck`")

# ─── WINDOW 3: COOLING ROI ────────────────────────────────────────────────────

elif window == 2:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">03</div>
        <div class="win-title-wrap">
            <div class="win-title">Cooling ROI Analyzer</div>
            <div class="win-sub">Economic impact of urban cooling interventions</div>
        </div>
    </div>""", unsafe_allow_html=True)

    weather_w3 = fetch_live_weather(city_cfg["lat"], city_cfg["lon"])
    air_w3     = fetch_air_quality_openmeteo(city_cfg["lat"], city_cfg["lon"])
    aqi_lbl, aqi_col = get_aqi_label(air_w3["aqi"])
    population = st.number_input("Population", 50_000, 50_000_000, city_cfg["pop"], 10_000)

    st.markdown(f"""
    <div class="info-banner">
        🌡 {weather_w3['temp']}°C &nbsp;·&nbsp; Feels {weather_w3['feels_like']}°C &nbsp;·&nbsp;
        💧 {weather_w3['humidity']}% &nbsp;·&nbsp; ⚡ ₹{city_cfg['elec']}/kWh &nbsp;·&nbsp;
        <span style="color:{aqi_col}">AQI {air_w3['aqi']} ({aqi_lbl})</span> &nbsp;·&nbsp;
        UV {air_w3['uv']}
    </div>""", unsafe_allow_html=True)

    trend_df    = fetch_temperature_trend(city_cfg["lat"], city_cfg["lon"])
    forecast_df = fetch_forecast_hourly(city_cfg["lat"], city_cfg["lon"])

    ch1, ch2 = st.columns(2)
    with ch1:
        if not trend_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=trend_df["time"], y=trend_df["temp"], mode="lines",
                line=dict(color="#4a9eff", width=2), fill="tozeroy", fillcolor="rgba(74,158,255,0.06)"))
            fig.add_hline(y=35, line_dash="dash", line_color="#ff4444", annotation_text="35°C threshold")
            plotly_dark_theme(fig, "PAST 7 DAYS TEMPERATURE TREND", 220)
            st.plotly_chart(fig, use_container_width=True)
    with ch2:
        if not forecast_df.empty:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=forecast_df["time"], y=forecast_df["feels"], mode="lines",
                line=dict(color="#ffd700", width=2), fill="tozeroy", fillcolor="rgba(255,215,0,0.06)"))
            plotly_dark_theme(fig2, "NEXT 24H HEAT INDEX FORECAST", 220)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        tree_improve   = st.slider("🌳 Tree Cover Increase (%)", 1, 50, 10)
        cost_per_tree  = st.number_input("Cost per Tree (₹)", 100, 50000, 2500, 100)
        trees_to_plant = st.number_input("Total Trees to Plant", 100, 5_000_000, 50000, 1000)
    with col_b:
        ac_hours   = st.number_input("AC Usage per HH/Day (hrs)", 0.0, 24.0, 6.0, 0.5, format="%.1f")
        ac_kw      = st.number_input("AC Capacity (kW)", 0.5, 5.0, 1.5, 0.1, format="%.1f")
        outdoor_pct= st.slider("Outdoor Workers (% of pop)", 1, 60, 18)
    with col_c:
        daily_wage    = st.number_input("Avg Daily Wage (₹)", 100, 5000, 600, 50)
        heat_hrs_lost = st.number_input("Heat Work Hours Lost/Worker/Yr", 0, 500, 48, 1)
        illness_cost  = st.number_input("Heat Illness Cost (₹)", 500, 200000, 8000, 500)
        illness_rate  = st.number_input("Heat Illness Cases/1000 People", 0.1, 50.0, 3.5, 0.1, format="%.1f")

    temp_factor       = max(0.8, (weather_w3["temp"] - 20) / 15)
    uv_factor         = max(1.0, air_w3["uv"] / 6)
    aqi_health_factor = max(1.0, air_w3["aqi"] / 80)
    households        = round(population / 4.5)
    outdoor_workers   = round(population * outdoor_pct / 100)
    f                 = tree_improve / 100

    daily_kwh_saved      = households * ac_kw * ac_hours * f * 0.25 * temp_factor
    annual_energy_saving = round(daily_kwh_saved * 365 * city_cfg["elec"])
    hourly_wage          = daily_wage / 8
    productivity_saving  = round(outdoor_workers * heat_hrs_lost * hourly_wage * f * temp_factor)
    total_cases          = round(population / 1000 * illness_rate)
    health_saving        = round(total_cases * illness_cost * f * aqi_health_factor)
    total_investment     = trees_to_plant * cost_per_tree
    co2_offset           = round(trees_to_plant * 22)
    total_benefit        = annual_energy_saving + productivity_saving + health_saving
    break_even           = round(total_investment / total_benefit, 1) if total_benefit > 0 else "∞"
    roi_pct              = round((total_benefit / total_investment) * 100, 1) if total_investment > 0 else 0

    st.markdown("---")
    st.success(f"**Total Annual Economic Benefit: {format_inr(total_benefit)}** | Break-Even: {break_even} yrs | ROI: {roi_pct}%")

    r1, r2, r3, r4 = st.columns(4)
    with r1: st.markdown(result_card_html("❄️", "Energy Savings",    format_inr(annual_energy_saving), f"₹{city_cfg['elec']}/kWh tariff", "#4a9eff"), unsafe_allow_html=True)
    with r2: st.markdown(result_card_html("💼", "Productivity Gain", format_inr(productivity_saving),  f"{outdoor_workers:,} workers",    "#ff8c35"), unsafe_allow_html=True)
    with r3: st.markdown(result_card_html("🏥", "Health Cost Saved", format_inr(health_saving),        f"AQI factor ×{aqi_health_factor:.2f}", "#f472b6"), unsafe_allow_html=True)
    with r4: st.markdown(result_card_html("🌿", "CO₂ Offset",        f"{co2_offset:,} kg/yr",           f"{trees_to_plant:,} trees",       "#2ecc71"), unsafe_allow_html=True)

    fig3 = go.Figure(go.Bar(
        x=["Energy Savings", "Productivity Gain", "Health Savings"],
        y=[annual_energy_saving, productivity_saving, health_saving],
        marker_color=["#4a9eff", "#ff8c35", "#f472b6"],
        text=[format_inr(annual_energy_saving), format_inr(productivity_saving), format_inr(health_saving)],
        textposition="outside",
    ))
    plotly_dark_theme(fig3, "BENEFIT BREAKDOWN — ANNUAL ECONOMIC IMPACT", 280)
    st.plotly_chart(fig3, use_container_width=True)

# ─── WINDOW 4: JOB CLIMATE RISK ANALYZER ──────────────────────────────────────

elif window == 3:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">04</div>
        <div class="win-title-wrap">
            <div class="win-title">Job Climate Risk Analyzer</div>
            <div class="win-sub">Employment stability under live weather & air quality conditions</div>
        </div>
    </div>""", unsafe_allow_html=True)

    weather_w4 = fetch_live_weather(city_cfg["lat"], city_cfg["lon"])
    air_w4     = fetch_air_quality_openmeteo(city_cfg["lat"], city_cfg["lon"])
    aqi_lbl, aqi_col = get_aqi_label(air_w4["aqi"])

    st.markdown(f"""
    <div class="info-banner">
        🌡 {weather_w4['temp']}°C &nbsp;·&nbsp; Feels {weather_w4['feels_like']}°C &nbsp;·&nbsp;
        💧 {weather_w4['humidity']}% RH &nbsp;·&nbsp;
        <span style="color:{aqi_col}">AQI {air_w4['aqi']} ({aqi_lbl})</span> &nbsp;·&nbsp;
        UV {air_w4['uv']} &nbsp;·&nbsp; Wind {weather_w4['wind']} km/h
    </div>""", unsafe_allow_html=True)

    jc1, jc2, jc3 = st.columns(3)
    with jc1:
        selected_job = st.selectbox("Job Sector", list(JOB_DATA_W4.keys()))
        job = JOB_DATA_W4[selected_job]
        outdoor_hrs = st.number_input("Daily Outdoor Hours", 0.0, 16.0, float(job["outdoor_hours"]), 0.5, format="%.1f")
        work_days   = st.number_input("Working Days per Year", 50, 365, 288, 1)
    with jc2:
        num_workers    = st.number_input("Workers in Sector", 100, 5_000_000, 50000, 1000)
        monthly_wage   = st.number_input("Avg Monthly Wage (₹)", 3000, 200000, 18000, 500)
        heat_threshold = st.number_input("Safe Work Temp (°C)", 25.0, 45.0, 35.0, 0.5, format="%.1f")
    with jc3:
        prod_loss_pct = st.slider("Productivity Loss Above Threshold (%)", 5, 80, 35)
        custom_heat   = st.slider("Override Heat Exposure (%) — 0=auto", 0, 100, 0)
        custom_auto   = st.slider("Override Automation Risk (%) — 0=auto", 0, 100, 0)

    temp_f  = max(0.7, (weather_w4["temp"] - 22) / 14)
    humid_f = max(0.9, (weather_w4["humidity"] - 40) / 50)
    uv_f    = max(1.0, air_w4["uv"] / 7)
    aqi_f   = max(1.0, air_w4["aqi"] / 100)

    heat_exp  = custom_heat if custom_heat > 0 else job["heat_exposure"]
    auto_risk = custom_auto if custom_auto > 0 else job["automation_risk"]
    eff_heat   = min(100, round(heat_exp * (0.5 + temp_f * 0.3 + uv_f * 0.2)))
    risk_score = min(100, round(job["base_risk"] * (0.55 + temp_f * 0.2 + humid_f * 0.1 + aqi_f * 0.15)))
    stability  = max(8, round(100 - risk_score * 0.55 - auto_risk * 0.45))

    above_thresh     = max(0.0, weather_w4["temp"] - heat_threshold)
    heat_days_est    = min(200, round(above_thresh * 10 + 20))
    prod_loss_annual = round(num_workers * (monthly_wage / 22) * (prod_loss_pct / 100) * heat_days_est)
    income_at_risk   = round(num_workers * monthly_wage * 12 * (risk_score / 100) * 0.15)
    total_loss       = prod_loss_annual + income_at_risk
    risk_label, risk_color = get_risk_label(risk_score)

    st.markdown(f"""
    <div style="background:{risk_color}15;border:1px solid {risk_color}44;
                border-radius:12px;padding:16px 22px;margin:16px 0;">
        <span style="font-size:20px;font-weight:800;color:{risk_color};">{risk_label} · {selected_job}</span><br>
        <span style="font-size:12px;color:#4a6080;font-family:'Space Mono',monospace;">
            {selected_city} · {weather_w4['temp']}°C / {weather_w4['humidity']}% RH / AQI {air_w4['aqi']} / {num_workers:,} workers
        </span>
    </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1.5])
    with col_l:
        progress_bar_w4("🌡️ Climate Risk Score",     risk_score,                  risk_color)
        progress_bar_w4("🛡️ Stability Index",         stability,                   "#2ecc71")
        progress_bar_w4("☀️ Effective Heat Exposure", eff_heat,                    "#ff8c35")
        progress_bar_w4("🤖 Automation Risk",         auto_risk,                   "#4a9eff")
        progress_bar_w4("🌬 AQI Stress",              min(100, air_w4["aqi"]),    "#f472b6")
        progress_bar_w4("🔆 UV Index",                min(100, int(air_w4["uv"]*8)), "#ffd700")

        fig_radar = go.Figure(go.Scatterpolar(
    r=[risk_score, eff_heat, auto_risk, min(100, air_w4["aqi"]), min(100, int(air_w4["uv"]*8)), stability],
    theta=["Heat Risk", "Effective Heat", "Automation Risk", "AQI", "UV Risk", "Infrastructure Stability"],
    fill='toself',
    fillcolor="rgba(255,140,0,0.2)",
    line=dict(color=risk_color, width=2),
))
        
        fig_radar.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True, range=[0,100]),
                       angularaxis=dict(tickfont=dict(size=9, color="#4a6080"))),
            paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=30,b=20),
            height=240, showlegend=False, font_color="#dde4f0",
            title=dict(text="RISK RADAR", font=dict(size=10, color="#4a6080"), x=0),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_r:
        st.markdown(f"""
        <div style="background:rgba(255,68,68,0.06);border:1px solid rgba(255,68,68,0.25);
                    border-radius:12px;padding:18px;margin-bottom:14px;">
            <div style="font-size:10px;color:#ff4444;margin-bottom:12px;text-transform:uppercase;letter-spacing:1.5px;font-family:'Space Mono',monospace;">
                Economic Impact — {num_workers:,} Workers · {selected_city}
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
                <div>
                    <div style="font-size:10px;color:#3a5070;">PRODUCTIVITY LOSS/YR</div>
                    <div style="font-size:22px;color:#ff4444;font-weight:800;font-family:'Space Mono',monospace;">{format_inr(prod_loss_annual)}</div>
                    <div style="font-size:10px;color:#3a5070;">~{heat_days_est} heat days/yr</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#3a5070;">INCOME AT RISK/YR</div>
                    <div style="font-size:22px;color:#ff8c35;font-weight:800;font-family:'Space Mono',monospace;">{format_inr(income_at_risk)}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#3a5070;">TOTAL WORKFORCE LOSS</div>
                    <div style="font-size:22px;color:#e8f0ff;font-weight:800;font-family:'Space Mono',monospace;">{format_inr(total_loss)}</div>
                </div>
                <div>
                    <div style="font-size:10px;color:#3a5070;">TEMP STATUS</div>
                    <div style="font-size:13px;color:{'#ff4444' if weather_w4['temp'] > heat_threshold else '#2ecc71'};margin-top:4px;font-weight:700;">
                        {'⚠ EXCEEDS THRESHOLD' if weather_w4['temp'] > heat_threshold else '✓ SAFE RANGE'}
                    </div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        if weather_w4["temp"] > heat_threshold:
            st.error(f"🚨 **LIVE ALERT** — {weather_w4['temp']}°C exceeds {heat_threshold}°C. Workers face active heat risk **right now**.")
        if air_w4["aqi"] > 100:
            st.warning(f"⚠️ AQI {air_w4['aqi']} ({aqi_lbl}). PM2.5: {air_w4['pm25']} µg. Extended outdoor work not advisable.")

        forecast_w4 = fetch_forecast_hourly(city_cfg["lat"], city_cfg["lon"])
        if not forecast_w4.empty:
            fig_fc = go.Figure()
            fig_fc.add_trace(go.Scatter(x=forecast_w4["time"], y=forecast_w4["feels"], mode="lines+markers",
                line=dict(color=risk_color, width=2), fill="tozeroy", fillcolor="rgba(255,140,0,0.2)"))
            fig_fc.add_hline(y=heat_threshold, line_dash="dash", line_color="#ff4444",
                             annotation_text=f"Safe Limit {heat_threshold}°C")
            plotly_dark_theme(fig_fc, "NEXT 24H — HEAT INDEX VS SAFE THRESHOLD", 200)
            st.plotly_chart(fig_fc, use_container_width=True)

    with st.expander("🌱 Livelihood Pivot Suggestions"):
        pc = st.columns(3)
        for i, p in enumerate(job["pivot"]):
            with pc[i]:
                rc = "#2ecc71" if "Low" in p["risk"] else "#ff8c35"
                st.markdown(f"""
                <div style="background:rgba(46,204,113,0.06);border:1px solid rgba(46,204,113,0.2);
                            border-radius:12px;padding:18px;">
                    <div style="font-size:14px;font-weight:700;color:#e8f0ff;margin-bottom:6px;">{p['title']}</div>
                    <div style="font-size:11px;color:#4a6080;margin-bottom:10px;">{p['skills']}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:10px;color:#3a5070;">STABILITY</div>
                            <div style="font-size:24px;color:#2ecc71;font-weight:800;font-family:'Space Mono',monospace;">{p['stability']}%</div>
                        </div>
                        <div style="padding:4px 10px;border-radius:100px;font-size:10px;background:{rc}20;color:{rc};">{p['risk']} RISK</div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ─── WINDOW 5: LIVELIHOOD PIVOT ENGINE ────────────────────────────────────────

elif window == 4:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">05</div>
        <div class="win-title-wrap">
            <div class="win-title">Livelihood Pivot Engine</div>
            <div class="win-sub">Climate stress → Green career transition pathways</div>
        </div>
    </div>""", unsafe_allow_html=True)

    weather_w5 = fetch_weather_ometeio(selected_city)

    st.markdown('<p class="section-label">Select Your Current Job Sector</p>', unsafe_allow_html=True)
    job_label = st.selectbox("", list(JOB_DATA_W5.keys()), label_visibility="collapsed")
    job_w5    = JOB_DATA_W5[job_label]

    scores_w5 = compute_job_risk_w5(job_w5, weather_w5["feels_like"])
    meta_w5   = risk_meta_w5(scores_w5["risk_score"])

    st.markdown("#### 📊 Risk Gauges")
    g1, g2, g3, g4 = st.columns(4)

    def gauge_card(col, label, val, note=""):
        with col:
            color = "#ff4444" if val >= 75 else "#ff8c35" if val >= 50 else "#2ecc71"
            col.markdown(f"""
            <div class="card">
                <div class="section-label">{label}</div>
                <div style="font-size:32px;font-weight:900;color:{color};font-family:'Space Mono',monospace;">{val}<span style="font-size:16px;color:#3a5070;">%</span></div>
                {f'<div style="font-size:11px;color:#3a5070;">{note}</div>' if note else ''}
            </div>""", unsafe_allow_html=True)
            col.progress(val / 100)

    gauge_card(g1, "🔥 Heat Exposure",    job_w5["heat_exposure"])
    gauge_card(g2, "🤖 Automation Risk",  job_w5["automation_risk"])
    gauge_card(g3, f"🌡 Live Heat Stress", scores_w5["heat_stress"], f"from {weather_w5['feels_like']}°C")
    gauge_card(g4, "✅ Job Stability",     scores_w5["stability"])

    st.markdown("**Transferable Skills:**")
    chips = " ".join([f'<span class="skill-chip">{s}</span>' for s in job_w5["skills"]])
    st.markdown(chips, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("⚡ Analyze Climate Risk & Find Green Pivots", use_container_width=True, type="primary"):
        with st.spinner("Analyzing..."):
            time.sleep(0.4)

        color_w5 = meta_w5["color"]
        st.markdown(f"""
        <div class="risk-banner">
            <div class="risk-score" style="color:{color_w5}">{scores_w5['risk_score']}</div>
            <div>
                <div class="risk-label" style="color:{color_w5}">{meta_w5['label']} Risk</div>
                <div class="risk-detail">
                    Live {weather_w5['temp']}°C · {job_w5['heat_exposure']}% heat exposure · {job_w5['automation_risk']}% automation risk
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if scores_w5["risk_score"] >= 45:
            st.markdown("### 🌱 Recommended Green Career Pivots")
            careers = GREEN_CAREERS.get(job_w5["key"], [])
            for c in careers:
                skill_html = " ".join([f'<span class="green-skill-chip">{s}</span>' for s in c["skills"]])
                risk_color_c = "#2ecc71" if c["risk"] == "Low" else "#ff8c35"
                st.markdown(f"""
                <div class="career-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span class="career-title">{c['title']}</span>
                        <span class="career-salary">{c['salary']}</span>
                    </div>
                    <span class="badge badge-green">✅ {c['stability']}% Stable</span>
                    <span class="badge badge-blue">🌍 {c['risk']} Climate Risk</span>
                    <br/><br/>{skill_html}
                </div>
                """, unsafe_allow_html=True)

            if api_key:
                if st.button("🤖 Get AI-Powered Career Advice", key="ai5"):
                    prompt = f"""You are a climate & career advisor. A {job_label} in {selected_city} faces:
- Live temperature: {weather_w5['temp']}°C (feels like {weather_w5['feels_like']}°C)
- Job heat exposure: {job_w5['heat_exposure']}%
- Automation risk: {job_w5['automation_risk']}%
- Overall risk score: {scores_w5['risk_score']}/100

In exactly 3 bullet points (max 25 words each), give actionable, India-specific advice for transitioning to a green career. Be direct and practical."""
                    with st.spinner("Getting AI advice..."):
                        insight = call_claude(prompt, api_key)
                    st.markdown(f"""
                    <div class="ai-box">
                        <div class="ai-title">🧠 AI Career Advisor — {selected_city}</div>
                        <div style="color:#8a9ab8; font-size:14px; line-height:1.9;">{insight.replace(chr(10), '<br>')}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Add your Claude API key in the sidebar to get personalized AI career advice.")
        else:
            st.success(f"✅ **{job_label}** shows relatively low climate risk (score: {scores_w5['risk_score']}/100). Focus on green certifications to future-proof your career.")

# ─── WINDOW 6: THERMAL EQUITY LENS ────────────────────────────────────────────

elif window == 5:
    st.markdown("""
    <div class="win-header">
        <div class="win-num">06</div>
        <div class="win-title-wrap">
            <div class="win-title">Thermal Equity Lens</div>
            <div class="win-sub">Climate justice — who bears the heat burden?</div>
        </div>
    </div>""", unsafe_allow_html=True)

    weather_w6 = fetch_weather_ometeio(selected_city)

    st.markdown('<p class="section-label">Projected Temperature Rise Scenario</p>', unsafe_allow_html=True)
    temp_rise = st.select_slider("", options=[1.0, 1.5, 2.0, 2.5, 3.0, 4.0], value=2.0,
                                  format_func=lambda x: f"+{x}°C", label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🏙️ Configure Two Zones")
    col_hi, col_lo = st.columns(2)

    with col_hi:
        st.markdown('<div class="zone-box-hi">', unsafe_allow_html=True)
        st.markdown("#### 🏙️ HIGH-INCOME ZONE")
        hi_tree  = st.slider("Tree Cover %",              0,  80, 35, key="hi_tree")
        hi_ac    = st.slider("AC Access %",               0, 100, 80, key="hi_ac")
        hi_age   = st.slider("Avg Building Age (yrs)",    1,  80, 10, key="hi_age")
        hi_green = st.slider("Green Spaces (parks/km²)",  0,  15,  5, key="hi_green")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_lo:
        st.markdown('<div class="zone-box-lo">', unsafe_allow_html=True)
        st.markdown("#### 🏚️ LOW-INCOME ZONE")
        lo_tree  = st.slider("Tree Cover %",              0,  80,  8, key="lo_tree")
        lo_ac    = st.slider("AC Access %",               0, 100, 15, key="lo_ac")
        lo_age   = st.slider("Avg Building Age (yrs)",    1,  80, 35, key="lo_age")
        lo_green = st.slider("Green Spaces (parks/km²)",  0,  15,  1, key="lo_green")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.button("⚖️ Analyze Thermal Inequality", use_container_width=True, type="primary"):
        base = weather_w6["temp"]
        hi = compute_zone(hi_tree, hi_ac, hi_age, hi_green, base, temp_rise, "high")
        lo = compute_zone(lo_tree, lo_ac, lo_age, lo_green, base, temp_rise, "low")

        temp_gap   = round(lo["eff_temp"]      - hi["eff_temp"],      1)
        vuln_gap   = lo["vulnerability"]  - hi["vulnerability"]
        energy_gap = lo["energy_burden"]  - hi["energy_burden"]
        health_gap = lo["health_risk"]    - hi["health_risk"]
        inequality_index = min(100, round((vuln_gap * 0.4 + energy_gap * 0.3 + health_gap * 0.3) / 2))

        st.markdown("### 📊 Comparison Results")
        r_hi, r_vs, r_lo = st.columns([2, 1.3, 2])

        with r_hi:
            st.markdown("""
            <div style="background:#080f1c;border:1px solid #1a3a6040;border-radius:12px;padding:18px;margin-bottom:8px;">
                <div style="font-size:10px;color:#3a5070;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;font-family:'Space Mono',monospace;">HIGH-INCOME ZONE</div>
            </div>""", unsafe_allow_html=True)
            st.metric("Effective Temperature", f"{hi['eff_temp']}°C")
            st.metric("Vulnerability Score",   f"{hi['vulnerability']}%")
            st.metric("Energy Burden",         f"{hi['energy_burden']}/100")
            st.metric("Health Risk",           f"{hi['health_risk']}%")

        with r_vs:
            ineq_color = "#ff2d55" if inequality_index > 50 else "#ffd60a"
            st.markdown(f"""
            <div class="vs-box">
                <div style="font-size:10px;color:#2a3a50;letter-spacing:1.5px;margin-bottom:8px;font-family:'Space Mono',monospace;">HEAT GAP</div>
                <div class="gap-num">+{temp_gap}°C</div>
                <div style="font-size:10px;color:#2a3a50;margin-bottom:12px;">temp diff</div>
                <div class="gap-num">+{vuln_gap}</div>
                <div style="font-size:10px;color:#2a3a50;margin-bottom:12px;">vulnerability pts</div>
                <div class="gap-num">+{energy_gap}</div>
                <div style="font-size:10px;color:#2a3a50;margin-bottom:16px;">energy burden pts</div>
                <div style="font-size:10px;color:#2a3a50;letter-spacing:1px;font-family:'Space Mono',monospace;">INEQUALITY INDEX</div>
                <div class="inequality-score" style="color:{ineq_color}">{inequality_index}</div>
                <div style="font-size:12px;color:#2a3a50;">/ 100</div>
            </div>
            """, unsafe_allow_html=True)

        with r_lo:
            st.markdown("""
            <div style="background:#080f1c;border:1px solid #5a1a2040;border-radius:12px;padding:18px;margin-bottom:8px;">
                <div style="font-size:10px;color:#5a3040;letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;font-family:'Space Mono',monospace;">LOW-INCOME ZONE</div>
            </div>""", unsafe_allow_html=True)
            st.metric("Effective Temperature", f"{lo['eff_temp']}°C",      delta=f"+{temp_gap}°C hotter",  delta_color="inverse")
            st.metric("Vulnerability Score",   f"{lo['vulnerability']}%",  delta=f"+{vuln_gap} pts",       delta_color="inverse")
            st.metric("Energy Burden",         f"{lo['energy_burden']}/100", delta=f"+{energy_gap} pts",   delta_color="inverse")
            st.metric("Health Risk",           f"{lo['health_risk']}%",    delta=f"+{health_gap} pts",     delta_color="inverse")

        st.markdown(f"""
        <div class="narrative-box">
            <strong style="color:#ff8c35">Low-income residents</strong> in {selected_city} experience
            <strong style="color:#ff4466">{temp_gap}°C higher</strong> effective temperatures, with {vuln_gap} points greater
            vulnerability and {energy_gap} points more energy burden — despite having only {lo_ac}% AC access vs
            {hi_ac}% in wealthier zones. At <strong>+{temp_rise}°C</strong> projected warming, this divide becomes
            a public health crisis. The <strong>Inequality Index of {inequality_index}/100</strong> signals
            {'🔴 <strong style="color:#ff4466">severe</strong>' if inequality_index > 60
             else '🟠 <strong style="color:#ff8c35">significant</strong>' if inequality_index > 40
             else '🟡 <strong style="color:#ffd60a">moderate</strong>'} thermal injustice.
        </div>
        """, unsafe_allow_html=True)

        # Comparison radar chart
        st.markdown("---")
        fig_comp = go.Figure()
        categories = ["Eff. Temp", "Vulnerability", "Energy Burden", "Health Risk"]
        hi_vals = [hi["eff_temp"] - 20, hi["vulnerability"], hi["energy_burden"], hi["health_risk"]]
        lo_vals = [lo["eff_temp"] - 20, lo["vulnerability"], lo["energy_burden"], lo["health_risk"]]

        fig_comp.add_trace(go.Scatterpolar(
            r=hi_vals + [hi_vals[0]], theta=categories + [categories[0]],
            fill="toself", fillcolor="rgba(74,158,255,0.15)",
            line=dict(color="#4a9eff", width=2), name="High-Income Zone"
        ))
        fig_comp.add_trace(go.Scatterpolar(
            r=lo_vals + [lo_vals[0]], theta=categories + [categories[0]],
            fill="toself", fillcolor="rgba(255,68,102,0.15)",
            line=dict(color="#ff4466", width=2), name="Low-Income Zone"
        ))
        fig_comp.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, color="#3a5070"),
                       angularaxis=dict(tickfont=dict(size=10, color="#4a6080"))),
            paper_bgcolor="rgba(0,0,0,0)", font_color="#dde4f0",
            legend=dict(orientation="h", y=-0.1, font=dict(size=11)),
            height=300, margin=dict(l=40, r=40, t=30, b=40),
            title=dict(text="ZONE COMPARISON RADAR", font=dict(size=10, color="#3a5070", family="Space Mono"), x=0),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        # Temperature bar comparison
        bar_comp = go.Figure(go.Bar(
            x=["High-Income Zone", "Low-Income Zone"],
            y=[hi["eff_temp"], lo["eff_temp"]],
            marker_color=["#4a9eff", "#ff4466"],
            text=[f"{hi['eff_temp']}°C", f"{lo['eff_temp']}°C"],
            textposition="outside",
            width=0.4,
        ))
        bar_comp.add_hline(y=base, line_dash="dot", line_color="#ffd700",
                           annotation_text=f"Baseline {base}°C")
        plotly_dark_theme(bar_comp, "EFFECTIVE TEMPERATURE COMPARISON", 260)
        st.plotly_chart(bar_comp, use_container_width=True)

        st.markdown("---")
        if api_key:
            if st.button("🤖 Generate AI Policy Recommendations", key="ai6"):
                prompt = f"""You are an urban climate equity expert. In {selected_city} with +{temp_rise}°C projected warming:

High-income zone: {hi_tree}% trees, {hi_ac}% AC access → effective temp {hi['eff_temp']}°C, vulnerability {hi['vulnerability']}%
Low-income zone:  {lo_tree}% trees, {lo_ac}% AC access → effective temp {lo['eff_temp']}°C, vulnerability {lo['vulnerability']}%
Thermal Inequality Index: {inequality_index}/100

In exactly 3 bullet points (max 30 words each), suggest specific, actionable policy interventions to close this thermal equity gap. Be concrete, India-specific, and mention government schemes where applicable."""
                with st.spinner("Generating policy recommendations..."):
                    insight = call_claude(prompt, api_key)
                st.markdown(f"""
                <div class="ai-box">
                    <div class="ai-title">⚖️ AI Climate Justice Advisor — Policy Brief for {selected_city}</div>
                    <div style="color:#8a9ab8; font-size:14px; line-height:1.9;">{insight.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Add your Claude API key in the sidebar to get AI-powered policy recommendations.")

# ─── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#1a2a40; font-size:11px; font-family:'Space Mono',monospace; letter-spacing:1px;">
    U.R.I.E — URBAN RESILIENCE INTELLIGENCE ENGINE &nbsp;·&nbsp;
    LIVE WEATHER VIA OPEN-METEO &nbsp;·&nbsp; AI VIA CLAUDE
</div>
""", unsafe_allow_html=True)