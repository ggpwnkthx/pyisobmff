"""
File: isobmff/box/file/track/sub.py

Contains all the classes specified in section 8.14 of ISO/IEC 14496-12:2015
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class SubTrack(Box):
    pass


class SubTrackInformation(FullBox, ChildlessBox):
    # Not implemented
    pass


class SubTrackDefinition(Box):
    pass


class SubTrackSampleGroupBox(FullBox):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        "strk": SubTrack,  # 8.14.3
        # "stri": SubTrackInformation,  # 8.14.4
        "strd": SubTrackDefinition,  # 8.14.5
        # "stsg": SubTrackDefinition,  # 8.14.6
    }
)
