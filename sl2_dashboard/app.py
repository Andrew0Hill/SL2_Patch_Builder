import dash
import webbrowser
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input

COLOR_MAIN = "#009999"

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],use_pages=True)

header = dbc.NavbarSimple(children=[],
                          brand="SL-2 Patch Editor",
                          brand_href="#",
                          color="primary",
                          dark=True)

settings = dbc.Card([
    dbc.CardHeader("Header"),
    dbc.CardBody([
        dbc.Nav(
            [
                dbc.NavLink("How-To", href="/", active="exact"),
                dbc.NavLink("Slicer", href="/slicer", active="exact"),
                dbc.NavLink("Phaser", href="#", active="exact", disabled=True),
                dbc.NavLink("Flanger", href="#", active="exact", disabled=True),
            ],
            vertical=True,
            pills=True,
        )
    ])
])

pane = html.Div(id="pane")

body = html.Div(children=[
    dbc.Row([
        dbc.Col([settings], width=3),
        dbc.Col([dash.page_container], width=9)
    ])
], style={"padding-top": "10px"})

app.layout = dbc.Container([header,
                            body],
                           fluid=True)

if __name__ == "__main__":
    app.run_server()
