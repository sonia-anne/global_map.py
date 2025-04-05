import streamlit as st
import geopandas as gpd
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx

# --- PAGE CONFIG ---
st.set_page_config(page_title="NEUROWEAVE: Global Implementation", layout="wide")

st.markdown("<h1 style='text-align: center;'>🌍 NEUROWEAVE: Global Rollout & Clinical Phases</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Mapping the deployment phases, coverage rates and logistical routes of NEUROWEAVE across continents.</p>", unsafe_allow_html=True)

# --- DATA ---
world = gpd.read_file("data/world-countries.geojson")
df_data = pd.DataFrame({
    "name": ["United States", "Germany", "Brazil", "India", "South Africa", "China", "Ecuador"],
    "Phase": ["Active", "Trials", "Pre-Launch", "Trials", "Monitoring", "Active", "Research"],
    "Coverage (%)": [90, 65, 40, 60, 30, 85, 20]
})
phase_map = {"Research": 1, "Trials": 2, "Pre-Launch": 3, "Active": 4, "Monitoring": 5}
df_data["Phase_Num"] = df_data["Phase"].map(phase_map)

# --- MERGE WITH WORLD MAP ---
merged = world.merge(df_data, on="name", how="left")
merged["id"] = merged.index.astype(str)
geojson = json.loads(merged.to_json())

# --- CHOROPLETH MAP ---
choropleth_fig = px.choropleth(
    merged,
    geojson=geojson,
    locations="id",
    color="Phase_Num",
    hover_name="name",
    hover_data={"Phase": True, "Coverage (%)": True, "id": False},
    color_continuous_scale="Plasma",
    labels={"Phase_Num": "Phase"},
    title="Global Clinical Phase by Country"
)
choropleth_fig.update_geos(fitbounds="locations", visible=False)
choropleth_fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(choropleth_fig, use_container_width=True)

# --- LOGISTICS ROUTES (NETWORKX + PLOTLY) ---
st.markdown("## 🧭 NEUROWEAVE Logistics & Distribution Network")

city_coords = {
    "Ecuador": (-78.4678, -0.1807),
    "United States": (-77.0369, 38.9072),
    "Germany": (13.4050, 52.5200),
    "China": (116.4074, 39.9042),
    "India": (77.2090, 28.6139),
    "Brazil": (-47.9292, -15.7801),
    "South Africa": (18.4241, -33.9249)
}
G = nx.Graph()
for country, (lon, lat) in city_coords.items():
    G.add_node(country, pos=(lon, lat))

edges = [("Ecuador", "United States"), ("United States", "Germany"), ("Germany", "India"),
         ("India", "China"), ("China", "South Africa"), ("South Africa", "Brazil")]
G.add_edges_from(edges)
pos = nx.get_node_attributes(G, 'pos')

edge_x, edge_y = [], []
for u, v in G.edges():
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x.append([x0, x1, None])
    edge_y.append([y0, y1, None])

route_fig = go.Figure()
for i in range(len(edge_x)):
    route_fig.add_trace(go.Scattergeo(
        lon=edge_x[i],
        lat=edge_y[i],
        mode='lines',
        line=dict(width=2, color='blue'),
        showlegend=False
    ))
for country in G.nodes():
    x, y = pos[country]
    route_fig.add_trace(go.Scattergeo(
        lon=[x],
        lat=[y],
        mode='markers+text',
        text=country,
        textposition="top center",
        marker=dict(size=10, color='red'),
        name=country
    ))
route_fig.update_layout(
    title="Global NEUROWEAVE Distribution Network",
    geo=dict(showland=True),
    height=600
)
st.plotly_chart(route_fig, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.success("This dashboard shows NEUROWEAVE's phased clinical deployment, real-time geographic distribution, and its international logistical backbone.")
