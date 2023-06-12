from . import FullAtom


class DrefAtom(FullAtom):
    """
    Class representing the 'dref' atom in an ISO Base Media File.

    This class extends the Atom class and represents the data reference atom.
    The data reference atom contains tabular data that instructs the data handler component how to access the media's data.

    Parameters:
    -----------
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

    Attributes:
    -----------
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

    version : int
        The version of the atom.
    flags : bytes
        The flags of the atom.

    entries : List[DataReference]
        The data references.

    Notes:
    ------
    - This class extends the Atom class and represents the 'dref' atom.

    Example:
    --------
    ```
    # Create a Registry and register the DataReferenceAtom class
    reg = Registry()
    reg["dref"] = DataReferenceAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the DataReferenceAtom
    atom = iso[-1][0]
    print(atom.version)    # Output: 0 (example value)
    print(atom.entries)    # Output: [DataReference, DataReference, ...] (example values)
    ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.entry_count = self._type_registry["int"](
            None, self._read_slice(slice(0, 4))
        )
        self.properties.update({"entry_count": None})
        self._header_size += 4

    def __iter_entries__(self):
        if hasattr(self, "slice"):
            next_start_pos = self.slice.start + self._header_size
            print(f"checking for atoms @{next_start_pos}")
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
            atom: "Entity" = Entity(
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

    def __iter__(self):
        for item in super().__iter__():
            yield item
        for entry in self.__iter_entries__():
            yield entry


class Entity(FullAtom):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.properties.update({"data": {"position": slice(0, None)}})
