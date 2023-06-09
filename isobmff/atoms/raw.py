# File: libs/utils/isobmff/atoms/raw.py

from . import Atom
import typing
if typing.TYPE_CHECKING:
    from ..registries import Registry


class RawAtom(Atom):
    """
    Class representing a raw atom in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for raw atoms.
    Raw atoms, such as 'free' and 'skip' atoms, are found in ISO Base Media Files and do not have specific parsing or decoding logic.

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
    properties : dict
        A dictionary containing the properties of the raw atom.

    Notes:
    ------
    This class inherits from the Atom class and extends it by adding the properties attribute specific to raw atoms.
    The properties attribute is left uninitialized and set to None in this class.

    Example:
    --------
    ```
    # Create a Registry and register the RawAtom class
    reg = Registry()
    reg["free"] = RawAtom
    reg["skip"] = RawAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of a RawAtom
    atom = iso[-1][0]
    print(atom.data)
    ```
    """

    def __init__(
        self,
        _type: str,
        _slice: slice,
        handler: typing.BinaryIO,
        atom_registry: "Registry" = None,
        type_registry: "Registry" = None,
    ) -> None:
        super().__init__(_type, _slice, handler, atom_registry, type_registry)
        self.properties.update({"data": None})
