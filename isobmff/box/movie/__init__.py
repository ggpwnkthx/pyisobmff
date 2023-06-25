"""
File: isobmff/box/movie/__init__.py

Contains all the classes specified in section 8.2 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from .. import BOX_TYPES, Box, FullBox
import functools
import typing


class MovieBox(Box):
    pass


class MovieHeaderBox(FullBox):
    @functools.cached_property
    def creation_time(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def modification_time(self) -> int:
        if self.version == 0:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            start = super().header_size + 8
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def timescale(self) -> int:
        if self.version == 0:
            start = super().header_size + 8
        elif self.version == 1:
            start = super().header_size + 16
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def duration(self) -> int:
        if self.version == 0:
            start = super().header_size + 12
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.version == 1:
            start = super().header_size + 20
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def rate(self) -> float:
        if self.version == 0:
            start = super().header_size + 16
        elif self.version == 1:
            start = super().header_size + 28
        return self.slice.subslice(start, start + 4).unpack(">i")[0] / (1 << 16)

    @functools.cached_property
    def volume(self) -> float:
        if self.version == 0:
            start = super().header_size + 20
        elif self.version == 1:
            start = super().header_size + 32
        return self.slice.subslice(start, start + 2).unpack(">h")[0] / (1 << 8)

    @functools.cached_property
    def reserved_0(self) -> bytes:
        if self.version == 0:
            start = super().header_size + 2
        elif self.version == 1:
            start = super().header_size + 34
        return self.slice.subslice(start, start + 2).read()

    @functools.cached_property
    def reserved_1(self) -> typing.Tuple[int, int]:
        if self.version == 0:
            start = super().header_size + 24
        elif self.version == 1:
            start = super().header_size + 36
        return self.slice.subslice(start, start + 8).unpack(">II")

    @functools.cached_property
    def matrix(
        self,
    ) -> typing.Tuple[
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, int],
        typing.Tuple[int, int, int],
    ]:
        if self.version == 0:
            start = super().header_size + 32
        elif self.version == 1:
            start = super().header_size + 44
        return tuple(
            self.slice.subslice(start, start + 36).unpack(">9i")[i * 3 : i * 3 + 3]
            for i in range(3)
        )

    @functools.cached_property
    def pre_defined_0(self) -> typing.Tuple[bytes, bytes, bytes, bytes, bytes, bytes]:
        if self.version == 0:
            start = super().header_size + 68
        elif self.version == 1:
            start = super().header_size + 80
        size = 4
        count = 6
        data = self.slice.subslice(start, start + (size * count))
        return tuple(data[i : i + size] for i in range(0, count, size))

    @functools.cached_property
    def next_track_id(self):
        if self.version == 0:
            start = super().header_size + 92
        elif self.version == 1:
            start = super().header_size + 104
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 96
        elif self.version == 1:
            return super().header_size + 108


BOX_TYPES.update(
    {
        "moov": MovieBox,  # 8.2.1
        "mvhd": MovieHeaderBox,  # 8.2.2
    }
)
