# File: isobmff/atoms/elst.py

from . import FullAtom


class ElstAtom(FullAtom):
    """
    Class representing the 'elst' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'elst' atom.
    The 'elst' atom contains an edit list table, which is used in the timing of media data.

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
        
    entry_count : int
        The number of edit list entries in the 'elst' atom.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding functionality specific to the 'elst' atom.
    - The 'elst' atom contains an edit list table that provides timing information for media data.

    Example:
    --------
    ```
    # Create a Registry and register the ElstAtom class
    reg = Registry()
    reg["elst"] = ElstAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the 'elst' atom
    atom = iso[-1][0]

    # Iterate over the edit list entries
    for entry in atom:
        print(entry)
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
        self._header_size += 4

    def __iter__(self):
        super().__iter__()
        match self.version:
            case 0:
                size = 12
            case 1:
                size = 20
        
        for i in range(self.entry_count):
            start = i * size
            stop = start + size
            yield self._read_slice(slice(start,stop))

