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
MP4["mdhd"] = MdhdAtom
MP4["hdlr"] = HdlrAtom
MP4["vmhd"] = VmhdAtom
MP4["dref"] = DrefAtom
MP4["stsd"] = StsdAtom
MP4["stts"] = SttsAtom
MP4["stss"] = StssAtom
MP4["ctts"] = CttsAtom
MP4["stsc"] = StscAtom
MP4["stsz"] = StszAtom
MP4["stco"] = StcoAtom
MP4["sgpd"] = SgpdAtom
MP4["sbgp"] = SbgpAtom
MP4["meta"] = FullAtom