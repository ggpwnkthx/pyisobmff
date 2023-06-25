"""
File: isobmff/box/user.py

Contains all the classes specified in section 8.10 of ISO/IEC 14496-12:2015
"""
from . import BOX_TYPES, Box, FullBox, ChildlessBox
from ..utils import iso639_2T_to_chars
import functools
import typing


class UserDataBox(Box):
    pass


class CopyrightBox(FullBox, ChildlessBox):
    @functools.cached_property
    def language(self) -> str:
        start = super().header_size
        return iso639_2T_to_chars(self.slice.subslice(start, start + 2).read())

    @functools.cached_property
    def notice(self) -> str:
        start = super().header_size + 2
        return self.slice.subslice(start, self.end).decode()

    @property
    def header_size(self) -> int:
        return self.end


class TrackSelectionBox(FullBox, ChildlessBox):
    @functools.cached_property
    def switch_group(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">i")[0]

    @functools.cached_property
    def attribute_list(self) -> typing.Tuple[str, ...]:
        start = super().header_size + 4
        return tuple(
            e[0] for e in self.slice.subslice(start, self.end).iter_unpack(f">4s")
        )

    @property
    def header_size(self) -> int:
        return self.end


class KindBox(Box):
    # Not implemented
    pass


BOX_TYPES.update(
    {
        "udta": UserDataBox,  # 8.10.1
        "cprt": CopyrightBox,  # 8.10.2
        "tsel": TrackSelectionBox,  # 8.10.3
        # "kind": KindBox,  # 8.10.4
    }
)
