import dash
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

mapbox_access_token = 'pk.eyJ1IjoibWFudWVsc24iLCJhIjoiY2szY2k5dTF2MHNhejNjbGRyNnNzcmF4dCJ9.-bX5MXB3Ezlbnwsr-JA1kA'


layout = html.Div([
    
    html.Div([
        html.P('Select a County'),
        dcc.Dropdown(
            id='user_county_dropdown',
            options= [{'label': str(item), 'value': str(item)} for item in set(df['county'])],
            value=['Garissa'],
            multi=True,
            style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "50%"},
            )
        ]),

    html.Div([
        dcc.Graph(
            id='map',
            animate=True, 
            style={'margin-top': '20'}
            )
        ]),

    ],className='container')

#callback for map and dropdown
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
            "layout": go.Layout(autosize=True, hovermode='closest', showlegend=False, height=700,
                                mapbox={'accesstoken': mapbox_access_token, 'bearing': 0,
                                        'center': {'lat': -0.023559, 'lon': 37.906193}, 'pitch': 0, 'zoom': 5,
                                        "style": 'mapbox://styles/mapbox/light-v9'})}



