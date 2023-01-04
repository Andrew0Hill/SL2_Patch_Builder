from patch import LiveSet,Patch,Memo,ParamSet

_PARAM_SET_KEYS = {"PATCH%COM",
                   "PATCH%SLICER(1)",
                   "PATCH%SLICER(2)",
                   "PATCH%COMP",
                   "PATCH%DIVIDER",
                   "PATCH%PHASER(1)",
                   "PATCH%PHASER(2)",
                   "PATCH%FLANGER(1)",
                   "PATCH%FLANGER(2)",
                   "PATCH%TREMOLO(1)",
                   "PATCH%TREMOLO(2)",
                   "PATCH%OVERTONE(1)",
                   "PATCH%OVERTONE(2)",
                   "PATCH%MIXER",
                   "PATCH%NS",
                   "PATCH%PEQ",
                   "PATCH%BEAT"}

_SLICER_PATCH_KEYS = {"memo", "paramSet"}

_MEMO_KEYS = {"memo", "isToneCentralPatch"}

_LIVE_SET_KEYS = {"name", "formatRev", "device", "data"}


def _object_hook_dispatch(dict):
    """Accepts a dictionary and calls the correct class based on keys."""
    dict_keys = set(dict.keys())
    if dict_keys == _MEMO_KEYS:
        return Memo(**dict)
    elif dict_keys == _SLICER_PATCH_KEYS:
        return Patch(**dict)
    elif dict_keys == _LIVE_SET_KEYS:
        return LiveSet(**dict)
    elif dict_keys == _PARAM_SET_KEYS:
        # ParamSet requires special behavior for two reasons:
        # 1. The keys of ParamSet contain invalid characters like % which cannot be used as an attribute name.
        # 2. We want to implement a special wrapping layer around the Hex arrays, so that reading and writing them
        #    is seamless.
        return ParamSet(dict)
    else:
        raise RuntimeError(f"Unable to find a matching class for parsed dictionary '{dict}'")
