# File: isobmff/atoms/table.py

from . import Atom

class Table(Atom):
    """
    Class representing a table of atoms in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for handling tables of atoms.

    Parameters
    ----------
    _type : str
        The type of the atom.
    _slice : slice
        The slice representing the start and end positions of the atom in the file.
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    atom_registry : Registry, optional
        The atom registry used to resolve atom classes (default: None).
    type_registry : Registry, optional
        The type registry used to resolve type classes (default: None).
    parent : Atom, optional
        The parent atom of this atom (default: None).
    entry_type : type, optional
        The class to use for entries in the table (default: None).

    Attributes
    ----------
    type : str
        The type of the atom.
    slice : slice
        The slice representing the start and end positions of the atom in the file.
    size : int
        The size of the atom.
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    properties : dict
        A dictionary containing additional properties of the atom.
    parent : Atom
        The parent atom of this atom.
    entry_type : type
        The class to use for entries in the table.

    Notes
    -----
    - This class inherits from the Atom class and extends it by adding properties and methods for handling tables of atoms.
    - Generally this class should not be used directly and should only be used inside of other classes that have tabular entries.

    Examples
    --------
    ```
    class CustomAtom(FullAtom)
        def __init__(
            self,
            *args,
            **kwargs,
        ) -> None:
            super().__init__(*args, **kwargs)
            self.properties.update({"entry_count": None, "entries": None})
            self.entry_count = self._type_registry["int"](
                None, self._read_slice(slice(0, 4))
            )
            self._header_size += 4
            self.entries = Table(
                None,
                slice(self.slice.start + self._header_size, self.slice.stop),
                self._handler,
                self._atom_registry,
                self._type_registry,
                self,
                entry_type=Entry,
            )

    class Entry(Atom):
        size = 4

        def __init__(
            self,
            *args,
            **kwargs,
        ) -> None:
            super().__init__(*args, **kwargs)
            self._header_size = 0
            self.properties.update(
                {
                    "offset": {
                        "position": slice(0, 4),
                        "decoder": self._type_registry["int"],
                    },
                }
            )
    ```
    """

    def __init__(self, *args, entry_type, **kwargs):
        super().__init__(*args, **kwargs)
        self._header_size = 0
        self._entry_type = entry_type
        self._entry_slices = []
        if size := getattr(entry_type, "size", None):
            for index in range(self._parent.entry_count):
                start = self.slice.start + self._header_size + (index * size)
                self._entry_slices.append(slice(start, start + size))
        else:
            for index in range(self._parent.entry_count):
                if index == 0:
                    start = self.slice.start + self._header_size
                else:
                    start = (
                        self.slice.start
                        + self._header_size
                        + self._entry_slices[index - 1].size
                    )
                self._handler.seek(start)
                size = int.from_bytes(self._handler.read(4), byteorder="big")
                self._entry_slices.append(slice(start, start + size))

    def __getitem__(self, index: int):
        if index < 0:
            index = self._parent.entry_count + index
        if index > (self._parent.entry_count - 1):
            raise IndexError()
        if index not in self._atom_cache.keys():
            self._atom_cache[index] = self._entry_type(
                None,
                self._entry_slices[index],
                self._handler,
                self._atom_registry,
                self._type_registry,
                self,
            )
        return self._atom_cache[index]

    def __iter__(self):
        for index in range(self._parent.entry_count):
            yield self[index]