from typing import Self

from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.text.text import _Paragraph as PptxParagraph
from pptx.util import Length as PptxLength

from tppt.pptx.converter import PptxConvertible, to_pptx_length
from tppt.pptx.text.font import Font
from tppt.pptx.text.run import Run
from tppt.types._length import Length, to_length


class Paragraph(PptxConvertible[PptxParagraph]):
    def __init__(self, pptx_obj: PptxParagraph) -> None:
        self._pptx = pptx_obj

    def add_line_break(self) -> None:
        self._pptx.add_line_break()

    def add_run(self) -> Run:
        return Run(self._pptx.add_run())

    @property
    def alignment(self) -> PP_PARAGRAPH_ALIGNMENT | None:
        return self._pptx.alignment

    @alignment.setter
    def alignment(self, value: PP_PARAGRAPH_ALIGNMENT | None) -> None:
        self._pptx.alignment = value

    def clear(self) -> None:
        self._pptx.clear()

    @property
    def font(self) -> Font:
        return Font(self._pptx.font)

    @property
    def level(self) -> int:
        return self._pptx.level

    @level.setter
    def level(self, value: int) -> None:
        self._pptx.level = value

    @property
    def line_spacing(self) -> int | float | Length | None:
        match self._pptx.line_spacing:
            case PptxLength():
                return to_length(self._pptx.line_spacing)
            case _:
                return self._pptx.line_spacing

    @line_spacing.setter
    def line_spacing(self, value: int | float | Length | PptxLength | None) -> None:
        match value:
            case int() | float() | PptxLength() | None:
                self._pptx.line_spacing = value
            case _:
                self._pptx.line_spacing = to_pptx_length(value)

    @property
    def runs(self) -> tuple[Run, ...]:
        return tuple(Run(run) for run in self._pptx.runs)

    @property
    def space_after(self) -> Length | None:
        match self._pptx.space_after:
            case PptxLength():
                return to_length(self._pptx.space_after)
            case _:
                return self._pptx.space_after

    @space_after.setter
    def space_after(self, value: Length | PptxLength | None) -> None:
        match value:
            case PptxLength() | None:
                self._pptx.space_after = value
            case _:
                self._pptx.space_after = to_pptx_length(value)

    @property
    def space_before(self) -> Length | None:
        match self._pptx.space_before:
            case PptxLength():
                return to_length(self._pptx.space_before)
            case _:
                return self._pptx.space_before

    @space_before.setter
    def space_before(self, value: Length | PptxLength | None) -> None:
        match value:
            case PptxLength() | None:
                self._pptx.space_before = value
            case _:
                self._pptx.space_before = to_pptx_length(value)

    @property
    def text(self) -> str:
        return self._pptx.text

    @text.setter
    def text(self, value: str) -> None:
        self._pptx.text = value

    def to_pptx(self) -> PptxParagraph:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxParagraph) -> Self:
        return cls(pptx_obj)
