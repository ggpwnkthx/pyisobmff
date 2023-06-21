# File: isobmff/atoms/sbgp.py

from . import FullAtom, Atom, Table


class SbgpAtom(FullAtom):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.grouping_type = int.from_bytes(
            self._read_slice(slice(0, 4)), byteorder="big"
        )
        self.properties.update({"grouping_type": None})
        self._header_size += 4
        
        if self.version == 1:
            self.grouping_type_parameter = int.from_bytes(
                self._read_slice(slice(0, 4)), byteorder="big"
            )
            self.properties.update({"grouping_type_parameter": None})
            self._header_size += 4
        
        self.entry_count = int.from_bytes(
            self._read_slice(slice(0, 4)), byteorder="big"
        )
        self._header_size += 4
        self.entries = Table(
            None,
            slice(self.slice.start + self._header_size, self.slice.stop),
            self._handler,
            self._atom_registry,
            self._type_registry,
            self,
            entry_type=Entry,
        )
        self.properties.update({"entry_count": None, "entries": None})


class Entry(Atom):
    size = 16

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._header_size = 0
        if self._parent.version == 1:
            if self._parent.default_length == 0:
                self.default_length = int.from_bytes(
                    self._read_slice(slice(0, 4)), byteorder="big"
                )
                self.properties.update({"default_length": None})
                self._header_size += 4
                
        self.properties.update(
            {
                "sample_count": {
                    "position": slice(0, 4),
                    "decoder": self._type_registry["int"],
                },
                "group_description_index": {
                    "position": slice(4, 8),
                    "decoder": self._type_registry["int"],
                },
            }
        )
