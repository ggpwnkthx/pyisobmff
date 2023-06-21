# File: isobmff/iterator.py

from .registries.types import DECODERS
from collections import OrderedDict
import logging
import typing

if typing.TYPE_CHECKING:
    from .atoms import Atom
    from .registries import Registry


class Iterator:
    """
    An iterator for parsing an ISO Base Media File and iterating over its atoms.

    Parameters:
    -----------
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    atom_registry : Registry, optional
        The atom registry used to resolve atom classes (default: an empty Registry).
    type_registry : Registry, optional
        The type registry used to resolve type classes (default: DECODERS).

    Attributes:
    -----------
    _handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    _atom_registry : Registry
        The atom registry used to resolve atom classes.
    _atom_cache : typing.Dict[int, Atom]
        A list to cache the parsed atoms for faster access.

    Notes
    -----
    - This iterator provides functionality to parse ISO Base Media Files and iterate over the atoms within the file.
    - It supports handling nested atoms.
    - The iterator is designed to work with a file handler that represents the ISO Base Media File.
    - The atom_registry parameter allows customization of atom class resolution.
    - The type_registry parameter allows customization of type class resolution.
    - The iterator caches the parsed atoms internally for faster access when retrieving atoms by index or type.
    - The iterator supports iteration using the __iter__ method and indexing using the __getitem__ method.
    - The iterator is compatible with the Atom class and other subclasses of Atom, allowing nested iteration.

    """

    def __init__(
        self,
        handler: typing.BinaryIO,
        atom_registry: "Registry",
        type_registry: "Registry" = DECODERS,
    ) -> None:
        """
        Initialize a new Iterator object.

        Parameters:
        -----------
        handler : typing.BinaryIO
            The file handler of the ISO Base Media File.
        atom_registry : Registry, optional
            The atom registry used to resolve atom classes (default: an empty Registry).
        type_registry : Registry, optional
            The type registry used to resolve type classes (default: DECODERS).
        """
        self._handler: typing.BinaryIO = handler
        if not self._handler.seekable():
            logging.warning(
                "The file handler is not seekable. The entire file will have to be read in order to parse it. This is likely undesireable. Continue with caution."
            )
        self._atom_registry: "Registry" = atom_registry
        self._atom_cache: typing.Dict[int, "Atom"] = OrderedDict()
        self._type_registry: "Registry" = type_registry

    def __iter_props__(self):
        if props := getattr(self, "properties", None):
            for prop in props:
                yield prop, getattr(self, prop)

    def __iter_atoms__(self):
        if hasattr(self, "slice"):
            next_start_pos = self.slice.start + self._header_size
        else:
            next_start_pos = 0

        while True:
            if hasattr(self, "slice") and next_start_pos >= self.slice.stop:
                break  # Reached the end of the slice
            self._handler.seek(next_start_pos)

            atom_size_bytes: bytes = self._handler.read(4)
            if not atom_size_bytes:
                break  # Reached the end of the file

            size: int = int.from_bytes(atom_size_bytes, byteorder="big")
            if size == 1:
                extended_size_bytes: bytes = self._handler.read(8)
                size = int.from_bytes(extended_size_bytes, byteorder="big")
            elif size == 0:
                curr_pos = self._handler.tell()
                size = self._handler.seek(0, 2) - next_start_pos
                self._handler.seek(curr_pos)

            end_pos: int = next_start_pos + size
            atom_type: str = self._handler.read(4).decode("utf-8").strip()
            atom: "Atom" = self._atom_registry[atom_type](
                atom_type,
                slice(next_start_pos, end_pos),
                self._handler,
                self._atom_registry,
                self._type_registry,
                self if issubclass(type(self), Iterator) else None
            )
            if hasattr(self, "_atom_cache"):
                max_key = max(self._atom_cache.keys()) if self._atom_cache else -1
                self._atom_cache[max_key + 1] = atom
            next_start_pos = end_pos  # Update next_start_pos with the end position
            yield atom

    def __iter__(self) -> typing.Iterator["Atom"]:
        """
        Make the Iterator object iterable.

        Yields:
        -------
        Atom
            The next atom in the file, including nested atoms.

        Raises:
        -------
        StopIteration
            If there are no more atoms in the file.

        Notes:
        ------
        - This method enables the iterator functionality, allowing iteration over atoms.
        - It reads the atom size, type, and other information from the file handler.
        """
        for prop in self.__iter_props__():
            yield prop
        if type(self).__name__ in ["Iterator", "Atom"]:
            for atom in self.__iter_atoms__():
                yield atom
        else:
            # Object is not an instance of Atom or Iterator, return an empty iterator
            return iter([])

    def __getitem__(
        self, handle: typing.Union[int, slice, str]
    ) -> typing.Union["Atom", typing.List["Atom"]]:
        """
        Get the atom(s) based on the provided handle.

        Parameters:
        -----------
        handle : Union[int, slice, str]
            The handle to retrieve the atom(s). It can be an integer, slice, or string.

        Returns:
        --------
        Union[Atom, List[Atom]]
            The atom(s) based on the handle.

        Notes:
        ------
        - This method allows retrieving atom(s) from the atom cache based on the provided handle.
        - The handle can be an index, slice, or atom type.
        """
        if not len(self._atom_cache):
            list(self)
        if isinstance(handle, int):
            return self._atom_cache[handle]
        elif isinstance(handle, slice):
            start, stop, step = handle.indices(len(self._atom_cache))
            return [self._atom_cache[i] for i in range(start, stop, step)]
        elif isinstance(handle, str):
            return [atom for _, atom in self._atom_cache.items() if atom.type == handle]
        else:
            raise ValueError("Invalid handle type.")
