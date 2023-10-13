import streamlit as st
import pandas as pd
from census import Census
from us import states

st.title('Michigan Commuting Data')

#background color 
custom_css = f"""
    <style>
        body {{
            background-color: #283757; /* Mute Dark Blue Color */
            color: white; /* Text Color */
        }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

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

# county selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

# Filter based on county
county_data = mi_df[mi_df['NAME'] == selected_county]

# bar chart for the selected county
st.bar_chart(county_data[['B08301_002E', 'B08301_003E', 'B08301_008E', 'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E']])



