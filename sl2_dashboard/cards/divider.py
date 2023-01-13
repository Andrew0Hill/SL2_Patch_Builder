import dash_bootstrap_components as dbc
from dash import html, dcc, Output, State
from sl2_dashboard.cards.common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS
from sl2.params import divider

divider_params = {f"Param {i}" : f"divider_param_{i}" for i in range(1,3)}

divider_tts = {k:v+"_tt" for k,v in divider_params.items()}



divider_card = dbc.AccordionItem(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label(["Param 1", make_tooltip(divider_tts["Param 1"])]),
                dbc.Select(id=divider_params["Param 1"],
                           options=opts_from_enum(divider.PARAM_1),
                           value=str(divider.PARAM_1.VALUE_1.value),
                           disabled=False)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(divider_tts["Param 2"])]),
                dbc.Select(id=divider_params["Param 2"],
                           options=opts_from_enum(divider.PARAM_2),
                           value=str(divider.PARAM_2.VALUE_9.value),
                           disabled=False)
            ],width="auto"),
        ])
    ],
    title=f"Divider Parameters",
    id=f"divider_params"
)

divider_outputs = [Output(dv, "value") for dv in divider_params.values()]

divider_state = [State(dv, "value") for dv in divider_params.values()]