"""Type definitions for pptxr."""

from enum import StrEnum
from pathlib import Path
from typing import Literal, Tuple, TypeAlias, Union

from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.util import Cm, Inches, Pt

FilePath: TypeAlias = str | Path

# Length units
Unit = Literal["pt", "in", "cm"]

# Length value with unit
LiteralLength = Tuple[Union[int, float], Unit]

# Length can be either a LiteralLength or a pptx length type
Length = Union[Pt, Inches, Cm]

# Point type
Point = Tuple[float, float]

# Color type
Color = Tuple[int, int, int]

# Custom string enum for shape types, populated from MSO_AUTO_SHAPE_TYPE member names as values.
ShapeType = StrEnum(
    "ShapeType",
    {name: name for name in MSO_AUTO_SHAPE_TYPE.__members__},
)


# Convert length to points
def to_points(length: Union[Length, LiteralLength]) -> float:
    """Convert a length value to points.

    Args:
        length: The length value to convert.

    Returns:
        The converted value in points.
    """
    if isinstance(length, (Pt, Inches, Cm)):
        return float(length.pt)
    value, unit = length
    if unit == "pt":
        return float(value)
    elif unit == "in":
        return float(value) * 72
    elif unit == "cm":
        return float(value) * 28.3465
    else:
        raise ValueError(f"Unknown unit: {unit}")


def pt(value: Union[int, float]) -> Length:
    """Create a length value in points.

    Args:
        value: The value in points.

    Returns:
        A length value in points.
    """
    return Pt(float(value))


def inch(value: Union[int, float]) -> Length:
    """Create a length value in inches.

    Args:
        value: The value in inches.

    Returns:
        A length value in inches.
    """
    return Inches(float(value))


def cm(value: Union[int, float]) -> Length:
    """Create a length value in centimeters.

    Args:
        value: The value in centimeters.

    Returns:
        A length value in centimeters.
    """
    return Cm(float(value))


__all__ = [
    "FilePath",
    "Unit",
    "LiteralLength",
    "Length",
    "Point",
    "Color",
    "to_points",
    "pt",
    "inch",
    "cm",
    "ShapeType",
]
