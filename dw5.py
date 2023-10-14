import streamlit as st
import pandas as pd
import geopandas as gpd
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
#DF 
mi_df = pd.DataFrame(mi_census)

mi_df.head()
# BOX 1
selected_county = st.selectbox('Select County', mi_df['NAME'])

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
st.write(f"### Commuting Data for {selected_county}")
st.write(f"Total Commuters: {county_data['B08301_001E'].values[0]}")
for variable, name in variable_names.items():
    st.write(f"{name}: {county_data[variable].values[0]}")

# BAR CHART
st.bar_chart(clean_data[['Driving Alone',
                         'Carpooling',
                         'Public Transportation',
                         'Walking', 'Cycling', 
                         'Other Means',
                         'Worked from Home']])

#                   -  PLOTLY  -
# CENSUS SHAPEFILE
shapefile_path = "https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/26_MICHIGAN/26/tl_rd22_26_cousub.zip"
gdf = gpd.read_file(shapefile_path)

# MERGE
merged_df = gdf.merge(mi_df, how='left', left_on='COUNTYFP', right_on='county')

st.markdown("Below is an interactive map of a commuting type, and the counties that effects. These are estimates, and are meant to be intepreted as such: more rural counties are subject to higher error.")
# SELECT BOX 2
selected_variable = st.selectbox('Select Variable', ['B08301_002E',
                                                     'B08301_003E',
                                                     'B08301_008E', 
                                                     'B08301_011E',
                                                     'B08301_012E', 
                                                     'B08301_013E', 
                                                     'B08301_014E'])

# CHLOROPLETH PX MAP 
fig = px.choropleth(merged_df, 
                    geojson=merged_df.geometry, 
                    locations=merged_df.index, 
                    color=selected_variable,  # Variable selected by the user
                    hover_name=selected_variable,
                    color_continuous_scale='Viridis',
                    range_color=(0, merged_df[selected_variable].max()))  # Adjust the color scale based on the selected variable

st.plotly_chart(fig)







