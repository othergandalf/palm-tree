import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import plotly.express as px
from census import Census
from us import states
def show():
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

st.header('Select a :blue[county]')

st.markdown("The left side bar selects a Michigan county. See the mix of commuting types for that county.")
st.subheader("Not familiar with Michigan?") 
st.markdown("Try :blue[Wayne] (Detroit), :blue[Ingham] (Lansing), or :blue[Grand Traverse] (Traverse City) counties.")

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

