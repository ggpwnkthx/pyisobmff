# File: libs/utils/isobmff/atoms/mvhd.py

from . import FullAtom
from datetime import datetime, timedelta
import typing

if typing.TYPE_CHECKING:
    from ..registries import Registry


class MvhdAtom(FullAtom):
    """
    Class representing the 'mvhd' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'mvhd' atom.
    The 'mvhd' atom is commonly found in ISO Base Media Files and contains metadata about the movie.

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
        A dictionary containing the properties of the 'mvhd' atom.

    Notes:
    ------
    This class inherits from the FullAtom class and extends it by adding properties specific to the 'mvhd' atom.
    The properties attribute is updated based on the version of the 'mvhd' atom (0 or 1).

    Example:
    --------
    ```
    # Create a Registry and register the MvhdAtom class
    reg = Registry()
    reg["mvhd"] = MvhdAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the MvhdAtom
    atom = iso[-1][0]
    print(atom.creation_time)      # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.modification_time)  # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.timescale)          # Output: 1000
    print(atom.duration)           # Output: datetime.timedelta(seconds=120)
    print(atom.rate)               # Output: 1
    print(atom.volume)             # Output: 0.5
    print(atom.reserved_0)         # Output: b'\x00\x00'
    print(atom.reserved_1)         # Output: b'\x00\x00\x00\x00'
    print(atom.matrix)             # Output: [65536, 0, 0, 0, 65536, 0, 0, 0, 1073741824]
    print(atom.pre_defined_0)      # Output: b'\x00\x00\x00\x00'
    print(atom.next_track_id)      # Output: 2
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
                        "timescale": {
                            "position": slice(8, 12),
                            "decoder": self._type_registry["int"],
                        },
                        "duration": {
                            "position": slice(12, 16),
                            "decoder": lambda _, data: timedelta(
                                seconds=self._type_registry["int"](None, data)
                                / self.timescale
                            ),
                        },
                        "rate": {
                            "position": slice(16, 20),
                            "decoder": lambda _, data: self._type_registry["int"],
                        },
                        "volume": {
                            "position": slice(20, 22),
                            "decoder": lambda _, data: self._type_registry["int"](
                                None, data
                            )
                            / 256,
                        },
                        "reserved_0": {
                            "position": slice(22, 24),
                            "decoder": lambda _, data: data,
                        },
                        "reserved_1": {
                            "position": slice(24, 28),
                            "decoder": lambda _, data: data,
                        },
                        "matrix": {
                            "position": slice(28, 32),
                            "decoder": lambda _, data: [
                                int.from_bytes(data[i : i + 4], byteorder="big")
                                for i in range(0, len(data), 4)
                            ],
                        },
                        "pre_defined_0": {
                            "position": slice(32, 36),
                            "decoder": lambda _, data: data,
                        },
                        "next_track_id": {
                            "position": slice(36, 40),
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
                        "timescale": {
                            "position": slice(16, 20),
                            "decoder": self._type_registry["int"],
                        },
                        "duration": {
                            "position": slice(20, 28),
                            "decoder": lambda _, data: timedelta(
                                seconds=self._type_registry["datetime"](None, data)
                                / self.timescale
                            ),
                        },
                        "rate": {
                            "position": slice(28, 32),
                            "decoder": self._type_registry["int"],
                        },
                        "volume": {
                            "position": slice(32, 34),
                            "decoder": lambda _, data: int.from_bytes(
                                data, byteorder="big"
                            )
                            / 256,
                        },
                        "reserved_0": {
                            "position": slice(34, 36),
                            "decoder": self._type_registry["default"],
                        },
                        "reserved_1": {
                            "position": slice(36, 40),
                            "decoder": self._type_registry["default"],
                        },
                        "matrix": {
                            "position": slice(40, 44),
                            "decoder": lambda _, data: [
                                int.from_bytes(data[i : i + 4], byteorder="big")
                                for i in range(0, len(data), 4)
                            ],
                        },
                        "pre_defined_0": {
                            "position": slice(44, 48),
                            "decoder": self._type_registry["default"],
                        },
                        "next_track_id": {
                            "position": slice(48, 52),
                            "decoder": self._type_registry["int"],
                        },
                    }
                )
