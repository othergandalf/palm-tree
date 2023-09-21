import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px
from sklearn.datasets import load_iris
iris = load_iris()
iris = sns.load_dataset('iris')
st.write("""
# Iris from Seaborn
Explore this dataset by selecting a species of flower to visualize physical characteristics of it's blooms. 
""")
species = st.selectbox("Species:", iris['species'].unique())
filtered_data = iris[iris['species'] == species]
fig = px.scatter_3d(filtered_data,
                     x='sepal_length', 
                    y='sepal_width',
                      z='petal_length',
                        color='species',
                     title=f"Visual Representation of {species} Iris")
st.plotly_chart(fig)