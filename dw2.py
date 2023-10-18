import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from census import Census
from us import states

# TITLE
st.title('Michigan Commuting Data')

# KEY
c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")

# Fetch census data
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

# Create DataFrame
mi_df = pd.DataFrame(mi_census)

# Sidebar - Select County and Variable
selected_county = st.sidebar.selectbox('Select County', mi_df['NAME'])
selected_variable = st.sidebar.selectbox('Select Variable', ['B08301_002E',
                                                     'B08301_003E',
                                                     'B08301_008E', 
                                                     'B08301_011E',
                                                     'B08301_012E', 
                                                     'B08301_013E', 
                                                     'B08301_014E'])

# Filter data based on selected county
county_data = mi_df[mi_df['NAME'] == selected_county]

# Mapping variable codes to clean names
variable_names = {
    'B08301_002E': 'Driving Alone',
    'B08301_003E': 'Carpooling',
    'B08301_008E': 'Public Transportation',
    'B08301_011E': 'Walking',
    'B08301_012E': 'Cycling',
    'B08301_013E': 'Other Means',
    'B08301_014E': 'Worked from Home'
}

# Create clean_data DataFrame
clean_data = county_data.rename(columns=variable_names)

# Display selected county data with clean variable names
st.sidebar.write(f"### Commuting Data for {selected_county}")
for variable, name in variable_names.items():
    st.sidebar.write(f"{name}: {county_data[variable].values[0]}")

# Pydeck chart
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=44.89,
        longitude=-84.76,
        zoom=6,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "GeoJsonLayer",
            data=clean_data,
            get_fill_color=f"[255, 255, 255, {selected_variable} * 0.1]",
            pickable=True,
        )
    ]
))
