"""Types module for pptxr."""

import pathlib

from .color import Color
from .length import (
    Length,
    LiteralLength,
    Point,
    to_length,
    to_point,
    to_points,
)

FilePath = str | pathlib.Path


def pt(value: int | float) -> LiteralLength:
    """Create a point length."""
    return (int(value), "pt")


__all__ = [
    "Color",
    "FilePath",
    "Length",
    "LiteralLength",
    "Point",
    "pt",
    "to_length",
    "to_point",
    "to_points",
]
