"""
File: isobmff/box/segment.py

Contains all the classes specified in section 8.16 of ISO/IEC 14496-12:2015
"""
from . import BOX_TYPES, Box, FullBox, FileTypeBox, CachedIterator, Slice
import functools
import typing


class RestrictedSchemeInfoBox(Box):
    pass


class SegmentIndexBox(FullBox):
    @functools.cached_property
    def reference_ID(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def timescale(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def earliest_presentation_time(self) -> int:
        start = super().header_size + 8
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        return self.slice.subslice(start, start + 8).unpack(">*")[0]

    @functools.cached_property
    def first_offset(self) -> int:
        if self.version == 0:
            start = super().header_size + 12
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        start = super().header_size + 16
        return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def reserved(self) -> int:
        if self.version == 0:
            start = super().header_size + 16
        else:
            start = super().header_size + 24
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def reference_count(self) -> int:
        if self.version == 0:
            start = super().header_size + 18
        else:
            start = super().header_size + 26
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def references(self):
        # Not implemented
        return None

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 20 + self.reference_count * 12
        return super().header_size + 28 + self.reference_count * 12


class SubsegmentIndexBox(FullBox):
    @functools.cached_property
    def subsegment_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def subsegments(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        start = super().header_size + 4
        return CachedIterator(
            self.slice.subslice(start, self.end),
            lambda this: Subsegment(this.slice, self),
            self.entry_count,
        )

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + self.subsegment_count * 12
        return super().header_size + self.subsegment_count * 12


class Subsegment:
    def __init__(self, slice: Slice, parent: SubsegmentIndexBox) -> None:
        self.slice = slice
        self.parent = parent

    @functools.cached_property
    def range_count(self):
        return self.slice.subslice(0, 4).unpack(">I")[0]

    @functools.cached_property
    def ranges(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        start = super().header_size + 4
        return CachedIterator(
            self.slice.subslice(start, self.end),
            lambda this: SubsegmentRange(this.slice, self),
            self.entry_count,
        )

    @functools.cached_property
    def size(self):
        return self.range_count * 4


class SubsegmentRange:
    def __init__(self, slice: Slice, parent: SubsegmentIndexBox) -> None:
        self.slice = slice
        self.parent = parent

    @functools.cached_property
    def level(self) -> int:
        return self.slice.subslice(0, 1).unpack(">B")[0]

    @functools.cached_property
    def range_size(self) -> int:
        return int.from_bytes(self.slice.subslice(1, 4).read(), byteorder="big")

    @functools.cached_property
    def size(self):
        return 4


class ProducerReferenceTimeBox(FullBox):
    @functools.cached_property
    def reference_ID(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def ntp_timestamp(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def media_time(self) -> int:
        start = super().header_size + 12
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 16
        return super().header_size + 20


BOX_TYPES.update(
    {
        "styp": FileTypeBox,  # 8.16.2
        "sidx": SegmentIndexBox,  # 8.16.3
        "ssix": SubsegmentIndexBox,  # 8.16.4
        "prft": ProducerReferenceTimeBox,  # 8.16.5
    }
)
