import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import requests, json
import pandas as pd
from pandas import DataFrame
import dash_table

from app import app


url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
counties = ['Wajir','Turkana','Garissa','Marsabit','Isiolo']
waterpoint_fields = ['mWaterId','county','siteName','expertStatus','siteLon','siteLat','localDate','mlStatusPred']

waterpoint_data = []
for county in counties:
    j_resp = requests.get(url.format(county)).json()

    waterpoint_sites = {
                'data': j_resp['data']
                }
    waterpoint_data.append(waterpoint_sites)

empty_df = []
for index in range(len(waterpoint_data)):
    for key in waterpoint_data[index]:
        chopped_df = pd.DataFrame(waterpoint_data[index][key])
    empty_df.append(chopped_df)

df = pd.concat(empty_df)
county_data = DataFrame(df, columns=waterpoint_fields)

PAGE_SIZE = 50


layout = html.Div([

# store = dcc.Store(id='my-store', data={'my-data': 'data'})

    html.Div([
        dash_table.DataTable(
            id='datatable',
            data=county_data.to_dict('records'),
            columns=[{"name": i, "id": i} for i in county_data.columns],

            page_action='native',
            page_size = PAGE_SIZE,

            sort_action='native',
            selected_rows=[],
            
            style_header={'backgroundColor': 'white','fontWeight': 'bold'},
            style_as_list_view=True,
            style_cell={'textAlign': 'left'},
            # style_cell_conditional=[
            #     {
            #         'if': {'column_id': i},
            #         'textAlign': 'left'
            #     } for c in ['Date', 'Region']
            # ],

            )]
        ),

    ])







