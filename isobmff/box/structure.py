"""
File: isobmff/box/structure.py

Contains all the classes specified in section 4 of ISO/IEC 14496-12:2015
"""
from . import BOX_TYPES
from ..slice import Slice, CachedIterator
from ..utils import iterate_bits
from uuid import UUID
import functools
import struct
import typing
import logging


class Box:
    """
    Class representing a box in an ISO Base Media File Format (ISOBMFF) file.

    This class provides functionality for working with boxes in an ISOBMFF file. It allows reading the box's data,
    determining its size and type, and accessing its children if it has any.

    Parameters
    ----------
    slice : Slice
        The slice of the file that this box represents.
    parent : Box, optional
        Useful for traversing nested boxes

    Attributes
    ----------
    size : int
        The size of the box.
    type : str
        The type of the box.
    usertype : str
        The user type of the box, if any.

    slice : Slice
        The slice of the file that this box represents.
    start : int
        The start position of the box in the file.
    end : int
        The end position of the box in the file.
    raw : bytes
        The raw data of the box.
    header_size : int
        The size of the box's header.

    parent : Box
        The parent box of this box, if any
    has_children : bool
        Whether the box has any children.
    children : iterator
        An iterator over the box's children.
    hierarchy_depth : int
        The depth of the box in the box hierarchy.

    Examples
    --------
    >>> with open('file.mp4', 'rb') as f:
    ...     isobmff = ISOBMFF(f)
    ...     for box in isobmff:
    ...         print(box)

    """

    def __new__(cls, slice: Slice, parent: typing.Type["Box"] = None):
        """
        This method is called before the __init__ method.

        In this method, we first read the first 16 bytes of the slice. This
        data contains the size and type of the box, which are crucial for
        determining how to initialize the object that represents the box.

        We then check if the type of the box matches any of the known box types
        in the BOX_TYPES dictionary. If it does, the corresponding box class is
        instantiated. This allows the use of specialized classes for different
        types of boxes, each with their own methods and attributes that are
        appropriate for that type of box.

        If the box type does not match any known box types, the Box class is
        instantiated. This is a generic box that can handle any type of box, but
        does not provide and specialized data parsing mechanisms.

        Finally, we store the head of the box in the instance for later use in
        the __init__ method.
        """
        _head = slice.read(0, 8)
        _type = _head[4:8].decode()

        if _type in BOX_TYPES:
            instance = super(Box, BOX_TYPES[_type]).__new__(BOX_TYPES[_type])
        else:
            instance = super(Box, cls).__new__(cls)
        instance._head = _head
        return instance

    def __init__(self, slice: Slice, parent: typing.Type["Box"] = None):
        self.slice = slice
        self.parent = parent
        self._ext_size = False
        if not hasattr(self, "_head"):
            logging.warning("reading head init")
            self._head = slice.read(0, 8)
        self._size = struct.unpack(">I", self._head[:4])[0]
        if self._size == 1:
            self._size = struct.unpack(">Q", self.slice.read(8, 16))[0]
            self._ext_size = True
        self._type = self._head[4:8].decode()

    @property
    def size(self) -> int:
        return self._size

    @property
    def type(self) -> str:
        return self._type

    @functools.cached_property
    def usertype(self) -> str:
        if self.type == "uuid":
            start = 8 + (8 if self._ext_size else 0)
            return UUID(bytes=self.slice.read(start, start + 16))
        else:
            return None

    @functools.cached_property
    def start(self) -> int:
        return self.slice.start

    @functools.cached_property
    def end(self) -> int:
        if not self.slice.stop:
            if self.size:
                return self.start + self.size
        return self.slice.stop

    @property
    def raw(self) -> bytes:
        return self.slice.read()

    @property
    def header_size(self) -> int:
        self.size
        return 8 + (8 if self._ext_size else 0) + (16 if self.usertype else 0)

    @functools.cached_property
    def has_children(self):
        return self.size != self.header_size

    @functools.cached_property
    def children(self):
        if self.has_children:
            return CachedIterator(
                self.slice.subslice(self.header_size, self.size),
                lambda this: Box(this.slice, self.parent),
            )
        return None

    def __getitem__(self, index: int):
        if self.has_children:
            return self.children[index]
        raise IndexError("list index out of range")

    @functools.cached_property
    def hierarchy_depth(self) -> int:
        depth = 0
        parent = self.parent
        while parent is not None:
            depth += 1
            parent = parent.parent
        return depth

    def __repr__(self):
        return f"<{self.__class__.__name__}(type={self.usertype or self.type},start={self.start},end={self.end},size={self.size},has_children={self.has_children})>"


class FullBox(Box):
    @functools.cached_property
    def version(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 1).unpack(">B")[0]

    @functools.cached_property
    def flags(self) -> typing.Tuple[bool, ...]:
        start = super().header_size + 1
        return tuple(iterate_bits(self.slice.read(start, start + 3)))

    @property
    def header_size(self) -> int:
        return super().header_size + 4

    def __repr__(self):
        return f"{super().__repr__()[:-2]},version={self.version})>"


class ChildlessBox(Box):
    @property
    def has_children(self):
        return False

    @property
    def children(self):
        return None


class FileTypeBox(ChildlessBox):
    @functools.cached_property
    def major_brand(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def minor_version(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def compatible_brands(self) -> typing.List[str]:
        start = super().header_size + 8
        return [
            b[0].decode()
            for b in self.slice.subslice(start, self.end).iter_unpack("4s")
        ]

    @property
    def header_size(self) -> int:
        return self.size


BOX_TYPES.update(
    {
        "ftyp": FileTypeBox,
    }
)
