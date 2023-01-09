import dash_bootstrap_components as dbc
from dash import html, dcc

ns_card = dbc.AccordionItem(
    [
        dbc.Label("Placeholder")
    ],
    title=f"Noise Suppressor Parameters",
    id=f"ns_params"
)