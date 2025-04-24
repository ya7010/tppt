"""Converter implementations for pptx objects."""

import os
from typing import IO, Any, assert_never

import pptx
import pptx.util
from pptx import Presentation as PptxPresentation
from pptx import presentation
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.shapes.base import BaseShape as PptxShape
from pptx.slide import Slide as PptxSlide

from pptxr.units import Centimeter, Inch, Length, LiteralLength, Point, to_length

from ..abstract.types import FilePath, PresentationFactory
from ..abstract.types import Presentation as AbstractPresentation
from ..abstract.types import Shape as AbstractShape
from ..abstract.types import Slide as AbstractSlide
from .types import PptxConvertible

# pyright: ignore
# type: ignore


class Shape(AbstractShape, PptxConvertible):
    """Shape wrapper with type safety."""

    def __init__(self, pptx_shape: PptxShape) -> None:
        """Initialize shape."""
        self._pptx = pptx_shape

    def get_text(self) -> str:
        """Get shape text."""
        return self._pptx.text  # type: ignore

    def set_text(self, text: str) -> None:
        """Set shape text."""
        self._pptx.text = text  # type: ignore

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Shape":
        """Create from pptx shape."""
        if not isinstance(pptx_obj, PptxShape):
            raise TypeError(f"Expected PptxShape, got {type(pptx_obj)}")
        return cls(pptx_obj)


class Slide(AbstractSlide, PptxConvertible):
    """Slide wrapper with type safety."""

    def __init__(self, pptx_slide: PptxSlide) -> None:
        """Initialize slide."""
        self._pptx = pptx_slide

    def get_shapes(self) -> list[AbstractShape]:
        """Get all shapes in the slide."""
        return [Shape(shape) for shape in self._pptx.shapes]

    def add_shape(
        self,
        shape_type: str,  # type: ignore
        left: Length | LiteralLength,
        top: Length | LiteralLength,
        width: Length | LiteralLength,
        height: Length | LiteralLength,
    ) -> AbstractShape:
        """Add a shape to the slide."""
        shape = self._pptx.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ACTION_BUTTON_CUSTOM,
            to_pptx_length(left),
            to_pptx_length(top),
            to_pptx_length(width),
            to_pptx_length(height),
        )
        return Shape(shape)

    def get_title(self) -> AbstractShape | None:
        """Get slide title shape."""
        if self._pptx.shapes.title:
            return Shape(self._pptx.shapes.title)
        return None

    def to_pptx(self) -> PptxSlide:
        """Convert to pptx slide."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Slide":
        """Create from pptx slide."""
        if not isinstance(pptx_obj, PptxSlide):
            raise TypeError(f"Expected PptxSlide, got {type(pptx_obj)}")
        return cls(pptx_obj)


class Presentation(AbstractPresentation, PptxConvertible):
    """Presentation wrapper with type safety."""

    def __init__(
        self, pptx_presentation: presentation.Presentation | None = None
    ) -> None:
        """Initialize presentation."""
        if pptx_presentation is None:
            self._presentation = PptxPresentation()
        else:
            self._presentation = pptx_presentation

    def get_slides(self) -> list[AbstractSlide]:
        """Get all slides in the presentation."""
        return [Slide(slide) for slide in self._presentation.slides]

    def add_slide(self, layout_type: str) -> AbstractSlide:
        """Add a slide with specified layout."""
        layout_map = {
            "TITLE": 0,
            "TITLE_AND_CONTENT": 1,
            "SECTION_HEADER": 2,
            "TWO_CONTENT": 3,
            "COMPARISON": 4,
            "TITLE_ONLY": 5,
            "BLANK": 6,
            "CONTENT_WITH_CAPTION": 7,
            "PICTURE_WITH_CAPTION": 8,
            "TITLE_AND_VERTICAL_TEXT": 9,
            "VERTICAL_TITLE_AND_TEXT": 10,
        }
        layout = self._presentation.slide_layouts[layout_map[layout_type]]
        slide = self._presentation.slides.add_slide(layout)
        return Slide(slide)

    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save presentation to file."""
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        self._presentation.save(file)

    def to_pptx(self) -> presentation.Presentation:
        """Convert to pptx presentation."""
        return self._presentation

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Presentation":
        """Create from pptx presentation."""
        if not hasattr(pptx_obj, "slides") or not hasattr(pptx_obj, "slide_layouts"):
            raise TypeError(f"Expected PptxPresentation, got {type(pptx_obj)}")
        return cls(pptx_obj)


class PptxPresentationFactory(PresentationFactory):
    """Factory for creating PPTX presentations."""

    def create_presentation(self) -> AbstractPresentation:
        """Create a new presentation."""
        return Presentation()

    def load_presentation(self, path: str) -> AbstractPresentation:
        """Load presentation from file."""
        return Presentation(PptxPresentation(path))


def to_pptx_length(length: Length | LiteralLength) -> pptx.util.Length:
    """Convert pptxr length to pptx length."""
    if isinstance(length, tuple):
        length = to_length(length)

    match length:
        case Inch():
            return pptx.util.Inches(length.value)
        case Centimeter():
            return pptx.util.Cm(length.value)
        case Point():
            return pptx.util.Pt(length.value)
        case _:
            assert_never(length)
