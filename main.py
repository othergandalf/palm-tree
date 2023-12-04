# main.py
import streamlit as st
import cenreg
import commuting

st.set_page_config(page_title='Michigan Commuting Data', page_icon='🚗')

page = st.sidebar.radio("Select Page", ["Exploring County-level Data", "Modeling Tract-level Data"])

if page == "Exploring County-level Data":
commuting.show()
elif page == "Modeling Tract-level Data":
cenreg.show()
