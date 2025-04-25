from typing import Self

from pptx.shapes.placeholder import SlidePlaceholder as PptxSlidePlaceholder

from tppt._pptx.presentation import PptxConvertible


class SlidePlaceholder(PptxConvertible[PptxSlidePlaceholder]):
    def __init__(self, pptx_obj: PptxSlidePlaceholder) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxSlidePlaceholder:
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlidePlaceholder) -> Self:
        return cls(pptx_obj)
