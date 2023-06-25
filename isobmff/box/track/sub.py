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
    @functools.cached_property
    def switch_group(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def alternate_group(self) -> int:
        start = super().header_size + 2
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def sub_track_ID(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def attribute_list(self) -> typing.Tuple[str, ...]:
        start = super().header_size + 8
        return tuple(
            e[0] for e in self.slice.subslice(start, self.end).iter_unpack(">4s")
        )

    @property
    def header_size(self) -> int:
        return self.size


class SubTrackDefinition(Box):
    pass


class SubTrackSampleGroupBox(FullBox):
    @functools.cached_property
    def grouping_type(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def item_count(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def items(self) -> typing.Tuple[int, ...]:
        start = super().header_size + 8
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.item_count * 4
            ).iter_unpack(">I")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 8 + self.item_count * 4


BOX_TYPES.update(
    {
        "strk": SubTrack,  # 8.14.3
        "stri": SubTrackInformation,  # 8.14.4
        "strd": SubTrackDefinition,  # 8.14.5
        "stsg": SubTrackDefinition,  # 8.14.6
    }
)
