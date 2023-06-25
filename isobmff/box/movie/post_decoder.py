"""
File: isobmff/box/movie/post_decoder.py

Contains all the classes specified in section 8.1 of ISO/IEC 14496-12:2015
"""
from .. import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class RestrictedSchemeInfoBox(Box):
    pass


class StereoVideoBox(FullBox, ChildlessBox):
    @functools.cached_property
    def reserved(self) -> int:
        start = super().header_size
        return int.from_bytes(self.slice.subslice(start, start + 4).read(), byteorder="big") >> 2
    
    @functools.cached_property
    def single_view_allowed(self) -> int:
        start = super().header_size
        return int.from_bytes(self.slice.subslice(start, start + 4).read(), byteorder="big") & 0b11
    
    @functools.cached_property
    def stereo_scheme(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]
    
    @functools.cached_property
    def length(self) -> int:
        start = super().header_size + 8
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def stereo_indication_type(self) -> typing.Tuple[int, ...]:
        start = super().header_size + 12
        return tuple(
            e[0]
            for e in self.slice.subslice(
                start, start + self.length
            ).iter_unpack(">B")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 12 + self.length


BOX_TYPES.update(
    {
        "rinf": RestrictedSchemeInfoBox,  # 8.15.3
        "stvi": StereoVideoBox,  # 8.15.4
    }
)
