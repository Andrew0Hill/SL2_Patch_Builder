import enum

import numpy as np
from enum import IntEnum
from ..params import ParamArray
from .. import defaults
from typing import Optional,List,Union
from functools import cached_property
import importlib.resources as pkg_resources

# Dynamically create this enum so we don't have 50 lines of
# PATTERN_n = n....
PATTERN = enum.IntEnum("PATTERN", {f"PATTERN_{i}":i for i in range(50)} | {"USER": 50})

class FX_TYPE(IntEnum):
    OFF = 0
    PITCH = 1
    FLANGER = 2 # ?
    PHASER = 3 # SWEEP ?
    SWEEP = 4 # PHASER ?
    FILTER = 5
    RING = 6

class STEP_NUMBER(IntEnum):
    STEP_8 = 0
    STEP_12 = 1
    STEP_16 = 2
    STEP_24 = 3

class SlicerParamArray(ParamArray):

    _pattern = 0
    _enable = 1
    _fx_type = 2
    _step_number = 3
    _step_length = slice(4, 28)
    _step_level = slice(28, 52)
    _band = slice(52, 76)
    _effect = slice(76, 100)
    _pitch = slice(100, 123)

    def to_db_list(self) -> list:
        """Special function for coverting the object to a list that can be read by the dashboard

        Note: This function just keeps the dashboard callbacks looking cleaner, and won't be useful for you if you are
        using the sl2 library directly

        :return: A list formatted for the dashboard output.
        """
        rv: list = self.tolist()

        # Pattern is converted to string
        rv[self._pattern] = str(rv[self._pattern])
        # fx_type is converted to string
        rv[self._fx_type] = str(rv[self._fx_type])
        # step_number is converted to string
        rv[self._step_number] = str(rv[self._step_number])

        return rv

    @property
    def pattern(self):
        return self[self._pattern]

    @pattern.setter
    def pattern(self, v):
        self[self._pattern] = v

    @property
    def enable(self):
        return self[self._enable]

    @enable.setter
    def enable(self, v):
        if type(v) is bool:
            v = int(v)
        elif v not in [0, 1]:
            raise ValueError("'enable' should only take a value of 0 or 1.")
        self[self._enable] = v

    @property
    def fx_type(self):
        return self[self._fx_type]

    @fx_type.setter
    def fx_type(self, v):
        self[self._fx_type] = v

    @property
    def step_number(self):
        return self[self._step_number]

    @step_number.setter
    def step_number(self, v):
        self[self._step_number] = v

    @property
    def step_length(self):
        return self[self._step_length]

    @step_length.setter
    def step_length(self, v):
        self[self._step_length] = v

    @property
    def step_level(self):
        return self[self._step_level]

    @step_level.setter
    def step_level(self, v):
        self[self._step_level] = v

    @property
    def band(self):
        return self[self._band]

    @band.setter
    def band(self,v):
        self[self._band] = v

    @property
    def effect(self):
        return self[self._effect]

    @effect.setter
    def effect(self,v):
        self[self._effect] = v

    @property
    def pitch(self):
        return self[self._pitch]

    @pitch.setter
    def pitch(self,v):
        self[self._pitch] = v
