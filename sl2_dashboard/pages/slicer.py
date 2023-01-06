import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, callback

dash.register_page(__name__)

slider_args = {"min":0,
               "max": 100,
               "tooltip": {"always_visible": True},
               "vertical": True,
               "verticalHeight":200,
               "marks":None,
               "dots":False,
               "persistence":True}


def create_channel_params(id):

    c1 = html.Div([dbc.Row(html.H6("Channel 1", className="card-subtitle")),
                               dbc.Row([dbc.Col(dcc.Slider(id=f"{id}_c1_slider{i}",**slider_args),style={"width":"0px"}) for i in range(24)]),
                               ])

    c2 = html.Div([dbc.Row(html.H6("Channel 2", className="card-subtitle")),
                               dbc.Row([dbc.Col(dcc.Slider(id=f"{id}_c2_slider{i}",**slider_args),style={"width":"0px"}) for i in range(24)]),
                               ])

    c = dbc.ListGroup([dbc.ListGroupItem(c1, id=f"{id}_c1"),
                                 dbc.ListGroupItem(c2, id=f"{id}_c2")],
                                flush=True)
    return c


step_length_group = create_channel_params("step_length_group")
step_level_group = create_channel_params("step_level_group")
band_group = create_channel_params("band_group")
effect_type_group = create_channel_params("effect_type_group")
pitch_shift_group = create_channel_params("pitch_shift_group")

layout = html.Div([
    html.Div([
        dbc.Card([
            dbc.CardHeader([
               "Global Params"
            ]),
            dbc.CardBody([
                "SOmething goes here I think."
            ])
        ])
    ],style={"padding-top":"10px",
             "padding-bottom":"10px"}),
    html.Div([
        dbc.Card([
            dbc.CardHeader([
                dbc.Tabs([
                    dbc.Tab(label="Step Length", tab_id="step_length"),
                    dbc.Tab(label="Step Level", tab_id="step_level"),
                    dbc.Tab(label="Band Pass", tab_id="band_pass"),
                    dbc.Tab(label="Effect Type", tab_id="effect_type"),
                    dbc.Tab(label="Pitch Shift", tab_id="pitch_shift"),
                ],
                    id="slicer-tabs",
                    active_tab="step_length")
            ]),
            html.Div(id="param_select")
        ])
    ])
])


@callback(Output("tmp","children"),[Input("c1_1","value")])
def test_get_values(value):
    print("Here")

@callback(Output("param_select", "children"), [Input("slicer-tabs", "active_tab")])
def slicer_channel(active_tab):
    if active_tab == "step_length":
        return step_length_group
    elif active_tab == "step_level":
        return step_level_group
    elif active_tab == "band_pass":
        return band_group
    elif active_tab == "effect_type":
        return effect_type_group
    elif active_tab == "pitch_shift":
        return pitch_shift_group
    else:
        return dash.no_update