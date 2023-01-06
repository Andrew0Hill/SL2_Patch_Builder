import json
import numpy as np
from typing import List
from dataclasses import dataclass
from .params import SlicerParamArray
from .consts import *


class ParamSet(object):

    def __init__(self, **kwargs):
        self._storage = {key: np.array(val) for key, val in kwargs.items()}

        self._slicer_1 = SlicerParamArray(self._storage["PATCH%SLICER(1)"])
        self._slicer_2 = SlicerParamArray(self._storage["PATCH%SLICER(2)"])

    @property
    def slicer_1(self):
        return self._slicer_1

    @property
    def slicer_2(self):
        return self._slicer_2

    def json(self) -> dict:
        pass


@dataclass
class Memo:
    memo: str
    isToneCentralPatch: bool


@dataclass
class Patch(object):
    memo: Memo
    paramSet: ParamSet


class LiveSet(object):

    def __init__(self, name: str, formatRev: str, device: str, data: List[List[ParamSet]]):
        self._name: str = name
        self._formatRev: str = formatRev
        self._device: str = device
        self._data: List[List[ParamSet]] = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def formatRev(self):
        return self._formatRev

    @property
    def device(self):
        return self._device

    @property
    def data(self):
        return self._data

    @staticmethod
    def from_tsl(filename: str):
        return Loader.load(filename)

class Loader(object):
    _KEY_TO_CLASS = {PARAM_SET_KEYS: ParamSet,
                     PATCH_KEYS: Patch,
                     MEMO_KEYS: Memo,
                     LIVE_SET_KEYS: LiveSet}

    @staticmethod
    def _object_hook_dispatch(obj):
        """Accepts a dictionary and calls the correct class based on keys."""
        parsed_keys = frozenset(obj.keys())

        cls = Loader._KEY_TO_CLASS.get(parsed_keys)
        if cls is not None:
            return cls(**obj)

        raise RuntimeError(f"Unable to find a matching class for parsed dictionary '{obj}'")

    @staticmethod
    def load(filename:str):
        with open(filename, "r") as f:
            obj = json.load(f, object_hook=Loader._object_hook_dispatch)
        return obj
