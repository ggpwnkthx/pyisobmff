# File: isobmff/atoms/vmhd.py

from . import FullAtom

class VmhdAtom(FullAtom):
    """
    Class representing the 'vmhd' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'vmhd' atom.
    The 'vmhd' atom contains specific color and graphics mode information for video media.

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
        The version of the full atom.
    flags : bytes
        The flags of the full atom.

    graphics_mode : int
        The transfer mode specifying the Boolean operation for drawing or transferring an image.
    opcolor : Tuple[int, int, int]
        The red, green, and blue colors for the transfer mode operation.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'vmhd' atom.

    Example:
    --------
    ```
    # Create a Registry and register the VmhdAtom class
    reg = Registry()
    reg["vmhd"] = VmhdAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the VmhdAtom
    atom = iso[-1][0]
    print(atom.graphics_mode)  # Output: 128 (example value)
    print(atom.opcolor)        # Output: (255, 0, 0) (example values)
    ```
    """

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.properties.update(
            {
                "graphics_mode": {
                    "position": slice(0, 2),
                    "decoder": self._type_registry["int"],
                },
                "opcolor": {
                    "position": slice(2, 8),
                    "decoder": lambda _, data: (
                        int.from_bytes(data[:2], byteorder="big"),
                        int.from_bytes(data[2:4], byteorder="big"),
                        int.from_bytes(data[4:6], byteorder="big"),
                    ),
                },
            }
        )
