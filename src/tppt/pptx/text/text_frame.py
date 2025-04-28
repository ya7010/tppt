from typing import Self

from pptx.text.text import TextFrame as PptxTextFrame

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.paragraph import Paragraph


class TextFrame(PptxConvertible[PptxTextFrame]):
    def __init__(self, pptx_obj: PptxTextFrame) -> None:
        self._pptx = pptx_obj

    def add_paragraph(self) -> Paragraph:
        return Paragraph(self._pptx.add_paragraph())

    def to_pptx(self) -> PptxTextFrame:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxTextFrame) -> Self:
        return cls(pptx_obj)
