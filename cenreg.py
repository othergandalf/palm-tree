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

def train_knn_model(df, y_variable):
    selected_features = ['Total Population', 'Median Income', 'Poverty Rate', 'Time of Commute']
    X = df[selected_features]
    y = df[y_variable]

    imputer = SimpleImputer(strategy='median')
    X_imp = imputer.fit_transform(X)
    df[selected_features] = X_imp

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X_imp)

    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(scaled_X, y)

    return knn_model, scaler

def visualize_model_output(df, knn_model, scaler, y_variable):
    # Generate a grid of points for visualization
    median_income_range = df['Median Income'].min(), df['Median Income'].max()
    variable_range = df['Time of Commute'].min(), df['Time of Commute'].max()  # You can change this to 'Total Population' if needed

    # Create a grid of points
    grid_points = pd.DataFrame({
        'Median Income': list(range(int(median_income_range[0]), int(median_income_range[1]), 1000)),
        'Time of Commute': list(range(int(variable_range[0]), int(variable_range[1]), 10)),
    })

    # Scale the grid points using the same scaler used for training
    scaled_grid_points = scaler.transform(grid_points)

    # Make predictions for the grid points
    predictions = knn_model.predict(scaled_grid_points)

    # Add the predictions to the grid points dataframe
    grid_points['Predicted Commute Behavior'] = predictions

    # Plot the model output
    fig = px.scatter(
        grid_points,
        x='Median Income',
        y='Time of Commute',
        color='Predicted Commute Behavior',
        title=f'Model Output: Predicted Commute Behavior ({y_variable})',
        labels={'Predicted Commute Behavior': 'Commute Behavior'},
        hover_data=['Median Income', 'Time of Commute']
    )

    st.plotly_chart(fig)

def show():
    st.title('KNN Model Page')

    # Load data
    df = fetch_census_data()

    # KNN model training
    st.header('KNN Model Training')

    # User selects the y-variable for the commute
    y_variable = st.selectbox("Select Commute Variable for KNN Model", ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home'],
                              key="0001")

    # Train the KNN model and get the scaler based on user-selected y-variable
    knn_model, scaler = train_knn_model(df, y_variable)

    # Add widgets for user inputs with unique keys
    total_population_slider = st.slider("Total Population", key="total_population", min_value=0, max_value=10000, value=5000)
    median_income_slider = st.slider("Median Income", key="median_income", min_value=0, max_value=100000, value=50000)
    poverty_rate_slider = st.slider("Poverty Rate", key="poverty_rate", min_value=0, max_value=100, value=10)
    time_of_commute_slider = st.slider("Time of Commute (minutes)", key="time_of_commute", min_value=0, max_value=120, value=30)

    # User inputs
    user_input = [total_population_slider, median_income_slider, poverty_rate_slider, time_of_commute_slider]

    # Make predictions
    prediction = make_predictions(knn_model, scaler, user_input)
    st.write(f"Updated Prediction ({y_variable}): {prediction}")

    # Visualize model output
    visualize_model_output(df, knn_model, scaler, y_variable)

show()
