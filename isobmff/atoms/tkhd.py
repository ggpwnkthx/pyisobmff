# File: isobmff/atoms/tkhd.py

from . import FullAtom


class TkhdAtom(FullAtom):
    """
    Class representing a Track Header (tkhd) atom in an ISO Base Media File Format (ISOBMFF).

    This class is a subclass of the FullAtom class and provides additional functionality for handling tkhd atoms.

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
    handler : typing.BinaryIO
        The file handler of the ISO Base Media File.
    properties : dict
        A dictionary containing additional properties of the atom.

    version : int
        The version of the full atom.
    flags : bytes
        The flags of the full atom.

    creation_time : datetime.datetime
        The creation time of the track.
    modification_time : datetime.datetime
        The modification time of the track.
    track_id : int
        The ID of the track.
    reserved_0 : bytes
        Reserved field in the 'tkhd' atom.
    duration : int
        The duration of the track.
    reserved_1 : bytes
        Reserved field in the 'tkhd' atom.
    layer : int
        The layer of the track.
    alternate_group : int
        The alternate group of the track.
    volume : float
        The volume of the track.
    reserved_2 : bytes
        Reserved field in the 'tkhd' atom (version 1).
    matrix : List[int]
        The transformation matrix of the track.
    width : int
        The width of the track.
    height : int
        The height of the track.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'tkhd' atom.
    - The properties attribute is updated based on the version of the 'tkhd' atom (0 or 1).

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
