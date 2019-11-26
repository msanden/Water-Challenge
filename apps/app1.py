import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


url = 'https://waterpoint-engine-challenge-dev.mybluemix.net/sensors/daily-county-readings/{}'
counties = ['Wajir','Turkana','Garissa','Marsabit','Isiolo']
waterpoint_fields = ['county','siteName','expertStatus','siteLon','siteLat','localDate','mlStatusPred']



layout = html.Div([
    'Choose a city:',
    dcc.Dropdown(
        id='persisted-city',
        value='Montreal',
        options=[{'label': v, 'value': v} for v in CITIES],
        persistence=True
    ),

    html.Br(),

    'correlated persistence - choose a neighborhood:',
    html.Div(
        dcc.Dropdown(
            id='neighborhood'
            
            ), id='neighborhood-container'),
    
    html.Br(),
    
    html.Div(id='persisted-choices')
])


@app.callback(
    Output('neighborhood-container', 'children'),
    [Input('persisted-city', 'value')]
)
def set_neighborhood(city):
    neighborhoods = NEIGHBORHOODS[city]
    return dcc.Dropdown(
        id='neighborhood',
        value=neighborhoods[0],
        options=[{'label': v, 'value': v} for v in neighborhoods],
        persistence_type='local',
        persistence=city
    )


@app.callback(
    Output('persisted-choices', 'children'),
    [Input('persisted-city', 'value'), Input('neighborhood', 'value')]
)
def set_out(city, neighborhood):
    return 'You chose: {}, {}'.format(neighborhood, city)

