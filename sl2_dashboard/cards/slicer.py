import dash_bootstrap_components as dbc
from sl2.params import slicer
from itertools import chain
from dash import dcc, Output, State
from sl2_dashboard.cards.common import make_tooltip, opts_from_enum, SLIDER_ARGS, SLIDER_TYPES, N_CHANNELS


def make_slider_group(id, cargs):
    return [dbc.Col(dcc.Slider(id=f"{id}_s{i}", disabled=(i >= 8), **cargs, **SLIDER_ARGS), style={"width": "0px"}) for
            i in range(N_CHANNELS)]


def create_slicer_channel_card(cnum: int):
    sliders_dict = {s_t: make_slider_group(f"{s_t}_c{cnum}", cargs=args) for s_t, args in SLIDER_TYPES}
    s_names = {s_t: [v.children.id for v in v_t] for s_t, v_t in sliders_dict.items()}

    p_names = {"Pattern": f"slicer_c{cnum}_pattern",
               "Enable": f"slicer_c{cnum}_enable",
               "Effect": f"slicer_c{cnum}_effect",
               "Step Num": f"slicer_c{cnum}_step_num"}

    tt_names = {"Pattern": f"slicer_pattern_c{cnum}_tt",
                "Enable": f"slicer_enable_c{cnum}_tt",
                "Effect": f"slicer_effect_c{cnum}_tt",
                "Step Num": f"slicer_step_num_c{cnum}_tt",
                "Parameter Arrays": f"slicer_param_arr_c{cnum}_tt"}

    slicer_card = dbc.AccordionItem([
        dbc.Row(
            [
                dbc.Col([
                    dbc.Label(["Enabled", make_tooltip(tt_names["Enable"])]),
                    dbc.Switch(value=True, id=p_names["Enable"], label=None)
                ], width="auto"),
                dbc.Col([
                    dbc.Label(["Pattern Select:", make_tooltip(tt_names["Pattern"])]),
                    dbc.Select(id=p_names["Pattern"],
                               options=opts_from_enum(slicer.PATTERN),
                               value=str(slicer.PATTERN.USER.value),
                               disabled=True)

                ], width="auto"),
                dbc.Col([
                    dbc.Label(["Effect Type:", make_tooltip(tt_names["Effect"])]),
                    dbc.Select(id=p_names["Effect"],
                               options=opts_from_enum(slicer.FX_TYPE),
                               value=str(slicer.FX_TYPE.OFF.value),
                               disabled=False)
                ], width="auto"),
                dbc.Col([
                    dbc.Label(["Step Number:", make_tooltip(tt_names["Step Num"])]),
                    dbc.Select(id=p_names["Step Num"],
                               options=opts_from_enum(slicer.STEP_NUMBER),
                               value=str(slicer.STEP_NUMBER.STEP_8.value),
                               disabled=False)
                ], width="auto")
            ], style={"padding-bottom": "15px"}),
        dbc.Row(dbc.Label(["Parameter Arrays:", make_tooltip(tt_names["Parameter Arrays"])])),
        dbc.Row(
            [
                dbc.Tabs([
                    dbc.Tab(children=dbc.Row(sliders_dict["step_length"]),
                            label="Step Length",
                            tab_id=f"slicer_step_length_c{cnum}"),
                    dbc.Tab(children=dbc.Row(sliders_dict["step_level"]),
                            label="Step Level",
                            tab_id=f"slicer_step_level_c{cnum}"),
                    dbc.Tab(children=dbc.Row(sliders_dict["band_pass"]),
                            label="Band Pass",
                            tab_id=f"slicer_band_pass_c{cnum}"),
                    dbc.Tab(children=dbc.Row(sliders_dict["effect_level"]),
                            label="Effect Level",
                            tab_id=f"slicer_effect_level_c{cnum}"),
                    dbc.Tab(children=dbc.Row(sliders_dict["pitch_shift"]),
                            label="Pitch Shift",
                            tab_id=f"slicer_pitch_shift_c{cnum}"),
                ], id=f"slicer_tabs_c{cnum}", active_tab=f"slicer_step_length_c{cnum}")
            ]
        )
    ], title=f"Slicer Channel {cnum} Parameters", id=f"slicer_c{cnum}_params")

    params = list(p_names.values())
    tooltips = list(tt_names.values())
    sliders = list(chain.from_iterable(s_names.values()))

    outputs = [Output(sl, "value") for sl in params + sliders]

    states = [State(sl, "value") for sl in params + sliders]

    return tooltips, sliders, slicer_card, outputs, states
