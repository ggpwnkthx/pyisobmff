# File: libs/utils/isobmff/atoms/full.py

from . import Atom
import typing

if typing.TYPE_CHECKING:
    from ..registries import Registry


class FullAtom(Atom):
    """
    Class representing a full atom in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for full atoms.
    Full atoms are commonly found in ISO Base Media Files and contain a version and flags in their headers.

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
    version : int
        The version of the full atom.
    flags : bytes
        The flags of the full atom.
    properties : dict
        A dictionary containing the properties of the full atom.

    Notes:
    ------
    This class inherits from the Atom class and extends it by adding version and flags properties specific to full atoms.
    The version is read as an integer from the first byte of the atom's slice, and the flags are read as a slice from the next three bytes.

    The properties attribute is updated to include the version and flags properties.

    Example:
    --------
    ```
    # Create a Registry and register the FullAtom class
    reg = Registry()
    reg["full"] = FullAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the version and flags properties
    print(iso[-1][0].version)  # Output: 1
    print(iso[-1][0].flags)    # Output: b'\x00\x10\x00'
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
        self.version = self._type_registry["int"](None, self._read_slice(slice(0, 1)))
        self.flags = self._type_registry["default"](None, self._read_slice(slice(1, 4)))
        self.properties.update({"version": None, "flags": None})
        self._header_size = 12
