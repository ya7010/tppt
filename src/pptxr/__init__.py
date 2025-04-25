"""PowerPoint Builder Library"""

from pptxr._pptx.presentation import Presentation
from pptxr._pptx.shape import Shape
from pptxr._pptx.slide import Slide, SlideBuilder
from pptxr._pptx.slide_layout import SlideLayout
from pptxr._pptx.slide_master import SlideMaster

__all__ = [
    "Presentation",
    "Shape",
    "Slide",
    "SlideBuilder",
    "SlideLayout",
    "SlideMaster",
]
