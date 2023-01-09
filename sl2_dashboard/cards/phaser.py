import dash_bootstrap_components as dbc
from dash import html, dcc


def create_phaser_channel_card(cnum: int):
    card = dbc.AccordionItem([
        dbc.Label("Placeholder")
    ], title=f"Phaser Channel {cnum} Parameters", id=f"phaser_c{cnum}_params")
    return card