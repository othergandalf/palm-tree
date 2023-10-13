import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
from census import Census
from us import states

st.title('Michigan Commuting Data')

# Import .shp file
michigan_counties_url = "https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/26_MICHIGAN/26/tl_rd22_26_cousub.zip"
# Load the Shapefile directly from the .zip file
michigan_counties = gpd.read_file(michigan_counties_url)

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

# Merge DataFrames
merged_data = michigan_counties.merge(mi_df, how='left', left_on='COUNTYFP', right_on='county')

# Plotly Express map
fig = px.choropleth(merged_data, 
                    geojson=merged_data.geometry, 
                    locations=merged_data.index, 
                    color='B08301_001E',  # Change this to the commuting data variable you want to visualize
                    color_continuous_scale='Viridis',
                    labels={'B08301_001E': 'Commuting Data'},
                    title='Michigan Counties Commuting Data',
                    projection='mercator')

# Display the map using Streamlit
st.plotly_chart(fig)
