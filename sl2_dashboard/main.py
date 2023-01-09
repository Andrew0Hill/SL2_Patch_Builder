# Base python
import base64
import io
import json
import re
# Third-party
import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc, Output, Input, State
# Local imports
import sl2
from sl2.params import slicer
from modals import all_modals, all_toasts
from cards.slicer import create_slicer_channel_card, N_CHANNELS, N_SLIDER_GROUPS
from cards.phaser import create_phaser_channel_card
from cards.flanger import create_flanger_channel_card
from cards.tremolo import create_tremolo_channel_card
from cards.overtone import create_overtone_channel_card
from cards.file_transfer import file_transfer_card
from cards.comp import compressor_card
from cards.mixer import mixer_card
from cards.noise_supressor import ns_card
from cards.para_eq import para_eq_card

# Helper function to make a hover-able tooltip
glbl_tooltips = []
def make_tooltip(id):
    tt = html.A(id=id,
                className="bi bi-question-circle",
                style={"margin-left": "5px",
                       "color":"info"})
    glbl_tooltips.append(id)
    return tt
# Main Plotly Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, dbc.icons.BOOTSTRAP])
app.title = "SL2 Patch Editor"
# The server for the application, used for running from gunicorn.
app_server = app.server

##############
# App Layout #
##############
# Header/Navigation bar for the app.
header = dbc.NavbarSimple(children=[
                            dbc.NavItem(dbc.NavLink([
                                dbc.Row([
                                    dbc.Col(html.I(className="bi bi-github fs-4"),
                                            width="auto",
                                            style={"margin-right": "5px"}),
                                    dbc.Col("View on GitHub")
                                ],align="center",className="g-0")
                            ],href="https://github.com/Andrew0Hill/SL2_Patch_Builder"))
                          ],
                          brand=html.H2("SL-2 Patch Editor"),
                          brand_href="#",
                          color="primary",
                          links_left=False,
                          dark=True,
                          fluid=True)

# Create the layouts for both channel cards using a function from slicer.py
slicer_c1_params, slicer_c1_tts, slicer_c1_slider_ids, slicer_c1_card = create_slicer_channel_card(1)
slicer_c2_params, slicer_c2_tts, slicer_c2_slider_ids, slicer_c2_card = create_slicer_channel_card(2)

phaser_c1_card = create_phaser_channel_card(1)
phaser_c2_card = create_phaser_channel_card(2)

flanger_c1_card = create_flanger_channel_card(1)
flanger_c2_card = create_flanger_channel_card(2)

tremolo_c1_card = create_tremolo_channel_card(1)
tremolo_c2_card = create_tremolo_channel_card(2)

overtone_c1_card = create_overtone_channel_card(1)
overtone_c2_card = create_overtone_channel_card(2)

channel_tooltips = list(zip(slicer_c1_tts, slicer_c2_tts))
# Layout for the Slicer C1 and C2 channel cards.
parameter_cards = dbc.Accordion([
    dbc.AccordionItem([
        dbc.Row([
            dbc.Col([
                dbc.Label(["Live Set Name:", make_tooltip("ls_name_tt")]),
                dbc.Input(id="ls_name", value="My Live Set", type="text", valid=True)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Patch Name:", make_tooltip("patch_name_tt")]),
                dbc.Input(id="patch_name", value="CUSTOM-P1", type="text", valid=True)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Format Rev:", make_tooltip("format_rev_tt")]),
                dbc.Input(id="ls_formatrev", value="0001", type="text", disabled=True)
            ], width="auto"),
            dbc.Col([
                dbc.Label(["Device:", make_tooltip("device_tt")]),
                dbc.Input(id="ls_device", value="SL-2", type="text", disabled=True)
            ], width="auto")
        ])
    ],title="Global Parameters",id="glbl_params"),
    slicer_c1_card,
    slicer_c2_card,
    compressor_card,
    phaser_c1_card,
    phaser_c2_card,
    flanger_c1_card,
    flanger_c2_card,
    tremolo_c1_card,
    tremolo_c2_card,
    overtone_c1_card,
    overtone_c2_card,
    mixer_card,
    ns_card,
    para_eq_card
],always_open=True)

# Layout for the body of the page.
body = dbc.Container(children=
                     all_modals +
                     all_toasts +
                     [dbc.Row([
        dbc.Col([file_transfer_card], width=2),
        dbc.Col([parameter_cards], width=10)
    ])],
    style={"padding-top": "10px"},
    fluid=True)

# Final app layout
app.layout = html.Div([header, body])

#################
# App Callbacks #
#################

# Function to validate the names for the Liveset and Patch.
def validate_name(name):
    context = dash.callback_context
    if context.triggered_id is None:
        return dash.no_update
    valid = name.isascii()
    return valid, not valid
# Callbacks to set up the validation for Liveset and Patch.
app.callback([Output("ls_name", "valid"), Output("ls_name", "invalid")],
             Input("ls_name", "value"))(validate_name)
app.callback([Output("patch_name", "valid"), Output("patch_name", "invalid")],
             Input("patch_name", "value"))(validate_name)

# Function to handle the upload of a .tsl file.
def handle_upload(contents):
    context = dash.callback_context
    if context.triggered_id is None:
        return dash.no_update

    # If we can't upload for some reason, just skip and we will display an error toast.
    glbl = [dash.no_update] * len(context.outputs_grouping[0])
    p1 = [dash.no_update] * len(context.outputs_grouping[1])
    p2 = [dash.no_update] * len(context.outputs_grouping[2])
    show_success = dash.no_update
    show_err = dash.no_update
    try:
        ctype, cstr = contents.split(",", maxsplit=1)
        bstr = base64.b64decode(cstr)
        buf = io.StringIO(bstr.decode("utf-8"))
        live_set = sl2.read_tsl(buf)
        # TODO: Handle patches within a liveset.
        params = live_set.data[0][0].paramSet
        p1 = params.slicer_1.to_db_list()
        p2 = params.slicer_2.to_db_list()
        glbl = [live_set.name, params.com.string, live_set.formatRev, live_set.device]
        show_success = True
    except:
        show_err = True
    return glbl, p1, p2, show_err, show_success
# Callback for uploading a .tsl file.
glbl_outputs = [Output(lsp, "value") for lsp in ["ls_name", "patch_name", "ls_formatrev", "ls_device"]]
c1_outputs = [Output(sl, "value") for sl in slicer_c1_params + slicer_c1_slider_ids]
c2_outputs = [Output(sl, "value") for sl in slicer_c2_params + slicer_c2_slider_ids]
app.callback([glbl_outputs,
              c1_outputs,
              c2_outputs,
              Output("err_toast", "is_open"),
              Output("success_toast", "is_open")],
             [Input("upload", "contents")])(handle_upload)

# Function to handle the download of a .tsl file
def handle_download(_, glbl_p, c1_p, c2_p):
    context = dash.callback_context
    if context.triggered_id is None:
        return dash.no_update
    # Make a parameter object and add in the parameters
    param_set = sl2.ParamSet()
    param_set.slicer_1 = [int(x) for x in c1_p]
    param_set.slicer_2 = [int(x) for x in c2_p]
    param_set.com.string = glbl_p[0]
    # Make a patch object with our single paramSet.
    patch = sl2.Patch(paramSet=param_set)
    # Create a live set object using live set arguments and the single Patch object.
    ls_args = glbl_p[1:] + [[[patch]]]
    live_set = sl2.LiveSet(*ls_args)
    # Convert the live set to JSON string.
    out_json = json.dumps(live_set.dict(), separators=(',', ':'))
    # Return the JSON output.
    return dict(content=out_json, filename="custom_patch.tsl")
# Callback for downloading a .tsl file.
glbl_state = [State(lsp, "value") for lsp in ["patch_name", "ls_name", "ls_formatrev", "ls_device"]]
c1_state = [State(sl, "value") for sl in slicer_c1_params + slicer_c1_slider_ids]
c2_state = [State(sl, "value") for sl in slicer_c2_params + slicer_c2_slider_ids]
app.callback(Output("download", "data"),
             [Input("download_button", "n_clicks")],
             [glbl_state, c1_state, c2_state])(handle_download)

# Function to set which sliders are disabled based on
# the channel enable flag, the step number, and the pattern flag
def disable_channels(enable, step_num, pattern, effect):
    # Step number flag
    step_num = int(step_num)
    step_num_flag = np.full(N_CHANNELS, False)
    for v in slicer.STEP_NUMBER:
        if step_num == v.value:
            d_val = int(v.name.replace("STEP_", ""))
            step_num_flag = np.array([False] * d_val + [True] * (N_CHANNELS - d_val))
            break
    # Pattern flag works just like enable
    # pattern = int(pattern)
    # Check if effect is set to anything other than pitch.
    effect = int(effect)
    # If so, we need to disable all pitch_shift sliders.
    if effect != slicer.FX_TYPE.PITCH:
        pitch_flag = np.array([elem["id"].startswith("pitch_shift") for elem in dash.callback_context.outputs_list])
    else:
        pitch_flag = False
    return (np.tile(step_num_flag, N_SLIDER_GROUPS) | (not enable) | pitch_flag).tolist()
# Callback to disable the appropriate sliders depending on user's settings.
app.callback([Output(c1_t, "disabled") for c1_t in slicer_c1_slider_ids],
             [Input("c1_enable", "value"),
              Input("c1_step_num", "value"),
              Input("c1_pattern", "value"),
              Input("c1_effect", "value")])(disable_channels)

app.callback([Output(c2_t, "disabled") for c2_t in slicer_c2_slider_ids],
             [Input("c2_enable", "value"),
              Input("c2_step_num", "value"),
              Input("c2_pattern", "value"),
              Input("c2_effect", "value")])(disable_channels)

#################
# Help Tooltips #
#################
def modal_open(*args):
    if dash.callback_context.triggered_id is None:
        return dash.no_update
    return True
# We have duplicate tooltip icons for each channel, but we will open the same modal for both so we strip out the
# channel identifier in the id (if it exists).
cmatch = re.compile("_c\d+_")
[app.callback(Output(f"{name}_modal","is_open"),[Input(name,"n_clicks")])(modal_open) for name in glbl_tooltips]
[app.callback(Output(f"{cmatch.sub('_',grp[0])}_modal","is_open"),
              [Input(name,"n_clicks") for name in grp])(modal_open) for grp in channel_tooltips]

##############################
# Local Server (Development) #
##############################
if __name__ == "__main__":
    app.run_server()
