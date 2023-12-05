import streamlit as st
import pandas as pd
from census import Census
from us import states
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")
fields = [
        'NAME', 'B08301_001E', 'B08301_002E', 'B08301_003E', 'B08301_008E',
        'B08301_011E', 'B08301_012E', 'B08301_013E', 'B08301_014E',
        'B01003_001E', 'B19101_001E', 'B17001_002E'
    ]
    
    # Fetch census data for all MI tracts
census_data = c.acs5.state_county_tract(
    fields=fields,
    county_fips = "*",
    state_fips=states.MI.fips,
    tract="*",
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

def train_knn_model(df):
    # Feature selection
    selected_features = ['Total Population', 'Driving Alone', 'Median Income', 'Poverty Rate']
    X = df[selected_features]
    y = df['Walking']  # Replace 'TargetColumn' with your actual target column
 # impute via SimpleImputer
imputer = SimpleImputer(strategy='median')

# Fit and transform the imputer on your data
X_imp = imputer.fit_transform(X)

# Replace the original X with the imputed values
df[selected_features] = X_imp

    # Standardization
scaler = StandardScaler()
scaled_X = scaler.fit_transform(X_imp)

    # Build KNN Model
knn_model = KNeighborsClassifier(n_neighbors=7)
knn_model.fit(scaled_X, y)

return knn_model, scaler

def make_predictions(model, scaler, user_input):
    # Scale user inputs and make predictions
scaled_input = scaler.transform([user_input])
prediction = model.predict(scaled_input)

return prediction

def show():
    st.title('KNN Model Page')

    # KNN model training
    st.header('KNN Model Training')

    # Train the KNN model and get the scaler
    knn_model, scaler = train_knn_model(df)

    st.success("KNN Model trained successfully!")

    # Add widgets for user inputs
    st.header('Make Predictions')
    total_population_slider = st.slider("Total Population", min_value=0, max_value=500000, value=250000)
    median_income_slider = st.slider("Median Income", min_value=0, max_value=100000, value=50000)
    poverty_rate_slider = st.slider("Poverty Rate", min_value=0, max_value=100, value=10)

    # User inputs
    user_input = [total_population_slider, median_income_slider, poverty_rate_slider]

    # Make predictions
    prediction = make_predictions(knn_model, scaler, user_input)

    st.write(f"Predicted Commuting Pattern: {prediction}")

# Uncomment the next line to run the Streamlit app
# show()
