"""
File: isobmff/box/file/delivery.py

Contains all the classes specified in section 8.13 of ISO/IEC 14496-12:2015
"""
from .. import BOX_TYPES, FullBox, ChildlessBox, Slice
import functools
import typing