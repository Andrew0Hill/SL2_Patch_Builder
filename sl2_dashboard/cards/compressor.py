import dash_bootstrap_components as dbc
from sl2_dashboard.cards.common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from dash import html, dcc, Output, State


compressor_params = {"Enable": "compressor_enable"}
compressor_params.update({f"Param {i}":f"compressor_param_{i}" for i in range(1,7)})

compressor_tts = {k:v+"_tt" for k,v in compressor_params.items()}

compressor_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enable",make_tooltip(compressor_tts["Enable"])]),
                dbc.Switch(id=compressor_params["Enable"],value=False,label=None)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 1",make_tooltip(compressor_tts["Param 1"])]),
                dcc.Slider(id=compressor_params["Param 1"],min=0,max=100,value=50,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(compressor_tts["Param 2"])]),
                dcc.Slider(id=compressor_params["Param 2"], min=0, max=100, value=50,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(compressor_tts["Param 3"])]),
                dcc.Slider(id=compressor_params["Param 3"], min=0, max=100, value=60,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(compressor_tts["Param 4"])]),
                dcc.Slider(id=compressor_params["Param 4"], min=0, max=100, value=50,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 5", make_tooltip(compressor_tts["Param 5"])]),
                dcc.Slider(id=compressor_params["Param 5"], min=0, max=17, value=12,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 6", make_tooltip(compressor_tts["Param 6"])]),
                dcc.Slider(id=compressor_params["Param 6"], min=0, max=0, value=0, **SLIDER_ARGS)
            ], width="auto")
        ])
    ],
    title=f"Compressor Parameters",
    id=f"compressor_params"
)

compressor_outputs = [Output(cm, "value") for cm in compressor_params.values()]

compressor_state = [State(cm, "value") for cm in compressor_params.values()]
