"""Slide wrapper implementation."""

from typing import Self, Unpack, cast

from pptx.presentation import Presentation as PptxPresentation
from pptx.slide import Slide as PptxSlide
from pptx.slide import SlideLayout as PptxSlideLayout

from pptxr._pptx.shape import Shape
from pptxr._pptx.text import TextProps
from pptxr._pptx.types import PptxConvertible
from pptxr.exception import SlideLayoutIndexError

from .title import Title


class Slide(PptxConvertible[PptxSlide]):
    """Slide wrapper with type safety."""

    def __init__(self, pptx_slide: PptxSlide) -> None:
        """Initialize slide."""
        self._pptx: PptxSlide = pptx_slide

    @property
    def shapes(self) -> list[Shape]:
        """Get all shapes in the slide."""
        return [Shape(shape) for shape in self._pptx.shapes]

    @property
    def title(self) -> Title | None:
        """Get slide title shape."""
        if title := self._pptx.shapes.title:
            return Title(title)
        return None

    def to_pptx(self) -> PptxSlide:
        """Convert to pptx slide."""
        return cast(PptxSlide, self._pptx)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlide) -> Self:
        """Create from pptx slide."""
        return cls(pptx_obj)


class SlideBuilder:
    """Slide builder."""

    def __init__(self, slide_layout: PptxSlideLayout | int = 0) -> None:
        self._slide_layout = slide_layout
        self._shapes: list[Shape]

    def text(self, contents: str, /, **kwargs: Unpack[TextProps]) -> Self:
        return self

    def _build(self, pptx_presentation: PptxPresentation) -> Slide:
        if isinstance(self._slide_layout, int):
            try:
                slide_layout = pptx_presentation.slide_layouts[self._slide_layout]
            except IndexError:
                raise SlideLayoutIndexError(
                    self._slide_layout,
                    pptx_presentation.slide_layouts,
                )
        else:
            slide_layout = self._slide_layout

        slide = pptx_presentation.slides.add_slide(slide_layout)

        return Slide(slide)
