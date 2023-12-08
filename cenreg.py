import streamlit as st
import pandas as pd
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import plotly.express as px

def fetch_census_data():
    # ... (unchanged)

def train_knn_model(df, y_variable):
    selected_features = ['Total Population', 'Median Income', 'Poverty Rate', 'Time of Commute']
    X = df[selected_features]
    y = df[y_variable]

    imputer = SimpleImputer(strategy='median')
    X_imp = imputer.fit_transform(X)
    
    # Create a copy of the DataFrame before modifying it
    df_copy = df.copy()
    df_copy[selected_features] = X_imp

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X_imp)

    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(scaled_X, y)

    return knn_model, scaler, df_copy

def make_predictions(knn_model, scaler, user_input):
    # Scale user input to match the scale of the training data
    scaled_input = scaler.transform([user_input])
    prediction = knn_model.predict(scaled_input)

    return prediction[0]

def show():
    st.title('KNN Model Page')

    # Load data
    df = fetch_census_data()

    # KNN model training
    st.header('KNN Model Training')

    # User selects the y-variable for the commute
    y_variable = st.selectbox("Select Commute Variable for KNN Model", ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home'],
                              key="0001")

    # Train the KNN model and get the scaler based on the user-selected y-variable
    knn_model, scaler, df_copy = train_knn_model(df, y_variable)

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

    # Plotting the data using Plotly Express with user customization
    st.header('Commute Count at the Tract-Level')
    color_variable = 'Poverty Rate'  # Assuming this as a default color variable
    graph_y_variable = st.selectbox("Select Y-Axis Commute Variable in Scatterplot",
                                     ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home'],
                                     key="0002")

    # Tract visual
    fig = px.scatter(df_copy,
        x='Median Income',
        y=graph_y_variable,
        color=color_variable,
        size='Total Population',
        hover_data=['NAME']
    )

    st.plotly_chart(fig)

show()
