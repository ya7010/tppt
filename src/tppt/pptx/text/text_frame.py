from typing import Callable, Self

from pptx.text.text import TextFrame as PptxTextFrame

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.paragraph import Paragraph, ParagraphBuilder


class TextFrame(PptxConvertible[PptxTextFrame]):
    def __init__(self, pptx_obj: PptxTextFrame) -> None:
        self._pptx = pptx_obj

    def builder(self) -> "TextFrameBuilder":
        return TextFrameBuilder(self._pptx)

    def to_pptx(self) -> PptxTextFrame:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxTextFrame) -> Self:
        return cls(pptx_obj)


class TextFrameBuilder:
    def __init__(self, pptx_obj: PptxTextFrame) -> None:
        self._pptx = pptx_obj

    def paragraph(
        self, callable: Callable[[Paragraph], Paragraph | ParagraphBuilder]
    ) -> "TextFrameBuilder":
        paragraph = callable(Paragraph(self._pptx.add_paragraph()))
        if isinstance(paragraph, ParagraphBuilder):
            paragraph._build()

        return self

    def _build(self) -> TextFrame:
        return TextFrame(self._pptx)
