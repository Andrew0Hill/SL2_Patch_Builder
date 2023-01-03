from utils import hex_array_to_integer, integer_array_to_hex, hex_param_name_to_str, str_param_name_to_hex
from enum import IntEnum
import numpy as np
import warnings
import json

PARAM_SET_KEYS = {"PATCH%COM",
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

class LiveSet(object):
    def __init__(self, name, data, format_rev="0001", device="SL-2"):
        self.name = name
        self.formatRev = format_rev
        self.device = device
        self.data = data

    @classmethod
    def from_json(cls, obj: dict):
        # Check that this LiveSet has a name and assign one if it doesn't
        name = obj.get("name")
        if name is None:
            name = "my_custom_liveset"
            warnings.warn(".tsl file should have a 'name' attribute in the top level, but found none! Continuing with"
                          f" default name '{name}'.")
        # Check format revision and raise a warning if it doesn't match.
        format_rev = obj.get("formatRev")
        if format_rev is None or format_rev != "0001":
            warnings.warn("This program is designed to operate on .tsl files using formatRev=0001, but this file is"
                          f" formatRev={format_rev}.")
        # Check device field and raise a warning if it doesn't match.
        device = obj.get("device")
        if device is None or device != "SL-2":
            warnings.warn("This program is designed to operate on .tsl files for the Boss SL-2 Slicer, but this file"
                          f" was generated for '{device}'.")
        # Check that there is a data field, and raise an error if it does not exist.
        data = obj.get("data")
        if data is None:
            raise RuntimeError("Unable to parse the 'data' field from this .tsl file! Exiting...")
        # Check that the data field contains a list and that the first list only contains 1 element.
        if type(data) != list:
            raise RuntimeError(f"Expected that the 'data' field would contain a list, but found {type(data)} instead,"
                               " exiting...")
        elif len(data) != 1:
            raise RuntimeError("Expected that the 'data' field would contain a list with a single element, but found"
                               f" {len(data)} elements.")

        data[0] = [SlicerPatch.from_dict(obj=patch) for patch in data[0]]

        return cls(name=name, data=data, format_rev=format_rev, device=device)

    def to_json(self, f):
        json.dump(self, f, default=lambda x: x.json())

    def json(self):
        return self.__dict__


class SlicerPatch(object):
    # Maps values in the slice array to their corresponding step values.
    _slice_map = {0: 8, 1: 12, 2: 16, 3: 24}

    def __init__(self, param_set: dict, memo: dict = None):
        self.memo = memo if memo is not None else {"memo": {"memo": "", "isToneCentralPatch": True}}
        pset_keys = set(param_set.keys())
        if pset_keys != PARAM_SET_KEYS:
            raise RuntimeError(f"'paramSet' keys do not match expected set! Expected: {PARAM_SET_KEYS},"
                               f" Found: {pset_keys}. Exiting...")

        param_set = {k: hex_param_name_to_str(v) if k == "PATCH%COM" else hex_array_to_integer(v) for k, v in
                     param_set.items()}

        self.paramSet = param_set

    @classmethod
    def from_dict(cls, obj: dict):
        """
        :param obj: A dictionary representing a userPatch parsed from JSON.
        :return: an instance of the UserPatch class
        """
        # Check that paramSet exists and is a dictionary.
        param_set = obj.get("paramSet")
        if param_set is None:
            raise RuntimeError("Unable to parse the 'paramSet' field from the .tsl file, exiting...")
        elif type(param_set) != dict:
            raise RuntimeError("Expected that the 'paramSet' field would contain a dict, but found"
                               f" {type(param_set)} instead, exiting...")
        # Memo probably doesn't matter
        memo = obj.get("memo")

        return cls(param_set=param_set, memo=memo)

    @property
    def step_length_c1(self):
        return np.array(self.paramSet["PATCH%SLICER(1)"][4:28])

    @property
    def step_level_c1(self):
        return np.array(self.paramSet["PATCH%SLICER(1)"][28:52])

    @property
    def step_number_c1(self):
        return self._slice_map[self.paramSet["PATCH%SLICER(1)"][3]]

    def json(self):
        json_dict = self.__dict__.copy()

        json_dict["paramSet"] = {k: str_param_name_to_hex(v) if k == "PATCH%COM" else integer_array_to_hex(v) for k, v
                                 in json_dict["paramSet"].items()}

        return json_dict


if __name__ == "__main__":
    with open("default_patch.tsl", "r") as f:
        tsl_file = json.load(f)

    liveset = LiveSet.from_json(tsl_file)

    with open("test_out.json", "w") as f:
        liveset.to_json(f)
