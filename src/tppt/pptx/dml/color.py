from typing import Self

from pptx.dml.color import ColorFormat as PptxColorFormat

from tppt.pptx.converter import PptxConvertible, to_pptx_rgb_color, to_tppt_color
from tppt.types import Color, LiteralColor


class ColorFormat(PptxConvertible[PptxColorFormat]):
    def __init__(self, pptx_obj: PptxColorFormat) -> None:
        self._pptx = pptx_obj

    @property
    def rgb(self) -> Color | None:
        return to_tppt_color(self._pptx.rgb)

    @rgb.setter
    def rgb(self, color: Color | LiteralColor):
        self._pptx.rgb = to_pptx_rgb_color(color)

    def builder(self) -> "ColorFormatBuilder":
        return ColorFormatBuilder(self._pptx)

    def to_pptx(self) -> PptxColorFormat:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxColorFormat) -> Self:
        return cls(pptx_obj)


class ColorFormatBuilder:
    def __init__(self, pptx_obj: PptxColorFormat) -> None:
        self._pptx = pptx_obj

    def rgb(self, color: Color | LiteralColor) -> Self:
        self._pptx.rgb = to_pptx_rgb_color(color)

        return self

    def _build(self) -> ColorFormat:
        return ColorFormat(self._pptx)
