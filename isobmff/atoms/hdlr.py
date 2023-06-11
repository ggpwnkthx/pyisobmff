# File: isobmff/atoms/hdlr.py

from . import FullAtom


class HdlrAtom(FullAtom):
    """
    Class representing the 'hdlr' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'hdlr' atom.
    The 'hdlr' atom specifies the media handler component that is to be used to interpret the media's data.

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

    component_type : str
        The component type of the handler reference atom.
    component_subtype : str
        The component subtype of the handler reference atom.
    component_manufacturer : str
        The component manufacturer of the handler reference atom.
    component_flags : bytes
        The component flags of the handler reference atom.
    component_flags_mask : bytes
        The component flags mask of the handler reference atom.
    component_name : str
        The name of the component.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'hdlr' atom.

    Example:
    --------
    ```
    # Create a Registry and register the HdlrAtom class
    reg = Registry()
    reg["hdlr"] = HdlrAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the HdlrAtom
    atom = iso[-1][0]
    print(atom.component_type)         # Output: 'mhlr'
    print(atom.component_subtype)      # Output: 'vide'
    print(atom.component_manufacturer) # Output: 'OpenAI'
    print(atom.component_flags)        # Output: 'flag'
    print(atom.component_flags_mask)   # Output: 'mask'
    print(atom.component_name)         # Output: 'Video Handler'
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
                "component_type": {
                    "position": slice(0, 4),
                    "decoder": self._type_registry["string"],
                },
                "component_subtype": {
                    "position": slice(4, 8),
                    "decoder": self._type_registry["string"],
                },
                "component_manufacturer": {
                    "position": slice(8, 12),
                    "decoder": self._type_registry["string"],
                },
                "component_flags": {
                    "position": slice(12, 16),
                    "decoder": lambda _, data: data,
                },
                "component_flags_mask": {
                    "position": slice(16, 20),
                    "decoder": lambda _, data: data,
                },
                "component_name": {
                    "position": slice(20, None),
                    "decoder": self._type_registry["string"],
                },
            }
        )
