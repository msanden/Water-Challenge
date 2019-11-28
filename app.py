import os
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.config.from_object(os.environ['APP_SETTINGS'])

app.title = 'IBM Water Challenge'
server = app.server
app.config.suppress_callback_exceptions = True