# File: isobmff/atoms/mdhd.py

from . import FullAtom
from datetime import timedelta


class MdhdAtom(FullAtom):
    """
    Class representing the 'mdhd' atom in an ISO Base Media File.

    This class is a subclass of the FullAtom class and provides additional functionality for the 'mdhd' atom.
    The 'mdhd' atom contains metadata about a media track.

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

    creation_time : datetime.datetime
        The creation time of the media track.
    modification_time : datetime.datetime
        The modification time of the media track.
    timescale : int
        The time scale for the media track.
    duration : datetime.timedelta
        The duration of the media track.
    language : str
        The language of the media track.
    pre_defined : int
        A pre-defined value for the media track.

    Notes:
    ------
    - This class inherits from the FullAtom class and extends it by adding properties specific to the 'mdhd' atom.
    - The properties attribute is updated based on the version of the 'mdhd' atom (0 or 1).

    Example:
    --------
    ```
    # Create a Registry and register the MdhdAtom class
    reg = Registry()
    reg["mdhd"] = MdhdAtom

    # Create an Iterator instance for an ISO Base Media File
    iso = Iterator(open("path/to/file.mp4", "rb"), reg)

    # Access the properties of the MdhdAtom
    atom = iso[-1][0]
    print(atom.creation_time)       # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.modification_time)   # Output: datetime.datetime(2022, 6, 1, 12, 0, tzinfo=datetime.timezone.utc)
    print(atom.timescale)           # Output: 1000
    print(atom.duration)            # Output: datetime.timedelta(seconds=120)
    print(atom.language)            # Output: 'eng'
    print(atom.pre_defined)         # Output: 0
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
                        "language": {
                            "position": slice(16, 18),
                            "decoder": self._type_registry["lang"],
                        },
                        "pre_defined": {
                            "position": slice(18, 20),
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
                                seconds=self._type_registry["int"](None, data)
                                / self.timescale
                            ),
                        },
                        "language": {
                            "position": slice(28, 30),
                            "decoder": self._type_registry["lang"],
                        },
                        "pre_defined": {
                            "position": slice(30, 32),
                            "decoder": self._type_registry["int"],
                        },
                    }
                )
