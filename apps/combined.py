from dash import html
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../datasets').resolve()

# begin table data---------------------------------------------------------
# read in demographics dataframe for plots
masterPivot = pd.read_csv(DATA_PATH.joinpath('thePivot.csv'))
# droping out all agency info because of the discrepancies can add back in later if found.
agencies = ['Unnamed: 0', 'Standard Pantry', 'CSFP Pantry', 'CSFP&TEFAP Pantry', 'TEFAP Pantry', 'Total Agencies']
masterPivot = masterPivot.drop(agencies, axis=1)
masterPivot['id'] = masterPivot['County']
masterPivot.set_index('id', inplace=True, drop=False)


clients = ['Client CSFP Visit', 'Client Pantry Visit', 'TEFAP Pantry Visit', 'Total Clients']
incAgeGen = ['Median Monthly Income', 'Average Age', 'Female', 'Male']
eth = ['American Indian', 'Asian', 'Black', 'Hispanic Latino', 'White Anglo']

# begin layout---------------------------------------------------------
layout = html.Div([
    html.Div([
        html.P(
            'Welcome to your interactive data table!'),
        html.P(
            'Selecting rows and columns will automatically populate a graph below the table.'),
        html.P(
            'Remember to always select the `County` column or the graph will not generate!')
    ]),
    # area below for data table and graph---------------
    html.Div(
        html.H2(children='Demographic Graphs'),
        style={'textAlign': 'center', 'color': 'black'}
    ),
    html.Div(dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
            for i in masterPivot.columns
        ],
        data=masterPivot.to_dict('records'),  # the contents of the table
        editable=False,  # allow editing of data inside all cells
        filter_action="native",  # allow filtering of data by user ('native') or not ('none')
        sort_action="native",  # enables data to be sorted per-column by user or not ('none')
        sort_mode="single",  # sort across 'multi' or 'single' columns
        column_selectable="multi",  # allow users to select 'multi' or 'single' columns
        row_selectable="multi",  # allow users to select 'multi' or 'single' rows
        row_deletable=True,  # choose if user can delete a row (True) or not (False)
        selected_columns=[],  # ids of columns that user selects
        selected_rows=[],  # indices of rows that user selects
        page_action="native",  # all data is passed to the table up-front or not ('none')
        page_current=0,  # page number that user is on
        page_size=12,  # number of rows visible per page
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            # 'minWidth': 120,
            # 'maxWidth': 120,
            # 'width': 120,
            'border': '1px solid black'
        },
        style_data={  # overflow cells' content into multiple lines
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold',
            'border': '1px solid black',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
    )
    ),
    html.Br(),
    html.Br(),
    html.Div(id='bar-container')
])


# Create bar chart
@app.callback(
    Output(component_id='bar-container', component_property='children'),
    [Input(component_id='datatable-interactivity', component_property="derived_virtual_data"),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_columns'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_cols, slctd_rows,
               order_of_rows_indices, order_of_rows_names, actv_cell, slctd_cell):
    #print('***************************************************************************')
    #print('Data across all pages pre or post filtering: {}'.format(all_rows_data))
    #print('---------------------------------------------')
    #print("Indices of selected rows if part of table after filtering:{}".format(slctd_row_indices))
    #print("Names of selected rows if part of table after filtering: {}".format(slct_rows_names))
    #print("Indices of selected rows regardless of filtering results: {}".format(slctd_rows))
    #print('---------------------------------------------')
    #print("Indices of all rows pre or post filtering: {}".format(order_of_rows_indices))
    #print("Names of all rows pre or post filtering: {}".format(order_of_rows_names))
    #print("---------------------------------------------")
    #print("Complete data of active cell: {}".format(actv_cell))
    #print("Complete data of all selected cells: {}".format(slctd_cell))

    dff = pd.DataFrame(all_rows_data)
    dff = dff[slctd_cols]
    yCol = []
    colLi = dff.columns.to_list()
    for col in colLi:
        if (col != 'County') & (col != 'id'):
            yCol.append(col)
    print('yCol info here {}'.format(yCol))
    if ('County' in dff) | ('id' in dff):
        return [
            dcc.Graph(id='bar-chart',
                      figure=px.bar(
                          data_frame=dff,
                          x='County',
                          y=yCol
                      )
                      )
        ]

