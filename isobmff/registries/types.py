# File: libs/utils/isobmff/registries/types.py

from . import Registry
from datetime import datetime
import typing

DECODERS = Registry(types=[typing.Callable])
DECODERS["default"] = lambda _, data: data
DECODERS["int"] = lambda _, data: int.from_bytes(data, byteorder="big")
DECODERS["datetime"] = lambda _, data: datetime.utcfromtimestamp(
    int.from_bytes(data, byteorder="big")
)
DECODERS["string"] = lambda _, data, encoding="utf-8": data.decode(encoding)
DECODERS["lang"] = lambda _, data: (
    chr(((int.from_bytes(data, 'big') >> 10) & 0x1F) + 0x60) +
    chr(((int.from_bytes(data, 'big') >> 5) & 0x1F) + 0x60) +
    chr((int.from_bytes(data, 'big') & 0x1F) + 0x60)
)