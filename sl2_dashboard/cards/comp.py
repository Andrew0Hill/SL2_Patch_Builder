import dash_bootstrap_components as dbc
from dash import html, dcc

compressor_card = dbc.AccordionItem(
    [
        dbc.Label("Placeholder")
    ],
    title=f"Compressor Parameters",
    id=f"compressor_params"
)
