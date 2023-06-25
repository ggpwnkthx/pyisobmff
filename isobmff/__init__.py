"""
File: isobmff/__init__.py

The main package for the ISO Base Media File Format (ISO/IEC 14496-12:2015)
"""
from .box import Box, BOX_TYPES
from .slice import Slice, CachedIterator
import typing


class Scanner(CachedIterator):
    """
    Class representing an ISO Base Media File Format (ISOBMFF) file.

    This class provides functionality for working with ISOBMFF files. It allows iterating over the boxes
    in the file on-demand and provides thread-safe access to the file's data.

    Parameters
    ----------
    handler : typing.BinaryIO
        The binary file handler for the ISOBMFF file.

    Examples
    --------
    >>> with open('file.mp4', 'rb') as f:
    ...     isobmff = ISOBMFF(f)
    ...     for box in isobmff:
    ...         print(box)
    """

    def __init__(self, handler: typing.BinaryIO):
        super().__init__(
            Slice(handler),
            lambda this: Box(this.slice),
        )


__all__ = [
    "Scanner",
    "BOX_TYPES",
]
