from typing import Self

from pptx.text.text import Font as PptxFont

from tppt.pptx.converter import PptxConvertible, to_pptx_length
from tppt.pptx.dml.color import ColorFormat
from tppt.types._length import Length, LiteralLength


class Font(PptxConvertible[PptxFont]):
    def __init__(self, pptx_obj: PptxFont) -> None:
        self._pptx = pptx_obj

    def color(self) -> ColorFormat:
        return ColorFormat(self._pptx.color)

    def builder(self) -> "FontBuilder":
        return FontBuilder(self._pptx)

    def to_pptx(self) -> PptxFont:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxFont) -> Self:
        return cls(pptx_obj)


class FontBuilder:
    def __init__(self, pptx_obj: PptxFont) -> None:
        self._pptx = pptx_obj

    def name(self, name: str) -> Self:
        self._pptx.name = name

        return self

    def size(self, size: Length | LiteralLength) -> Self:
        self._pptx.size = to_pptx_length(size)

        return self

    def bold(self, bold: bool) -> Self:
        self._pptx.bold = bold

        return self

    def italic(self, italic: bool) -> Self:
        self._pptx.italic = italic

        return self

    def _build(self) -> Font:
        return Font(self._pptx)
