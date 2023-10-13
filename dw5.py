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

merged_data = merged_data.to_crs(epsg=32616) 

# Extract lat and long geometryco lumn after re-projection
 merged_data['LAT'] = merged_data['geometry'].centroid.y
 merged_data['LON'] = merged_data['geometry'].centroid.x

#county selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

#Filter based on county
county_data = mi_df[mi_df['NAME'] == selected_county]

#bar chart for the selected county
st.bar_chart(county_data[['B08301_002E', 'B08301_003E', 'B08301_008E', 'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E']])

# Display the map using Streamlit
st.map(merged_data, use_container_width=True)

