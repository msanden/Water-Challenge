import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([

    'Choose a County:',
    dcc.Dropdown(
        id='persisted-county',
        value='Marsabit',
        options= [{'label': str(item), 'value': str(item)} for item in set(county_data['county'])],
        persistence=True
        ),
        
    html.Div(id='persisted-choices'),
    
  ]),

@app.callback(
    Output('persisted-choices', 'children'),
    [Input('persisted-county', 'value')]
)
def set_out(county):
    return 'You chose: {}'.format(county)