# File: isobmff/atoms/stsd.py

from . import FullAtom, Atom


class StsdAtom(FullAtom):
    """
    Class representing the 'stsd' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'stsd' atom.
    The 'stsd' atom stores information that allows decoding samples in the media.

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
        The version of the full atom.
    flags : bytes
        The flags of the full atom.

    entry_count : int
        The number of sample descriptions.

    sample_descriptions : List[Dict[str, Any]]
        A list of sample descriptions, where each description is represented by a dictionary.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'stsd' atom.

    Example:
    --------
    ```
    # Create a Registry and register the StsdAtom class
    reg = Registry()
    reg["stsd"] = StsdAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the StsdAtom
    atom = iso[-1][0]
    print(atom.entry_count)         # Output: 2 (example value)

    # Iterate over the sample descriptions
    for description in atom.sample_descriptions:
        print(description)
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
        self.entries = []
        next_start_pos = self.slice.start + self._header_size
        for i in range(self.entry_count):
            self._handler.seek(next_start_pos)
            atom_size: int = int.from_bytes(self._handler.read(4), byteorder="big")
            atom_type: str = self._handler.read(4).decode("utf-8").strip()
            end_pos: int = next_start_pos + atom_size
            atom = Entity(
                atom_type,
                slice(next_start_pos, end_pos),
                self._handler,
                self._atom_registry,
                self._type_registry,
            )
            self.entries.append(atom)
            next_start_pos = end_pos  # Update next_start_pos with the end position


class Entity(Atom):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.properties.update(
            {
                "reserved_0": {
                    "position": slice(0, 6),
                },
                "index": {
                    "position": slice(6, 8),
                    "decoder": self._type_registry["int"],
                },
                "data": {
                    "position": slice(8, None),
                }
            }
        )
