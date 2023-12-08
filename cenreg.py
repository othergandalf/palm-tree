import streamlit as st
import pandas as pd
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import plotly.express as px

def fetch_census_data():
    c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")
    fields = [
        'NAME', 'B08301_001E', 'B08301_002E', 'B08301_003E', 'B08301_008E',
        'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E',
        'B01003_001E', 'B19101_001E', 'B17001_002E', 'B08303_001E'
    ]

    # #Fetch census data for all MI tracts
    census_data = c.acs5.state_county_tract(
        fields=fields,
        county_fips="*",
        state_fips=states.MI.fips,
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
        'B08303_001E': 'Time of Commute'
    }, inplace=True)

    df['Poverty Rate'] = (df['Poverty Count'] / df['Total Population']) * 100

    return df

def train_knn_model(df):
    selected_features = ['Total Population', 'Median Income', 'Poverty Rate', 'Time of Commute']
    X = df[selected_features]

    # Train KNN model for each commute type
    knn_models = {}
    scalers = {}
    commute_variables = ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home']
    
    for y_variable in commute_variables:
        y = df[y_variable]

        imputer = SimpleImputer(strategy='median')
        X_imp = imputer.fit_transform(X)
        df[selected_features] = X_imp

        scaler = StandardScaler()
        scaled_X = scaler.fit_transform(X_imp)

        knn_model = KNeighborsClassifier(n_neighbors=3)
        knn_model.fit(scaled_X, y)

        knn_models[y_variable] = knn_model
        scalers[y_variable] = scaler

    return knn_models, scalers

def make_predictions(knn_model, scaler, user_input):
    # Scale user input to match the scale of the training data
    scaled_input = scaler.transform([user_input])
    prediction = knn_model.predict_proba(scaled_input)[0]

    return prediction

def show():
    st.title('KNN Model Page')

    # Load data
    df = fetch_census_data()

    # KNN model training
    st.header('KNN Model Training')

    # Add widgets for user inputs with unique keys
    total_population_slider = st.slider("Total Population", key="total_population", min_value=0, max_value=10000, value=5000)
    median_income_slider = st.slider("Median Income", key="median_income", min_value=0, max_value=100000, value=50000)
    poverty_rate_slider = st.slider("Poverty Rate", key="poverty_rate", min_value=0, max_value=100, value=10)
    time_of_commute_slider = st.slider("Time of Commute (minutes)", key="time_of_commute", min_value=0, max_value=120, value=30)

    # Train the KNN models and get the scalers
    knn_models, scalers = train_knn_model(df)

    # User inputs
    user_input = [total_population_slider, median_income_slider, poverty_rate_slider, time_of_commute_slider]

    # Make predictions for each commute variable
    predictions = {}
    for y_variable in knn_models.keys():
        predictions[y_variable] = make_predictions(knn_models[y_variable], scalers[y_variable], user_input)

    # Plotting the data using Plotly Express with user customization
    st.header('Expected Mix of Commuting')

    fig = px.bar(predictions, x=predictions.keys(), y=[prediction[1] for prediction in predictions.values()], labels={'y': 'Probability'}, title='Expected Mix of Commuting')
    st.plotly_chart(fig)

if __name__ == "__main__":
    show()
