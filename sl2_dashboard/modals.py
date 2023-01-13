import dash_bootstrap_components as dbc
from dash import html

######################
# Toast Declarations #
######################

# Error toast is displayed when a file upload fails for some reason
err_toast = dbc.Toast("Unable to parse .tsl file!",
                      id="err_toast",
                      header="File Error",
                      is_open=False,
                      dismissable=True,
                      duration=3000,
                      icon="danger",
                      style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 999})

# Success toast is displayed when a file upload is successful, to let the user know that their file has been uploaded.
success_toast = dbc.Toast("Loaded .tsl file sucessfully!",
                          id="success_toast",
                          header="File Upload Successful",
                          is_open=False,
                          dismissable=True,
                          duration=1500,
                          icon="success",
                          style={"position": "fixed", "top": 66, "right": 10, "width": 350, "zIndex": 999})

all_toasts = [err_toast,success_toast]

###########################
# Modal View Declarations #
###########################

# Disclaimer modal shows up when the site is opened for the first time, to explain the tool and current limitations.
disclaimer_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("About This Tool")),
    dbc.ModalBody([
        html.P("This tool can be used to create and edit the .tsl patch files exported for the"
               " SL-2 Slicer effect pedal."),
        html.P("The tool is currently under development, so many parameters (including most of the non-slicer effect"
               " parameters) do not have meaningful names yet as we are unsure of their function."),
        html.P("You can click on the help tooltips next to each parameter to view the information (if any) we currently"
               " have about that parameter."),
        html.P("As we learn more about the functions of the unlabeled parameters, we will update the names, tooltip"
               " descriptions, and permissible value ranges."),
        html.P("If you encounter issues with the tool, have information about one of the parameters,"
               " or just have a suggestion, please open an issue on GitHub using the link in the header."),
        html.P("Thanks for trying out the tool, and happy slicing!")
    ]),
    dbc.ModalFooter(
            html.P("This tool is licensed under the MIT license, and provided as-is without any warranty. This tool"
                   " and its creators are not affiliated or endorsed in any way by BOSS or Roland Corporation.",
                   style={"font-size":"x-small","align":"left"})
    )
], is_open=True)

# Live set tooltip modal explains the live set name
live_set_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Live Set Name")),
    dbc.ModalBody([
        html.P("Sets the 'name' property of the .tsl file."),
        html.B("Note:"),
        html.P(" Currently, importing a .tsl file into Tone Studio sets 'name' property to the filename of the .tsl "
               " file you are importing, so this field will be overwritten when importing into Tone Studio.")
    ])
], id="ls_name_tt_modal")

# Patch name modal
patch_name_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Patch Name")),
    dbc.ModalBody([
        html.P("Sets the name for the patch, which is displayed in Tone Studio."),
        html.B("Note:"),
        html.P(" This name is only displayed in Tone Studio. The PATCH%COM array (and therefore the Patch Name value)"
               " is limited to 20 characters.")
    ])
], id="patch_name_tt_modal")

# Format rev modal
format_rev_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Format Rev")),
    dbc.ModalBody([
        html.P("Sets the 'formatRev' of the .tsl file (?). For now this value is "
               "only allowed to be '0001'.")
    ])
], id="format_rev_tt_modal")

# Device modal
device_rev_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Device")),
    dbc.ModalBody([
        html.P("Sets the 'device' field in the .tsl file."),
        html.B("Note:"),
        html.P("This is locked to 'SL-2' for now.")
    ])
], id="device_tt_modal")

# Pattern modal
pattern_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Pattern Select")),
    dbc.ModalBody([
        html.P("Sets the pattern preset for the patch."),
        html.P("This can be a number of preset values, or 'USER' to enable a custom slicer patch."),
        html.B("Note:"),
        html.P("This value is locked to 'USER' for now since other values ignore the values in the parameter arrays.")
    ])
], id="slicer_pattern_tt_modal")

# Enable modal
enable_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Enable")),
    dbc.ModalBody([
        html.P("Enables or disables signal processing for this channel."),
        html.B("Note:"),
        html.P("Disabling the channel will also disable the sliders for all parameter arrays in the channel.")
    ])
], id="slicer_enable_tt_modal")

# Effect Type Modal
effect_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Effect Type")),
    dbc.ModalBody([
        html.P("Sets the type of effect used at each step."),
        html.P("If the value is set to 'PITCH', per-step pitch control is available in the Pitch Shift parameter"
               " array."),
        html.P("(If the value is anything other than 'PITCH', the Pitch Shift sliders are disabled since they have no "
               " effect in other modes.)"),
        html.B("Note:"),
        html.P("The effect names may not be completely correct, and these effects may not sound good since their"
               " configuration parameters are not available in the tool yet.")
    ])
], id="slicer_effect_tt_modal")

# Step Number Modal
step_number_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Step Number")),
    dbc.ModalBody([
        html.P("Divides each measure into this number equal steps, where each step can be modified using the"
               " Parameter Array sliders. "),
        html.B("Note:"),
        html.P("Choosing a value < STEP_24 will disable some sliders to indicate that these values will be ignored.")
    ])
], id="slicer_step_num_tt_modal")

# Parameter Arrays Modal
param_array_modal = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Parameter Arrays")),
    dbc.ModalBody([
        html.H5("Step Length"),
        html.P("Sets the length for each step in the pattern."),
        html.P("Values are [0-100] and represent the length of time audio is heard for this step (i.e. value=50 means"
               " that sound will be heard for 50% of the length of this step."),
        html.P("A value of 0 mutes sound completely, and a value of 100 means audio plays uninterrupted for"
               " this step."),
        html.H5("Step Level"),
        html.P("Values are [0-100] and represent relative volume/level of this step."),
        html.H5("Band Pass"),
        html.P("Sets a preset band pass filter value on each step."),
        html.P("Values are [0-6]. A value of 0 disables the filter, and values 1-6 apply a band pass filter."),
        html.H5("Effect Level"),
        html.P("Sets the level of the effect sound specified by 'Effect Type' for this step."),
        html.P("Values are [0-100] and represent relative level at each step."),
        html.H5("Pitch Shift"),
        html.P("Sets the amount of pitch shifting applied to this step."),
        html.P("Values are [0,24] where 0 is one octave below, and 24 is one octave above. Default is 12 (no shift)."),
        html.B("Note:"),
        html.P("Choosing a value other than 'PITCH' for Effect Type will disable these sliders, since they have"
               " no effect for other Effect Type modes.")
    ])
], id="slicer_param_arr_tt_modal")

all_modals = [disclaimer_modal,
              live_set_modal,
              patch_name_modal,
              format_rev_modal,
              device_rev_modal,
              pattern_modal,
              enable_modal,
              effect_modal,
              step_number_modal,
              param_array_modal]