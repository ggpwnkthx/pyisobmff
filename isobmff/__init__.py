"""
File: isobmff/__init__.py

The main package for the ISO Base Media File Format (ISO/IEC 14496-12:2015)
"""
from .box import Box, BOX_TYPES
from .slice import Slice, CachedIterator
import typing


class Scanner(CachedIterator):
    """
    A class that represents an ISO Base Media File Format (ISOBMFF) file.

    The Scanner class inherits from the CachedIterator class, which means 
    it caches the boxes it iterates over. This is useful because it allows 
    the boxes to be accessed again without needing to recompute them.

    Parameters
    ----------
    handler : typing.BinaryIO
        The binary file handler for the ISOBMFF file.

    Examples
    --------
    >>> with open('file.mp4', 'rb') as f:
    ...     scanner = Scanner(f)
    ...     for box in scanner:
    ...         print(box)
    """
    def __init__(self, handler: typing.BinaryIO):
        """
        Initialize the Scanner with a binary file handler.

        Parameters
        ----------
        handler : typing.BinaryIO
            The binary file handler for the ISOBMFF file.
        """
        super().__init__(
            Slice(handler),
            lambda this: Box(this.slice),
        )

    def __getitem__(self, index: int | str):
        """
        Retrieve a box by its index or type.

        Parameters
        ----------
        index : int | str
            The index or type of the box to retrieve.

        Returns
        -------
        Box | list[Box]
            The box(es) matching the given index or type.
        """
        if isinstance(index, int):
            return super().__getitem__(index)
        elif isinstance(index, str):
            items = [b for b in self if b.type == index]
            return items if len(items) > 1 else items[0]


__all__ = [
    "Scanner",
    "BOX_TYPES",
]

__version__ = "1.0.0"
