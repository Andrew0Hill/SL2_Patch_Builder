import dash_bootstrap_components as dbc
from dash import html, dcc

mixer_card = dbc.AccordionItem(
    [
        dbc.Label("Placeholder")
    ],
    title=f"Mixer Parameters",
    id=f"mixer_params"
)