"""PPTX implementation package."""

# pyright: ignore
# type: ignore

from .presentation import PptxPresentationFactory, Presentation
from .shape import Shape
from .slide import Slide

__all__ = [
    "Presentation",
    "PptxPresentationFactory",
    "Shape",
    "Slide",
]
