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
from cards.beat import beat_card, beat_outputs, beat_state
from cards.compressor import compressor_card, compressor_outputs, compressor_state
from cards.divider import divider_card, divider_outputs, divider_state
from cards.file_transfer import file_transfer_card
from cards.flanger import create_flanger_channel_card
from cards.mixer import mixer_card, mixer_outputs, mixer_state
from cards.noise_supressor import noise_suppressor_card, noise_suppressor_outputs, noise_suppressor_state
from cards.overtone import create_overtone_channel_card
from cards.para_eq import para_eq_card, para_eq_outputs, para_eq_state
from cards.phaser import create_phaser_channel_card
from cards.slicer import create_slicer_channel_card
from cards.tremolo import create_tremolo_channel_card
from modals import all_modals, all_toasts
from sl2.params import slicer
from sl2_dashboard.cards.common import N_SLIDER_GROUPS, N_CHANNELS

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
slicer_c1_tts, slicer_c1_slider_ids, slicer_c1_card, slicer_c1_outputs, slicer_c1_state = create_slicer_channel_card(1)
slicer_c2_tts, slicer_c2_slider_ids, slicer_c2_card, slicer_c2_outputs, slicer_c2_state = create_slicer_channel_card(2)

phaser_c1_tts, phaser_c1_card, phaser_c1_outputs, phaser_c1_state = create_phaser_channel_card(1)
phaser_c2_tts, phaser_c2_card, phaser_c2_outputs, phaser_c2_state = create_phaser_channel_card(2)

flanger_c1_tts, flanger_c1_card, flanger_c1_outputs, flanger_c1_state = create_flanger_channel_card(1)
flanger_c2_tts, flanger_c2_card, flanger_c2_outputs, flanger_c2_state = create_flanger_channel_card(2)

tremolo_c1_tts, tremolo_c1_card, tremolo_c1_outputs, tremolo_c1_state = create_tremolo_channel_card(1)
tremolo_c2_tts, tremolo_c2_card, tremolo_c2_outputs, tremolo_c2_state = create_tremolo_channel_card(2)

overtone_c1_tts, overtone_c1_card, overtone_c1_outputs, overtone_c1_state = create_overtone_channel_card(1)
overtone_c2_tts, overtone_c2_card, overtone_c2_outputs, overtone_c2_state = create_overtone_channel_card(2)

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
    divider_card,
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
    noise_suppressor_card,
    para_eq_card,
    beat_card
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

# JSON store for uploaded data
store = dcc.Store(id="json_store")

# Final app layout
app.layout = html.Div([store, header, body])

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
    sl_1 = [dash.no_update] * len(context.outputs_grouping[1])
    sl_2 = [dash.no_update] * len(context.outputs_grouping[2])
    dv_1 = [dash.no_update] * len(context.outputs_grouping[3])
    cm_1 = [dash.no_update] * len(context.outputs_grouping[4])
    ph_1 = [dash.no_update] * len(context.outputs_grouping[5])
    ph_2 = [dash.no_update] * len(context.outputs_grouping[6])
    fl_1 = [dash.no_update] * len(context.outputs_grouping[7])
    fl_2 = [dash.no_update] * len(context.outputs_grouping[8])
    tr_1 = [dash.no_update] * len(context.outputs_grouping[9])
    tr_2 = [dash.no_update] * len(context.outputs_grouping[10])
    ov_1 = [dash.no_update] * len(context.outputs_grouping[11])
    ov_2 = [dash.no_update] * len(context.outputs_grouping[12])
    mx_1 = [dash.no_update] * len(context.outputs_grouping[13])
    ns_1 = [dash.no_update] * len(context.outputs_grouping[14])
    pq_1 = [dash.no_update] * len(context.outputs_grouping[15])
    bt_1 = [dash.no_update] * len(context.outputs_grouping[16])
    store_data = dash.no_update
    show_success = dash.no_update
    show_err = dash.no_update
    try:
        ctype, cstr = contents.split(",", maxsplit=1)
        bstr = base64.b64decode(cstr)
        buf = io.StringIO(bstr.decode("utf-8"))
        live_set = sl2.read_tsl(buf)
        # This stores all parameter data in the JSON storage object.
        # This is only necessary because some parameters cannot be modified yet, which means that they
        # would be overwritten with the default values when the file is downloaded.
        # We can avoid this by loading this JSON data as the live set, then updating the parameters that have changed.
        store_data = json.dumps(live_set.dict(), separators=(',', ':'))
        # TODO: Handle patches within a liveset.
        params = live_set.data[0][0].paramSet
        sl_1 = params.slicer_1.to_db_list()
        sl_2 = params.slicer_2.to_db_list()
        dv_1 = params.divider.to_db_list()
        cm_1 = params.comp.to_db_list()
        ph_1 = params.phaser_1.to_db_list()
        ph_2 = params.phaser_2.to_db_list()
        fl_1 = params.flanger_1.to_db_list()
        fl_2 = params.flanger_2.to_db_list()
        tr_1 = params.tremolo_1.to_db_list()
        tr_2 = params.tremolo_2.to_db_list()
        ov_1 = params.overtone_1.to_db_list()
        ov_2 = params.overtone_2.to_db_list()
        mx_1 = params.mixer.to_db_list()
        ns_1 = params.ns.to_db_list()
        pq_1 = params.peq.to_db_list()
        bt_1 = params.beat.to_db_list()
        
        glbl = [live_set.name, params.com.string, live_set.formatRev, live_set.device]

        show_success = True
    except:
        show_err = True
    return glbl, \
           sl_1, sl_2, \
           dv_1, cm_1, \
           ph_1, ph_2, \
           fl_1, fl_2, \
           tr_1, tr_2, \
           ov_1, ov_2, \
           mx_1, ns_1, pq_1, bt_1, \
           store_data, show_err, show_success
# Callback for uploading a .tsl file.
glbl_outputs = [Output(lsp, "value") for lsp in ["ls_name", "patch_name", "ls_formatrev", "ls_device"]]
app.callback([glbl_outputs,
              slicer_c1_outputs, slicer_c2_outputs,
              divider_outputs, compressor_outputs,
              phaser_c1_outputs, phaser_c2_outputs,
              flanger_c1_outputs, flanger_c2_outputs,
              tremolo_c1_outputs, tremolo_c2_outputs,
              overtone_c1_outputs, overtone_c2_outputs,
              mixer_outputs, noise_suppressor_outputs, para_eq_outputs, beat_outputs,
              Output("json_store","data"),
              Output("err_toast", "is_open"),
              Output("success_toast", "is_open")],
             [Input("upload", "contents")])(handle_upload)

# Function to handle the download of a .tsl file
def handle_download(_, glbl_p,
                    sl_1, sl_2,
                    dv_1, cm_1,
                    ph_1, ph_2,
                    fl_1, fl_2,
                    tr_1, tr_2,
                    ov_1, ov_2,
                    mx_1, ns_1, pq_1, bt_1,
                    json_str):
    context = dash.callback_context
    if context.triggered_id is None:
        return dash.no_update
    # Restore the uploaded data if it exists
    if json_str is not None:
        # Make a LiveSet from the stored JSON data.
        live_set = sl2.read_tsl(io.StringIO(json_str))
        # Patch already exists if the .tsl is valid.
        patch = live_set.data[0][0]
        # paramSet already exists as well.
        param_set = patch.paramSet
    else:
        # Make a new paramSet, Patch and LiveSet from defaults, and just update what's been changed.
        param_set = sl2.ParamSet()
        # Patch can be built using the param_set
        patch = sl2.Patch(paramSet=param_set)
        # LiveSet is built using the Patch.
        ls_args = glbl_p[1:] + [[[patch]]]
        live_set = sl2.LiveSet(*ls_args)

    # Update the parameters
    param_set.slicer_1 = [int(x) for x in sl_1]
    param_set.slicer_2 = [int(x) for x in sl_2]
    param_set.divider = [int(x) for x in dv_1]
    param_set.compressor = [int(x) for x in cm_1]
    param_set.phaser_1 = [int(x) for x in ph_1]
    param_set.phaser_2 = [int(x) for x in ph_2]
    param_set.flanger_1 = [int(x) for x in fl_1]
    param_set.flanger_2 = [int(x) for x in fl_2]
    param_set.overtone_1 = [int(x) for x in ov_1]
    param_set.overtone_2 = [int(x) for x in ov_2]
    param_set.mixer = [int(x) for x in mx_1]
    param_set.ns = [int(x) for x in ns_1]
    param_set.peq = [int(x) for x in pq_1]
    param_set.beat = [int(x) for x in bt_1]
    param_set.com.string = glbl_p[0]

    # Convert the live set to JSON string.
    out_json = json.dumps(live_set.dict(), separators=(',', ':'))
    # Return the JSON output.
    return dict(content=out_json, filename="custom_patch.tsl")
# Callback for downloading a .tsl file.
glbl_state = [State(lsp, "value") for lsp in ["patch_name", "ls_name", "ls_formatrev", "ls_device"]]
json_state = State("json_store","data")
app.callback(Output("download", "data"),
             [Input("download_button", "n_clicks")],
             [glbl_state,
              slicer_c1_state, slicer_c2_state,
              divider_state, compressor_state,
              phaser_c1_state, phaser_c2_state,
              flanger_c1_state, flanger_c2_state,
              tremolo_c1_state, tremolo_c2_state,
              overtone_c1_state, overtone_c2_state,
              mixer_state, noise_suppressor_state, para_eq_state, beat_state,
              json_state])(handle_download)

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
             [Input("slicer_c1_enable", "value"),
              Input("slicer_c1_step_num", "value"),
              Input("slicer_c1_pattern", "value"),
              Input("slicer_c1_effect", "value")])(disable_channels)

app.callback([Output(c2_t, "disabled") for c2_t in slicer_c2_slider_ids],
             [Input("slicer_c2_enable", "value"),
              Input("slicer_c2_step_num", "value"),
              Input("slicer_c2_pattern", "value"),
              Input("slicer_c2_effect", "value")])(disable_channels)

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
