from typing import Self, cast

from pptx.dml.fill import FillFormat as PptxFillFormat
from pptx.dml.fill import _GradFill as PptxGradFill
from pptx.dml.fill import _GradientStop as PptxGradientStop
from pptx.dml.fill import _GradientStops as PptxGradientStops
from pptx.dml.fill import _NoFill as PptxNoFill
from pptx.dml.fill import _PattFill as PptxPattFill
from pptx.dml.fill import _SolidFill as PptxSolidFill
from pptx.enum.dml import MSO_PATTERN_TYPE

from tppt.pptx.converter import PptxConvertible, to_pptx_angle, to_tppt_angle
from tppt.pptx.dml.color import ColorFormat
from tppt.types._angle import Angle


class FillFormat(PptxConvertible[PptxFillFormat]):
    """Fill format."""

    def __init__(self, pptx_obj: PptxFillFormat) -> None:
        self._pptx = pptx_obj

    @property
    def fore_color(self) -> ColorFormat:
        """Fore color."""
        return ColorFormat(self._pptx.fore_color)

    @property
    def back_color(self) -> ColorFormat:
        """Back color."""
        return ColorFormat(self._pptx.back_color)

    @property
    def pattern(self) -> MSO_PATTERN_TYPE:
        """Pattern."""
        return self._pptx.pattern

    @pattern.setter
    def pattern(self, value: MSO_PATTERN_TYPE) -> None:
        self._pptx.pattern = value

    def patterned(self) -> "PattFill":
        """Set the fill type to patterned."""
        self._pptx.patterned()
        return PattFill(cast(PptxPattFill, self._pptx._fill))

    def background(self) -> "NoFill":
        """Set the fill type to noFill, i.e. transparent."""
        self._pptx.background()
        return NoFill(cast(PptxNoFill, self._pptx._fill))

    def solid(self) -> "SolidFill":
        """Set the fill type to solid."""
        self._pptx.solid()
        return SolidFill(cast(PptxSolidFill, self._pptx._fill))

    def gradient(self) -> "GradFill":
        """Sets the fill type to gradient."""
        self._pptx.gradient()
        return GradFill(cast(PptxGradFill, self._pptx._fill))

    def to_pptx(self) -> PptxFillFormat:
        """Convert to pptx fill format."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxFillFormat) -> Self:
        """Create from pptx fill format."""
        return cls(pptx_obj)


class NoFill(PptxConvertible[PptxNoFill]):
    """No fill."""

    def __init__(self, pptx_obj: PptxNoFill) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxNoFill:
        """Convert to pptx no fill."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxNoFill) -> Self:
        """Create from pptx no fill."""
        return cls(pptx_obj)


class PattFill(PptxConvertible[PptxPattFill]):
    """Pattern fill."""

    def __init__(self, pptx_obj: PptxPattFill) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxPattFill:
        """Convert to pptx pattern fill."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxPattFill) -> Self:
        """Create from pptx pattern fill."""
        return cls(pptx_obj)


class SolidFill(PptxConvertible[PptxSolidFill]):
    """Solid fill."""

    def __init__(self, pptx_obj: PptxSolidFill) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxSolidFill:
        """Convert to pptx solid fill."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSolidFill) -> Self:
        """Create from pptx solid fill."""
        return cls(pptx_obj)


class GradFill(PptxConvertible[PptxGradFill]):
    """Gradient fill."""

    def __init__(self, pptx_obj: PptxGradFill) -> None:
        self._pptx = pptx_obj

    @property
    def gradient_angle(self) -> Angle | None:
        """Angle in float degrees of line of a linear gradient."""
        return to_tppt_angle(cast(float | None, self._pptx.gradient_angle))

    @gradient_angle.setter
    def gradient_angle(self, value: Angle) -> None:
        self._pptx.gradient_angle = to_pptx_angle(value)

    @property
    def gradient_stops(self) -> "GradientStops":
        """Gradient stops."""
        return GradientStops(self._pptx.gradient_stops)

    def to_pptx(self) -> PptxGradFill:
        """Convert to pptx gradient fill."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxGradFill) -> Self:
        """Create from pptx gradient fill."""
        return cls(pptx_obj)


class GradientStops(PptxConvertible[PptxGradientStops]):
    """Gradient stops."""

    def __init__(self, pptx_obj: PptxGradientStops) -> None:
        self._pptx = pptx_obj

    def __getitem__(self, idx: int) -> "GradientStop":
        return GradientStop(self._pptx[idx])

    def __len__(self) -> int:
        return len(self._pptx)

    def to_pptx(self) -> PptxGradientStops:
        """Convert to pptx gradient stops."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxGradientStops) -> Self:
        """Create from pptx gradient stops."""
        return cls(pptx_obj)


class GradientStop(PptxConvertible[PptxGradientStop]):
    """Gradient stop."""

    def __init__(self, pptx_obj: PptxGradientStop) -> None:
        self._pptx = pptx_obj

    @property
    def color(self) -> ColorFormat:
        """Color."""
        return ColorFormat(self._pptx.color)

    @property
    def position(self) -> float:
        """Location of stop in gradient path as float between 0.0 and 1.0.

        The value represents a percentage, where 0.0 (0%) represents the
        start of the path and 1.0 (100%) represents the end of the path. For
        a linear gradient, these would represent opposing extents of the
        filled area.
        """
        return self._pptx.position

    @position.setter
    def position(self, value: float) -> None:
        self._pptx.position = value

    def to_pptx(self) -> PptxGradientStop:
        """Convert to pptx gradient stop."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxGradientStop) -> Self:
        """Create from pptx gradient stop."""
        return cls(pptx_obj)
