from typing import Callable, Self

from pptx.text.text import _Run as PptxRun

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.font import Font, FontBuilder


class Run(PptxConvertible[PptxRun]):
    def __init__(self, pptx_obj: PptxRun) -> None:
        self._pptx = pptx_obj

    @property
    def text(self) -> str:
        return self._pptx.text

    @text.setter
    def text(self, text: str) -> None:
        self._pptx.text = text

    @property
    def font(self) -> Font:
        return Font(self._pptx.font)

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

    def text(self, text: str) -> Self:
        self._pptx.text = text

        return self

    def font(self, callable: Callable[[Font], Font | FontBuilder]) -> Self:
        font = callable(Font(self._pptx.font))
        if isinstance(font, FontBuilder):
            font._build()

        return self

    def _build(self) -> Run:
        return Run(self._pptx)
