"""Types module for pptxr."""

import pathlib
from typing import Literal, TypeAlias

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from ._color import Color
from ._length import (
    Length,
    LiteralLength,
    Point,
    to_length,
    to_point,
)

FilePath = str | pathlib.Path
ShapeType: TypeAlias = MSO_AUTO_SHAPE_TYPE

SlideLayoutType: TypeAlias = Literal[
    "TITLE",
    "TITLE_AND_CONTENT",
    "SECTION_HEADER",
    "TWO_CONTENT",
    "COMPARISON",
    "TITLE_ONLY",
    "BLANK",
    "CONTENT_WITH_CAPTION",
    "PICTURE_WITH_CAPTION",
    "TITLE_AND_VERTICAL_TEXT",
    "VERTICAL_TITLE_AND_TEXT",
]


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
    "SlideLayoutType",
]
