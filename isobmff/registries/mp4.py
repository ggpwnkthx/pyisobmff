# File: libs/utils/isobmff/registries/mp4.py

from . import Registry
from ..atoms import *

MP4 = Registry(types=[Atom])
MP4["ftyp"] = TypeAtom
MP4["styp"] = TypeAtom
MP4["free"] = RawAtom
MP4["skip"] = RawAtom
MP4["mdat"] = RawAtom
MP4["mvhd"] = MvhdAtom
MP4["tkhd"] = TkhdAtom
MP4["elst"] = ElstAtom
