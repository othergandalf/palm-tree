import streamlit as st
import pandas as pd
import altair as alt
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

st.write("### Commuting Modes Distribution")
chart_data = county_data[["B08301_002E", "B08301_003E", "B08301_008E", "B08301_011E", "B08301_012E", "B08301_013E", "B08301_014E"]]

# Use altair for more customization
chart = alt.Chart(chart_data.melt(var_name="Commuting Mode", value_name="Number of Commuters")).mark_bar().encode(
    x=alt.X("Commuting Mode:N", title="Commuting Mode"),  # Customize x-axis label
    y=alt.Y("sum('Number of Commuters'):Q"),  # Customize y-axis label
    color='Commuting Mode:N'
).properties(
    width=600,
    height=400) 

# Render the chart
st.altair_chart(chart)











