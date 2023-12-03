# main.py
import streamlit as st
import cenreg
import commuting

st.set_page_config(page_title='Michigan Commuting Data', page_icon='🚗')

page = st.sidebar.radio("Select Page", ["Commuting Data Map", "KNN Model"])

if page == "Commuting Data Map":
  commuting.show()
elif page == "KNN Model":
  cenreg.show()
