import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
from streamlit_autorefresh import st_autorefresh
@st.cache_data(ttl=60)
def get_air_quality(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    return response.json()

# ---------------- WEATHER FUNCTION ----------------
@st.cache_data(ttl=60)
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="U.R.I.E.", layout="wide")

st.title("🌍 U.R.I.E. – Urban Resilience Intelligence Engine")

# ---------------- SIDEBAR ----------------
module = st.sidebar.radio("Select Window", [
    "1️⃣ Live Heat Dashboard",
    "2️⃣ Behaviour Simulator",
    "3️⃣ Cooling ROI Analyzer",
    "4️⃣ Job Risk Analyzer",
    "5️⃣ Livelihood Pivot Engine",
    "6️⃣ Thermal Equity Lens"
])

# ============================================================
# ==================== WINDOW 1 ==============================
# ============================================================
# ================= WINDOW 1 =================

if module == "1️⃣ Live Heat Dashboard":

    st_autorefresh(interval=30000, key="heat_refresh")

    st.header("🔥 Live Urban Heat Dashboard")
    st.caption("Real-Time Climate + Behaviour Intelligence")

    API_KEY = "fbbfdfb1aff4c893505cf9f9e1731d11"
    city = st.text_input("Enter City Name")

    if city:

        data = get_weather_data(city, API_KEY)

        if data.get("cod") != 200:
            st.error(f"API Error: {data.get('message')}")
            st.stop()

        live_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_condition = data["weather"][0]["main"]

        heat_index = live_temp + (humidity * 0.05)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌡 Temp (°C)", live_temp)
        col2.metric("💧 Humidity (%)", humidity)
        col3.metric("💨 Wind Speed (m/s)", wind_speed)
        col4.metric("🌤 Condition", weather_condition)

        st.divider()
        st.subheader("🏙 Urban Behaviour Inputs")

        tree_cover = st.slider("Tree Cover %", 0, 100, 20)
        building_density = st.slider("Building Density %", 0, 100, 70)
        traffic = st.slider("Traffic Level %", 0, 100, 60)
        ac_usage = st.slider("AC Usage %", 0, 100, 75)
        population_density = st.slider("Population Density %", 0, 100, 80)

        calculate = st.button("🚀 Calculate Heat Score")

        if calculate:

            simulation_score = (
                (100 - tree_cover) * 0.25 +
                building_density * 0.2 +
                traffic * 0.2 +
                ac_usage * 0.2 +
                population_density * 0.15
            )

            final_score = (simulation_score * 0.6) + (heat_index * 0.4)

            st.divider()
            st.subheader("🔥 Urban Heat Vulnerability Score")

            st.progress(min(int(final_score), 100))

            if final_score < 40:
                st.success("🟢 Low Heat Risk")
            elif final_score < 70:
                st.warning("🟠 Moderate Heat Risk")
            else:
                st.error("🔴 Extreme Heat Risk")

            st.metric("Final Heat Score", round(final_score, 2))

            energy_stress = (ac_usage * 0.5 + population_density * 0.5)

            st.subheader("⚡ Energy Stress Index")
            st.progress(min(int(energy_stress), 100))
            st.metric("Energy Load Score", round(energy_stress, 2))
            st.subheader("🔥 Heat Intensity Meter")
 

# ============================================================
# ==================== WINDOW 2 ==============================
# ============================================================
elif module == "2️⃣ Behaviour Simulator":

    st.header("🌍 Real-Time Behaviour Impact Engine")
    st.caption("Live Environmental Data + Urban Scenario Projection")

    API_KEY = "fbbfdfb1aff4c893505cf9f9e1731d11"

    city = st.text_input("Enter City for Simulation")

    if city:

        weather = get_weather_data(city, API_KEY)

        if weather.get("cod") != 200:
            st.error("City not found.")
            st.stop()

        live_temp = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        lat = weather["coord"]["lat"]
        lon = weather["coord"]["lon"]

        air = get_air_quality(lat, lon, API_KEY)
        aqi = air["list"][0]["main"]["aqi"]

        st.subheader("🌡 Live Environmental Baseline")

        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature (°C)", live_temp)
        col2.metric("Humidity (%)", humidity)
        col3.metric("Air Quality Index", aqi)

        st.divider()
        st.subheader("🏙 Select Urban Development Scenario")

        scenario = st.selectbox(
            "Choose Scenario",
            [
                "🌆 Rapid Urban Expansion",
                "🌳 Green Smart City",
                "🏭 Industrial Growth Zone",
                "🚦 Traffic Dominated City"
            ]
        )

        # Scenario Mapping
        if scenario == "🌆 Rapid Urban Expansion":
            tree_cover = 20
            ac_usage = 75
            traffic = 70
            construction = 80

        elif scenario == "🌳 Green Smart City":
            tree_cover = 75
            ac_usage = 40
            traffic = 35
            construction = 30

        elif scenario == "🏭 Industrial Growth Zone":
            tree_cover = 25
            ac_usage = 65
            traffic = 60
            construction = 85

        elif scenario == "🚦 Traffic Dominated City":
            tree_cover = 35
            ac_usage = 60
            traffic = 85
            construction = 50

        # ---------------- CALCULATIONS ----------------

        baseline_heat = live_temp + (humidity * 0.05) + (aqi * 2)

        behaviour_impact = (
            (100 - tree_cover) * 0.3 +
            ac_usage * 0.25 +
            traffic * 0.25 +
            construction * 0.2
        )

        final_heat_score = min(max((baseline_heat * 0.5) + (behaviour_impact * 0.5), 0), 100)

        energy_stress = min(max((ac_usage * 0.6 + traffic * 0.4), 0), 100)

        sustainability = min(max(
            tree_cover * 0.6 +
            (100 - construction) * 0.2 +
            (100 - ac_usage) * 0.2,
            0
        ), 100)

        projected_temp_rise = final_heat_score * 0.03

        st.divider()
        st.subheader("📊 Impact Projection")

        c1, c2, c3 = st.columns(3)
        c1.metric("🔥 Projected Heat Score", round(final_heat_score, 2))
        c2.metric("⚡ Energy Stress", round(energy_stress, 2))
        c3.metric("🌱 Sustainability Score", round(sustainability, 2))

        st.metric("🌡 Projected Temperature Rise (°C)", round(projected_temp_rise, 2))

        st.progress(int(final_heat_score))

        # Recommendation Engine
        st.subheader("🧠 Urban Strategy Recommendation")

        if sustainability < 40:
            st.error("Increase green cover and reduce AC dependency immediately.")
        elif sustainability < 70:
            st.warning("Improve sustainable infrastructure and regulate traffic.")
        else:
            st.success("Urban system shows strong sustainability balance.")
            