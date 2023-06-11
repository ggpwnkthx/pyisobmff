# File: isobmff/atoms/type.py

from .atom import Atom


class TypeAtom(Atom):
    """
    Class representing a type atom in an ISO Base Media File.

    This class is a subclass of the Atom class and provides additional functionality for type atoms.
    Type atoms, such as 'ftyp' and 'styp' atoms, contain information about the file's type and compatibility.

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

    major_brand : str
        The major brand of the file.
    minor_version : int
        The minor version of the file.
    compatible_brands : List[str]
        A list of compatible brands for the file.

    Notes:
    ------
    This class inherits from the Atom class and extends it by adding properties specific to type atoms.
    
    The 'major_brand' is read as a utf-8 string from the first 4 bytes of the atom's slice.
    The 'minor_version' is read as in integer from the next 4 bytes.
    The 'compatible_brands' is read as a list of utf-8 strings until the end of the atom's slice.
    
    The properties attribute is updated to include the 'major_brand', 'minor_version', and 'compatible_brands' properties.

    Example:
    --------
    ```
    # Create a Registry and register the TypeAtom class
    reg = Registry()
    reg["ftyp"] = TypeAtom
    reg["styp"] = TypeAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the TypeAtom
    atom = iso[0]
    print(atom.major_brand)        # Output: 'isom'
    print(atom.minor_version)      # Output: 512
    print(atom.compatible_brands)  # Output: ['isom', 'iso2', 'avc1']
    ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Initialize a new TypeAtom object.

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
        super().__init__(*args, **kwargs)
        self.properties.update(
            {
                "major_brand": {
                    "position": slice(0, 4),
                    "decoder": lambda _, data: data.decode("utf-8"),
                },
                "minor_version": {
                    "position": slice(4, 8),
                    "decoder": self._type_registry["int"],
                },
                "compatible_brands": {
                    "position": slice(8, None),
                    "decoder": lambda _, data: [
                        data[i : i + 4].decode("utf-8") for i in range(0, len(data), 4)
                    ],
                },
            }
        )
