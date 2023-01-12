from ..utils import ParamArray


class ParaEQParamArray(ParamArray):
    _enable = 0
    _param_1 = 1
    _param_2 = 2
    _param_3 = 3
    _param_4 = 4
    _param_5 = 5
    _param_6 = 6
    _param_7 = 7
    _param_8 = 8
    _param_9 = 9
    _param_10 = 10
    _param_11 = 11
    _param_12 = 12

    @property
    def enable(self):
        return self._enable

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

    @property
    def param_6(self):
        return self[self._param_6]

    @param_6.setter
    def param_6(self, v):
        self[self._param_6] = v

    @property
    def param_7(self):
        return self[self._param_7]

    @param_7.setter
    def param_7(self, v):
        self[self._param_7] = v

    @property
    def param_8(self):
        return self[self._param_8]

    @param_8.setter
    def param_8(self, v):
        self[self._param_8] = v

    @property
    def param_9(self):
        return self[self._param_9]

    @param_9.setter
    def param_9(self, v):
        self[self._param_9] = v

    @property
    def param_10(self):
        return self[self._param_10]

    @param_10.setter
    def param_10(self, v):
        self[self._param_10] = v

    @property
    def param_11(self):
        return self[self._param_11]

    @param_11.setter
    def param_11(self, v):
        self[self._param_11] = v
