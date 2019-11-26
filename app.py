import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'IBM Water Challenge'
server = app.server
app.config.suppress_callback_exceptions = True