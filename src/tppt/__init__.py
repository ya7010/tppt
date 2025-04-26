"""Typed Python PowerPoint Tool"""

from tppt import types as types
from tppt.pptx.presentation import Presentation
from tppt.pptx.shape import Shape
from tppt.pptx.slide import Slide, SlideBuilder
from tppt.pptx.slide_layout import SlideLayout
from tppt.pptx.slide_master import SlideMaster
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
