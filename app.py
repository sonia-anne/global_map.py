import streamlit as st
import pydeck as pdk
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="NEUROWEAVE 3D Global Rollout", layout="wide")

st.markdown("<h1 style='text-align: center;'>🌍 NEUROWEAVE: 3D Global Deployment Map</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>A 3D interactive view of the clinical rollout of NEUROWEAVE across countries, visualized by coverage and deployment phase.</p>", unsafe_allow_html=True)

# --- DATA ---
data = pd.DataFrame({
    "Country": ["United States", "Germany", "Brazil", "India", "South Africa", "China", "Ecuador"],
    "Latitude": [38.9072, 52.5200, -15.7801, 28.6139, -33.9249, 39.9042, -0.1807],
    "Longitude": [-77.0369, 13.4050, -47.9292, 77.2090, 18.4241, 116.4074, -78.4678],
    "Coverage": [90, 65, 40, 60, 30, 85, 20],
    "Deployment_Phase": ["Active", "Trials", "Pre-Launch", "Trials", "Monitoring", "Active", "Research"]
})

# --- FILTER ---
selected_phase = st.sidebar.multiselect(
    "Filter by Deployment Phase",
    options=data["Deployment_Phase"].unique(),
    default=data["Deployment_Phase"].unique()
)
filtered_data = data[data["Deployment_Phase"].isin(selected_phase)]

# --- 3D LAYER ---
layer = pdk.Layer(
    "ScatterplotLayer",
    filtered_data,
    pickable=True,
    opacity=0.9,
    stroked=True,
    filled=True,
    radius_scale=40000,
    radius_min_pixels=6,
    radius_max_pixels=120,
    line_width_min_pixels=1,
    get_position='[Longitude, Latitude]',
    get_radius="Coverage",
    get_fill_color="[255 - Coverage, 120, Coverage]",
    get_line_color=[20, 20, 20],
)

# --- INITIAL VIEW ---
view_state = pdk.ViewState(
    latitude=10,
    longitude=0,
    zoom=1.2,
    pitch=45,
)

# --- FINAL OUTPUT ---
st.subheader("📌 Interactive 3D Deployment Visualization")
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "🧬 {Country}\nCoverage: {Coverage}%\nPhase: {Deployment_Phase}"},
    map_style="mapbox://styles/mapbox/light-v9"
)

st.pydeck_chart(deck)

# --- FOOTER ---
st.markdown("---")
st.success("The visualization shows current NEUROWEAVE deployment status by country, based on clinical implementation data.")
st.markdown("<p style='text-align: center;'>Designed by Sonia Annette Echeverría Vera – Candidate to UNESCO-Al Fozan Prize</p>", unsafe_allow_html=True)
