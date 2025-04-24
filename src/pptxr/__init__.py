"""pptxr - A type-safe PowerPoint presentation builder."""

from ._builders.slide import SlideBuilder
from ._data import ImageBone, SlideTemplate, TextBone
from ._presentation import Presentation
from ._slide_master import SlideMaster

__all__ = [
    "Presentation",
    "SlideMaster",
    "SlideTemplate",
    "SlideBuilder",
    "TextBone",
    "ImageBone",
]
