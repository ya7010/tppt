from typing import Callable, Self

from pptx.enum.text import MSO_TEXT_UNDERLINE_TYPE
from pptx.text.text import Font as PptxFont

from tppt.pptx.converter import PptxConvertible, to_pptx_length, to_tppt_length
from tppt.pptx.dml.color import ColorFormat, ColorFormatBuilder
from tppt.types._length import Length, LiteralLength


class Font(PptxConvertible[PptxFont]):
    def __init__(self, pptx_obj: PptxFont) -> None:
        self._pptx = pptx_obj

    @property
    def name(self) -> str | None:
        return self._pptx.name

    @name.setter
    def name(self, name: str) -> None:
        self._pptx.name = name

    @property
    def size(self) -> Length | None:
        return to_tppt_length(self._pptx.size)

    @size.setter
    def size(self, size: Length) -> None:
        self._pptx.size = to_pptx_length(size)

    @property
    def bold(self) -> bool | None:
        return self._pptx.bold

    @bold.setter
    def bold(self, bold: bool) -> None:
        self._pptx.bold = bold

    @property
    def italic(self) -> bool | None:
        return self._pptx.italic

    @italic.setter
    def italic(self, italic: bool) -> None:
        self._pptx.italic = italic

    @property
    def underline(self) -> bool | MSO_TEXT_UNDERLINE_TYPE | None:
        return self._pptx.underline

    @underline.setter
    def underline(self, underline: bool | MSO_TEXT_UNDERLINE_TYPE) -> None:
        self._pptx.underline = underline

    @property
    def color(self) -> ColorFormat:
        return ColorFormat(self._pptx.color)

    @color.setter
    def color(self, color: ColorFormat) -> None:
        self._pptx.color = color.to_pptx()

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

    def underline(self, underline: bool | MSO_TEXT_UNDERLINE_TYPE) -> Self:
        self._pptx.underline = underline

        return self

    def color(
        self, callable: Callable[[ColorFormat], ColorFormat | ColorFormatBuilder]
    ) -> Self:
        color = callable(ColorFormat(self._pptx.color))
        if isinstance(color, ColorFormatBuilder):
            color._build()

        return self

    def _build(self) -> Font:
        return Font(self._pptx)
