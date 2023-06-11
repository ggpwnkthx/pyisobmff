from . import FullAtom, Atom


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

    Attributes:
    -----------
    entry_count : int
        The number of entries in the edit list table.
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

