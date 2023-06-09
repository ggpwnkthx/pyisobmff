# File: libs/utils/isobmff/atoms/atom.py

from ..iterator import Iterator
import typing

if typing.TYPE_CHECKING:
    from ..registries import Registry


class Atom(Iterator):
    """
    Class representing an atom in an ISO Base Media File.

    Parameters:
    -----------
    type : str
        The type of the atom.
    slice : slice
        The slice representing the start and end positions of the atom in the file.
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.

    Attributes:
    -----------
    type : str
        The type of the atom.
    slice : slice
        The slice representing the start and end positions of the atom in the file.
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    """

    def __init__(
        self,
        _type: str,
        slice: slice,
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
        slice : slice
            The slice representing the start and end positions of the atom in the file.
        handler : typing.BinaryIO
            The file handler of the ISO Base Media File.
        atom_registry : Registry, optional
            The atom registry used to resolve atom classes (default: None).
        """
        super().__init__(handler, atom_registry, type_registry)
        self.type: str = _type
        self.slice: slice = slice
        self.size: int = slice.stop - slice.start
        self.properties: dict = {
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
        """
        attrs = [
            f"{key}={value}" for key in self.properties if (value := getattr(self, key))
        ]
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
        """
        start = self.slice.start + self._header_size + (_slice.start or 0)
        stop = (
            self.slice.stop
            if _slice.stop is None
            else start + (_slice.stop - _slice.start)
        )

        if stop > self.slice.stop:
            raise ValueError("Slice exceeds the available data range of the atom.")

        self._handler.seek(start)
        return self._handler.read(stop - start)

    def __getattr__(self, name):
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
        """
        if prop := self.properties.get(name, None):
            if prop is None:
                prop = {}

            data = self._read_slice(prop.get("position", None))

            if callable(func := prop.get("decoder", None)):
                data = func(self, data)

            setattr(self, name, data)
            return data

        raise TypeError(f"Attribute '{name}' not found")
