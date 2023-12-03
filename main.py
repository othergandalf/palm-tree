# main.py
import streamlit as st
import page1
import page2

st.set_page_config(page_title='Michigan Commuting Data', page_icon='🚗')

page = st.sidebar.radio("Select Page", ["Page 1", "Page 2"])

if page == "Page 1":
    page1.show()
elif page == "Page 2":
    page2.show()
