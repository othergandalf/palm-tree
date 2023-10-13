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

# Convert the 'geometry' column to a projected CRS (UTM Zone 16N)
merged_data = merged_data.to_crs(epsg=32616)

# Check if the 'NAME' column is present in merged_data
if 'NAME' in merged_data.columns:
    county_selector = st.selectbox('Select County', ['All Counties'] + list(merged_data['NAME']))
else:
    county_selector = 'All Counties'

# Filter data based on county selection
if county_selector == 'All Counties':
    filtered_data = merged_data
else:
    filtered_data = merged_data[merged_data['NAME'] == county_selector]

# Variable selection
selected_variable = st.selectbox('Select Variable', ['B08301_001E', 'B08301_002E', 'B08301_003E', 'B08301_008E', 'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E'])

# Plotly Choropleth Map
fig = px.choropleth(filtered_data, 
                    geojson=filtered_data.geometry, 
                    locations=filtered_data.index, 
                    color=selected_variable,
                    color_continuous_scale="Viridis",
                    labels={selected_variable: 'Variable'},
                    title=f'Choropleth Map of {selected_variable}',
                    projection='mercator',
                    hover_name='NAME_x')  # Use 'NAME_x' as the hover column

# Display the map using Streamlit
st.plotly_chart(fig, use_container_width=True)
In this modified version, the hover_name parameter is set to 'NAME_x' to match the column name in the filtered_data DataFrame. Please ensure that 'NAME_x' contains the correct county names for the hover functionality to work as intended.





