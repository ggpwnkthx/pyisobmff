# File: libs/utils/isobmff/iterator.py

from .registries.types import DECODERS
import logging
import typing

if typing.TYPE_CHECKING:
    from .atoms import Atom
    from .registries import Registry


class Iterator:
    """
    Class responsible for parsing an ISO Base Media File and iterating over the atoms.

    Parameters:
    -----------
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    atom_registry : Registry, optional
        The atom registry used to resolve atom classes (default: an empty Registry).

    Attributes:
    -----------
    _handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    _atom_registry : Registry
        The atom registry used to resolve atom classes.
    _atom_cache : typing.List[Atom]
        A list to cache the parsed atoms for faster access.
    """

    def __init__(
        self,
        handler: typing.BinaryIO,
        atom_registry: typing.Type["Registry"],
        type_registry: typing.Type["Registry"] = DECODERS,
    ) -> None:
        """
        Initialize a new Iterator object.

        Parameters:
        -----------
        handler : typing.BinaryIO
            The file handler of the ISO Base Media File.
        atom_registry : Registry, optional
            The atom registry used to resolve atom classes (default: an empty Registry).
        """
        self._handler: typing.BinaryIO = handler
        self._atom_registry: typing.Type["Registry"] = atom_registry
        self._atom_cache: typing.List[typing.Type["Atom"]] = []
        self._type_registry: typing.Type["Registry"] = type_registry

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
        """

        if type(self).__name__ in ["Iterator", "Atom"]:
            logging.debug(type(self))
            if hasattr(self, "slice"):
                logging.debug(self.type)
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
                atom_type: str = self._handler.read(4).decode("utf-8")
                atom: "Atom" = self._atom_registry[atom_type](
                    atom_type,
                    slice(next_start_pos, end_pos),
                    self._handler,
                    self._atom_registry,
                    self._type_registry,
                )
                if hasattr(self, "_atom_cache"):
                    self._atom_cache.append(atom)
                next_start_pos = end_pos  # Update next_start_pos with the end position
                yield atom
        else:
            # Object is not an instance of Atom or Iterator, return an empty iterator
            if props := getattr(self, "properties", None):
                for prop in props:
                    yield prop, getattr(self, prop)
            else:
                return iter([])

    def __getitem__(
        self, handle: typing.Union[int, slice, str]
    ) -> typing.Union["Atom", typing.List["Atom"]]:
        """
        Get the atom(s) from the index based on the provided handle.

        Parameters:
        -----------
        handle : Union[int, slice, str]
            The handle to retrieve the atom(s). It can be an integer, slice, or string.

        Returns:
        --------
        Union[Atom, List[Atom]]
            The atom(s) from the index based on the handle.
        """
        if not len(self._atom_cache):
            list(self)
        if isinstance(handle, int) or isinstance(handle, slice):
            return self._atom_cache[handle]
        elif isinstance(handle, str):
            return [atom for atom in self._atom_cache if atom.type == handle]
        else:
            raise ValueError("Invalid handle type.")
