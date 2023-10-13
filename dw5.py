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


#contextily
ctx.add_basemap(st.pydeck_chart(), crs="EPSG:3857")

#pydeck
deck_map = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude= 42.2,
        longitude=84.4,
        zoom=6,
    ),
    layers=[
        # Add your data layers here if needed
    ],
)

# Add basemap (ctx)
bmp = ctx.providers.CartoDB.PositronNoLabels  # You can choose a different basemap if you prefer
deck_map = deck_map.to_pydeck()
deck_map = deck_map.add_basemap(bmp)

# Display the map using Streamlit
st.pydeck_chart(deck_map)
# Replace YOUR_LATITUDE, YOUR_LONGITUDE, and YOUR_ZOOM_LEVEL with the appropriate values for your map's initial view state. Also, modify the layers parameter in the Deck() function to add any data layers you want to display on the map.



#county selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

#Filter based on county
county_data = mi_df[mi_df['NAME'] == selected_county]

#bar chart for the selected county
st.bar_chart(county_data[['B08301_002E', 'B08301_003E', 'B08301_008E', 'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E']])

#map with the merged dfs
st.map(merged_data)

