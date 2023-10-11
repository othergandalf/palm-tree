import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
# Sample data for the custom dataset
custom_data = pd.DataFrame({'X': [0.5, 1], 'Y': [2, 1]})
# Load Seaborn MPG dataset
mpg_data = sns.load_dataset("mpg")
# Title and dataset selection
st.title("Regression Analysis App")
dataset_choice = st.selectbox("Select a dataset:", ("Custom Dataset", "Seaborn MPG Dataset"))
# User selects dataset
if dataset_choice == "Custom Dataset":
    selected_data = custom_data
    x_variable = 'X'  # Set the default x-variable for the custom dataset
    y_variable = 'Y'  # Set the default y-variable for the custom dataset
else:
    selected_data = mpg_data
    x_variable = st.selectbox("Select the X-variable:", list(mpg_data.columns))
    y_variable = st.selectbox("Select the Y-variable:", list(mpg_data.columns))
# Display selected dataset
st.dataframe(selected_data)
# Regression model selection
model_choice = st.radio("Select a regression model:", ("Line", "RBF-NN"))
# Regression and Plotting
if model_choice == "Line":
    st.subheader("Linear Regression")
    slope = st.slider("Select slope:", min_value=-10.0, max_value=10.0, step=0.1, value=1.0)
    intercept = st.slider("Select intercept:", min_value=-10.0, max_value=10.0, step=0.1, value=0.0)
    # Calculate predictions
    y_pred = slope * selected_data[x_variable] + intercept
    # Plot the data and regression line
    plt.figure(figsize=(8, 6))
    plt.scatter(selected_data[x_variable], selected_data[y_variable], label="Data Points")
    plt.plot(selected_data[x_variable], y_pred, color='red', label="Regression Line")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.legend()
    st.pyplot()
    # Calculate and display error metrics
    mae = mean_absolute_error(selected_data[y_variable], y_pred)
    mse = mean_squared_error(selected_data[y_variable], y_pred)
    st.write(f"Mean Absolute Error (MAE): {mae}")
    st.write(f"Mean Squared Error (MSE): {mse}")
elif model_choice == "RBF-NN":
    st.subheader("Radial Basis Function Neural Network (RBF-NN)")
    # User input for RBF-NN
    center1 = st.slider("Center 1:", min_value=-10.0, max_value=10.0, step=0.1, value=0.0)
    center2 = st.slider("Center 2:", min_value=-10.0, max_value=10.0, step=0.1, value=0.0)
    bandwidth = st.slider("Bandwidth (L):", min_value=0.01, max_value=10.0, step=0.01, value=1.0)
    weights = st.slider("Weights:", min_value=0.1, max_value=10.0, step=0.1, value=1.0)
    # Calculate RBF-NN predictions
    rbf_nn_predictions = weights * np.exp(-((selected_data[x_variable] - center1) ** 2) / (2 * bandwidth ** 2)) + \
                        weights * np.exp(-((selected_data[x_variable] - center2) ** 2) / (2 * bandwidth ** 2))
    # Plot the data and RBF-NN predictions
    plt.figure(figsize=(8, 6))
    plt.scatter(selected_data[x_variable], selected_data[y_variable], label="Data Points")
    plt.plot(selected_data[x_variable], rbf_nn_predictions, color='red', label="RBF-NN")
    plt.xlabel(x_variable)
    plt.ylabel(y_variable)
    plt.legend()
    st.pyplot()
    # Calculate and display error metrics
    mae = mean_absolute_error(selected_data[y_variable], rbf_nn_predictions)
    mse = mean_squared_error(selected_data[y_variable], rbf_nn_predictions)
    st.write(f"Mean Absolute Error (MAE): {mae}")
    st.write(f"Mean Squared Error (MSE): {mse}")