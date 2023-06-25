"""
File: isobmff/box/track/data.py

Contains all the classes specified in section 8.7 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified, however the following
classes may require review:

SubSampleInformationBox
SampleAuxiliaryInformationSizesBox
SampleAuxiliaryInformationOffsetsBox
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class DataInformationBox(Box):
    pass


class DataEntryUrlBox(FullBox, ChildlessBox):
    @functools.cached_property
    def location(self) -> str:
        start = super().header_size
        return self.slice.subslice(start).decode(terminator="\x00")

    @property
    def header_size(self) -> int:
        return super().header_size + len(self.location) + 1


class DataEntryUrnBox(FullBox, ChildlessBox):
    @functools.cached_property
    def name(self) -> str:
        start = super().header_size
        return self.slice.subslice(start).decode(terminator="\x00")

    @functools.cached_property
    def location(self) -> str:
        start = super().header_size + len(self.name) + 1
        return self.slice.subslice(start).decode(terminator="\x00")

    @property
    def header_size(self) -> int:
        return super().header_size + len(self.name) + len(self.location) + 2


class DataReferenceBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class SampleSizeBox(FullBox):
    @functools.cached_property
    def sample_size(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def sample_count(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entry_sizes(self) -> typing.Tuple[int, ...]:
        if self.sample_size == 0:
            start = super().header_size + 8
            return tuple(
                e[0]
                for e in self.slice.subslice(
                    start, start + 4 * self.sample_count
                ).iter_unpack(f">I")
            )
        else:
            return None

    @property
    def header_size(self) -> int:
        return super().header_size + 8 + len(self.entry_sizes) * 4


class CompactSampleSizeBox(FullBox):
    @functools.cached_property
    def reserved(self) -> int:
        start = super().header_size
        return int.from_bytes(
            self.slice.subslice(start, start + 3).read(), byteorder="big"
        )

    @functools.cached_property
    def sample_size(self) -> int:
        start = super().header_size + 3
        return self.slice.subslice(start, start + 1).unpack(">B")[0]

    @functools.cached_property
    def sample_count(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entry_size(self) -> typing.Tuple[int, ...]:
        start = super().header_size + 8
        end = start + (self.sample_count * self.sample_size / 8)
        if self.sample_size == 4:
            return tuple(
                i
                for e in self.slice.subslice(start, end).iter_unpack(">B")
                for i in (e[0] >> 4, e[0] & 0x0F)
            )
        elif self.sample_size == 8:
            return tuple(self.slice.subslice(start, end).iter_unpack(">B"))
        elif self.sample_size == 16:
            return tuple(self.slice.subslice(start, end).iter_unpack(">H"))

    @property
    def header_size(self) -> int:
        return (
            super().header_size
            + 8
            + (0 if self.sample_size else (self.sample_count * self.sample_size / 8))
        )


class SampleToChunkBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[int, int, int]]:
        start = super().header_size + 4
        return tuple(
            self.slice.subslice(start, start + self.entry_count * 12).iter_unpack(
                ">III"
            )
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 12


class ChunkOffsetBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[int]:
        start = super().header_size + 4
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.entry_count * 4
            ).iter_unpack(">I")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 4


class ChunkLargeOffsetBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[int]:
        start = super().header_size + 4
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.entry_count * 8
            ).iter_unpack(">Q")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count * 8


class PaddingBitsBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(self) -> typing.Tuple[typing.Tuple[bool, int, bool, int]]:
        start = super().header_size + 4
        return tuple(
            tuple(
                bool((e[0] >> 7) & 0x01),
                (e[0] >> 4) & 0x07,
                bool((e[0] >> 3) & 0x01),
                e[0] & 0x07,
            )
            for e in self.slice.subslice(start, start + self.entry_count).iter_unpack(
                ">B"
            )
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.entry_count


class SubSampleInformationBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def entries(
        self,
    ) -> typing.Tuple[
        typing.Tuple[int, int, typing.Tuple[typing.Tuple[int, int, int, int]]]
    ]:
        start = super().header_size + 4
        return tuple(
            (
                self.slice.subslice(start + i * 6, start + i * 6 + 4).unpack(">I")[
                    0
                ],  # sample_delta
                self.slice.subslice(start + i * 6 + 4, start + i * 6 + 6).unpack(">H")[
                    0
                ],  # subsample_count
                tuple(
                    (
                        self.slice.subslice(
                            start + i * 6 + 6 + j * (10 if self.version == 1 else 8),
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2),
                        ).unpack(">I" if self.version == 1 else ">H")[
                            0
                        ],  # subsample_size
                        self.slice.subslice(
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2),
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2)
                            + 1,
                        ).unpack(">B")[
                            0
                        ],  # subsample_priority
                        self.slice.subslice(
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2)
                            + 1,
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2)
                            + 2,
                        ).unpack(">B")[
                            0
                        ],  # discardable
                        self.slice.subslice(
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2)
                            + 2,
                            start
                            + i * 6
                            + 6
                            + j * (10 if self.version == 1 else 8)
                            + (4 if self.version == 1 else 2)
                            + 6,
                        ).unpack(">I")[
                            0
                        ],  # reserved
                    )
                    for j in range(
                        self.slice.subslice(
                            start + i * 6 + 4, start + i * 6 + 6
                        ).unpack(">H")[0]
                    )
                ),
            )
            for i in range(self.entry_count)
        )

    @property
    def header_size(self):
        if self.version == 0:
            return (
                super().header_size
                + 4
                + sum(6 + 8 * subsample_count for _, subsample_count, _ in self.entries)
            )

        elif self.version == 1:
            return (
                super().header_size
                + 4
                + sum(
                    8 + 10 * subsample_count for _, subsample_count, _ in self.entries
                )
            )


class SampleAuxiliaryInformationSizesBox(FullBox):
    @functools.cached_property
    def aux_info_type(self) -> int:
        if self.flags[0]:
            start = super().header_size
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        else:
            return None

    @functools.cached_property
    def aux_info_type_parameter(self) -> int:
        if self.flags[0]:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        else:
            return None

    @functools.cached_property
    def default_sample_info_size(self) -> int:
        if self.flags[0]:
            start = super().header_size + 8
        else:
            start = super().header_size
        return self.slice.subslice(start, start + 1).unpack(">B")[0]

    @functools.cached_property
    def sample_count(self) -> int:
        if self.flags[0]:
            start = super().header_size + 9
        else:
            start = super().header_size + 1
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def sample_info_size(self) -> typing.Tuple[int, ...]:
        if self.default_sample_info_size == 0:
            if self.flags[0]:
                start = super().header_size + 13
            else:
                start = super().header_size + 5
            return tuple(
                self.slice.subslice(start, start + self.sample_count).iter_unpack(">B")
            )
        else:
            return None

    @property
    def header_size(self) -> int:
        if self.flags[0]:
            return (
                super().header_size
                + 8
                + 1
                + 4
                + (self.sample_count if self.default_sample_info_size == 0 else 0)
            )
        else:
            return (
                super().header_size
                + 1
                + 4
                + (self.sample_count if self.default_sample_info_size == 0 else 0)
            )


class SampleAuxiliaryInformationOffsetsBox(FullBox):
    @functools.cached_property
    def aux_info_type(self) -> int:
        if self.flags[0]:
            start = super().header_size
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        else:
            return None

    @functools.cached_property
    def aux_info_type_parameter(self) -> int:
        if self.flags[0]:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        else:
            return None

    @functools.cached_property
    def entry_count(self) -> int:
        if self.flags[0]:
            start = super().header_size + 8
        else:
            start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def offsets(self) -> typing.Tuple[int, ...]:
        if self.flags[0]:
            start = super().header_size + 12
        else:
            start = super().header_size + 4
        if self.version == 0:
            return tuple(
                e[0]
                for e in self.slice.subslice(
                    start, start + self.entry_count * 4
                ).iter_unpack(">I")
            )
        elif self.version == 1:
            return tuple(
                e[0]
                for e in self.slice.subslice(
                    start, start + self.entry_count * 8
                ).iter_unpack(">Q")
            )

    @property
    def header_size(self) -> int:
        if self.flags[0]:
            start = super().header_size + 8
        else:
            start = super().header_size
        if self.version == 0:
            return start + 4 + (self.entry_count * 4)
        elif self.version == 1:
            return start + 4 + (self.entry_count * 8)


BOX_TYPES.update(
    {
        "dinf": DataInformationBox,  # 8.7.1
        "url ": DataEntryUrlBox,  # 8.7.2
        "urn ": DataEntryUrnBox,  # 8.7.2
        "dref": DataReferenceBox,  # 8.7.2
        "stsz": SampleSizeBox,  # 8.7.3.2
        "stz2": CompactSampleSizeBox,  # 8.7.3.3
        "stsc": SampleToChunkBox,  # 8.7.4
        "stco": ChunkOffsetBox,  # 8.7.5
        "co64": ChunkLargeOffsetBox,  # 8.7.5
        "padb": PaddingBitsBox,  # 8.7.6
        "subs": SubSampleInformationBox,  # 8.7.7
        "saiz": SampleAuxiliaryInformationSizesBox,  # 8.7.8
        "saio": SampleAuxiliaryInformationOffsetsBox,  # 8.7.9
    }
)
