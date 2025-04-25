"""Slide wrapper implementation."""

from typing import cast

from pptx.slide import Slide as PptxSlideType

from pptxr._pptx.converters import to_pptx_length, to_pptx_shape_type
from pptxr._pptx.shape import Shape
from pptxr._pptx.types import PptxConvertible, PptxSlide
from pptxr.types import Length, LiteralLength


class Slide(PptxConvertible):
    """Slide wrapper with type safety."""

    def __init__(self, pptx_slide: PptxSlideType) -> None:
        """Initialize slide."""
        self._pptx = pptx_slide

    def get_shapes(self) -> list[Shape]:
        """Get all shapes in the slide."""
        return [Shape(shape) for shape in self._pptx.shapes]

    def add_shape(
        self,
        shape_type: str,
        left: Length | LiteralLength,
        top: Length | LiteralLength,
        width: Length | LiteralLength,
        height: Length | LiteralLength,
    ) -> Shape:
        """Add a shape to the slide."""
        shape = self._pptx.shapes.add_shape(
            to_pptx_shape_type(shape_type),
            to_pptx_length(left),
            to_pptx_length(top),
            to_pptx_length(width),
            to_pptx_length(height),
        )
        return Shape(shape)

    def get_title(self) -> Shape | None:
        """Get slide title shape."""
        if self._pptx.shapes.title:
            return Shape(self._pptx.shapes.title)
        return None

    def to_pptx(self) -> PptxSlide:
        """Convert to pptx slide."""
        return cast(PptxSlide, self._pptx)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlide) -> "Slide":
        """Create from pptx slide."""
        if not isinstance(pptx_obj, PptxSlideType):
            raise TypeError(f"Expected PptxSlide, got {type(pptx_obj)}")
        return cls(pptx_obj)
