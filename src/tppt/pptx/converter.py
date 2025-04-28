"""Type definitions for pptx wrapper."""

from typing import Protocol, Self, TypeVar, assert_never, overload, runtime_checkable

from pptx.dml.color import RGBColor as PptxRGBColor
from pptx.util import Cm as PptxCm
from pptx.util import Emu as PptxEmu
from pptx.util import Inches as PptxInches
from pptx.util import Length as PptxLength
from pptx.util import Mm as PptxMm
from pptx.util import Pt as PptxPt

from tppt.types._color import Color, LiteralColor, to_color
from tppt.types._length import (
    CentiMeters,
    EnglishMetricUnits,
    Inchs,
    Length,
    LiteralLength,
    MilliMeters,
    Points,
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
        case Inchs():
            return PptxInches(length.value)
        case CentiMeters():
            return PptxCm(length.value)
        case Points():
            return PptxPt(length.value)
        case MilliMeters():
            return PptxMm(length.value)
        case EnglishMetricUnits():
            return PptxEmu(length.value)
        case None:
            return None
        case _:
            assert_never(length)


@overload
def to_tppt_length(length: PptxLength) -> Length: ...


@overload
def to_tppt_length(length: PptxLength | None) -> Length | None: ...


def to_tppt_length(length: PptxLength | None) -> Length | None:
    return to_length((length.emu, "emu")) if length else None


@overload
def to_pptx_rgb_color(color: Color | LiteralColor) -> PptxRGBColor: ...


@overload
def to_pptx_rgb_color(color: Color | LiteralColor | None) -> PptxRGBColor | None: ...


def to_pptx_rgb_color(color: Color | LiteralColor | None) -> PptxRGBColor | None:
    if color is None:
        return None

    color = to_color(color)

    return PptxRGBColor(color.r, color.g, color.b)


@overload
def to_tppt_color(color: PptxRGBColor) -> Color: ...


@overload
def to_tppt_color(color: PptxRGBColor | None) -> Color | None: ...


def to_tppt_color(color: PptxRGBColor | None) -> Color | None:
    return Color(*color) if color else None
