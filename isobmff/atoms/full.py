# File: isobmff/atoms/full.py

from . import Atom


class FullAtom(Atom):
    """
    Class representing a full atom in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for handling full atoms.

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
    version : int
        The version of the atom.
    flags : bytes
        The flags of the atom.

    Notes
    -----
    - This class inherits from the Atom class and extends it by adding properties and methods for handling full atoms.

    Examples
    --------
    ```
    # Create a Registry and register the FullAtom class
    reg = Registry()
    reg["full"] = FullAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the FullAtom
    atom = iso[-1][0]
    print(atom.type)                  # Output: 'full' (example value)
    print(atom.size)                  # Output: 1024 (example value)
    print(atom.version)               # Output: 1 (example value)
    print(atom.flags)                 # Output: b'\x00\x00\x01' (example value)
    ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initialize a new FullAtom object.

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
        parent : Atom, optional
            The parent atom of this atom (default: None).
        """
        super().__init__(*args, **kwargs)
        self.version = self._type_registry["int"](None, self._read_slice(slice(0, 1)))
        self.flags = self._type_registry["default"](None, self._read_slice(slice(1, 4)))
        self.properties.update({"version": None, "flags": None})
        self._header_size += 4
