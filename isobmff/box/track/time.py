"""
File: isobmff/box/track/time.py

Contains all the classes specified in section 8.6 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from .. import BOX_TYPES, Box, FullBox
import functools
import typing


class TimeToSampleBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        start = super().header_size + 4
        return tuple(
            self.slice.subslice(start, start + self.entry_count * 8).iter_unpack(">II")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 8


class CompositionOffsetBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        start = super().header_size + 4
        if self.version == 0:
            __format = ">II"
        elif self.version == 1:
            __format == ">Ii"
        return tuple(
            self.slice.subslice(start, start + self.entry_count * 8).iter_unpack(
                __format
            )
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 8


class CompositionToDecodeBox(FullBox):
    @functools.cached_property
    def compositionToDTSShift(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 4).unpack(">i")[0]
        elif self.version == 1:
            return self.slice.subslice(start, start + 8).unpack(">q")[0]

    @functools.cached_property
    def leastDecodeToDisplayDelta(self) -> int:
        if self.version == 0:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">i")[0]
        elif self.version == 1:
            start = super().header_size + 8
            return self.slice.subslice(start, start + 8).unpack(">q")[0]

    @functools.cached_property
    def greatestDecodeToDisplayDelta(self) -> int:
        if self.version == 0:
            start = super().header_size + 8
            return self.slice.subslice(start, start + 4).unpack(">i")[0]
        elif self.version == 1:
            start = super().header_size + 16
            return self.slice.subslice(start, start + 8).unpack(">q")[0]

    @functools.cached_property
    def compositionStartTime(self) -> int:
        if self.version == 0:
            start = super().header_size + 12
            return self.slice.subslice(start, start + 4).unpack(">i")[0]
        elif self.version == 1:
            start = super().header_size + 24
            return self.slice.subslice(start, start + 8).unpack(">q")[0]

    @functools.cached_property
    def compositionEndTime(self) -> int:
        if self.version == 0:
            start = super().header_size + 16
            return self.slice.subslice(start, start + 4).unpack(">i")[0]
        elif self.version == 1:
            start = super().header_size + 32
            return self.slice.subslice(start, start + 8).unpack(">q")[0]

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 20
        elif self.version == 1:
            return super().header_size + 40


class SyncSampleBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[int, ...]:
        start = super().header_size + 4
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.entry_count * 8
            ).iter_unpack(">I")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 4


class ShadowSyncSampleBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        start = super().header_size + 4
        return tuple(
            self.slice.subslice(start, start + self.entry_count * 8).iter_unpack(">II")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 8


class SampleDependencyTypeBox(FullBox):
    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int, int, int], ...]:
        start = super().header_size
        return tuple(
            tuple((e[0] >> shift) & 0x03 for shift in [6, 4, 2, 0])
            for e in self.slice.subslice(
                start, start + self.parent["stsz"].sample_count
            ).iter_unpack("B")
        )

    @property
    def header_size(self) -> int:
        return self.end


class EditBox(Box):
    pass


class EditListBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int, int, int], ...]:
        start = super().header_size + 4
        if self.version == 0:
            return tuple(
                self.slice.subslice(start, start + self.entry_count * 12).iter_unpack(
                    ">Iihh"
                )
            )
        if self.version == 1:
            return tuple(
                self.slice.subslice(start, start + self.entry_count * 20).iter_unpack(
                    ">Qqhh"
                )
            )

    @property
    def header_size(self) -> int:
        if self.version == 1:
            return super().header_size + 4 + self.entry_count * 20
        else:
            return super().header_size + 4 + self.entry_count * 12


BOX_TYPES.update(
    {
        "stts": TimeToSampleBox,  # 8.6.1.2
        "ctts": CompositionOffsetBox,  # 8.6.1.3
        "cslg": CompositionToDecodeBox,  # 8.6.1.4
        "stss": SyncSampleBox,  # 8.6.2
        "stsh": ShadowSyncSampleBox,  # 8.6.3
        "sdtp": SampleDependencyTypeBox,  # 8.6.4
        "edts": EditBox,  # 8.6.5
        "elst": EditListBox,  # 8.6.6
    }
)
