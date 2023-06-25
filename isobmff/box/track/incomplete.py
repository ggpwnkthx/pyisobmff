"""
File: isobmff/box/file/track/sub.py

Contains all the classes specified in section 8.17 of ISO/IEC 14496-12:2015
"""
from .. import BOX_TYPES, Box


class IncompleteAVCSampleEntry(Box):  # VisualSampleEntry <- SampleEntry
    pass


class CompleteTrackInfoBox(Box):
    pass


BOX_TYPES.update(
    {
        "icpv": IncompleteAVCSampleEntry,  # 8.17.2
        "cinf": CompleteTrackInfoBox,  # 8.17.3
    }
)
