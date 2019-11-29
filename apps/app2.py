import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import requests, requests_cache, json
import pandas as pd
from pandas import DataFrame
import dash_table

from app import app
from .resource import make_request, table_data


requests_cache.install_cache('waterpoint_cache', backend='sqlite', expire_after=86400)
url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
waterpoint_data = make_request(url)
df = table_data(waterpoint_data)
waterpoint_fields = ['mWaterId','county','siteName','expertStatus','households','siteLon','siteLat','mlStatusPred']
df = DataFrame(df, columns=waterpoint_fields)
df = df.drop_duplicates()

PAGE_SIZE = 20

layout = html.Div([

        html.P('Water Point Status:'),

        html.Div([
            dcc.Dropdown(
                id='user_status_dropdown',
                value=['offline','repair','normal use'],
                options= [{'label': str(item), 'value': str(item)} for item in set(df['expertStatus'])],
                multi=True,
                # value=list(set(df['expertStatus']))
                )
        ],className='row'),

        html.Br(),

        html.Div([dcc.Graph(id='bar-graph')], className='row'),

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

        ], className='row'),

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
    layout = go.Layout(bargap=0.05, bargroupgap=0, barmode='group', showlegend=False, dragmode="select",
                    xaxis=dict(showgrid=False, nticks=50, fixedrange=False),
                    yaxis=dict(showticklabels=True, showgrid=False, fixedrange=False, rangemode='nonnegative', zeroline=False)
                    )
    trace = go.Bar(x=dff.groupby('county',as_index = False).count()['county'],
                   y=dff.groupby('county',as_index = False).count()['expertStatus'])
    
    return go.Figure(data=trace, layout=layout)