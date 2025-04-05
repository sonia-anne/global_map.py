import streamlit as st
import pydeck as pdk
import pandas as pd

# --- CONFIG PAGE ---
st.set_page_config(page_title="NEUROWEAVE - Global Phase Rollout", layout="wide")
st.markdown("<h1 style='text-align: center;'>🌍 NEUROWEAVE: Global Implementation by Clinical Phase</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Visual analysis of NEUROWEAVE deployment by country, phase, and biotech readiness.</p>", unsafe_allow_html=True)

# --- SAMPLE DATA ---
data = pd.DataFrame({
    "Country": ["USA", "Germany", "Brazil", "India", "South Africa", "China", "Ecuador", "Japan", "Australia", "Canada"],
    "Latitude": [38.9, 52.5, -15.78, 28.6, -33.92, 39.9, -0.18, 35.6, -25.3, 45.4],
    "Longitude": [-77.03, 13.4, -47.9, 77.2, 18.42, 116.4, -78.4, 139.7, 133.8, -75.7],
    "Coverage": [92, 76, 47, 65, 33, 88, 25, 90, 82, 77],
    "Phase": ["Active", "Trials", "Pre-Launch", "Trials", "Monitoring", "Active", "Research", "Active", "Pre-Launch", "Trials"],
    "R&D Score": [95, 91, 74, 83, 62, 94, 68, 96, 85, 89]
})
phase_map = {"Research": 1, "Trials": 2, "Pre-Launch": 3, "Active": 4, "Monitoring": 5}
data["Phase_Num"] = data["Phase"].map(phase_map)

# --- SIDEBAR FILTER ---
selected = st.sidebar.multiselect("Filter by Deployment Phase", options=data["Phase"].unique(), default=data["Phase"].unique())
filtered_data = data[data["Phase"].isin(selected)]

# --- 3D MAP ---
layer = pdk.Layer(
    "ColumnLayer",
    data=filtered_data,
    get_position='[Longitude, Latitude]',
    get_elevation="R&D Score",
    elevation_scale=1000,
    radius=300000,
    get_fill_color='[255 - Coverage, 80 + Phase_Num*20, Coverage]',
    pickable=True,
    auto_highlight=True
)
view_state = pdk.ViewState(latitude=10, longitude=20, zoom=1, pitch=40)
deck = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v9",
                tooltip={"text": "🌎 {Country}\nPhase: {Phase}\nCoverage: {Coverage}%\nR&D: {R&D Score}"})
st.pydeck_chart(deck)

# --- PIE CHART ---
import plotly.express as px
fig_pie = px.pie(data_frame=data, names="Phase", title="🌐 Distribution of Deployment by Phase",
                 color_discrete_sequence=px.colors.sequential.Rainbow)
st.plotly_chart(fig_pie, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.info("Sources: WHO ICTRP, Global Biotech Index, World Bank R&D Data, UNESCO Science Reports.")
st.markdown("<p style='text-align: center;'>Designed by Sonia Annette Echeverría Vera – Young Scientist | UNESCO-Al Fozan Candidate</p>", unsafe_allow_html=True)
