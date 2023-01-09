import dash_bootstrap_components as dbc
from sl2.params import slicer
from itertools import chain
from dash import html, dcc
from typing import List


N_CHANNELS = 24
SLIDER_ARGS = {"tooltip": {"always_visible": True,"placement":"bottom"},
               "vertical": True,
               "verticalHeight": 200,
               "marks": None,
               "dots": False,
               #"persistence": True,
               "step":1}

def make_tooltip(id):
    tt = html.A(id=id,
                className="bi bi-question-circle",
                style={"margin-left": "5px",
                       "color":"info"})
    return tt

def opts_from_enum(enum):
    return [{"label": e.name, "value": e.value} for e in enum]


def make_slider_group(id, cargs):
    return [dbc.Col(dcc.Slider(id=f"{id}_s{i}", disabled=(i >= 8), **cargs, **SLIDER_ARGS), style={"width": "0px"}) for i in range(N_CHANNELS)]


def create_channel_card(cnum: int,slider_types: List):
    sliders_dict = {s_t: make_slider_group(f"{s_t}_c{cnum}", cargs=args) for s_t, args in slider_types}
    s_names = {s_t: [v.children.id for v in v_t] for s_t,v_t in sliders_dict.items()}

    p_names = {"Pattern": f"c{cnum}_pattern",
               "Enable": f"c{cnum}_enable",
               "Effect": f"c{cnum}_effect",
               "Step Num": f"c{cnum}_step_num"}

    tt_names = {"Pattern": f"pattern_c{cnum}_tt",
                "Enable": f"enable_c{cnum}_tt",
                "Effect": f"effect_c{cnum}_tt",
                "Step Num": f"step_num_c{cnum}_tt",
                "Parameter Arrays":f"param_arr_c{cnum}_tt"}

    slider_card = dbc.Card(
        [
            dbc.CardHeader([
                dbc.Row(
                    [
                        dbc.Col(f"Slicer Channel {cnum} Parameters", width="auto")
                    ],
                    align="center"
                ),
            ]),
            dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Col([
                            dbc.Label(["Enabled",make_tooltip(tt_names["Enable"])]),
                            dbc.Switch(value=True, id=p_names["Enable"],label=None)
                        ],width="auto"),
                        dbc.Col([
                            dbc.Label(["Pattern Select:",make_tooltip(tt_names["Pattern"])]),
                            dbc.Select(id=p_names["Pattern"],
                                       options=opts_from_enum(slicer.PATTERN),
                                       value=str(slicer.PATTERN.USER.value),
                                       disabled=True)

                        ], width="auto"),
                        dbc.Col([
                            dbc.Label(["Effect Type:",make_tooltip(tt_names["Effect"])]),
                            dbc.Select(id=p_names["Effect"],
                                       options=opts_from_enum(slicer.FX_TYPE),
                                       value=str(slicer.FX_TYPE.OFF.value),
                                       disabled=False)
                        ], width="auto"),
                        dbc.Col([
                            dbc.Label(["Step Number:",make_tooltip(tt_names["Step Num"])]),
                            dbc.Select(id=p_names["Step Num"],
                                       options=opts_from_enum(slicer.STEP_NUMBER),
                                       value=str(slicer.STEP_NUMBER.STEP_8.value),
                                       disabled=False)
                        ], width="auto")
                    ],style={"padding-bottom":"15px"}),
                dbc.Row(dbc.Label(["Parameter Arrays:",make_tooltip(tt_names["Parameter Arrays"])])),
                dbc.Row(
                    [
                        dbc.Tabs([
                            dbc.Tab(children=dbc.Row(sliders_dict["step_length"]),
                                    label="Step Length",
                                    tab_id=f"step_length_c{cnum}"),
                            dbc.Tab(children=dbc.Row(sliders_dict["step_level"]),
                                    label="Step Level",
                                    tab_id=f"step_level_c{cnum}"),
                            dbc.Tab(children=dbc.Row(sliders_dict["band_pass"]),
                                    label="Band Pass",
                                    tab_id=f"band_pass_c{cnum}"),
                            dbc.Tab(children=dbc.Row(sliders_dict["effect_level"]),
                                    label="Effect Level",
                                    tab_id=f"effect_level_c{cnum}"),
                            dbc.Tab(children=dbc.Row(sliders_dict["pitch_shift"]),
                                    label="Pitch Shift",
                                    tab_id=f"pitch_shift_c{cnum}"),
                        ], id=f"slicer_tabs_c{cnum}", active_tab=f"step_length_c{cnum}")
                    ]
                )
            ])
        ]
    )

    return list(p_names.values()),list(tt_names.values()),list(chain.from_iterable(s_names.values())),slider_card