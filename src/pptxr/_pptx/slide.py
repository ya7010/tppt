"""Slide wrapper implementation."""

from typing import TYPE_CHECKING, Self, Unpack, cast

from pptx.slide import Slide as PptxSlide
from pptx.slide import SlideLayout as PptxSlideLayout

from pptxr._pptx.shape import Shape
from pptxr._pptx.text import TextData, TextProps
from pptxr.exception import SlideLayoutIndexError

from .converter import PptxConvertible, to_pptx_length
from .text import Text
from .title import Title

if TYPE_CHECKING:
    from .presentation import PresentationBuilder


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

    def __init__(
        self,
        slide_layout: PptxSlideLayout | int = 0,
    ) -> None:
        self._slide_layout = slide_layout
        self._data: list[TextData] = []

    def text(self, contents: str, /, **kwargs: Unpack[TextProps]) -> Self:
        self._data.append(TextData(contents=contents, **kwargs))

        return self

    def _build(
        self,
        builder: "PresentationBuilder",
    ) -> Slide:
        if isinstance(self._slide_layout, int):
            try:
                slide_layout = builder._pptx.slide_layouts[self._slide_layout]
            except IndexError:
                raise SlideLayoutIndexError(
                    self._slide_layout,
                    builder._pptx.slide_layouts,
                )
        else:
            slide_layout = self._slide_layout

        slide = builder._pptx.slides.add_slide(slide_layout)

        for data in self._data:
            Text(
                slide.shapes.add_textbox(
                    to_pptx_length(data["left"]),
                    to_pptx_length(data["top"]),
                    to_pptx_length(data["width"]),
                    to_pptx_length(data["height"]),
                ),
                data,
            )

        return Slide(slide)
