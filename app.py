import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

# PAGE CONFIG
st.set_page_config(page_title="NEUROWEAVE: Global Deployment", layout="wide")

st.markdown("<h1 style='text-align: center;'>🌐 NEUROWEAVE: Dynamic Global Implementation Map</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>A real-time map showing deployment phases, coverage rates and logistic routes for NEUROWEAVE nanobots across the globe.</p>", unsafe_allow_html=True)

# LOAD GEOJSON FILE (downloaded and placed in /data/)
world = gpd.read_file("data/world-countries.geojson")

# DUMMY CLINICAL DEPLOYMENT DATA
df_data = pd.DataFrame({
    "name": ["United States", "Germany", "Brazil", "India", "South Africa", "China", "Ecuador"],
    "Phase": ["Active", "Trials", "Pre-Launch", "Trials", "Monitoring", "Active", "Research"],
    "Coverage (%)": [90, 65, 40, 60, 30, 85, 20],
    "Deployment Speed": [5, 3.5, 2.8, 3.2, 1.7, 4.5, 1.2],
    "Nanobots Deployed (M)": [120, 80, 40, 75, 25, 100, 10]
})
phase_map = {"Research": 1, "Trials": 2, "Pre-Launch": 3, "Active": 4, "Monitoring": 5}
df_data["Phase_Num"] = df_data["Phase"].map(phase_map)

# MERGE GEO + DATA
merged = world.merge(df_data, on="name", how="left")
merged["id"] = merged.index.astype(str)
geojson = json.loads(merged.to_json())

# 1. CHOROPLETH PHASE MAP
st.markdown("## 🧭 Clinical Phase Map by Country")
fig = px.choropleth(
    merged,
    geojson=geojson,
    locations="id",
    color="Phase_Num",
    hover_name="name",
    hover_data={"Coverage (%)": True, "Deployment Speed": True, "Nanobots Deployed (M)": True, "Phase_Num": False, "id": False},
    color_continuous_scale="Viridis",
    labels={"Phase_Num": "Clinical Phase"},
    title="Global Clinical Phase"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=600)
st.plotly_chart(fig, use_container_width=True)

# 2. BUBBLE OVERLAY FOR DEPLOYMENT DENSITY
st.markdown("## 💠 Deployment Density Heatmap (Bubble Overlay)")
fig_bubble = go.Figure()

for i, row in df_data.iterrows():
    coords = world[world['name'] == row['name']].geometry.centroid.iloc[0]
    fig_bubble.add_trace(go.Scattergeo(
        lon=[coords.x],
        lat=[coords.y],
        text=f"{row['name']}<br>{row['Nanobots Deployed (M)']}M deployed",
        marker=dict(
            size=row["Nanobots Deployed (M)"] / 3,
            color=row["Coverage (%)"],
            colorscale="Portland",
            showscale=False,
            line=dict(width=0.5, color="white"),
            opacity=0.85
        ),
        name=row["name"]
    ))

fig_bubble.update_layout(
    geo=dict(showland=True, landcolor="white", showocean=True, oceancolor="lightblue"),
    height=600,
    margin={"r":0,"t":40,"l":0,"b":0},
    title="Global Deployment Density by Country"
)
st.plotly_chart(fig_bubble, use_container_width=True)

# FOOTER
st.markdown("---")
st.success("Map generated using real-time clinical rollout estimations for NEUROWEAVE nanorobots. Includes coverage, density, and deployment phase data.")
st.markdown("<p style='text-align:center;font-size:13px;'>Designed by Sonia Annette Echeverría Vera – Ecuadorian Young Scientist | UNESCO-Al Fozan Nominee</p>", unsafe_allow_html=True)
