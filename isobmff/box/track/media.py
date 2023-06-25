"""
File: isobmff/box/track/media.py

Contains all the classes specified in section 8.4 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
from ...utils import iso639_2T_to_chars
import functools
import typing


class MediaBox(Box):
    pass


class MediaHeaderBox(FullBox):
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
    def language(self) -> str:
        if self.version == 0:
            start = super().header_size + 16
        elif self.version == 1:
            start = super().header_size + 24
        return iso639_2T_to_chars(self.slice.subslice(start, start + 2).read())

    @functools.cached_property
    def pre_defined(self) -> int:
        if self.version == 0:
            start = super().header_size + 18
        elif self.version == 1:
            start = super().header_size + 26
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 20
        elif self.version == 1:
            return super().header_size + 28


class HandlerBox(FullBox, ChildlessBox):
    @functools.cached_property
    def pre_defined(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def handler_type(self) -> str:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).decode()

    @functools.cached_property
    def reserved(self) -> typing.Tuple[int, int, int]:
        start = super().header_size + 8
        return self.slice.subslice(start, start + 12).unpack(">III")

    @functools.cached_property
    def name(self) -> str:
        start = super().header_size + 20
        return self.slice.subslice(start, self.end).decode()

    @property
    def header_size(self) -> int:
        return self.end


class MediaInformationBox(Box):
    pass


class NullMediaHeaderBox(FullBox):
    pass


class ExtendedLanguageBox(FullBox, ChildlessBox):
    @functools.cached_property
    def handler_type(self) -> str:
        start = super().header_size
        return self.slice.subslice(start, self.end).decode()

    @property
    def header_size(self) -> int:
        return self.end

BOX_TYPES.update(
    {
        "mdia": MediaBox,  # 8.4.1
        "mdhd": MediaHeaderBox,  # 8.4.2
        "hdlr": HandlerBox,  # 8.4.3
        "minf": MediaInformationBox,  # 8.4.4
        "nmhd": NullMediaHeaderBox,  # 8.4.5
        "elng": ExtendedLanguageBox,  # 8.4.6
    }
)
