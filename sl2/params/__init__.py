import numpy as np
from slicer import SlicerParamArray
from com import ComParamArray
from phaser import PhaserParamArray
from flanger import FlangerParamArray
from comp import CompParamArray
from ns import NSParamArray
from overtone import OvertoneParamArray
from peq import ParaEQParamArray
from tremolo import TremoloParamArray
from mixer import MixerParamArray
from beat import BeatParamArray
from divider import DividerParamArray

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