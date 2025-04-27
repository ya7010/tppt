from typing import Self

from pptx.text.text import _Run as PptxRun

from tppt.pptx.converter import PptxConvertible


class Run(PptxConvertible[PptxRun]):
    def __init__(self, pptx_obj: PptxRun) -> None:
        self._pptx = pptx_obj

    def builder(self) -> "RunBuilder":
        return RunBuilder(self._pptx)

    def to_pptx(self) -> PptxRun:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxRun) -> Self:
        return cls(pptx_obj)


class RunBuilder:
    def __init__(self, pptx_obj: PptxRun) -> None:
        self._pptx = pptx_obj

    def _build(self) -> Run:
        return Run(self._pptx)
