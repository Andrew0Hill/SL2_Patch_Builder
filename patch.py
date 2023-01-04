from dataclasses import dataclass
from utils import hex_to_str,str_to_hex,hex_to_int,int_to_hex
from typing import List, Dict, Optional, TypedDict
import json

class JSONBackedData:

    def __init__(self,key):
        """
        :param key: The key inside the JSON backing object which stores this parameter
        """
        self.key = key

    def __get__(self, instance, owner):
        return instance._json[self.key]

    def __set__(self, instance, value):
        raise AttributeError
        #instance._json[self.key] = value

# class JSONBackedSlice(object):
#
#     def __init__(self,name: str,a_slice: slice):
#         self.name = name
#         self.slice = a_slice
#
#     def __get__(self, instance, owner):
#         return getattr(instance,self.name)
#
#     def __set__(self, instance, value):
#         tmp_arr = getattr(instance,self.name)
#         tmp_arr[self.slice] = value
#         setattr(instance,self.name,tmp_arr)

class ParamArray(list):
    
    def __init__(self,iterable,to_func,from_func):
        super(ParamArray, self).__init__(iterable)
        self.to_func = to_func
        self.from_func = from_func
    
    def __getitem__(self, i):
        if type(i) == slice:
            r_val = [self.from_func(r) for r in list.__getitem__(self,i)]
        else:
            r_val = self.from_func(list.__getitem__(self,i))
        return r_val

    def __setitem__(self, key, value):
        if type(key) == slice:
            t_val = [self.to_func(v) for v in value]
        else:
            t_val = self.to_func(value)
        list.__setitem__(self,key,t_val)

    def __delitem__(self, key):
        raise NotImplementedError

    def append(self, __object) -> None:
        raise NotImplementedError

    def clear(self) -> None:
        raise NotImplementedError

    def extend(self, __iterable) -> None:
        raise NotImplementedError

class SlicerParams(ParamArray):

    @property
    def PATTERN(self):
        return self[0]

    @PATTERN.setter
    def PATTERN(self, v):
        self[0] = v

    @property
    def ON_OFF(self):
        return self[1]

    @ON_OFF.setter
    def ON_OFF(self, v):
        if type(v) is bool:
            v = int(v)
        elif v not in [0,1]:
            raise ValueError("ON_OFF should only take a value of 0 or 1.")
        self[1] = v


class ParamSet(object):

    # Name for Patch/ParamSet
    COM = JSONBackedData("PATCH%COM")
    SLICER_1 = JSONBackedData("PATCH%SLICER(1)")
    SLICER_2 = JSONBackedData("PATCH%SLICER(2)")
    COMP = JSONBackedData("PATCH%COMP")
    DIVIDER = JSONBackedData("PATCH%DIVIDER")
    PHASER_1 = JSONBackedData("PATCH%PHASER(1)")
    PHASER_2 = JSONBackedData("PATCH%PHASER(2)")
    FLANGER_1 = JSONBackedData("PATCH%FLANGER(1)")
    FLANGER_2 = JSONBackedData("PATCH%FLANGER(2)")
    TREMOLO_1 = JSONBackedData("PATCH%TREMOLO(1)")
    TREMOLO_2 = JSONBackedData("PATCH%TREMOLO(2)")
    OVERTONE_1 = JSONBackedData("PATCH%OVERTONE(1)")
    OVERTONE_2 = JSONBackedData("PATCH%OVERTONE(2)")
    MIXER = JSONBackedData("PATCH%MIXER")
    NS = JSONBackedData("PATCH%NS")
    PEQ = JSONBackedData("PATCH%PEQ")
    BEAT = JSONBackedData("PATCH%BEAT")

    """Class to hold parameters for a ParamSet."""
    def __init__(self, obj: dict):
        upd_obj = self.__convert_arrays(obj)
        self._json = upd_obj

    @staticmethod
    def __convert_arrays(obj):
        upd_obj = {}
        for key, p_arr in obj.items():

            if key == "PATCH%COM":
                to_func = str_to_hex
                from_func = hex_to_str
            else:
                to_func = int_to_hex
                from_func = hex_to_int

            if key == "PATCH%SLICER(1)":
                upd_obj[key] = SlicerParams(p_arr,to_func=to_func,from_func=from_func)
            else:
                upd_obj[key] = ParamArray(p_arr, to_func=to_func, from_func=from_func)
        return upd_obj

@dataclass
class Memo:
    memo: str
    isToneCentralPatch: bool

@dataclass
class Patch(object):
    memo: Memo
    paramSet: ParamSet

@dataclass
class LiveSet(object):
    name: str
    formatRev: str
    device: str
    data: List[List[ParamSet]]

if __name__ == "__main__":
    from loader import _object_hook_dispatch

    with open("default_patch.tsl", "r") as f:
        tsl_file = json.load(f,object_hook=_object_hook_dispatch)

    print("Here!")