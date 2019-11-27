import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.graph_objs as go

import requests, json
import pandas as pd
from pandas import DataFrame
import dash_table

from app import app

# layout = html.Div([

#     'Choose a County:',
#     dcc.Dropdown(
#         id='persisted-county',
#         value='Marsabit',
#         options= [{'label': str(item), 'value': str(item)} for item in set(county_data['county'])],
#         persistence=True
#         ),
        
#     html.Div(id='persisted-choices'),

#   ]),

# @app.callback(
#     Output('persisted-choices', 'children'),
#     [Input('persisted-county', 'value')]
# )
# def set_out(county):
#     return 'You chose: {}'.format(county)

url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
counties = ['Wajir','Turkana','Garissa','Marsabit','Isiolo']
waterpoint_fields = ['mWaterId','county','siteName','expertStatus','households','siteLon','siteLat','mlStatusPred']

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

        html.Div([
            html.P('Water Point Status:'),
            dcc.Dropdown(
                id='status',
                value=['offline','repair','normal use'],
                options= [{'label': str(item), 'value': str(item)} for item in set(county_data['expertStatus'])],
                multi=True,
                # value=list(set(county_data['expertStatus']))
                )
        ]),

        html.Div([
            dash_table.DataTable(
                id='datatable',
                data=county_data.to_dict('records'),
                columns=[{"name": i, "id": i, "deletable": True} for i in sorted(county_data.columns)],

                page_action='native',
                page_size = PAGE_SIZE,

                sort_action='native',
                selected_rows=[])
        ]),

        html.Div([dcc.Graph(id='bar-graph')]),

    ])

@app.callback(
    Output('datatable', 'data'),
    [Input('status', 'value')])
def update_selected_row_indices(status):
    map_aux = county_data.copy()
    map_aux = map_aux[map_aux['expertStatus'].isin(status)] # status filter 
    data = map_aux.to_dict('records')
    return data


#datatable to bar graph
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('datatable', 'data'),
     Input('datatable', 'selected_rows')])
def update_figure(data, selected_rows):
    dff = pd.DataFrame(data)  #??? what does this return
    layout = go.Layout(bargap=0.05, bargroupgap=0, barmode='group', showlegend=False, dragmode="select",
                    xaxis=dict(showgrid=False, nticks=50, fixedrange=False),
                    yaxis=dict(showticklabels=True, showgrid=False, fixedrange=False, rangemode='nonnegative', zeroline=False)
                    )
    data = go.Bar(x=dff.groupby('county', as_index = False).count()['county'],
                  y=dff.groupby('county', as_index = False).count()['expertStatus'])
    
    return go.Figure(data=data, layout=layout)