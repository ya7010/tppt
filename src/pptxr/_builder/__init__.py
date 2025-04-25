"""Builder pattern implementations for pptxr."""

from .presentation import PresentationBuilder
from .slide import SlideBuilder

__all__ = [
    "PresentationBuilder",
    "SlideBuilder",
]
