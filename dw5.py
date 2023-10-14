import streamlit as st
import pandas as pd
import json
from census import Census
from us import states
from urllib.request import urlopen
import plotly.express as px

st.title('Michigan Commuting Data')

# Load GeoJSON data containing Michigan counties
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties_geojson = json.load(response)

# Filter GeoJSON data to only include Michigan counties
michigan_counties_geojson = {
    "type": "FeatureCollection",
    "features": [county for county in counties_geojson["features"] if county["id"][:2] == "26"]  # "26" is the FIPS code for Michigan
}

# API key
c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")

# Retrieve Census data
mi_census = c.acs5.state_county(fields=('NAME',
                                        'B08301_001E',
                                        'B08301_002E',
                                        'B08301_003E',
                                        'B08301_008E',
                                        'B08301_011E',
                                        'B08301_012E',
                                        'B08301_013E',
                                        'B08301_014E'),
                               state_fips=states.MI.fips,
                               county_fips="*",
                               year=2021)

# Create DataFrame from Census data
mi_df = pd.DataFrame(mi_census)

# Create DataFrame from GeoJSON data
geojson_df = pd.json_normalize(counties_geojson['features'])
geojson_df['id'] = geojson_df['id'].astype(str)  # Convert id to string for consistency

# Merge Census data and GeoJSON data on the 'id' column
merged_data = pd.merge(geojson_df, mi_df, left_on='GEO_ID', right_on='GEOID')

# Plotly Express choropleth map
fig = px.choropleth(merged_data, 
                    geojson=michigan_counties_geojson,
                    locations='id',  # 'id' is the common column between GeoJSON and Census data
                    color='B08301_001E',  # Change this to the commuting data variable you want to visualize
                    color_continuous_scale='Viridis',
                    labels={'B08301_001E': 'Commuting Data'},
                    title='Michigan Counties Commuting Data',
                    projection='mercator')

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the map using Streamlit
st.plotly_chart(fig)
