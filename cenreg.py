def show():
    import streamlit as st
    import pandas as pd
    import geopandas as gpd
    import pydeck as pdk
    import plotly.express as px
    from census import Census
    from us import states
    # TITLE
    #  st.title('Michigan Commuting Data')
    # KEY
    c = Census("2cad02e99c0bde70c790f7391ffb3363c5e426ef")

    mi_census = c.acs5.state_county_tract(fields=('NAME',
                                            'B08301_001E',
                                            'B08301_002E',
                                            'B08301_003E',
                                            'B08301_008E',
                                            'B08301_011E',
                                            'B08301_012E',
                                            'B08301_013E',
                                            'B08301_014E',
                                            'B01003_001E', # med income
                                            'B17001_002E',
                                            'B01003_001E',), 
                                state_fips=states.MI.fips,
                                county_fips="*",
                                year=2021)
    # B01003_001E: total population
    # B19101_001E: median income
    # B17001_002E: poverty count 

    #DF 
    mi_df = pd.DataFrame(mi_census)

    mi_df.head()
    st.header('Select a :blue[something]')

    ## KNN MODEL BEGINS HERE
    
    data['poverty_count'] = data['B17001_002E']
    data['total_population'] = data['B01003_001E']
    data['median_income'] = data['B19101_001E']
    data['poverty_rate'] = (data['poverty_count'] / data['total_population']) * 100

shp = "https://raw.githubusercontent.com/othergandalf/palm-tree/main/Counties_(v17a).geojson"

gdf = gpd.read_file(shp)

    # MERGE
    merged_df = gdf.merge(mi_df, how='left', left_on='FIPSCODE', right_on='county')

    # NEW CLEAN NAMES
    variable_names = {
        'B08301_002E': 'Driving Alone',
        'B08301_003E': 'Carpooling',
        'B08301_008E': 'Public Transportation',
        'B08301_011E': 'Walking',
        'B08301_012E': 'Cycling',
        'B08301_013E': 'Other Means',
        'B08301_014E': 'Worked from Home'
    }
poverty_rate = (poverty_count / total_population) * 100
    # NEW DF
    clean_data = county_data.rename(columns=variable_names)

    # Assuming you've loaded the additional variables into your DataFrame
    selected_features = ['B08006_001E', 'B08136_001E', 'B08132_001E', 'median_income', 'poverty_rate', ...]
    X = data[selected_features]

    # Standardization
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)

    # Build KNN Model
    knn_model = KNeighborsClassifier(n_neighbors=7)
    knn_model.fit(scaled_X, y)

    # Add widgets for the new variables
    total_population_slider = st.slider("Total Population", min_value=0, max_value=500000, value=250000)
    median_income_slider = st.slider("Median Income", min_value=0, max_value=100000, value=50000)
    poverty_rate_slider = st.slider("Poverty Rate", min_value=0, max_value=100, value=10)

    # Scale user inputs and make predictions
    user_input = scaler.transform([[..., total_population_slider, median_income_slider, poverty_rate_slider]])
    prediction = knn_model.predict(user_input)

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=44.89,
            longitude=-84.76,
            zoom=5,
            pitch=0,
        ), layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=merged_df,
                get_fill_color=f"[100, 190, 245, {selected_variable} * 0.1]",
                pickable=True,
                auto_highlight=True,
                on_hover=True,
                tooltip={"text": "{NAME}\n{value}".format(NAME="{NAME}", value="{" + selected_variable + "}")},
            )
        ]
    ))




