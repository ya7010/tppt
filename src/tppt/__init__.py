"""Typed Python PowerPoint Tool"""

from tppt.pptx.presentation import Presentation
from tppt.pptx.shape import Shape
from tppt.pptx.slide import Slide, SlideBuilder
from tppt.slide_layout import Placeholder, SlideLayout
from tppt.slide_master import SlideMaster

from . import pptx as pptx
from . import types as types

__all__ = [
    "Presentation",
    "Shape",
    "Slide",
    "SlideBuilder",
    "SlideLayout",
    "Placeholder",
    "SlideLayout",
    "SlideMaster",
]
