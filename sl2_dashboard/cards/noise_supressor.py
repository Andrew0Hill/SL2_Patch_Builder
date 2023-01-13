import dash_bootstrap_components as dbc
from .common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from dash import html, dcc, Output, State

noise_suppressor_params = {"Enable": "noise_suppressor_enable",
                           "Threshold": "noise_suppressor_threshold",
                           "Release": "noise_suppressor_release"}

noise_suppressor_tts = {k:v+"_tt" for k,v in noise_suppressor_params.items()}

noise_suppressor_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enable",make_tooltip(noise_suppressor_tts["Enable"])]),
                dbc.Switch(id=noise_suppressor_params["Enable"],value=1,label=None)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Threshold", make_tooltip(noise_suppressor_tts["Threshold"])]),
                dcc.Slider(id=noise_suppressor_params["Threshold"], min=0, max=100, value=30,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Release", make_tooltip(noise_suppressor_tts["Release"])]),
                dcc.Slider(id=noise_suppressor_params["Release"], min=0, max=100, value=30, **SLIDER_ARGS)
            ],width="auto"),
        ])
    ],
    title=f"Noise Suppressor Parameters",
    id=f"noise_suppressor_params"
)

noise_suppressor_outputs = [Output(ns, "value") for ns in noise_suppressor_params.values()]

noise_suppressor_state = [State(ns, "value") for ns in noise_suppressor_params.values()]
