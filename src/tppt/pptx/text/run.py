from typing import Self

from pptx.text.text import _Run as PptxRun

from tppt.pptx.converter import PptxConvertible
from tppt.pptx.text.font import Font
from tppt.pptx.text.hyperlink import Hyperlink


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

    @property
    def hyperlink(self) -> Hyperlink:
        return Hyperlink(self._pptx.hyperlink)

    def to_pptx(self) -> PptxRun:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxRun) -> Self:
        return cls(pptx_obj)
