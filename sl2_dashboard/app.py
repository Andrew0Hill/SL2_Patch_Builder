import dash
import dash_bootstrap_components as dbc
import base64
import io
import sl2
from sl2.params import slicer
import numpy as np
from dash import html, dcc, Output, Input
from slicer import create_channel_card,N_CHANNELS

COLOR_MAIN = "#009999"
SLIDER_TYPES = [("step_length",{"min":0,"max":100,"value":50}),
                ("step_level",{"min":0,"max":100,"value":100}),
                ("band_pass",{"min":0,"max":6,"value":0}),
                ("effect_level",{"min":0,"max":100,"value":50}),
                ("pitch_shift",{"min":0,"max":24,"value":12})]

N_SLIDER_TYPES = len(SLIDER_TYPES)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

header = dbc.NavbarSimple(children=[],
                          brand="SL-2 Patch Editor",
                          brand_href="#",
                          color="primary",
                          links_left=True,
                          dark=True,
                          fluid=True)

settings = dbc.Card([
    dbc.CardHeader("Upload"),
    dbc.CardBody(dcc.Upload(dbc.Button("Upload File",className="d-grid gap-2"),id="upload"))
])

# Create both channel cards
c1_params, c1_slider_ids, c1_card = create_channel_card(1, slider_types=SLIDER_TYPES)
c2_params, c2_slider_ids, c2_card = create_channel_card(2, slider_types=SLIDER_TYPES)

channel_cards = html.Div([
    html.Div(
        [
        dbc.Card([
            dbc.CardHeader([
                dbc.Col(html.H4(f"Live Set", className="card-title"), width="auto"),
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Name:"),
                        dbc.Input(id="ls_name",value="My Live Set",type="text")
                    ],width="auto"),
                    dbc.Col([
                        dbc.Label("Format Rev:"),
                        dbc.Input(id="ls_formatrev",value="0001", type="text", disabled=True)
                    ],width="auto"),
                    dbc.Col([
                        dbc.Label("Device:"),
                        dbc.Input(id="ls_device",value="SL-2", type="text", disabled=True)
                    ],width="auto")
                ])
            ])
        ])
        ], style={"padding-bottom": "10px"}
    ),
    html.Div(c1_card, style={"padding-bottom": "10px"}),
    html.Div(c2_card, style={"padding-bottom": "10px"})
])

err_toast = dbc.Toast("Unable to parse .tsl file!",
                      id="err_toast",
                      header="File Error",
                      is_open=False,
                      dismissable=True,
                      duration=3000,
                      icon="danger",
                      style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex":999})

success_toast = dbc.Toast("Loaded .tsl file sucessfully!",
                    id="success_toast",
                    header="File Upload Successful",
                    is_open=False,
                    dismissable=True,
                    duration=1500,
                    icon="success",
                    style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 999})

body = html.Div(children=[
    success_toast,
    err_toast,
    dbc.Row([
        dbc.Col([settings], width=2),
        dbc.Col([channel_cards], width=10)
    ])
], style={"padding": "10px"})

app.layout = html.Div([header,body])


def handle_upload(contents):
    context = dash.callback_context
    if context.triggered_id is None:
        return dash.no_update

    # If we can't upload for some reason, just skip and we will display an error toast.
    ls = [dash.no_update] * len(context.outputs_grouping[0])
    p1 = [dash.no_update] * len(context.outputs_grouping[1])
    p2 = [dash.no_update] * len(context.outputs_grouping[2])
    show_success = dash.no_update
    show_err = dash.no_update
    try:
        ctype,cstr = contents.split(",",maxsplit=1)
        bstr = base64.b64decode(cstr)
        buf = io.StringIO(bstr.decode("utf-8"))
        live_set = sl2.LiveSet.from_tsl(buf)
        # TODO: Handle patches within a liveset.
        params = live_set.data[0][0].paramSet
        p1 = params.slicer_1.tolist()
        p2 = params.slicer_2.tolist()
        ls = [live_set.name,live_set.formatRev,live_set.device]
        p1[0] = str(p1[0])
        p2[0] = str(p2[0])
        p1[2:4] = [str(x) for x in p1[2:4]]
        p2[2:4] = [str(x) for x in p2[2:4]]
        show_success = True
    except:
        show_err = True
    return ls,p1,p2,show_err,show_success


ls_outputs = [Output(lsp,"value") for lsp in ["ls_name","ls_formatrev","ls_device"]]
c1_outputs = [Output(sl,"value") for sl in c1_params + c1_slider_ids]
c2_outputs = [Output(sl,"value") for sl in c2_params + c2_slider_ids]
app.callback([ls_outputs,
              c1_outputs,
              c2_outputs,
              Output("err_toast","is_open"),
              Output("success_toast","is_open")],
             [Input("upload","contents")])(handle_upload)

def disable_channels(enable, step_num, pattern):
    # Step number flag
    step_num = int(step_num)
    step_num_flag = np.full(N_CHANNELS, False)
    for v in slicer.STEP_NUMBER:
        if step_num == v.value:
            d_val = int(v.name.replace("STEP_",""))
            step_num_flag = np.array([False] * d_val + [True] * (N_CHANNELS - d_val))
            break
    # Pattern flag works just like enable
    #pattern = int(pattern)
    return np.tile(step_num_flag | (not enable),N_SLIDER_TYPES).tolist()

# Set up callbacks
app.callback([Output(c1_t, "disabled") for c1_t in c1_slider_ids],
         [Input("c1_enable", "value"),
          Input("c1_step_num", "value"),
          Input("c1_pattern", "value")])(disable_channels)

app.callback([Output(c2_t, "disabled") for c2_t in c2_slider_ids],
         [Input("c2_enable", "value"),
          Input("c2_step_num", "value"),
          Input("c2_pattern", "value")])(disable_channels)


if __name__ == "__main__":
    app.run_server()
