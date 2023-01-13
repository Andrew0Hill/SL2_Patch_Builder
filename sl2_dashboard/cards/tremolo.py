import dash_bootstrap_components as dbc
from dash import html, dcc, Output, State
from .common import make_tooltip, SLIDER_ARGS


def create_tremolo_channel_card(cnum: int):
    p_names = {"Enable": f"tremolo_c{cnum}_enable"}
    p_names.update({f"Param {i}": f"tremolo_c{cnum}_param_{i}" for i in range(1,6)})

    tt_names = {k: v + "_tt" for k, v in p_names.items()}

    card = dbc.AccordionItem([
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enabled", make_tooltip(tt_names["Enable"])]),
                dbc.Switch(value=False, id=p_names["Enable"], label=None)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Param 1", make_tooltip(tt_names["Param 1"])]),
                dcc.Slider(id=p_names["Param 1"], min=0, max=100, value=100, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(tt_names["Param 2"])]),
                dcc.Slider(id=p_names["Param 2"], min=0, max=255, value=85, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(tt_names["Param 3"])]),
                dcc.Slider(id=p_names["Param 3"], min=0, max=6, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(tt_names["Param 4"])]),
                dcc.Slider(id=p_names["Param 4"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 5", make_tooltip(tt_names["Param 5"])]),
                dcc.Slider(id=p_names["Param 5"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto")
        ])
    ], title=f"Tremolo Channel {cnum} Parameters", id=f"tremolo_c{cnum}_params")

    params = list(p_names.values())

    tooltips = list(tt_names.values())

    output = [Output(tr,"value") for tr in params]

    state = [State(tr,"value") for tr in params]

    return tooltips, card, output, state