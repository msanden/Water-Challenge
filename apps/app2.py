import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import requests, requests_cache, json
import pandas as pd
from pandas import DataFrame
import dash_table

from app import app
from .resource import make_request, concat_data


requests_cache.install_cache('waterpoint_cache', backend='sqlite', expire_after=86400)

url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
waterpoint_data = make_request(url)

df = concat_data(waterpoint_data)
waterpoint_fields = ['mWaterId','county','siteName','expertStatus','households','siteLon','siteLat']

df = DataFrame(df, columns=waterpoint_fields)

df = df.drop_duplicates(subset='siteLon', keep='first')

# df = df.drop_duplicates()

PAGE_SIZE = 20

layout = html.Div([

        html.Div([html.H3('Waterpoint Services: Detail View')], style={'text-align': 'center'}),

        html.Div([
            
            'Select Status:  ',

            html.Div([

                dcc.Dropdown(
                    id='user_status_dropdown',
                    value=list(set(df['expertStatus'])),
                    options= [{'label': str(item), 'value': str(item)} for item in set(df['expertStatus'])],
                    multi=True,
                    style={"display": "block"},
                    )
            ],className='six columns'),

            html.Br(),html.Br(),

            html.Div([
                dash_table.DataTable(
                    id='data_table',
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i, "deletable": True} for i in df.columns],

                    page_action='native',
                    page_size = PAGE_SIZE,

                    sort_action='native',
                    selected_rows=[],
                    style_table = {'overflowX': 'scroll','overflowY': 'scroll', 'border': 'thin lightgrey solid'},            
                    style_header={'backgroundColor': 'white','fontWeight': 'bold'},
                    style_as_list_view=True,
                    style_cell={'textAlign': 'left'},
                    ),

            ], className='six columns'),            

        ], className='row'),

        html.Div([dcc.Graph(id='bar-graph')], className='six columns'),


    ],className='container')


#callback table after user updates the dropdown menu
@app.callback(
    Output('data_table', 'data'),
    [Input('user_status_dropdown', 'value')])
def filter_table_with_dropdown(user_selected_status):
    map_aux = df.copy()
    map_aux = map_aux[map_aux['expertStatus'].isin(user_selected_status)] # filter table with expertStatus selection 
    data = map_aux.to_dict('records')
    return data


#callback bar graph after dropdown menu filters rows
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('data_table', 'selected_rows'),
     Input('data_table', 'data')])
def update_figure(selected_rows, data):
    dff = pd.DataFrame(data)  
    layout = go.Layout(barmode='group', dragmode="select",
                    title='Waterpoint Status',
                    titlefont={'color':'#191A1A', 'size':14},
                    margin={'l':35,'r':35, 'b':35,'t':45},
                    )
    trace = go.Bar(x=dff.groupby('county',as_index = False).count()['county'],
                   y=dff.groupby('county',as_index = False).count()['expertStatus'])
    
    return go.Figure(data=trace, layout=layout)