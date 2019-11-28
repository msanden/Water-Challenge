import dash
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

mapbox_access_token = 'pk.eyJ1IjoibWFudWVsc24iLCJhIjoiY2szY2k5dTF2MHNhejNjbGRyNnNzcmF4dCJ9.-bX5MXB3Ezlbnwsr-JA1kA'

layout = html.Div([
    
    html.Div([
        html.Div([
            html.P('Select a County'),
            dcc.Dropdown(
                id='user_county_dropdown',
                options= [{'label': str(item), 'value': str(item)} for item in set(df['county'])],
                value=['Garissa'],
                multi=True,
                # style={"display": "block"},
                )
            ])
        ], className="row"),

    html.Div([
        dcc.Graph(
            id='map',
            animate=True, 
            style={'margin-top': '20'}
            )
        ], className="row"),

    ],className='container')

#callback map after user updates the dropdown menu
@app.callback(
    dash.dependencies.Output("map", "figure"),
    [dash.dependencies.Input("user_county_dropdown", "value")])
def mapping(user_selected_county):
    trace = []
    for county_val in user_selected_county:
        dff = df[df["county"] == county_val]
        trace.append(
            go.Scattermapbox(lat=dff["siteLat"], lon=dff["siteLon"], mode='markers', marker={'symbol': "circle", 'size': 10},
                             text=dff['expertStatus'], hoverinfo='text', name=county_val))
    return {"data": trace,
            "layout": go.Layout(autosize=True, hovermode='closest', showlegend=False, height=700, title='Locate WaterServices',
                                mapbox={'accesstoken': mapbox_access_token, 'bearing': 0,
                                        'center': {'lat': -0.023559, 'lon': 37.906193}, 'pitch': 0, 'zoom': 5,
                                        "style": 'mapbox://styles/mapbox/light-v9'})}



