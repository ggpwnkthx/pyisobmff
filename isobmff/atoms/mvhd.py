# File: isobmff/atoms/mvhd.py

from . import FullAtom
from datetime import timedelta


class MvhdAtom(FullAtom):
    """
    Class representing a Movie Header ('mvhd') atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for handling 'mvhd' atoms.

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

    version : int
        The version of the full atom.
    flags : bytes
        The flags of the full atom.

    creation_time : datetime.datetime
        The creation time of the movie.
    modification_time : datetime.datetime
        The modification time of the movie.
    timescale : int
        The time scale of the movie.
    duration : datetime.timedelta
        The duration of the movie.
    rate : int
        The rate of the movie.
    volume : float
        The volume of the movie.
    reserved_0 : bytes
        Reserved field in the 'mvhd' atom.
    reserved_1 : bytes
        Reserved field in the 'mvhd' atom.
    matrix : List[int]
        The transformation matrix of the movie.
    pre_defined_0 : bytes
        Pre-defined field in the 'mvhd' atom.
    next_track_id : int
        The next available track ID for the movie.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'mvhd' atom.
    - The properties attribute is updated based on the version of the 'mvhd' atom (0 or 1).

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
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
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
                            "decoder": self._type_registry["int"],
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
