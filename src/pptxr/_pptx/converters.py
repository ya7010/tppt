"""Converter implementations for pptx objects."""

from typing import assert_never

import pptx
import pptx.util
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from pptxr.types import Length, LiteralLength, ShapeType
from pptxr.types.length import Centimeter, Inch, Point, to_length

# pyright: ignore


def to_pptx_length(length: Length | LiteralLength) -> pptx.util.Length:
    """Convert pptxr length to pptx length."""
    if isinstance(length, tuple):
        length = to_length(length)

    match length:
        case Inch():
            return pptx.util.Inches(length.value)
        case Centimeter():
            return pptx.util.Cm(length.value)
        case Point():
            return pptx.util.Pt(length.value)
        case _:
            assert_never(length)


def to_pptx_shape_type(shape_type: ShapeType) -> MSO_AUTO_SHAPE_TYPE:
    """Convert pptxr ShapeType to MSO_AUTO_SHAPE_TYPE."""
    return shape_type.value
