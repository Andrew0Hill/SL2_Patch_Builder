import dash_bootstrap_components as dbc
from sl2_dashboard.cards.common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from dash import html, dcc, Output, State

para_eq_params = {"Enable": "para_eq_enable"}
para_eq_params.update({f"Param {i}":f"para_eq_param_{i}" for i in range(1,12)})

para_eq_tts = {k:v+"_tt" for k,v in para_eq_params.items()}

para_eq_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enable",make_tooltip(para_eq_tts["Enable"])]),
                dbc.Switch(id=para_eq_params["Enable"],value=1,label=None)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 1",make_tooltip(para_eq_tts["Param 1"])]),
                dcc.Slider(id=para_eq_params["Param 1"],min=0,max=100,value=20,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(para_eq_tts["Param 2"])]),
                dcc.Slider(id=para_eq_params["Param 2"], min=0, max=100, value=20,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(para_eq_tts["Param 3"])]),
                dcc.Slider(id=para_eq_params["Param 3"], min=0, max=100, value=17,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(para_eq_tts["Param 4"])]),
                dcc.Slider(id=para_eq_params["Param 4"], min=0, max=100, value=14,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 5", make_tooltip(para_eq_tts["Param 5"])]),
                dcc.Slider(id=para_eq_params["Param 5"], min=1, max=4, value=1,**SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 6", make_tooltip(para_eq_tts["Param 6"])]),
                dcc.Slider(id=para_eq_params["Param 6"], min=0, max=100, value=20, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 7", make_tooltip(para_eq_tts["Param 7"])]),
                dcc.Slider(id=para_eq_params["Param 7"], min=0, max=100, value=23, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 8", make_tooltip(para_eq_tts["Param 8"])]),
                dcc.Slider(id=para_eq_params["Param 8"], min=0, max=2, value=1, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 9", make_tooltip(para_eq_tts["Param 9"])]),
                dcc.Slider(id=para_eq_params["Param 9"], min=0, max=100, value=20, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 10", make_tooltip(para_eq_tts["Param 10"])]),
                dcc.Slider(id=para_eq_params["Param 10"], min=0, max=10, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 11", make_tooltip(para_eq_tts["Param 11"])]),
                dcc.Slider(id=para_eq_params["Param 11"], min=0, max=100, value=29, **SLIDER_ARGS)
            ],width="auto")
        ])
    ],
    title=f"Parametric EQ Parameters",
    id=f"para_eq_params"
)

para_eq_outputs = [Output(peq, "value") for peq in para_eq_params.values()]

para_eq_state = [State(peq, "value") for peq in para_eq_params.values()]
