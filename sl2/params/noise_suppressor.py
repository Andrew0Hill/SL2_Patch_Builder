from .array import ParamArray


class NSParamArray(ParamArray):
    _enable = 0
    _threshold = 1
    _release = 2

    @property
    def enable(self):
        return self._enable

    @enable.setter
    def enable(self, v):
        self[self._enable] = v

    @property
    def threshold(self):
        return self[self._threshold]

    @threshold.setter
    def threshold(self, v):
        self[self._threshold] = v

    @property
    def release(self):
        return self[self._release]

    @release.setter
    def release(self, v):
        self[self._release] = v
