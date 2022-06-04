from dash import html
from dash import dcc
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()

# read in demographics dataframe for plots
ballerMap = 'ballerMap.html'

# begin layout
layout = html.Div([
    html.Div(
        html.H2(children='Client and Pantry Map Tool'),
        style={'textAlign': 'center', 'color': 'black'}
    ),
    html.Div([
        html.Iframe(id='mp',
                    srcDoc=open(DATA_PATH.joinpath('ballerMap.html'))
                    .read(), width='78%', height='600'),
        dcc.Textarea(
            id='textarea-example',
            value='Notes:',
            style={'width': '20%', 'height': 600},
        ),
    ]),
    html.Div([
        html.H3('Legend'),
        html.Div([
            html.P(["Blue dots = clients most recent visit was CSFP visit",
                    html.Br(),
                    "Green dots = clients most recent visit was TEFAP visit",
                    html.Br(),
                    "Red dots = clients most recent visit was Pantry visit",
                    ]),
            html.P(["Numbers in Pantry Callout Boxes:",
                    html.Br(),
                    "1. = agency present only in master agency dataset",
                    html.Br(),
                    "2. = agency present only in distribution dataset",
                    html.Br(),
                    "3. = agency present in master and distribution sets only",
                    html.Br(),
                    "4. = agency present only in link2feed dataset",
                    html.Br(),
                    "5. = agency present in master and link2feed dataset only",
                    html.Br(),
                    "6. = agency present in distribution and link2feed only",
                    html.Br(),
                    "7. = agency present in all three data sets."])
        ]),
    ]),
])
