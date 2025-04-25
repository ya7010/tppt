"""Converter implementations for pptx objects."""

from typing import assert_never

import pptx
import pptx.util
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from pptxr.types import Length, LiteralLength
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


def to_pptx_shape_type(shape_type: str) -> MSO_AUTO_SHAPE_TYPE:
    """Convert shape type string to MSO_AUTO_SHAPE_TYPE."""
    try:
        return getattr(MSO_AUTO_SHAPE_TYPE, shape_type)
    except AttributeError:
        raise ValueError(f"Invalid shape type: {shape_type}")
