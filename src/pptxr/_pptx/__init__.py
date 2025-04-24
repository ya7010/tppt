"""pptx library wrapper for type safety.

This module provides type-safe interface for pptx library.
"""

# pyright: ignore
# type: ignore

from .converters import Presentation, Shape, Slide
from .types import PptxConverter, PptxConvertible

__all__ = [
    "PptxConvertible",
    "PptxConverter",
    "Presentation",
    "Slide",
    "Shape",
]
