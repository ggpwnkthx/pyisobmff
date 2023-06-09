# File: libs/utils/isobmff/atoms/tkhd.py

from . import FullAtom
from datetime import datetime, timedelta
import typing

if typing.TYPE_CHECKING:
    from ..registries import Registry


class TkhdAtom(FullAtom):
    """
    Class representing the 'tkhd' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'tkhd' atom.
    The 'tkhd' atom is commonly found in ISO Base Media Files and contains metadata about a track.

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
        A dictionary containing the properties of the 'tkhd' atom.

    Notes:
    ------
    This class inherits from the FullAtom class and extends it by adding properties specific to the 'tkhd' atom.
    The properties attribute is updated based on the version of the 'tkhd' atom (0 or 1).

    Example:
    --------
    ```
    # Create a Registry and register the TkhdAtom class
    reg = Registry()
    reg["tkhd"] = TkhdAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the TkhdAtom
    atom = iso[-1][0]
    print(atom.creation_time)          # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.modification_time)      # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.track_id)               # Output: 1
    print(atom.duration)               # Output: datetime.timedelta(seconds=120)
    print(atom.layer)                  # Output: 0
    print(atom.alternate_group)        # Output: 0
    print(atom.volume)                 # Output: 1.0
    print(atom.matrix)                 # Output: [65536, 0, 0, 0, 65536, 0, 0, 0, 1073741824]
    print(atom.track_width)            # Output: 1280
    print(atom.track_height)           # Output: 720
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
        match self.version:
            case 0:
                self.properties.update(
                    {
                        "creation_time": {
                            "position": slice(0, 4),
                            "decoder": self._type_registry["datetime"],
                        },
                        "modification_time": {
                            "position": slice(4, 8),
                            "decoder": self._type_registry["datetime"],
                        },
                        "track_id": {
                            "position": slice(8, 12),
                            "decoder": self._type_registry["int"],
                        },
                        "reserved_0": {
                            "position": slice(12, 16),
                            "decoder": lambda _, data: data,
                        },
                        "duration": {
                            "position": slice(16, 20),
                            "decoder": self._type_registry["int"],
                        },
                        "reserved_1": {
                            "position": slice(20, 24),
                            "decoder": lambda _, data: data,
                        },
                        "layer": {
                            "position": slice(24, 26),
                            "decoder": self._type_registry["int"],
                        },
                        "alternate_group": {
                            "position": slice(26, 28),
                            "decoder": self._type_registry["int"],
                        },
                        "volume": {
                            "position": slice(28, 30),
                            "decoder": lambda _, data: int.from_bytes(
                                data, byteorder="big"
                            )
                            / 256,
                        },
                        "reserved_3": {
                            "position": slice(30, 32),
                            "decoder": lambda _, data: data,
                        },
                        "matrix": {
                            "position": slice(32, 36),
                            "decoder": lambda _, data: [
                                int.from_bytes(data[i : i + 4], byteorder="big")
                                for i in range(0, len(data), 4)
                            ],
                        },
                        "width": {
                            "position": slice(36, 40),
                            "decoder": self._type_registry["int"],
                        },
                        "height": {
                            "position": slice(40, 44),
                            "decoder": self._type_registry["int"],
                        },
                    }
                )
            case 1:
                self.properties.update(
                    {
                        "creation_time": {
                            "position": slice(0, 8),
                            "decoder": self._type_registry["datetime"],
                        },
                        "modification_time": {
                            "position": slice(8, 16),
                            "decoder": self._type_registry["datetime"],
                        },
                        "track_id": {
                            "position": slice(16, 20),
                            "decoder": self._type_registry["int"],
                        },
                        "reserved_0": {
                            "position": slice(16, 20),
                            "decoder": lambda _, data: data,
                        },
                        "duration": {
                            "position": slice(20, 28),
                            "decoder": self._type_registry["int"],
                        },
                        "reserved_1": {
                            "position": slice(28, 32),
                            "decoder": lambda _, data: data,
                        },
                        "layer": {
                            "position": slice(32, 34),
                            "decoder": self._type_registry["int"],
                        },
                        "alternate_group": {
                            "position": slice(34, 36),
                            "decoder": self._type_registry["int"],
                        },
                        "volume": {
                            "position": slice(36, 38),
                            "decoder": lambda _, data: int.from_bytes(
                                data, byteorder="big"
                            )
                            / 256,
                        },
                        "reserved_2": {
                            "position": slice(38, 40),
                            "decoder": lambda _, data: data,
                        },
                        "matrix": {
                            "position": slice(40, 44),
                            "decoder": lambda _, data: [
                                int.from_bytes(data[i : i + 4], byteorder="big")
                                for i in range(0, len(data), 4)
                            ],
                        },
                        "width": {
                            "position": slice(44, 48),
                            "decoder": self._type_registry["int"],
                        },
                        "height": {
                            "position": slice(48, 52),
                            "decoder": self._type_registry["int"],
                        },
                    }
                )
