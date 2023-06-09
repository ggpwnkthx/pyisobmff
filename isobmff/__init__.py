# File: libs/utils/isobmff/__init__.py

from .iterator import Iterator
from .registries.mp4 import MP4
from .registries.types import DECODERS


__all__ = [
    "Iterator",
    "MP4",
    "DECODERS",
]

def crawl(iso: Iterator, indent=0) -> None:
    """Prints a tree of atoms in an ISO Base Media File.

    Parameters:
    iso : Iterator
        The Iterator instance for the ISO Base Media File.
    """
    for atom in iso:
        if issubclass(type(atom), Iterator):
            print("  " * indent + f"{atom.type}")
            crawl(atom, indent+1)
        else:
            print("  " * indent + f"{atom}")
