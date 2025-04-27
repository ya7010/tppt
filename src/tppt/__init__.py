"""Typed Python PowerPoint Tool"""

from tppt.pptx.presentation import Presentation
from tppt.pptx.shape import Shape
from tppt.pptx.slide import Slide, SlideBuilder
from tppt.template.slide_layout import Placeholder, SlideLayout
from tppt.template.slide_master import Layout, SlideMaster, slide_master

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
    "Layout",
    "slide_master",
]
