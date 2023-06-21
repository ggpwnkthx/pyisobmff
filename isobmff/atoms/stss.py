# File: isobmff/atoms/stss.py

from . import FullAtom, Atom, Table

class StssAtom(FullAtom):
    """
    Class representing the 'stss' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'stss' atom.
    The 'stss' atom identifies key frames in the media. If no 'stss' atom exists, then all the samples are key frames.

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
        The number of entries in the sync sample table.
    entries : List[int]
        A list of sample numbers; each sample number corresponds to a key frame.
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
                "reserved_0": {
                    "position": slice(0, 6),
                },
                "index": {
                    "position": slice(6, 8),
                    "decoder": self._type_registry["int"],
                },
                "data": {
                    "position": slice(8, None),
                },
            }
        )