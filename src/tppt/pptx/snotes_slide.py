from typing import Self

from pptx.slide import NotesSlide as PptxNotesSlide

from tppt.pptx.converter import PptxConvertible


class NotesSlide(PptxConvertible[PptxNotesSlide]):
    """Notes slide."""

    def __init__(self, pptx_obj: PptxNotesSlide) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxNotesSlide:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxNotesSlide) -> Self:
        return cls(pptx_obj)
