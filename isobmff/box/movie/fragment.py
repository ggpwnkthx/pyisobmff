"""
File: isobmff/box/movie/fragment.py

Contains all the classes specified in section 8.8 of ISO/IEC 14496-12:2015
"""
from isobmff.box.structure import Box
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class MovieExtendsBox(Box):
    pass


class MovieExtendsHeaderBox(FullBox):
    @functools.cached_property
    def fragment_duration(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")
        elif self.version == 1:
            return self.slice.subslice(start, start + 8).unpack(">Q")

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 4
        elif self.version == 1:
            return super().header_size + 8


class TrackExtendsBox(FullBox):
    @functools.cached_property
    def track_ID(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")

    @functools.cached_property
    def default_sample_description_index(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")

    @functools.cached_property
    def default_sample_duration(self) -> int:
        start = super().header_size + 8
        return self.slice.subslice(start, start + 4).unpack(">I")

    @functools.cached_property
    def default_sample_size(self) -> int:
        start = super().header_size + 12
        return self.slice.subslice(start, start + 4).unpack(">I")

    @functools.cached_property
    def default_sample_flags(self) -> int:
        start = super().header_size + 16
        return self.slice.subslice(start, start + 4).unpack(">I")

    @property
    def header_size(self) -> int:
        return super().header_size + 20


class MovieFragmentBox(Box):
    pass


class MovieFragmentHeaderBox(FullBox):
    @functools.cached_property
    def sequence_number(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class TrackFragmentBox(Box):
    pass


class TrackFragmentHeaderBox(FullBox):
    # Not implemented
    pass


class TrackRunBox(FullBox):
    # Not implemented
    pass


class MovieFragmentRandomAccessBox(Box):
    pass


class TrackFragmentRandomAccessBox(FullBox):
    # Not implemented
    pass


class MovieFragmentRandomAccessOffsetBox(FullBox):
    @functools.cached_property
    def size(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class TrackFragmentBaseMediaDecodeTimeBox(FullBox):
    @functools.cached_property
    def baseMediaDecodeTime(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")
        elif self.version == 1:
            return self.slice.subslice(start, start + 8).unpack(">Q")

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 4
        elif self.version == 1:
            return super().header_size + 8


class LevelAssignmentBox(FullBox):
    # Not implemented
    pass


class TrackExtensionPropertiesBox(FullBox):
    @functools.cached_property
    def track_id(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class AlternativeStartupSequencePropertiesBox(FullBox):
    #
    pass


BOX_TYPES.update(
    {
        "mvex": MovieExtendsBox,  # 8.8.1
        "mehd": MovieExtendsHeaderBox,  # 8.8.2
        "trex": TrackExtendsBox,  # 8.8.3
        "moof": MovieFragmentBox,  # 8.8.4
        "mfhd": MovieFragmentHeaderBox,  # 8.8.5
        "traf": TrackFragmentBox,  # 8.8.6
        # "tfhd": TrackFragmentHeaderBox,  # 8.8.7
        # "trun": TrackRunBox,  # 8.8.8
        "mfra": MovieFragmentRandomAccessBox,  # 8.8.9
        # "tfra": TrackFragmentRandomAccessBox,  # 8.8.10
        "mfro": MovieFragmentRandomAccessOffsetBox,  # 8.8.11
        "tfdt": TrackFragmentBaseMediaDecodeTimeBox,  # 8.8.12
        # "leva": LevelAssignmentBox,  # 8.8.13
        "trep": TrackExtensionPropertiesBox,  # 8.8.15
        # "assp": AlternativeStartupSequencePropertiesBox,  # 8.8.16
    }
)
