def show():
import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# Fetch census data
def fetch_census_data(api_key, state_code, county_code):
    c = Census(api_key)
    fields = [
        'NAME', 'B08301_001E', 'B08301_002E', 'B08301_003E', 'B08301_008E',
        'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E',
        'B01003_001E', 'B19101_001E', 'B17001_002E'
    ]

    census_data = c.acs5.state_county_tract(
        fields=fields,
        state_fips=state_code,
        county_fips=county_code,
        tract="*",
        year=2021
    )

    df = pd.DataFrame(census_data)
    df.rename(columns={
        'B08301_002E': 'Driving Alone',
        'B08301_003E': 'Carpooling',
        'B08301_008E': 'Public Transportation',
        'B08301_011E': 'Walking',
        'B08301_012E': 'Cycling',
        'B08301_013E': 'Other Means',
        'B08301_014E': 'Worked from Home',
        'B01003_001E': 'Total Population',
        'B19101_001E': 'Median Income',
        'B17001_002E': 'Poverty Count',
    }, inplace=True)

    df['Poverty Rate'] = (df['Poverty Count'] / df['Total Population']) * 100

    return df

# Streamlit app
def main():
    st.title('Michigan Commuting Data')

    # Add your Census API key here
    census_api_key = "YOUR_CENSUS_API_KEY"
    st.markdown("Replace 'YOUR_CENSUS_API_KEY' with your actual Census API key.")

    # Input for state and county codes
    state_code = st.text_input("Enter State FIPS Code (e.g., 26 for Michigan):", "26")
    county_code = st.text_input("Enter County FIPS Code (e.g., 163 for Wayne County):", "163")

    if st.button("Fetch Data"):
        try:
            st.info("Fetching data. Please wait...")

            # Fetch data
            data = fetch_census_data(census_api_key, state_code, county_code)

            # Display the cleaned data
            st.dataframe(data.head())
            st.success("Data fetched successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    # KNN model
    if 'data' in locals():
        selected_features = ['B08006_001E', 'B08136_001E', 'B08132_001E', 'Median Income', 'Poverty Rate', ...]
        X = data[selected_features]
        y = data['TargetColumn']  # Replace 'TargetColumn' with your actual target column

        scaler = StandardScaler()
        scaled_X = scaler.fit_transform(X)

        knn_model = KNeighborsClassifier(n_neighbors=7)
        knn_model.fit(scaled_X, y)

        total_population_slider = st.slider("Total Population", min_value=0, max_value=500000, value=250000)
        median_income_slider = st.slider("Median Income", min_value=0, max_value=100000, value=50000)
        poverty_rate_slider = st.slider("Poverty Rate", min_value=0, max_value=100, value=10)

        user_input = scaler.transform([[..., total_population_slider, median_income_slider, poverty_rate_slider]])
        prediction = knn_model.predict(user_input)

        st.write(f"KNN Prediction: {prediction}")

# Rest of your code for visualization remains unchanged

if __name__ == "__main__":
    main()
