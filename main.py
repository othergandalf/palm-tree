# main.py
import streamlit as st
st.set_page_config(page_title='Michigan Commuting Data', page_icon='🚗') #
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import plotly.express as px
from census import Census
from us import states

import cenreg
import commuting

#  have to import pages AFTER set_page_config is called. Good to know!

page = st.sidebar.radio("Select Page", ["Exploring County-level Data", "Modeling Tract-level Data"])

if page == "Exploring County-level Data":
  commuting.show()
elif page == "Modeling Tract-level Data":
  cenreg.show()
