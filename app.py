import streamlit as st
import os
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta
import pycountry
from dotenv import load_dotenv

load_dotenv()  # take environment variables

# Streamlit app title
st.title("🌍 Top Tracks by Country (Last.fm)")

# Last.fm API setup
API_KEY = os.getenv("LASTFM_API_KEY")
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

# In-memory cache with 24-hour expiry


@st.cache_data(ttl=86400)  # Cache for 24 hours (86400 seconds)
def get_top_tracks(country, limit=5):
    params = {
        "method": "geo.gettoptracks",
        "country": country,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        tracks = data.get("tracks", {}).get("track", [])
        return pd.DataFrame([
            {"Track": track["name"], "Artist": track["artist"]
                ["name"], "Listeners": int(track["listeners"])}
            for track in tracks
        ])
    except (requests.RequestException, KeyError):
        return pd.DataFrame()


# Get list of all ISO 3166-1 country names
countries = [country.name for country in pycountry.countries]

# Fetch data for all countries and cache


@st.cache_data(ttl=86400)
def get_all_countries_data():
    country_data = {}
    for country in countries:
        tracks_df = get_top_tracks(country)
        if not tracks_df.empty:
            country_data[country] = tracks_df
    return country_data


# Load cached data
all_tracks = get_all_countries_data()

# Prepare data for globe
globe_data = []
for country in countries:
    tracks_df = all_tracks.get(country, pd.DataFrame())
    if not tracks_df.empty:
        # Create tooltip text with top 5 tracks
        tooltip = "<br>".join([f"{row['Track']} by {row['Artist']} ({row['Listeners']:,} listeners)"
                              for _, row in tracks_df.iterrows()])
        globe_data.append({
            "Country": country,
            # Total listeners for top tracks
            "Listeners": tracks_df["Listeners"].sum(),
            "Tooltip": tooltip
        })

globe_df = pd.DataFrame(globe_data)

# Streamlit country selector
selected_country = st.selectbox("Select a Country", ["All"] + countries)

# Display tracks for selected country
if selected_country != "All" and selected_country in all_tracks:
    tracks_df = all_tracks[selected_country]
    if not tracks_df.empty:
        st.write(f"Top 5 Tracks in {selected_country} (Last Week)")
        st.dataframe(tracks_df)
else:
    st.write(
        "Select a country to see its top tracks, or hover on the globe for tooltips!")

# Create a larger Plotly globe with flashy colors
fig = px.choropleth(
    globe_df,
    locations="Country",
    locationmode="country names",
    color="Listeners",
    hover_name="Country",
    # Show tooltip, hide listeners
    hover_data={"Tooltip": True, "Listeners": False},
    projection="orthographic",  # 3D globe
    color_continuous_scale=px.colors.sequential.Plasma,  # Flashy color scheme
    title="Top Tracks by Country (Hover for Details)",
    height=800  # Larger globe
)
fig.update_layout(
    # Minimize margins for bigger globe
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    coloraxis_colorbar_title="Total Listeners",
    geo=dict(
        showland=True,
        landcolor="rgb(50, 50, 50)",  # Dark land for contrast
        showocean=True,
        oceancolor="rgb(0, 100, 200)",  # Vibrant ocean
    )
)
fig.update_traces(
    # Custom tooltip
    hovertemplate="%{hovertext}<br>%{customdata[0]}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)
