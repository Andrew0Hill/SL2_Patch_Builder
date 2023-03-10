import dash_bootstrap_components as dbc
from .common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from dash import html, dcc, Output, State

mixer_params = {"Ch. 2 Bypass": "mixer_ch2_bypass",
                "Param 1": "Param 1",
                "Param 2": "Param 2",
                "Param 3": "Param 3",
                "Param 4": "Param 4"}
#mixer_params.update({f"Param {i}":f"mixer_param_{i}" for i in range(1,5)})

mixer_tts = {k:v+"_tt" for k,v in mixer_params.items()}

mixer_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Ch. 2 Bypass",make_tooltip(mixer_tts["Ch. 2 Bypass"])]),
                dbc.Switch(id=mixer_params["Ch. 2 Bypass"],value=0,label=None)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 1",make_tooltip(mixer_tts["Param 1"])]),
                dbc.Switch(id=mixer_params["Param 1"],value=1)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(mixer_tts["Param 2"])]),
                dcc.Slider(id=mixer_params["Param 2"], min=0, max=100, value=100,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(mixer_tts["Param 3"])]),
                dbc.Switch(id=mixer_params["Param 3"],value=0)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(mixer_tts["Param 4"])]),
                dcc.Slider(id=mixer_params["Param 4"], min=0, max=100, value=100,**SLIDER_ARGS)
            ],width="auto")
        ])
    ],
    title=f"Mixer Parameters",
    id=f"mixer_params"
)

mixer_outputs = [Output(mx, "value") for mx in mixer_params.values()]

mixer_state = [State(mx, "value") for mx in mixer_params.values()]