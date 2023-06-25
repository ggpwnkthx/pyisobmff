"""
File: isobmff/box/movie/post_decoder.py

Contains all the classes specified in section 8.1 of ISO/IEC 14496-12:2015
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class RestrictedSchemeInfoBox(Box):
    pass


class StereoVideoBox(FullBox, ChildlessBox):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        "rinf": RestrictedSchemeInfoBox,  # 8.15.3
        # "stvi": StereoVideoBox,  # 8.15.4
    }
)
