from .array import ParamArray

class ComParamArray(ParamArray):

    # Max length for PATCH%COM is 16.
    _LENGTH = 16

    @property
    def string(self):
        tmp_s = "".join([chr(x) for x in self])
        return tmp_s.rstrip()

    @string.setter
    def string(self, v: str):
        if not v.isascii():
            return
        # Concat to 16 characters, then pad with spaces.
        tmp_s = v[:self._LENGTH].upper().ljust(self._LENGTH)
        self[:self._LENGTH] = [ord(s) for s in tmp_s]