import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from census import Census
from us import states
import os

# MICHIGAN

mi_census = c.acs5.state_county(fields = ('NAME',
                                           'B08301_001E',
                                            'B08301_002E',
                                            'B08301_003E',
                                            'B08301_008E',
                                            'B08301_011E',
                                            'B08301_012E',
                                            'B08301_013E',
                                            'B08301_014E'),
                                      state_fips = states.MI.fips,
                                      county_fips = "*",
                                      year = 2021)

# Create dataframe
mi_df = pd.DataFrame(mi_census)

# Show dataframe
print(mi_df.head())
print('Shape: ', mi_df.shape)