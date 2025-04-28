from typing import Self

from pptx.text.text import _Paragraph as PptxParagraph

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.run import Run


class Paragraph(PptxConvertible[PptxParagraph]):
    def __init__(self, pptx_obj: PptxParagraph) -> None:
        self._pptx = pptx_obj

    @property
    def runs(self) -> list[Run]:
        return [Run(run) for run in self._pptx.runs]

    def add_run(self) -> Run:
        return Run(self._pptx.add_run())

    def to_pptx(self) -> PptxParagraph:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxParagraph) -> Self:
        return cls(pptx_obj)
