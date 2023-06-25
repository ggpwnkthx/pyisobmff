"""
File: isobmff/box/__init__.py

The box package, containing all the box classes specified in ISO/IEC 14496-12:2015
"""
# Global registry of box types and classes
BOX_TYPES = {}

from .structure import *  # 4.2
from .file import *  # 8.1
from .movie import *  # 8.2
from .track import *  # 8.3
from .track.media import *  # 8.4
from .track.sample import *  # 8.5
from .track.time import *  # 8.6
from .track.data import *  # 8.7
from .movie.fragment import *  # 8.8
from .track.sample.group import *  # 8.9
from .user import *  # 8.10
from .meta import *  # 8.11
from .protected import *  # 8.12
from .file.delivery import *  # 8.13
from .track.sub import *  # 8.14
from .movie.post_decoder import *  # 8.15
from .segment import *  # 8.16
from .track.incomplete import *  # 8.17


__all__ = [
    "BOX_TYPES",
    "Box",
    "FullBox",
    "ChildlessBox"
]
