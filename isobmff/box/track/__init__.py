"""
File: isobmff/box/track/__init__.py

Contains all the classes specified in section 8.3 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class TrackBox(Box):
    pass


class TrackHeaderBox(FullBox):
    @functools.cached_property
    def creation_time(self):
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def modification_time(self):
        if self.version == 0:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            start = super().header_size + 8
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def track_id(self) -> int:
        if self.version == 0:
            start = super().header_size + 8
        elif self.version == 1:
            start = super().header_size + 16
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def reserved_0(self) -> int:
        if self.version == 0:
            start = super().header_size + 12
        elif self.version == 1:
            start = super().header_size + 20
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def duration(self) -> int:
        if self.version == 0:
            start = super().header_size + 16
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            start = super().header_size + 24
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def reserved_1(self) -> typing.Tuple[int, int]:
        if self.version == 0:
            start = super().header_size + 20
        elif self.version == 1:
            start = super().header_size + 32
        return self.slice.subslice(start, start + 8).unpack(">II")[0]

    @functools.cached_property
    def layer(self) -> float:
        if self.version == 0:
            start = super().header_size + 28
        elif self.version == 1:
            start = super().header_size + 40
        return self.slice.subslice(start, start + 2).unpack(">h")[0] / (1 << 8)

    @functools.cached_property
    def alternate_group(self) -> int:
        if self.version == 0:
            start = super().header_size + 30
        elif self.version == 1:
            start = super().header_size + 42
        return self.slice.subslice(start, start + 2).unpack(">h")[0]

    @functools.cached_property
    def volume(self) -> float:
        if self.version == 0:
            start = super().header_size + 32
        elif self.version == 1:
            start = super().header_size + 44
        return self.slice.subslice(start, start + 2).unpack(">h")[0] / (1 << 8)

    @functools.cached_property
    def reserved_2(self) -> int:
        if self.version == 0:
            start = super().header_size + 34
        elif self.version == 1:
            start = super().header_size + 46
        return self.slice.subslice(start, start + 2).unpack(">I")[0]

    @functools.cached_property
    def matrix(
        self,
    ) -> typing.Tuple[
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, int],
    ]:
        if self.version == 0:
            start = super().header_size + 36
        elif self.version == 1:
            start = super().header_size + 48
        return tuple(
            self.slice.subslice(start, start + 36).unpack(">9i")[i * 3 : i * 3 + 3]
            for i in range(3)
        )

    @functools.cached_property
    def width(self) -> float:
        if self.version == 0:
            start = super().header_size + 72
        elif self.version == 1:
            start = super().header_size + 84
        return self.slice.subslice(start, start + 4).unpack(">I")[0] / (1 << 16)

    @functools.cached_property
    def height(self) -> float:
        if self.version == 0:
            start = super().header_size + 76
        elif self.version == 1:
            start = super().header_size + 88
        return self.slice.subslice(start, start + 4).unpack(">I")[0] / (1 << 16)

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 80
        elif self.version == 1:
            return super().header_size + 92


class TrackReferenceBox(Box):
    pass


class TrackReferenceTypeBox(ChildlessBox):
    @functools.cached_property
    def track_ids(self) -> typing.Tuple[int]:
        start = super().header_size + 4
        return tuple(
            track_id[0]
            for track_id in self.slice.subslice(start, self.end).iter_unpack(">I")
        )

    @property
    def header_size(self) -> int:
        return self.size

class TrackGroupBox(Box):
    pass


class TrackGroupTypeBox(FullBox):
    @functools.cached_property
    def track_group_id(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @property
    def header_size(self) -> int:
        return super().header_size + 4


BOX_TYPES.update(
    {
        "trak": TrackBox,  # 8.3.1
        "tkhd": TrackHeaderBox,  # 8.3.2
        "tref": TrackReferenceBox,  # 8.3.3
        "hint": TrackReferenceTypeBox,  # 8.3.3
        "cdsc": TrackReferenceTypeBox,  # 8.3.3
        "font": TrackReferenceTypeBox,  # 8.3.3
        "hind": TrackReferenceTypeBox,  # 8.3.3
        "vdep": TrackReferenceTypeBox,  # 8.3.3
        "vplx": TrackReferenceTypeBox,  # 8.3.3
        "subt": TrackReferenceTypeBox,  # 8.3.3
        "trgr": TrackGroupBox,  # 8.3.4
        "msrc": TrackGroupTypeBox,  # 8.3.4
    }
)
