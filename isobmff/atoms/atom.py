# File: isobmff/atoms/atom.py

from ..iterator import Iterator
import typing

if typing.TYPE_CHECKING:
    from ..registries import Registry


class Atom(Iterator):
    """
    Class representing an atom in an ISO Base Media File.

    Parameters:
    -----------
    _type : str
        The type of the atom.
    _slice : slice
        The slice representing the start and end positions of the atom in the file.
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    atom_registry : typing.Type["Registry"], optional
        The atom registry used to resolve atom classes (default: None).
    type_registry : typing.Type["Registry"], optional
        The type registry used to resolve type classes (default: None).

    Attributes:
    -----------
    type : str
        The type of the atom.
    slice : slice
        The slice representing the start and end positions of the atom in the file.
    size : int
        The size of the atom.
    properties : dict
        A dictionary containing additional properties of the atom.

    Notes:
    ------
    - An atom represents a unit of data within an ISO Base Media File.
    - The `_type` parameter specifies the type of the atom.
    - The `_slice` parameter represents the range of bytes in the file occupied by the atom.
    - The `handler` parameter is the file handler for the ISO Base Media File.
    - The `atom_registry` parameter allows customization of atom class resolution (optional).
    - The `type_registry` parameter allows customization of type class resolution (optional).
    - The `type`, `slice`, `size`, and `properties` attributes provide information about the atom.
    - The `properties` dictionary contains additional attributes of the atom.

    """

    def __init__(
        self,
        _type: str,
        _slice: slice,
        handler: typing.BinaryIO,
        atom_registry: typing.Type["Registry"] = None,
        type_registry: typing.Type["Registry"] = None,
    ) -> None:
        """
        Initialize a new Atom object.

        Parameters:
        -----------
        _type : str
            The type of the atom.
        _slice : slice
            The slice representing the start and end positions of the atom in the file.
        handler : typing.BinaryIO
            The file handler of the ISO Base Media File.
        atom_registry : typing.Type["Registry"], optional
            The atom registry used to resolve atom classes (default: None).
        type_registry : typing.Type["Registry"], optional
            The type registry used to resolve type classes (default: None).
        """
        super().__init__(handler, atom_registry, type_registry)
        self.type = _type
        self.slice = _slice
        self.size = _slice.stop - _slice.start
        self.properties = {
            "type": None,
            "slice": None,
            "size": None,
        }
        self._header_size = 8

    def __repr__(self) -> str:
        """
        Return a string representation of the Atom object.

        Returns:
        --------
        str
            A string representation of the Atom object.

        Notes:
        ------
        - This method returns a string that represents the Atom object.
        - The string includes the properties of the Atom object.
        """
        attrs = [f"{key}={value}" for key, value in self.properties.items() if value is not None]
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def _read_slice(self, _slice: slice = slice(None)) -> bytes:
        """
        Read and return the data from the specified slice within the atom.

        Parameters:
        -----------
        _slice : slice, optional
            The slice representing the range of data to read from the atom (default: slice(None)).

        Returns:
        --------
        bytes
            The data read from the specified slice within the atom.

        Raises:
        -------
        ValueError
            If the specified slice exceeds the available data range of the atom.

        Notes:
        ------
        - This method reads the data from the specified slice within the atom.
        - The `_slice` parameter represents the range of bytes to read.
        - The method returns the data as a bytes object.
        - If the specified slice exceeds the available data range of the atom, a ValueError is raised.
        """
        start = self.slice.start + self._header_size + (_slice.start or 0)
        stop = (
            self.slice.stop
            if _slice.stop is None
            else start + (_slice.stop - _slice.start)
        )

        if stop > self.slice.stop:
            raise ValueError(f"Slice ({start},{stop}) exceeds the available data range of the atom ({self.slice.start},{self.slice.stop}).")

        self._handler.seek(start)
        return self._handler.read(stop - start)

    def __getattr__(self, name: str) -> typing.Any:
        """
        Retrieve and return the value of the specified attribute from the atom.

        Parameters:
        -----------
        name : str
            The name of the attribute to retrieve.

        Returns:
        --------
        Any
            The value of the specified attribute from the atom.

        Raises:
        -------
        TypeError
            If the attribute is not found.

        Notes:
        ------
        - This method retrieves and returns the value of the specified attribute from the atom specified in its `properties` dictionary.
        - If the attribute is not found, a TypeError is raised.
        """
        if prop := self.properties.get(name):
            data = self._read_slice(prop.get("position"))
            if callable(func := prop.get("decoder")):
                data = func(self, data)

            setattr(self, name, data)
            return data
        if name != "data":
            raise TypeError(f"Attribute '{name}' not found")
