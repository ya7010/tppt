"""PPTX implementation package."""

# pyright: ignore
# type: ignore

from .converters import (
    PptxPresentationFactory,
    Presentation,
    Shape,
    Slide,
)

__all__ = [
    "Presentation",
    "PptxPresentationFactory",
    "Shape",
    "Slide",
]
