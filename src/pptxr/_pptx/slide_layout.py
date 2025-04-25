from typing import Self

from pptx.slide import SlideLayout as PptxSlideLayout

from pptxr._pptx.converter import PptxConvertible


class SlideLayout(PptxConvertible[PptxSlideLayout]):
    """Slide layout data class."""

    def __init__(self, pptx_slide_layout: PptxSlideLayout) -> None:
        self._pptx = pptx_slide_layout

    def to_pptx(self) -> PptxSlideLayout:
        """Convert to pptx slide layout."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlideLayout) -> Self:
        return cls(pptx_obj)
