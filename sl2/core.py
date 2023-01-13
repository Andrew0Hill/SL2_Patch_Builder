import json
import numpy as np
from importlib.resources import is_resource,read_text
from typing import List
from dataclasses import dataclass
from typing import Optional
from .params import *
from .consts import *
from . import defaults
import copy

class ParamSet(object):

    _DEFAULTS = "param_set.json"

    def __init__(self, **kwargs):
        # Load the defaults, so that we provide default values for anything that isn't passed in.
        self._storage = ParamSet._load_defaults()
        # Make everything a generic ParamArray for now, we will create more specific views using subclasses
        # of ParamArray below.
        np_kwargs = {k:ParamArray(v) for k,v in kwargs.items()}
        self._storage.update(np_kwargs)
        # Get views of specific values we are interested in.
        self._com = self._storage["PATCH%COM"].view(ComParamArray)
        self._slicer_1 = self._storage["PATCH%SLICER(1)"].view(SlicerParamArray)
        self._slicer_2 = self._storage["PATCH%SLICER(2)"].view(SlicerParamArray)
        self._comp = self._storage["PATCH%COMP"].view(CompParamArray)
        self._divider = self._storage["PATCH%DIVIDER"].view(DividerParamArray)
        self._phaser_1 = self._storage["PATCH%PHASER(1)"].view(PhaserParamArray)
        self._phaser_2 = self._storage["PATCH%PHASER(2)"].view(PhaserParamArray)
        self._flanger_1 = self._storage["PATCH%FLANGER(1)"].view(FlangerParamArray)
        self._flanger_2 = self._storage["PATCH%FLANGER(2)"].view(FlangerParamArray)
        self._tremolo_1 = self._storage["PATCH%TREMOLO(1)"].view(TremoloParamArray)
        self._tremolo_2 = self._storage["PATCH%TREMOLO(2)"].view(TremoloParamArray)
        self._overtone_1 = self._storage["PATCH%OVERTONE(1)"].view(OvertoneParamArray)
        self._overtone_2 = self._storage["PATCH%OVERTONE(2)"].view(OvertoneParamArray)
        self._mixer = self._storage["PATCH%MIXER"].view(MixerParamArray)
        self._ns = self._storage["PATCH%NS"].view(NSParamArray)
        self._peq = self._storage["PATCH%PEQ"].view(ParaEQParamArray)
        self._beat = self._storage["PATCH%BEAT"].view(BeatParamArray)

    @staticmethod
    def _load_defaults():
        if not is_resource(defaults,ParamSet._DEFAULTS):
            raise RuntimeError(f"Can't find default file {ParamSet._DEFAULTS} in resources!")

        rfile = read_text(defaults, "param_set.json")
        json_defaults = json.loads(rfile)

        return {k:ParamArray(v) for k,v in json_defaults.items()}

    @property
    def com(self):
        return self._com

    @property
    def slicer_1(self):
        return self._slicer_1

    @slicer_1.setter
    def slicer_1(self,v):
        self._slicer_1[:] = v

    @property
    def slicer_2(self):
        return self._slicer_2

    @slicer_2.setter
    def slicer_2(self,v):
        self._slicer_2[:] = v
    
    @property
    def comp(self):
        return self._comp
    
    @comp.setter
    def comp(self,v):
        self._comp[:] = v

    @property
    def divider(self):
        return self._divider

    @divider.setter
    def divider(self,v):
        self._divider[:] = v

    @property
    def phaser_1(self):
        return self._phaser_1
    
    @phaser_1.setter
    def phaser_1(self,v):
        self._phaser_1[:] = v

    @property
    def phaser_2(self):
        return self._phaser_2

    @phaser_2.setter
    def phaser_2(self, v):
        self._phaser_2[:] = v

    @property
    def flanger_1(self):
        return self._flanger_1

    @flanger_1.setter
    def flanger_1(self, v):
        self._flanger_1[:] = v

    @property
    def flanger_2(self):
        return self._flanger_2

    @flanger_2.setter
    def flanger_2(self, v):
        self._flanger_2[:] = v
        
    @property
    def tremolo_1(self):
        return self._tremolo_1

    @tremolo_1.setter
    def tremolo_1(self, v):
        self._tremolo_1[:] = v

    @property
    def tremolo_2(self):
        return self._tremolo_2

    @tremolo_2.setter
    def tremolo_2(self, v):
        self._tremolo_2[:] = v
        
    @property
    def overtone_1(self):
        return self._overtone_1

    @overtone_1.setter
    def overtone_1(self, v):
        self._overtone_1[:] = v

    @property
    def overtone_2(self):
        return self._overtone_2

    @overtone_2.setter
    def overtone_2(self, v):
        self._overtone_2[:] = v

    @property
    def mixer(self):
        return self._mixer

    @mixer.setter
    def mixer(self,v):
        self._mixer[:] = v

    @property
    def ns(self):
        return self._ns

    @ns.setter
    def ns(self,v):
        self._ns[:] = v

    @property
    def peq(self):
        return self._peq

    @peq.setter
    def peq(self,v):
        self._peq[:] = v

    @property
    def beat(self):
        return self._beat

    @beat.setter
    def beat(self,v):
        self._beat[:] = v

    def dict(self) -> dict:
        return {k:v.json() for k,v in self._storage.items()}

class Memo:
    def __init__(self, memo: str = "", isToneCentralPatch: bool = True):
        self.memo = memo
        self.isToneCentralPatch = isToneCentralPatch

    def dict(self):
        return self.__dict__

class Patch:
    def __init__(self, paramSet: ParamSet, memo: Optional[Memo] = None):
        self.memo: Memo = memo if memo is not None else Memo()
        self.paramSet: ParamSet = paramSet

    def dict(self):
        return {"memo":self.memo.dict(),
                "paramSet":self.paramSet.dict()}

class LiveSet(object):

    def __init__(self, name: str, formatRev: str, device: str, data: List[List[ParamSet]]):
        self._name: str = name
        self._formatRev: str = formatRev
        self._device: str = device
        self._data: List[List[ParamSet]] = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = v

    @property
    def formatRev(self):
        return self._formatRev

    @property
    def device(self):
        return self._device

    @property
    def data(self):
        return self._data

    def to_json(self):
        return json.dumps(self, default=lambda x: x.dict())

    def dict(self):
        json_rep = {"name":self.name,
                    "formatRev":self.formatRev,
                    "device":self.device,
                    "data":[[data.dict() for data in self.data[0]]]}
        return json_rep


_KEY_TO_CLASS = {PARAM_SET_KEYS: ParamSet,
                 PATCH_KEYS: Patch,
                 MEMO_KEYS: Memo,
                 LIVE_SET_KEYS: LiveSet}

def _object_hook_dispatch(obj):
    """Accepts a dictionary and calls the correct class based on keys."""
    parsed_keys = frozenset(obj.keys())

    cls = _KEY_TO_CLASS.get(parsed_keys)
    if cls is not None:
        return cls(**obj)

    raise RuntimeError(f"Unable to find a matching class for parsed dictionary '{obj}'")

def read_tsl(file_or_name):
    if type(file_or_name) is str:
        file_obj = open(file_or_name,"r")
    else:
        file_obj = file_or_name

    obj = json.load(file_obj, object_hook=_object_hook_dispatch)

    file_obj.close()
    return obj
