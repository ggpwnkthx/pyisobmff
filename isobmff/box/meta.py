"""
File: isobmff/box/meta.py

Contains all the classes specified in section 8.11 of ISO/IEC 14496-12:2015
"""
from isobmff.slice import Slice
from . import BOX_TYPES, Box, FullBox, ChildlessBox, Slice, CachedIterator
import functools
import typing


class MetaBox(FullBox):
    @functools.cached_property
    def handler_type(self) -> str:
        start = super().header_size
        return self.slice.subslice(start, start + 4).decode()

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class XMLBox(FullBox, ChildlessBox):
    @functools.cached_property
    def handler_type(self) -> str:
        start = super().header_size
        return self.slice.subslice(start).decode(terminator="\x00")

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class BinaryXMLBox(FullBox, ChildlessBox):
    @functools.cached_property
    def handler_type(self) -> str:
        start = super().header_size
        return self.slice.subslice(start, self.end).read()

    @property
    def header_size(self) -> int:
        return super().header_size + 4


class ItemLocationBox(FullBox):
    @functools.cached_property
    def offset_size(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 1).unpack(">B")[0] >> 4

    @functools.cached_property
    def length_size(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 1).unpack(">B")[0] & 0xF

    @functools.cached_property
    def base_offset_size(self) -> int:
        start = super().header_size + 1
        if self.version == 1 or self.version == 2:
            return self.slice.subslice(start, start + 1).unpack(">B")[0] >> 4
        return None

    @functools.cached_property
    def index_size(self) -> int:
        start = super().header_size + 1
        if self.version == 1 or self.version == 2:
            return self.slice.subslice(start, start + 1).unpack(">B")[0] & 0xF
        return None

    @functools.cached_property
    def item_count(self) -> int:
        start = super().header_size + 2
        if self.version == 0 or self.version == 1:
            return self.slice.subslice(start, start + 2).unpack(">H")[0]
        elif self.version == 2:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def items(self) -> int:
        if self.version == 0 or self.version == 1:
            start = super().header_size + 4
        elif self.version == 2:
            start = super().header_size + 6
        return CachedIterator(
            self.slice.subslice(start, self.end),
            lambda this: ItemLocationEntry(this.slice, self),
            self.item_count,
        )

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 4
        elif self.version == 1 or self.version == 2:
            return super().header_size + 6


class ItemLocationEntry:
    def __init__(self, slice: Slice, parent: ItemLocationBox) -> None:
        self.slice = slice
        self.parent = parent

    @functools.cached_property
    def item_ID(self):
        if self.parent.version == 0 or self.parent.version == 1:
            return self.slice.subslice(0, 2).unpack(">H")[0]
        elif self.parent.version == 2:
            return self.slice.subslice(0, 4).unpack(">I")[0]

    @functools.cached_property
    def construction_method(self):
        if self.parent.version == 0:
            return None
        elif self.parent.version == 1:
            return self.slice.subslice(2, 4).read()
        elif self.parent.version == 2:
            return self.slice.subslice(4, 6).read()

    @functools.cached_property
    def data_reference_index(self):
        if self.parent.version == 0:
            return self.slice.subslice(2, 4).unpack(">H")[0]
        elif self.parent.version == 1:
            return self.slice.subslice(4, 6).unpack(">H")[0]
        elif self.parent.version == 2:
            return self.slice.subslice(6, 8).unpack(">H")[0]

    @functools.cached_property
    def base_offset(self):
        if self.parent.version == 0:
            start = 4
        elif self.parent.version == 1:
            start = 6
        elif self.parent.version == 2:
            start = 8

        if self.parent.base_offset_size == 0:
            return 0
        elif self.parent.base_offset_size == 4:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]
        elif self.parent.base_offset_size == 8:
            return self.slice.subslice(start, start + 8).unpack(">Q")[0]

    @functools.cached_property
    def extent_count(self):
        if self.parent.version == 0:
            start = 4 + self.parent.base_offset_size
        elif self.parent.version == 1:
            start = 6 + self.parent.base_offset_size
        elif self.parent.version == 2:
            start = 8 + self.parent.base_offset_size

        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def extent_size(self) -> int:
        size = self.parent.offset_size + self.parent.length_size
        if self.parent.version == 1:
            if self.parent.index_size > 0:
                size += self.parent.index_size
        elif self.parent.version == 2:
            if self.parent.index_size > 0:
                size += self.parent.index_size
        return size

    @functools.cached_property
    def extents(self) -> int:
        if self.parent.version == 0:
            start = 4 + self.parent.base_offset_size + 2
        elif self.parent.version == 1:
            start = 6 + self.parent.base_offset_size + 2
        elif self.parent.version == 2:
            start = 8 + self.parent.base_offset_size + 2
        return CachedIterator(
            self.slice.subslice(start, start + self.extent_size * self.extent_count),
            lambda this: ItemLocationEntryExtent(this.slice, self),
            self.extent_count,
        )

    @functools.cached_property
    def size(self) -> int:
        if self.parent.version == 0:
            size = 4 + self.parent.base_offset_size + 2
        elif self.parent.version == 1:
            size = 6 + self.parent.base_offset_size + 2
        elif self.parent.version == 2:
            size = 8 + self.parent.base_offset_size + 2
        return size + self.extent_size * self.extent_count


class ItemLocationEntryExtent:
    def __init__(self, slice: Slice, parent: ItemLocationEntry) -> None:
        self.slice = slice
        self.parent = parent

    @functools.cached_property
    def extent_index(self):
        if self.parent.parent.version == 1 or self.parent.parent.version == 2:
            if self.parent.parent.index_size == 4:
                return self.slice.subslice(0, 4).unpack(">I")[0]
            elif self.parent.parent.index_size == 8:
                return self.slice.subslice(0, 8).unpack(">Q")[0]
        return None

    @functools.cached_property
    def extent_offset(self):
        start = 0
        if self.parent.parent.index_size:
            start += self.parent.parent.index_size
        if self.parent.parent.offset_size == 4:
            return self.slice.subslice(0, 4).unpack(">I")[0]
        elif self.parent.parent.offset_size == 8:
            return self.slice.subslice(0, 8).unpack(">Q")[0]
        return 0

    @functools.cached_property
    def extent_length(self):
        start = self.parent.parent.offset_size
        if self.parent.parent.index_size:
            start += self.parent.parent.index_size
        if self.parent.parent.length_size == 4:
            return self.slice.subslice(0, 4).unpack(">I")[0]
        elif self.parent.parent.length_size == 8:
            return self.slice.subslice(0, 8).unpack(">Q")[0]
        return 0

    @functools.cached_property
    def size(self):
        return self.parent.extent_size


class PrimaryItemBox(FullBox):
    @functools.cached_property
    def item_ID(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 2).unpack(">H")
        elif self.version == 1:
            return self.slice.subslice(start, start + 4).unpack(">I")

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return super().header_size + 2
        elif self.version == 1:
            return super().header_size + 4


class ItemProtectionBox(FullBox):
    @functools.cached_property
    def protection_count(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def has_children(self):
        return self.protection_count > 0


class ItemInfoExtension:
    pass


class FDItemInfoExtension(ItemInfoExtension):
    pass


class ItemInfoEntry(FullBox):
    @functools.cached_property
    def item_ID(self) -> int:
        start = super().header_size
        if self.version == 0 or self.version == 1 or self.version == 2:
            return self.slice.subslice(start, start + 2).unpack(">H")[0]
        elif self.version == 3:
            return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def item_protection_index(self) -> int:
        if self.version == 0 or self.version == 1 or self.version == 2:
            start = super().header_size + 2
            return self.slice.subslice(start, start + 2).unpack(">H")[0]
        elif self.version == 3:
            start = super().header_size + 4
            return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def item_type(self) -> str:
        if self.version == 0 or self.version == 1:
            return None
        elif self.version == 2:
            start = super().header_size + 4
        elif self.version == 3:
            start = super().header_size + 8
        return self.slice.subslice(start, start + 4).decode()

    @functools.cached_property
    def item_name(self) -> str:
        if self.version == 0 or self.version == 1:
            start = super().header_size + 4
        elif self.version == 2:
            start = super().header_size + 8
        elif self.version == 3:
            start = super().header_size + 10
        return self.slice.subslice(start).decode(terminator="\x00")

    @functools.cached_property
    def content_type(self) -> str:
        if self.version == 0 or self.version == 1:
            start = super().header_size + 5 + len(self.item_name)
        elif self.version == 2:
            if self.item_type != "mime":
                return None
            start = super().header_size + 9 + len(self.item_name)
        elif self.version == 3:
            if self.item_type != "mime":
                return None
            start = super().header_size + 11 + len(self.item_name)
        return self.slice.subslice(start).decode(terminator="\x00")

    @functools.cached_property
    def content_encoding(self) -> str:
        if self.version == 0 or self.version == 1:
            start = (
                super().header_size + 6 + len(self.item_name) + len(self.content_type)
            )
        elif self.version == 2:
            if self.item_type != "mime":
                return None
            start = (
                super().header_size + 10 + len(self.item_name) + len(self.content_type)
            )
        elif self.version == 3:
            if self.item_type != "mime":
                return None
            start = (
                super().header_size + 12 + len(self.item_name) + len(self.content_type)
            )
        if start < self.end:
            return self.slice.subslice(start).decode(terminator="\x00")

    @functools.cached_property
    def extension_type(self) -> int:
        if self.version == 1:
            start = (
                super().header_size
                + 6
                + len(self.item_name)
                + len(self.content_type)
                + (1 + len(self.content_encoding) if self.content_encoding else 0)
            )
            if start < self.end:
                return self.slice.subslice(start, start + 4).unpack(">I")[0]
        return None

    @functools.cached_property
    def extensions(self):
        if self.version == 1:
            pass
        return None

    @functools.cached_property
    def item_uri_type(self):
        if self.item_type == "uri ":
            if self.version == 2:
                start = (
                    super().header_size
                    + 9
                    + len(self.item_name)
                )
            elif self.version == 3:
                start = (
                    super().header_size
                    + 11
                    + len(self.item_name)
                )
            return self.slice.subslice(start).decode(terminator="\x00")
        return None

    @property
    def header_size(self) -> int:
        if self.version == 0:
            return (
                super().header_size
                + 6
                + len(self.item_name)
                + len(self.content_type)
                + (1 + len(self.content_encoding) if self.content_encoding else 0)
            )
        elif self.version == 1:
            return (
                super().header_size
                + 6
                + len(self.item_name)
                + len(self.content_type)
                + (1 + len(self.content_encoding) if self.content_encoding else 0)
                + (4 if self.extension_type else 0)
            )
        elif self.version == 2:
            return (
                super().header_size
                + 9
                + len(self.item_name)
                + (1 + len(self.content_type) if self.content_type else 0)
                + (1 + len(self.content_encoding) if self.content_encoding else 0)
                + (1 + len(self.item_uri_type) if self.item_uri_type else 0)
            )
        elif self.version == 3:
            return (
                super().header_size
                + 11
                + len(self.item_name)
                + (1 + len(self.content_type) if self.content_type else 0)
                + (1 + len(self.content_encoding) if self.content_encoding else 0)
                + (1 + len(self.item_uri_type) if self.item_uri_type else 0)
            )


class ItemInfoBox(FullBox):
    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size
        if self.version == 0:
            return self.slice.subslice(start, start + 2).unpack(">H")
        elif self.version == 1:
            return self.slice.subslice(start, start + 4).unpack(">I")

    @functools.cached_property
    def sample_entries(self) -> typing.List[ItemInfoEntry]:
        if self.version == 0:
            start = super().header_size + 2
        elif self.version == 1:
            start = super().header_size + 4
        return CachedIterator(
            self.slice.subslice(start, self.end),
            lambda this: ItemInfoEntry(this.slice, self),
            self.entry_count,
        )

    @property
    def header_size(self) -> int:
        return (
            super().header_size + 4 + sum(entry.size for entry in self.sample_entries)
        )


class AdditionalMetadataContainerBox(Box):
    pass


class MetaboxRelationBox(FullBox):
    @functools.cached_property
    def first_metabox_handler_type(self) -> str:
        start = super().header_size
        return self.slice.subslice(start, start + 4).decode()

    @functools.cached_property
    def second_metabox_handler_type(self) -> str:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 4).decode()

    @functools.cached_property
    def entry_count(self) -> int:
        start = super().header_size + 8
        return self.slice.subslice(start, start + 1).unpack(">B")[0]

    @property
    def header_size(self) -> int:
        return super().header_size + 9


class ItemDataBox(ChildlessBox):
    @property
    def data(self) -> Slice:
        return self.slice.subslice(super().header_size, self.end)

    @property
    def header_size(self) -> int:
        return self.size


class SingleItemTypeReferenceBox(FullBox):
    @functools.cached_property
    def from_item_ID(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def reference_count(self) -> int:
        start = super().header_size + 2
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def to_item_ID(self) -> typing.Tuple[int, ...]:
        if self.reference_count == 0:
            start = super().header_size + 4
            return tuple(
                e[0]
                for e in self.slice.subslice(
                    start, start + 4 * self.sample_count
                ).iter_unpack(f">I")
            )
        else:
            return None

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.reference_count * 4


class SingleItemTypeReferenceBoxLarge(FullBox):
    @functools.cached_property
    def from_item_ID(self) -> int:
        start = super().header_size
        return self.slice.subslice(start, start + 4).unpack(">I")[0]

    @functools.cached_property
    def reference_count(self) -> int:
        start = super().header_size + 4
        return self.slice.subslice(start, start + 2).unpack(">H")[0]

    @functools.cached_property
    def to_item_ID(self) -> typing.Tuple[int, ...]:
        if self.reference_count == 0:
            start = super().header_size + 4
            return tuple(
                e[0]
                for e in self.slice.subslice(
                    start, start + 4 * self.sample_count
                ).iter_unpack(f">I")
            )
        else:
            return None

    @property
    def header_size(self) -> int:
        return super().header_size + 4 + self.reference_count * 4


class ItemReferenceBox(FullBox):
    @property
    def children(self):
        if self.has_children:
            if self.version == 0:
                return CachedIterator(
                    self.slice.subslice(self.header_size, self.size),
                    lambda this: SingleItemTypeReferenceBox(this.slice, self.parent),
                )
            elif self.version == 1:
                return CachedIterator(
                    self.slice.subslice(self.header_size, self.size),
                    lambda this: SingleItemTypeReferenceBoxLarge(
                        this.slice, self.parent
                    ),
                )
        return None


BOX_TYPES.update(
    {
        "meta": MetaBox,  # 8.11.1
        "xml ": XMLBox,  # 8.11.2
        "bxml": BinaryXMLBox,  # 8.11.2
        "iloc": ItemLocationBox,  # 8.11.3
        "pitm": PrimaryItemBox,  # 8.11.4
        "ipro": ItemProtectionBox,  # 8.11.5
        "fdel": FDItemInfoExtension,  # 8.11.6
        "infe": ItemInfoEntry,  # 8.11.6
        "iinf": ItemInfoBox,  # 8.11.6
        "meco": AdditionalMetadataContainerBox,  # 8.11.7
        "mere": MetaboxRelationBox,  # 8.11.8
        "idat": ItemDataBox,  # 8.11.11
        "iref": ItemReferenceBox,  # 8.11.12
    }
)
