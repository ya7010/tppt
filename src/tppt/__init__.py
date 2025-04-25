"""Typed Python PowerPoint Tool"""

from tppt import types as types
from tppt._pptx.presentation import Presentation
from tppt._pptx.shape import Shape
from tppt._pptx.slide import Slide, SlideBuilder
from tppt._pptx.slide_layout import SlideLayout
from tppt._pptx.slide_master import SlideMaster
from tppt._tppt.slide_master import tpptSlideMaster

__all__ = [
    # Pptx
    "Presentation",
    "Shape",
    "Slide",
    "SlideBuilder",
    "SlideLayout",
    "SlideMaster",
    # tppt
    "tpptSlideMaster",
]
