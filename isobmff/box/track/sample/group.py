"""
File: isobmff/box/track/sample/group.py

Contains all the classes specified in section 8.9 of ISO/IEC 14496-12:2015
"""
from ... import BOX_TYPES, FullBox
import functools
import typing


class SampleToGroupBox(FullBox):
    @functools.cached_property
    def grouping_type(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def grouping_type_parameter(self) -> int:
        if self.version == 1:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        return None

    @functools.cached_property
    def entry_count(self) -> int:
        if self.version == 0:
            start = super().header_size + 4
        elif self.version == 1:
            start = super().header_size + 8
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        if self.version == 0:
            start = super().header_size + 8
        elif self.version == 1:
            start = super().header_size + 12
        return tuple(self.slice.subslice(start, start + self.entry_count * 8).iter_unpack(">II"))

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 8 + self.entry_count * 8
        return super().header_size + 12 + self.entry_count * 8


class SampleGroupDescriptionBox(FullBox):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        "sbgp": SampleToGroupBox,  # 8.9.2
        # "sgpd": SampleGroupDescriptionBox,  # 8.9.3
    }
)
