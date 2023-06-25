"""
File: isobmff/box/track/sample/__init__.py

Contains all the classes specified in section 8.5 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from ... import BOX_TYPES, Box, FullBox
import functools
import typing


class SampleTableBox(Box):
    pass


class SampleEntry(Box):
    @functools.cached_property
    def reserved(self) -> typing.Tuple[int, int, int, int, int, int]:
        start = super().header_size
        return self.slice.subslice(start, start + 6).unpack(">6B")

    @functools.cached_property
    def data_reference_index(self) -> int:
        start = super().header_size + 6
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @property
    def header_size(self) -> int:
        return super().header_size + 8


class BitRateBox(FullBox):
    @functools.cached_property
    def decoding_buffer_size(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def max_bitrate(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def avg_bitrate(self) -> int:
        start = super().header_size + 8
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @property
    def header_size(self) -> int:
        return super().header_size + 12


class SampleDescriptionBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def sample_entries(self) -> typing.List[SampleEntry]:
        start = super().header_size + 4
        entries = []
        for _ in range(self.entry_count):
            entry = SampleEntry(self.slice.subslice(start))
            entries.append(entry)
            start += entry.size
        return entries

    @property
    def header_size(self) -> int:
        return (
            super().header_size + 4 + sum(entry.size for entry in self.sample_entries)
        )


class DegradationPriorityBox(FullBox):
    @functools.cached_property
    def priorities(self) -> typing.Tuple[int, ...]:
        start = super().header_size
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.parent["stsz"].sample_count * 2
            ).iter_unpack(">H")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + self.parent["stsz"].sample_count * 2


BOX_TYPES.update(
    {
        "stbl": SampleTableBox,  # 8.5.1
        "btrt": BitRateBox,  # 8.5.2
        "stsd": SampleDescriptionBox,  # 8.5.2
        "stdp": DegradationPriorityBox,  # 8.5.3
    }
)
