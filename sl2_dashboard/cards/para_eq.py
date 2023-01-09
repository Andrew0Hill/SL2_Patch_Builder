import dash_bootstrap_components as dbc
from dash import html, dcc

para_eq_card = dbc.AccordionItem(
    [
        dbc.Label("Placeholder")
    ],
    title=f"Parametric EQ Parameters",
    id=f"para_eq_params"
)