from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import json
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()

# begin choropleth data---------------------------------------------------------
# read in demographics dataframe for plots
mp = pd.read_csv(DATA_PATH.joinpath('thePivot.csv'))
# droping out all agency info because of the discrepancies can add back in later if found.
agencies = ['Unnamed: 0', 'Standard Pantry', 'CSFP Pantry', 'CSFP&TEFAP Pantry', 'TEFAP Pantry', 'Total Agencies']
mp = mp.drop(agencies, axis=1)

with open(DATA_PATH.joinpath('NCDOT_County_Boundaries.geojson')) as f:
    geo = json.load(f)

ddOptions = ['Client CSFP Visit', 'Client Pantry Visit', 'TEFAP Pantry Visit', 'Total Clients',
             'Median Monthly Income', 'Average Age', 'Female', 'Male', 'American Indian', 'Asian',
             'Black', 'Hispanic Latino', 'White Anglo']

counties = []
tmp = mp.set_index('County')
for county in geo['features']:
    county_name = county['properties']['UpperCountyName']
    if county_name in tmp.index:
        geometry = county['geometry']
        counties.append({
            'type': 'Feature',
            'id': county_name,
            'geometry': geometry,
        })

countiesSort = sorted(counties, key=lambda d: d['id'])
geo_ok = {'type': "FeatureCollection", 'features': countiesSort}

# begin layout---------------------------------------------------------
layout = html.Div([
    html.Div(
        html.H2(children='Data by County'),
        style={'textAlign': 'center', 'color': 'black'}
    ),
    html.Br(),
    html.Div(
        dcc.Dropdown(id='my_dropdown',
                     options=[
                         {'label': i, 'value': i}
                         for i in ddOptions
                     ],
                     optionHeight=35,  # height/space between dropdown options
                     value='Total Clients',  # dropdown value selected automatically when page loads
                     disabled=False,  # disable dropdown value selection
                     multi=False,  # allow multiple dropdown values to be selected
                     searchable=True,  # allow user-searching of dropdown values
                     search_value='',  # remembers the value searched in dropdown
                     placeholder='Please select...',  # gray, default text shown when no option is selected
                     clearable=True,  # allow user to removes the selected value
                     style={'width': "100%"},  # use dictionary to define CSS styles of your dropdown
                     # className='select_box',           #activate separate CSS document in assets folder
                     # persistence=True,                 #remembers dropdown value. Used with persistence_type
                     # persistence_type='memory'         #remembers dropdown value selected until...
                     ),
    ),
    html.Div([
        dcc.Graph(id='choromap')
    ])
])


# choropleth callback ---------------------------------------------------------
@app.callback(
    Output(component_id='choromap', component_property='figure'),
    Input(component_id='my_dropdown', component_property="value"),
)
def create_choro(my_dropdown):
    df = mp.copy()
    fig = px.choropleth_mapbox(
        df,
        geojson=geo_ok,
        locations='County',
        color=df[my_dropdown],
        mapbox_style='white-bg',
        center={'lat': 35.4404, 'lon': -78.3842},
        zoom=6.5,
        color_continuous_scale='aggrnyl',
        range_color=(0, df[my_dropdown].max()),
    )
    fig.update_layout(height=500, margin={"r": 0, "t": 10, "l": 0, "b": 0})
    return fig
