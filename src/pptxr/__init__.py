"""PowerPoint presentation library."""

from pptxr._data import Presentation, Shape, Slide

from ._builder.slide import SlideBuilder
from ._data import Image, SlideTemplate, Text
from ._presentation import Presentation
from ._slide_master import SlideMaster

__all__ = ["Presentation", "Shape", "Slide"]
