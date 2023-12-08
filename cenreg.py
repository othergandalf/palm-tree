import streamlit as st
import pandas as pd
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

    # Fetch census data for all MI tracts
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
def train_knn_model(df, knn_y_variable):
    selected_features = ['Total Population', 'Median Income', 'Poverty Rate', 'Time of Commute']
    X = df[selected_features]
    y = df[knn_y_variable]

    imputer = SimpleImputer(strategy='median')
    X_imp = imputer.fit_transform(X)
    df[selected_features] = X_imp

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X_imp)

    X_train, X_test, y_train, y_test = train_test_split(scaled_X, y, test_size=0.2, random_state=42)

    knn_model = KNeighborsClassifier(n_neighbors=3)
    knn_model.fit(X_train, y_train)

    # Calculate KNN training score
    training_score = knn_model.score(X_train, y_train)

    return knn_model, scaler, training_score

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
    knn_y_variable = st.selectbox("Select Commute Variable for KNN Model", ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home'],
                              key="selectbox1")

    # Train the KNN model and get the scaler based on user-selected y-variable
    knn_model, scaler, training_score = train_knn_model(df, knn_y_variable)

    # Add widgets for user inputs with unique keys
    total_population_slider = st.slider("Total Population", key="total_population", min_value=0, max_value=10000, value=5000)
    median_income_slider = st.slider("Median Income", key="median_income", min_value=0, max_value=100000, value=50000)
    poverty_rate_slider = st.slider("Poverty Rate", key="poverty_rate", min_value=0, max_value=100, value=10)
    time_of_commute_slider = st.slider("Time of Commute (minutes)", key="time_of_commute", min_value=0, max_value=120, value=30)

    # User inputs
    user_input = [total_population_slider, median_income_slider, poverty_rate_slider, time_of_commute_slider]

    # Make predictions
    prediction = make_predictions(knn_model, scaler, user_input)
    st.write(f"Updated Prediction ({knn_y_variable}): {prediction}")

    # Display the actual y-variable from user-selected data
    actual_value = df[df[knn_y_variable] == prediction].head(1)[knn_y_variable].values[0]
    st.write(f"Actual {knn_y_variable} from user-selected data: {actual_value}")

    # Display the KNN training score
    st.write(f"KNN Training Score: {training_score:.2%}")

    # Plotting the data using Plotly Express with user customization
    st.header('Commute Count at the Tract-Level')
    color_variable = 'Poverty Rate'  # Assuming this as a default color variable
    graph_y_variable = st.selectbox("Select Y-Axis Commute Variable in Scatterplot",
                                     ['Driving Alone', 'Carpooling', 'Public Transportation', 'Walking', 'Cycling', 'Other Means', 'Worked from Home'],
                                     key="0002")

    # Tract visual
    fig = px.scatter(df,
        x='Median Income',
        y=graph_y_variable,
        color=color_variable,
        size='Total Population',
        hover_data=['NAME']
    )

    st.plotly_chart(fig)

show()
