"""
File: isobmff/box/protected.py

Contains all the classes specified in section 8.12 of ISO/IEC 14496-12:2015
"""
from . import BOX_TYPES, Box, FullBox, ChildlessBox
import functools


class ProtectionSchemeInfoBox(Box):
    pass


class OriginalFormatBox(Box):
    @functools.cached_property
    def data_format(self) -> str:
        start = super().header_size
        return self.slice.subslice(start, start + 4).decode()


class SchemeTypeBox(FullBox, ChildlessBox):
    @functools.cached_property
    def scheme_type(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]
    
    @functools.cached_property
    def scheme_version(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]
    
    @functools.cached_property
    def scheme_uri(self) -> str:
        if self.flags[0]:
            start = super().header_size + 8
            return self.slice.subslice(start, self.end).decode()
        return None

    @property
    def header_size(self) -> int:
        return self.end

class SchemeInformationBox(Box):
    pass

BOX_TYPES.update(
    {
        "sinf": ProtectionSchemeInfoBox,  # 8.12.1
        "frma": OriginalFormatBox,  # 8.12.2
        "schm": SchemeTypeBox,  # 8.12.5
        "schi": SchemeInformationBox,  # 8.12.6
    }
)