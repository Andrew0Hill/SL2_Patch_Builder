from ..utils import ParamArray


class BeatParamArray(ParamArray):
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

