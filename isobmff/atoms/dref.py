from . import Atom

class DrefAtom(Atom):
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
        self.properties.update(
            {
                "version": {
                    "position": slice(8, 9),
                    "decoder": self._type_registry["int"],
                },
                "flags": {
                    "position": slice(9, 12),
                    "decoder": lambda _, data: data,
                },
                "entries": {
                    "position": slice(12, None),
                    "decoder": self._parse_data_references,
                },
            }
        )

    def _parse_data_references(self, _, data):
        references = []
        index = 0

        while index < len(data):
            size = self._type_registry["int"](None, data[index:index + 4])
            ref_type = self._type_registry["string"](None, data[index + 4:index + 8])
            version = self._type_registry["int"](None, data[index + 8])
            flags = data[index + 9:index + 12]
            self_reference = bool(flags[0] & 0x01)

            reference = DataReference(size, ref_type, version, flags, self_reference)
            references.append(reference)

            index += size

        return references


class DataReference:
    """
    Class representing a data reference in an ISO Base Media File.

    This class represents a data reference, which is a part of the data reference atom.
    Each data reference specifies the type and information about the media's data.

    Parameters:
    -----------
    size : int
        The size of the data reference.
    ref_type : str
        The type of the data reference.
    version : int
        The version of the data reference.
    flags : bytes
        The flags of the data reference.
    self_reference : bool
        Flag indicating if the media's data is in the same file as the movie atom.

    Attributes:
    -----------
    size : int
        The size of the data reference.
    ref_type : str
        The type of the data reference.
    version : int
        The version of the data reference.
    flags : bytes
        The flags of the data reference.
    self_reference : bool
        Flag indicating if the media's data is in the same file as the movie atom.

    Example:
    --------
    ```
    # Create a DataReference instance
    reference = DataReference(24, 'url ', 0, b'\x00\x00\x00', False)

    # Access the properties of the DataReference
    print(reference.size)            # Output: 24
    print(reference.ref_type)        # Output: 'url '
    print(reference.version)         # Output: 0
    print(reference.flags)           # Output: b'\x00\x00\x00'
    print(reference.self_reference)  # Output: False
    ```
    """

    def __init__(
        self,
        size: int,
        ref_type: str,
        version: int,
        flags: bytes,
        self_reference: bool,
    ) -> None:
        self.size = size
        self.ref_type = ref_type
        self.version = version
        self.flags = flags
        self.self_reference = self_reference
