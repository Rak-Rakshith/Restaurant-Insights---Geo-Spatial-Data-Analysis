import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap

st.set_page_config(page_title="Restaurant Analysis", layout="wide")

st.title("🍽️ Restaurant Data Analysis")

# Load Data
df = pd.read_csv("cleaned_restaurant_data.csv")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

# Rating Filter
min_rating = float(df["Aggregate_rating"].min())
max_rating = float(df["Aggregate_rating"].max())

rating_filter = st.sidebar.slider(
    "Select Rating",
    min_rating,
    max_rating,
    (min_rating, max_rating)
)

# Location Filter
st.sidebar.subheader("📍 Location Filter")

cities = df["City"].dropna().unique()

selected_city = st.sidebar.selectbox(
    "Select City",
    sorted(cities)
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["Aggregate_rating"] >= rating_filter[0]) &
    (df["Aggregate_rating"] <= rating_filter[1]) &
    (df["City"] == selected_city)
]

# Handle empty case
if filtered_df.empty:
    st.warning("No restaurants found for selected filters")
    st.stop()

# ---------------- DISPLAY DATA ----------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# ---------------- TOP RESTAURANTS ----------------
st.subheader(f"⭐ Top Restaurants in {selected_city}")

top_restaurants = filtered_df.sort_values(
    by="Aggregate_rating", ascending=False
).head(10)

st.dataframe(top_restaurants)

# ---------------- MAP ----------------
st.subheader(f"📍 Restaurant Locations in {selected_city}")

map_center = [
    filtered_df["Latitude"].mean(),
    filtered_df["Longitude"].mean()
]

m = folium.Map(location=map_center, zoom_start=12)

for _, row in filtered_df.iterrows():
    color = "green" if row["Aggregate_rating"] >= 4 else "orange" if row["Aggregate_rating"] >= 3 else "red"
    
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{row['Restaurant_Name']} | Rating: {row['Aggregate_rating']}"
    ).add_to(m)

st_folium(m, width=900, height=500)

# ---------------- HEATMAP ----------------
st.subheader("🔥 Restaurant Density Heatmap")

heat_data = filtered_df[["Latitude", "Longitude"]].values.tolist()

heat_map = folium.Map(location=map_center, zoom_start=12)
HeatMap(heat_data).add_to(heat_map)

st_folium(heat_map, width=900, height=500)