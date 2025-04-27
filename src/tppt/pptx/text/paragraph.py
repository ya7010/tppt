from typing import Callable, Self

from pptx.text.text import _Paragraph as PptxParagraph

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.run import Run, RunBuilder


class Paragraph(PptxConvertible[PptxParagraph]):
    def __init__(self, pptx_obj: PptxParagraph) -> None:
        self._pptx = pptx_obj

    def builder(self) -> "ParagraphBuilder":
        return ParagraphBuilder(self._pptx)

    def to_pptx(self) -> PptxParagraph:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxParagraph) -> Self:
        return cls(pptx_obj)


class ParagraphBuilder:
    def __init__(self, pptx_obj: PptxParagraph) -> None:
        self._pptx = pptx_obj

    def text(self, text: str) -> "ParagraphBuilder":
        self._pptx.text = text

        return self

    def run(self, callable: Callable[[Run], Run | RunBuilder]) -> "ParagraphBuilder":
        run = callable(Run(self._pptx.add_run()))
        if isinstance(run, RunBuilder):
            run._build()

        return self

    def _build(self) -> Paragraph:
        return Paragraph(self._pptx)
