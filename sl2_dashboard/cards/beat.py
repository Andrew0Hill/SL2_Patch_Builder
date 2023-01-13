import dash_bootstrap_components as dbc
from .common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from dash import html, dcc, Output, State

beat_params = {"Param 1": "beat_param_1",
               "Param 2": "beat_param_2"}

beat_tts = {k: v + "_tt" for k, v in beat_params.items()}

beat_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Param 1", make_tooltip(beat_tts["Param 1"])]),
                dcc.Slider(id=beat_params["Param 1"], min=0, max=255, value=0, disabled=False, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(beat_tts["Param 2"])]),
                dcc.Slider(id=beat_params["Param 2"], min=0, max=255, value=1, disabled=False, **SLIDER_ARGS)
            ],width="auto"),
        ])
    ],
    title=f"Beat Parameters",
    id=f"beat_params"
)

beat_outputs = [Output(b,"value") for b in beat_params.values()]

beat_state = [State(beat, "value") for beat in beat_params.values()]
