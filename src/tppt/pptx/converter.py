"""Type definitions for pptx wrapper."""

from typing import Protocol, Self, TypeVar, assert_never, overload, runtime_checkable

from pptx.dml.color import RGBColor as PptxRGBColor
from pptx.util import Cm as PptxCm
from pptx.util import Inches as PptxInches
from pptx.util import Length as PptxLength
from pptx.util import Pt as PptxPt

from tppt.types._color import Color, LiteralColor, to_color
from tppt.types._length import (
    Centimeter,
    Inch,
    Length,
    LiteralLength,
    Point,
    to_length,
)

PT = TypeVar("PT")


@runtime_checkable
class PptxConvertible(Protocol[PT]):
    """Protocol for objects that can be converted to and from pptx objects."""

    def to_pptx(self) -> PT:
        """Convert to pptx object."""
        ...

    @classmethod
    def from_pptx(cls, pptx_obj: PT) -> Self:
        """Create from pptx object."""
        ...


@overload
def to_pptx_length(length: Length | LiteralLength) -> PptxLength: ...


@overload
def to_pptx_length(length: Length | LiteralLength | None) -> PptxLength | None: ...


def to_pptx_length(length: Length | LiteralLength | None) -> PptxLength | None:
    if isinstance(length, tuple):
        length = to_length(length)

    match length:
        case Inch():
            return PptxInches(length.value)
        case Centimeter():
            return PptxCm(length.value)
        case Point():
            return PptxPt(length.value)
        case None:
            return None
        case _:
            assert_never(length)

def to_tppt_length(length: PptxLength) -> Length:
    return to_length((length.cm, "cm"))

def to_pptx_color(color: Color | LiteralColor) -> PptxRGBColor:
    color = to_color(color)

    return PptxRGBColor(color.r, color.g, color.b)

def to_tppt_color(color: PptxRGBColor) -> Color:
    return Color(*color)
