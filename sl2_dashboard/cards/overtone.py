import dash_bootstrap_components as dbc
from dash import html, dcc


def create_overtone_channel_card(cnum: int):
    card = dbc.AccordionItem([
        dbc.Label("Placeholder")
    ], title=f"Overtone Channel {cnum} Parameters", id=f"overtone_c{cnum}_params")
    return card