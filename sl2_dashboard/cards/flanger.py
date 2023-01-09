import dash_bootstrap_components as dbc
from dash import html, dcc


def create_flanger_channel_card(cnum: int):
    card = dbc.AccordionItem([
        dbc.Label("Placeholder")
    ], title=f"Flanger Channel {cnum} Parameters", id=f"flanger_c{cnum}_params")
    return card