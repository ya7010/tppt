from typing import Self

from pptx.slide import _Background as PptxBackground

from tppt.pptx.converter import PptxConvertible


class Background(PptxConvertible[PptxBackground]):
    """Background of the slide."""

    def __init__(self, pptx_obj: PptxBackground) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxBackground:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxBackground) -> Self:
        return cls(pptx_obj)
