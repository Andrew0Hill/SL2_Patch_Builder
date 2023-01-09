import dash_bootstrap_components as dbc
from dash import html, dcc


def create_tremolo_channel_card(cnum: int):
    card = dbc.AccordionItem([
        dbc.Label("Placeholder")
    ], title=f"Tremolo Channel {cnum} Parameters", id=f"tremolo_c{cnum}_params")
    return card