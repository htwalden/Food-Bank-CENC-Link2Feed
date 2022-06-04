from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from app import server

# connect to app pages
from apps import map, combined, colormap


# begin layout--------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname=''),
    html.Div([
        html.Div(
            html.Img(src='assets/fbicon2.jpg'),
            style={'width': '25%',
                   'display': 'flex',
                   'padding-left': '3rem'}
        ),
        html.Div(
            html.H1([
                html.P('Link2Feed Dashboard',
                            className="fs-1 text",
                            style={'fontStyle': 'italic',
                                   'color': '#001745'
                                   })
            ]),
            style={'fontStyle': 'italic',
                   'width': '50%',
                   'textAlign': 'center',
                   'display': 'inline-block'}
        ),
        html.Div([
            dcc.Link(
                dbc.Button("Interactive Map",
                           id='button1',
                           outline=True,
                           color="dark",
                           className="d-grid gap-2 col-6 mx-auto"),
                href='/apps/map'),
            dcc.Link(
                dbc.Button("Demographics",
                           id='button2',
                           outline=True,
                           color="dark",
                           className="d-grid gap-2 col-6 mx-auto"),
                href='/apps/combined'),
            dcc.Link(
                dbc.Button("Color Map",
                           id='button3',
                           outline=True,
                           color="dark",
                           className="d-grid gap-2 col-6 mx-auto"),
                href='/apps/colormap')
        ], className='row',
            style={'width': '25%',
                   'display': 'flex'}
        ),
    ],
        style={'display': 'flex',
               'flex-wrap': 'wrap',
               'justify-content': 'space-around',
               'align-items': 'center',
               'margin-top': '2rem'}
    ),
    html.Hr(),
    html.Hr(),
    html.Br(),
    html.Div(id='page-content', children=[])
])


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/map':
        return map.layout
    elif pathname == '/apps/combined':
        return combined.layout
    elif pathname == '/apps/colormap':
        return colormap.layout


if __name__ == '__main__':
    app.run_server(debug=True)
