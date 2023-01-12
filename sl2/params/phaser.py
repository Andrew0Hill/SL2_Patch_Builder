from ..utils import ParamArray


class PhaserParamArray(ParamArray):
    _enable = 0
    _phaser_type = 1
    _param_2 = 2
    _param_3 = 3
    _param_4 = 4
    _param_5 = 5
    _param_6 = 6
    _param_7 = 7
    _param_8 = 8
    _param_9 = 9

    @property
    def enable(self):
        return self[self._enable]

    @enable.setter
    def enable(self, v):
        self[self._enable] = v

    @property
    def phaser_type(self):
        return self[self._phaser_type]

    @phaser_type.setter
    def param_1(self, v):
        self[self._phaser_type] = v

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
