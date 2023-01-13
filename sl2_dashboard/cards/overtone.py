import dash_bootstrap_components as dbc
from dash import html, dcc, Output, State
from sl2_dashboard.cards.common import make_tooltip, SLIDER_ARGS


def create_overtone_channel_card(cnum: int):
    p_names = {"Enable": f"overtone_c{cnum}_enable"}
    p_names.update({f"Param {i}": f"overtone_c{cnum}_param_{i}" for i in range(1,9)})

    tt_names = {k: v + "_tt" for k, v in p_names.items()}

    card = dbc.AccordionItem([
        dbc.Row([
            dbc.Col([
                dbc.Label(["Enabled", make_tooltip(tt_names["Enable"])]),
                dbc.Switch(value=False, id=p_names["Enable"], label=None)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Param 1", make_tooltip(tt_names["Param 1"])]),
                dcc.Slider(id=p_names["Param 1"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 2", make_tooltip(tt_names["Param 2"])]),
                dcc.Slider(id=p_names["Param 2"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 3", make_tooltip(tt_names["Param 3"])]),
                dcc.Slider(id=p_names["Param 3"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 4", make_tooltip(tt_names["Param 4"])]),
                dcc.Slider(id=p_names["Param 4"], min=0, max=100, value=100, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 5", make_tooltip(tt_names["Param 5"])]),
                dcc.Slider(id=p_names["Param 5"], min=0, max=100, value=35, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 6", make_tooltip(tt_names["Param 6"])]),
                dcc.Slider(id=p_names["Param 6"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 7", make_tooltip(tt_names["Param 7"])]),
                dcc.Slider(id=p_names["Param 7"], min=0, max=100, value=50, **SLIDER_ARGS)
            ],width="auto"),
            dbc.Col([
                dbc.Label(["Param 8", make_tooltip(tt_names["Param 8"])]),
                dcc.Slider(id=p_names["Param 8"], min=0, max=1, value=1, **SLIDER_ARGS)
            ],width="auto")
        ])
    ], title=f"Overtone Channel {cnum} Parameters", id=f"overtone_c{cnum}_params")

    params = list(p_names.values())

    tooltips = list(tt_names.values())

    output = [Output(ov,"value") for ov in params]

    state = [State(ov,"value") for ov in params]

    return tooltips, card, output, state