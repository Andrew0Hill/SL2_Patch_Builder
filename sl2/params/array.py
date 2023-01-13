import numpy as np

class ParamArray(np.ndarray):

    def __new__(cls, arr):
        if any(type(x) != int for x in arr):
            hex_arr = [int(x,16) for x in arr]
        else:
            hex_arr = arr
        obj = np.asarray(hex_arr,dtype=np.int8).view(cls)
        return obj

    def json(self):
        return [hex(x).replace("0x","").rjust(2,"0").upper() for x in self]

    def to_db_list(self) -> list:
        return self.tolist()