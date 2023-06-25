"""
File: isobmff/box/segment.py

Contains all the classes specified in section 8.16 of ISO/IEC 14496-12:2015
"""
from . import BOX_TYPES, Box, FullBox, FileTypeBox
import functools
import typing


class RestrictedSchemeInfoBox(Box):
    pass


class SegmentIndexBox(FullBox):
    # Not implemented
    pass


class SubsegmentIndexBox(FullBox):
    # Not implemented
    pass


class ProducerReferenceTimeBox(FullBox):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        "styp": FileTypeBox,  # 8.16.2
        # "sidx": SegmentIndexBox,  # 8.16.3
        # "ssix": SubsegmentIndexBox,  # 8.16.4
        # "prft": ProducerReferenceTimeBox,  # 8.16.5
    }
)
