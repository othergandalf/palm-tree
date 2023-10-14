import streamlit as st
import pandas as pd
from census import Census
from us import states

st.title('Michigan Commuting Data')

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

mi_df.head()
# county selection
selected_county = st.selectbox('Select County', mi_df['NAME'])

# Filter based on county
county_data = mi_df[mi_df['NAME'] == selected_county]

# Display selected county data
st.write(f"### Commuting Data for {selected_county}")
st.write(f"Total Commuters: {county_data['B08301_001E'].values[0]}")
st.write(f"Driving Alone: {county_data['B08301_002E'].values[0]}")
st.write(f"Carpooling: {county_data['B08301_003E'].values[0]}")
st.write(f"Public Transportation: {county_data['B08301_008E'].values[0]}")
st.write(f"Walking: {county_data['B08301_011E'].values[0]}")
st.write(f"Cycling: {county_data['B08301_012E'].values[0]}")
st.write(f"Taxicab, Motorcycle, or Other Means: {county_data['B08301_013E'].values[0]}")
st.write(f"Worked from Home: {county_data['B08301_014E'].values[0]}")

# Mapping clean names to variable codes
variable_names = {
    'B08301_002E': 'Driving Alone',
    'B08301_003E': 'Carpooling',
    'B08301_008E': 'Public Transportation',
    'B08301_011E': 'Walking',
    'B08301_012E': 'Cycling',
    'B08301_013E': 'Other Means',
    'B08301_014E': 'Worked from Home'
}

# Create a new DataFrame with clean variable names
clean_data = county_data.rename(columns=variable_names)

# Display selected county data with clean variable names
st.write(f"### Commuting Data for {selected_county}")
st.write(f"Total Commuters: {county_data['B08301_001E'].values[0]}")
for variable, name in variable_names.items():
    st.write(f"{name}: {county_data[variable].values[0]}")

# Bar chart for the selected county with clean variable names
st.bar_chart(clean_data[['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home']])











