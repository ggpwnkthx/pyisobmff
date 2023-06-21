# File: isobmff/atoms/table.py

from . import Atom

class Table(Atom):
    def __init__(self, *args, entry_type, **kwargs):
        super().__init__(*args, **kwargs)
        self._header_size = 0
        self._entry_type = entry_type
        self._entry_slices = []
        if size := getattr(entry_type, "size", None):
            for index in range(self._parent.entry_count):
                start = self.slice.start + self._header_size + (index * size)
                self._entry_slices.append(slice(start, start + size))
        else:
            for index in range(self._parent.entry_count):
                if index == 0:
                    start = self.slice.start + self._header_size
                else:
                    start = (
                        self.slice.start
                        + self._header_size
                        + self._entry_slices[index - 1].size
                    )
                self._handler.seek(start)
                size = int.from_bytes(self._handler.read(4), byteorder="big")
                self._entry_slices.append(slice(start, start + size))

    def __getitem__(self, index: int):
        if index < 0:
            index = self._parent.entry_count + index
        if index > (self._parent.entry_count - 1):
            raise IndexError()
        if index not in self._atom_cache.keys():
            self._atom_cache[index] = self._entry_type(
                None,
                self._entry_slices[index],
                self._handler,
                self._atom_registry,
                self._type_registry,
                self,
            )
        return self._atom_cache[index]

    def __iter__(self):
        for index in range(self._parent.entry_count):
            yield self[index]