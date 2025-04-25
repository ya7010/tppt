"""pptx wrapper implementation."""

# pyright: ignore
# type: ignore

from pptxr._pptx.presentation import PptxPresentationFactory, Presentation
from pptxr._pptx.shape import Shape
from pptxr._pptx.slide import Slide
from pptxr._pptx.types import PptxConvertible

__all__ = [
    "Presentation",
    "PptxPresentationFactory",
    "Shape",
    "Slide",
    "PptxConvertible",
]
