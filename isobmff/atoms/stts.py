# File: isobmff/atoms/stts.py

from . import FullAtom


class SttsAtom(FullAtom):
    """
    Class representing the 'stts' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'stts' atom.
    The 'stts' atom contains a table that defines the duration of each sample in the media.

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

    entry_count : int
        The number of entries in the time-to-sample table
    entries : List[Dict[str, int]]
        A list of dictionaries representing each entry in the time-to-sample table.
        Each dictionary contains 'sample_count' and 'sample_duration' fields.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'stts' atom.

    Example:
    --------
    ```
    # Create a Registry and register the SttsAtom class
    reg = Registry()
    reg["stts"] = SttsAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the SttsAtom
    atom = iso[-1][0]
    print(atom.version)                  # Output: 0 (example value)
    print(atom.entry_count)              # Output: 2 (example value)

    # Iterate over the time-to-sample table
    for entry in atom.entries:
        print(entry)
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
            self.entries.append(
                {
                    "count": int.from_bytes(self._handler.read(4), byteorder="big"),
                    "duration": int.from_bytes(self._handler.read(4), byteorder="big"),
                }
            )
            next_start_pos += 8  # Move to the next entry in the table
