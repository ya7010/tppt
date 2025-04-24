"""Converter implementations for pptx objects."""

from typing import Any, Union

from pptx import Presentation as PptxPresentation
from pptx.shapes.base import BaseShape as PptxShape
from pptx.slide import Slide as PptxSlide

from .types import PptxConvertible

# pyright: ignore
# type: ignore


class Presentation:
    """Presentation wrapper."""

    def __init__(self, pptx_presentation: Union[PptxPresentation, None] = None) -> None:
        """Initialize presentation."""
        if pptx_presentation is None:
            self._presentation = PptxPresentation()
        else:
            self._presentation = pptx_presentation

    @property
    def presentation(self) -> PptxPresentation:
        """Get presentation."""
        return self._presentation

    def to_pptx(self) -> PptxPresentation:
        """Convert to pptx presentation."""
        return self.presentation

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Presentation":
        """Create from pptx presentation."""
        if not hasattr(pptx_obj, "slides") or not hasattr(pptx_obj, "slide_layouts"):
            raise TypeError(f"Expected PptxPresentation, got {type(pptx_obj)}")
        return cls(pptx_obj)


class Slide(PptxConvertible):
    """Slide wrapper with type safety."""

    def __init__(self, pptx_slide: PptxSlide) -> None:
        """Initialize slide."""
        self._pptx = pptx_slide

    def to_pptx(self) -> PptxSlide:
        """Convert to pptx slide."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Slide":
        """Create from pptx slide."""
        if not isinstance(pptx_obj, PptxSlide):
            raise TypeError(f"Expected PptxSlide, got {type(pptx_obj)}")
        return cls(pptx_obj)


class Shape(PptxConvertible):
    """Shape wrapper with type safety."""

    def __init__(self, pptx_shape: PptxShape) -> None:
        """Initialize shape."""
        self._pptx = pptx_shape

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "Shape":
        """Create from pptx shape."""
        if not isinstance(pptx_obj, PptxShape):
            raise TypeError(f"Expected PptxShape, got {type(pptx_obj)}")
        return cls(pptx_obj)
