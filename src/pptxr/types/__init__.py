"""Types module for pptxr."""

import pathlib

from .color import Color
from .length import Length, LiteralLength

FilePath = str | pathlib.Path

__all__ = [
    "Color",
    "FilePath",
    "Length",
    "LiteralLength",
]
