"""
File: isobmff/box/track/sample/group.py

Contains all the classes specified in section 8.9 of ISO/IEC 14496-12:2015
"""
from ... import BOX_TYPES, FullBox
import functools
import typing


class SampleToGroupBox(FullBox):
    # Not implemented
    pass


class SampleGroupDescriptionBox(FullBox):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        # "sbgp": SampleToGroupBox,  # 8.9.2
        # "sgpd": SampleGroupDescriptionBox,  # 8.9.3
    }
)
