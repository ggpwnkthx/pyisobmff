"""
File: isobmff/box/track/media/handler.py

Contains all the classes specified in section 12 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from ... import BOX_TYPES, Box, FullBox, ChildlessBox
import functools
import typing


class VideoMediaHeaderBox(FullBox):
    @functools.cached_property
    def graphicsmode(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def items(self) -> typing.Tuple[int, ...]:
        start = super().header_size + 2
        return tuple(
            self.slice.subslice(
                start, start + 6
            ).unpack(">HHH")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + 8
    


BOX_TYPES.update(
    {
        "vmhd": VideoMediaHeaderBox,  # 12.1.2
    }
)
