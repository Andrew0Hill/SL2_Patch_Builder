from dash import html

# Types of slider for each channel
SLIDER_TYPES = [("step_length", {"min": 0, "max": 100, "value": 50}),
                ("step_level", {"min": 0, "max": 100, "value": 100}),
                ("band_pass", {"min": 0, "max": 6, "value": 0}),
                ("effect_level", {"min": 0, "max": 100, "value": 50}),
                ("pitch_shift", {"min": 0, "max": 24, "value": 12})]

# Number of slider groups
N_SLIDER_GROUPS = len(SLIDER_TYPES)

# Number of sliders per group
N_CHANNELS = 24

# General arguments for each slider
SLIDER_ARGS = {"tooltip": {"always_visible": True, "placement": "bottom"},
               "vertical": True,
               "verticalHeight": 200,
               "marks": None,
               "dots": False,
               # "persistence": True,
               "step": 1}

def make_tooltip(id):
    tt = html.A(id=id,
                className="bi bi-question-circle",
                style={"margin-left": "5px",
                       "color": "info"})
    return tt


def opts_from_enum(enum):
    return [{"label": e.name, "value": e.value} for e in enum]
# Get the number of slider groups

# The number of sliders per group


