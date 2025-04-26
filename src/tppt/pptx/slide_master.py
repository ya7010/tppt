from typing import Self

from pptx.slide import SlideMaster as PptxSlideMaster

from tppt.pptx.converter import PptxConvertible

from .slide_layout import SlideLayout


class SlideMaster(PptxConvertible[PptxSlideMaster]):
    """Slide master data class."""

    def __init__(self, pptx_slide_master: PptxSlideMaster) -> None:
        self._pptx = pptx_slide_master

    @property
    def slide_layouts(self) -> list[SlideLayout]:
        return [SlideLayout.from_pptx(layout) for layout in self._pptx.slide_layouts]

    def to_pptx(self) -> PptxSlideMaster:
        """Convert to pptx slide master."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlideMaster) -> Self:
        return cls(pptx_obj)
