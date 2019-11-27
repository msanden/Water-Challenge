import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import requests, json
import pandas as pd
from pandas import DataFrame
import dash_table

from app import app


url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
counties = ['Garissa','Isiolo','Marsabit','Turkana','Wajir']
waterpoint_fields = ['mWaterId','county','siteName','expertStatus','households','siteLon','siteLat','mlStatusPred']

def make_request(url):
    waterpoint_data = []
    for county in counties:
        j_resp = requests.get(url.format(county)).json()
        waterpoint_sites = {'data': j_resp['data']}
        waterpoint_data.append(waterpoint_sites) 
    return waterpoint_data

waterpoint_data = make_request(url)

def table_data(list_dict):
    empty_df = []
    for index in range(len(list_dict)):
        for key in list_dict[index]:
            broken_df = pd.DataFrame(list_dict[index][key])
        empty_df.append(broken_df)
    df = pd.concat(empty_df)
    return df

df = table_data(waterpoint_data)

df = DataFrame(df, columns=waterpoint_fields)
df = df.drop_duplicates()


PAGE_SIZE = 20


layout = html.Div([
    html.Div([
        html.P('Select a County'),
        dcc.Dropdown(
            id='county',
            value=['Garissa'],
            options= [{'label': str(item), 'value': str(item)} for item in set(df['county'])],
            multi=True,
            # value=list(set(df['expertStatus']))
            )
        ]),







    ],className='container')







