# File: isobmff/atoms/raw.py

from . import Atom


class RawAtom(Atom):
    """
    Class representing a raw atom in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for handling raw atoms.

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

    Notes
    -----
    - This class inherits from the Atom class and extends it by adding properties and methods for handling raw atoms.
    - This class acts as a placeholder for custom data associated with raw atoms.
    - The "data" property is intentionally left uninitialized and not read from the file handler. 

    Examples
    --------
    ```
    # Create a Registry and register the RawAtom class
    reg = Registry()
    reg["free"] = RawAtom
    reg["skip"] = RawAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the RawAtom
    atom = iso[-1][0]
    print(atom.type)                  # Output: 'raw' (example value)
    print(atom.size)                  # Output: 1024 (example value)
    ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initialize a new RawAtom object.

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
        self.properties.update({"data": None})
