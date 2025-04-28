"""Typed Python PowerPoint Tool"""

from tppt.pptx.presentation import Presentation
from tppt.template.slide_layout import Placeholder, SlideLayout
from tppt.template.slide_master import Layout, SlideMaster, slide_master

from . import types as types

__all__ = [
    "Presentation",
    "SlideLayout",
    "Placeholder",
    "SlideLayout",
    "SlideMaster",
    "Layout",
    "slide_master",
]
