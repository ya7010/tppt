"""Converter implementations for pptx objects."""

import os
from typing import IO, assert_never

import pptx
import pptx.util
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

from pptxr.types import FilePath, Length, LiteralLength
from pptxr.types.length import Centimeter, Inch, Point, to_length

from .types import PptxPresentation as PptxPres

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


def save_presentation(presentation: PptxPres, file: FilePath | IO[bytes]) -> None:
    """Save presentation to file."""
    if isinstance(file, os.PathLike):
        file = os.fspath(file)
    presentation.save(file)
