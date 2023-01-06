import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, callback

dash.register_page(__name__,path="/")

layout = dbc.Card([
    dbc.CardHeader("Welcome!"),
    dbc.CardBody(["Here's how to use this app. "])
])