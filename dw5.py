import streamlit as st
import pandas as pd
import geopandas as gpd
import contextily as ctx
import pydeck as pdk
from census import Census
from us import states

st.title('Michigan Commuting Data')

#import .shp file
michigan_counties_url = "https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/26_MICHIGAN/26/tl_rd22_26_cousub.zip"
# Load the Shapefile directly from the .zip file
michigan_counties = gpd.read_file(michigan_counties_url)

#api key
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

#merge dfs
merged_data = michigan_counties.merge(mi_df, how='left', left_on='COUNTYFP', right_on='county')

# Polygonal Layer
layer_b08301_001E = pdk.Layer(
    "PolygonLayer",
    data=merged_data,
    get_polygon="geometry",
    get_fill_color="[B08301_001E, 0, B08301_001E, 150]",
    pickable=True,
    extruded=True,
    auto_highlight=True,
    get_elevation="B08301_001E * 10",  # You can adjust the multiplier for elevation
    elevation_scale=0.1,
)

# Deck.GL map
view_state = pdk.ViewState(
    latitude=42.2459,
    longitude=-84.4013,
    zoom=YOUR_ZOOM_LEVEL,  # Adjust this according to your visualization needs
    bearing=0,
    pitch=0,
)

r = pdk.Deck(
    layers=[layer_b08301_001E],
    initial_view_state=view_state,
)

# Render the map
st.pydeck_chart(r)

# ... Create similar layers for other census variables ...


#county selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

#Filter based on county
county_data = mi_df[mi_df['NAME'] == selected_county]

#bar chart for the selected county
st.bar_chart(county_data[['B08301_002E', 'B08301_003E', 'B08301_008E', 'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E']])

#map with the merged dfs
st.map(merged_data)

