import streamlit as st
import pandas as pd
import geopandas as gpd
import contextily as ctx
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


# Print merged data columns
print(merged_data.columns)

# County selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

# Print selected county name
print(selected_county)

# Filter data based on county selection
county_data = merged_data[merged_data['NAME'] == selected_county]

# Display bar chart for the selected county
st.bar_chart(county_data[columns_to_visualize])

# Display map with the merged data and basemap
with st.expander("Show Map"):
    # Convert DataFrame to GeoDataFrame
    county_data_gdf = gpd.GeoDataFrame(county_data, geometry='geometry')

    # Set up basemap
    basemap = ctx.providers.Stamen.TerrainBackground

    # Plot GeoDataFrame with basemap using contextily
    ax = county_data_gdf.plot(figsize=(12, 12), alpha=0.7, cmap='coolwarm', legend=True)
    ctx.add_basemap(ax, crs=county_data_gdf.crs, source=basemap)

    # Show legend
    st.pyplot()

# You can add more interactivity and visualization options as needed
