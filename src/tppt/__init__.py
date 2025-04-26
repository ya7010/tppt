"""Typed Python PowerPoint Tool"""

from tppt import types as types
from tppt._pptx.presentation import Presentation
from tppt._pptx.shape import Shape
from tppt._pptx.slide import Slide, SlideBuilder
from tppt._pptx.slide_layout import SlideLayout
from tppt._pptx.slide_master import SlideMaster
from tppt.slide_layout import Placeholder, TpptSlideLayout
from tppt.slide_master import TpptSlideMaster

__all__ = [
    "Presentation",
    "Shape",
    "Slide",
    "SlideBuilder",
    "SlideLayout",
    "SlideMaster",
    "Placeholder",
    "TpptSlideLayout",
    "TpptSlideMaster",
]
