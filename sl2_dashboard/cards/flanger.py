import dash_bootstrap_components as dbc
from dash import html, dcc, Output, State
from .common import make_tooltip, SLIDER_ARGS


def create_flanger_channel_card(cnum: int):
    p_names = {"Enable": f"flanger_c{cnum}_enable"}
    p_names.update({f"Param {i}": f"flanger_c{cnum}_param_{i}" for i in range(1,11)})

    tt_names = {k: v + "_tt" for k, v in p_names.items()}

    card = dbc.AccordionItem([
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enabled", make_tooltip(tt_names["Enable"])]),
                dbc.Switch(value=False, id=p_names["Enable"], label=None)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Param 1", make_tooltip(tt_names["Param 1"])]),
                dcc.Slider(id=p_names["Param 1"], min=0, max=180, value=25, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(tt_names["Param 2"])]),
                dcc.Slider(id=p_names["Param 2"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(tt_names["Param 3"])]),
                dcc.Slider(id=p_names["Param 3"], min=0, max=80, value=80, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(tt_names["Param 4"])]),
                dcc.Slider(id=p_names["Param 4"], min=0, max=75, value=75, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 5", make_tooltip(tt_names["Param 5"])]),
                dcc.Slider(id=p_names["Param 5"], min=0, max=180, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 6", make_tooltip(tt_names["Param 6"])]),
                dcc.Slider(id=p_names["Param 6"], min=0, max=12, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 7", make_tooltip(tt_names["Param 7"])]),
                dcc.Slider(id=p_names["Param 7"], min=0, max=100, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 8", make_tooltip(tt_names["Param 8"])]),
                dcc.Slider(id=p_names["Param 8"], min=0, max=3, value=0, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 9", make_tooltip(tt_names["Param 9"])]),
                dcc.Slider(id=p_names["Param 9"], min=0, max=100, value=100, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 10", make_tooltip(tt_names["Param 10"])]),
                dcc.Slider(id=p_names["Param 10"], min=0, max=100, value=0, **SLIDER_ARGS)
            ],width="auto")
        ])
    ], title=f"Flanger Channel {cnum} Parameters", id=f"flanger_c{cnum}_params")

    params = list(p_names.values())

    tooltips = list(tt_names.values())

    output = [Output(fl,"value") for fl in params]

    state = [State(fl, "value") for fl in params]

    return tooltips, card, output, state
