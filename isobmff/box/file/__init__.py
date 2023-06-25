"""
File: isobmff/box/file/__init__.py

Contains all the classes specified in section 8.1 of ISO/IEC 14496-12:2015
Class property formats and sizes have been verified.
"""
from .. import BOX_TYPES, FullBox, ChildlessBox, Slice
import typing


class MediaDataBox(ChildlessBox):
    @property
    def data(self) -> Slice:
        return self.slice.subslice(super().header_size, self.end)

    @property
    def header_size(self) -> int:
        return self.size


class FreeSpaceBox(ChildlessBox):
    @property
    def data(self) -> typing.Iterator:
        return self.slice.subslice(super().header_size, self.end).iter_unpack(">B")

    @property
    def header_size(self) -> int:
        return self.size


class ProgressiveDownloadInfoBox(FullBox, ChildlessBox):
    @property
    def rate_and_initial_delay(self) -> typing.Tuple[typing.Tuple[int, int], ...]:
        return tuple(
            self.slice.subslice(super().header_size, self.end).iter_unpack(">II")
        )

    @property
    def header_size(self) -> int:
        return super().header_size + len(self.rate_and_initial_delay) * 8


BOX_TYPES.update(
    {
        "mdat": MediaDataBox,  # 8.1.1
        "free": FreeSpaceBox,  # 8.1.2
        "skip": FreeSpaceBox,  # 8.1.2
        "pdin": ProgressiveDownloadInfoBox,  # 8.1.3
    }
)
