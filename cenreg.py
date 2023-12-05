import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler    

def show():
    st.title('KNN Model Page')

    # Fetch census data
    #naming some objects for the API call
        c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")
        fields = [
            'NAME', 'B08301_001E', 'B08301_002E', 'B08301_003E', 'B08301_008E',
            'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E',
            'B01003_001E', 'B19101_001E', 'B17001_002E'
        ]
     census_data = c.acs5.state_county(fields=('NAME',
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

    # KNN model training
    if 'data' in locals():
        st.header('KNN Model Training')

        # Feature selection
        selected_features = ['Total Population', 'Median Income', 'Poverty Rate']
        X = data[selected_features]
        y = data['Cycling']  # Replace 'TargetColumn' with your actual target column

        # Standardization
        scaler = StandardScaler()
        scaled_X = scaler.fit_transform(X)

        # Build KNN Model
        knn_model = KNeighborsClassifier(n_neighbors=7)
        knn_model.fit(scaled_X, y)

        st.success("KNN Model trained successfully!")

        # Add widgets for user inputs
        st.header('Make Predictions')
        total_population_slider = st.slider("Total Population", min_value=0, max_value=500000, value=250000)
        median_income_slider = st.slider("Median Income", min_value=0, max_value=100000, value=50000)
        poverty_rate_slider = st.slider("Poverty Rate", min_value=0, max_value=100, value=10)

        # Scale user inputs and make predictions
        user_input = scaler.transform([[..., total_population_slider, median_income_slider, poverty_rate_slider]])
        prediction = knn_model.predict(user_input)

        st.write(f"Predicted Commuting Pattern: {prediction}")


    
        
