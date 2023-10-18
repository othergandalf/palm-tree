import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import plotly.express as px
from census import Census
from us import states
# TITLE
st.title('Michigan Commuting Data')
# KEY
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
# B01003_001E: total population
# B19101_001E: median income
# B17001_002E: poverty count 
# poverty_rate = (poverty_count / total_population) * 100
#will come to back to these variables once the mapping issue has been solved.

#DF 
mi_df = pd.DataFrame(mi_census)

mi_df.head()
# BOX 1
selected_county = st.sidebar.selectbox('Select County', mi_df['NAME'])

st.markdown("Select a MI county to see the mix of commuting types for that county.")

# SELECT BOX 1
county_data = mi_df[mi_df['NAME'] == selected_county]

# NEW CLEAN NAMES
variable_names = {
    'B08301_002E': 'Driving Alone',
    'B08301_003E': 'Carpooling',
    'B08301_008E': 'Public Transportation',
    'B08301_011E': 'Walking',
    'B08301_012E': 'Cycling',
    'B08301_013E': 'Other Means',
    'B08301_014E': 'Worked from Home'
}

# NEW DF
clean_data = county_data.rename(columns=variable_names)

# TEXT DISPLAY BOXES OF COUNTY SELECTED
st.sidebar.write(f"### Commuting Data for {selected_county}")
st.sidebar.write(f"Total Commuters: {county_data['B08301_001E'].values[0]}")
for variable, name in variable_names.items():
    st.sidebar.write(f"{name}: {county_data[variable].values[0]}")

# BAR CHART
st.bar_chart(clean_data[['Driving Alone',
                         'Carpooling',
                         'Public Transportation',
                         'Walking', 'Cycling', 
                         'Other Means',
                         'Worked from Home']])

#                   -  PLOTLY  -
# SHAPEFILE
# GEOJSON:https://github.com/othergandalf/palm-tree/blob/main/Counties_(v17a).geojson
# TIGER: https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/26_MICHIGAN/26/tl_rd22_26_cousub.zip
shapefile_path = "https://raw.githubusercontent.com/othergandalf/palm-tree/main/Counties_(v17a).geojson"

gdf = gpd.read_file(shapefile_path)

# MERGE
merged_df = gdf.merge(clean_data, how='left', left_on='FIPSCODE', right_on='county')

}

st.markdown("Below is an interactive map of a commuting type, and the counties that effects. These are estimates, and are meant to be intepreted as such: more rural counties are subject to higher error.")
# SELECT BOX 2
selected_variable = st.sidebar.selectbox('Select Variable', ['B08301_002E',
                                                     'B08301_003E',
                                                     'B08301_008E', 
                                                     'B08301_011E',
                                                     'B08301_012E', 
                                                     'B08301_013E', 
                                                     'B08301_014E'])
# 43.5978° N, 84.7675° W
# PYDECK MAP 
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=44.89,
        longitude=-84.76,
        zoom=5,
        pitch=0,
    ),  layers = [
      pdk.Layer(
            "GeoJsonLayer",
            data=merged_df,
            get_fill_color=f"[224, 255, 255, {selected_variable} * 0.1]",
            pickable=True
    ) ]  ) )
