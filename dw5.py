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
    counties = json.load(response)

# Filter GeoJSON data to only include Michigan counties
michigan_counties_geojson = {
    "type": "FeatureCollection",
    "features": [county for county in counties["features"] if county["id"][:2] == "26"]  # "26" is the FIPS code for Michigan
}

# API key
c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")

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

mi_df = pd.DataFrame(mi_census)

# Plotly Express choropleth map
fig = px.choropleth(mi_df, 
                    scope='usa',
                    geojson=michigan_counties_geojson, 
                    locations='NAME',
                    color='B08301_001E',  # Change this to the commuting data variable you want to visualize
                    color_continuous_scale='Viridis',
                    labels={'B08301_001E': 'Commuting Data'},
                    title='Michigan Counties Commuting Data',
                    projection='mercator')
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Display the map using Streamlit
st.plotly_chart(fig)
