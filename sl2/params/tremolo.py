from .array import ParamArray


class TremoloParamArray(ParamArray):
    _enable = 0
    _param_1 = 1
    _param_2 = 2
    _param_3 = 3
    _param_4 = 4
    _param_5 = 5

    @property
    def enable(self):
        return self[self._enable]

    @enable.setter
    def enable(self, v):
        self[self._enable] = v

    @property
    def param_1(self):
        return self[self._param_1]

    @param_1.setter
    def param_1(self, v):
        self[self._param_1] = v

    @property
    def param_2(self):
        return self[self._param_2]

    @param_2.setter
    def param_2(self, v):
        self[self._param_2] = v

    @property
    def param_3(self):
        return self[self._param_3]

    @param_3.setter
    def param_3(self, v):
        self[self._param_3] = v

    @property
    def param_4(self):
        return self[self._param_4]

    @param_4.setter
    def param_4(self, v):
        self[self._param_4] = v

    @property
    def param_5(self):
        return self[self._param_5]

    @param_5.setter
    def param_5(self, v):
        self[self._param_5] = v
