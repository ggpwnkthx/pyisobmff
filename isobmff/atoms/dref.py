# File: isobmff/atoms/dref.py

from . import FullAtom, Table


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

class Entry(FullAtom):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.properties.update({"data": {"position": slice(0, None)}})
