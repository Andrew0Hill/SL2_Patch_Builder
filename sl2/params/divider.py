from .array import ParamArray
from enum import IntEnum

class PARAM_1(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3

class PARAM_2(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_8 = 8
    VALUE_9 = 9

class DividerParamArray(ParamArray):
    _param_1 = 0
    _param_2 = 1

    @property
    def param_1(self):
        return self._param_1

    @param_1.setter
    def param_1(self, v):
        self[self._param_1] = v

    @property
    def param_2(self):
        return self[self._param_2]

    @param_2.setter
    def param_2(self, v):
        self[self._param_2] = v

    def to_db_list(self) -> list:
        rv: list = self.tolist()

        rv[self._param_1] = str(rv[self._param_1])
        rv[self._param_2] = str(rv[self._param_2])

        return rv
