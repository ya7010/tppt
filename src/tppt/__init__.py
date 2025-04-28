"""Typed Python PowerPoint Tool"""

import importlib.metadata
from typing import Callable, Concatenate, ParamSpec, TypeVar

from tppt.pptx.presentation import Presentation as Presentation
from tppt.pptx.shape.picture import Picture as Picture
from tppt.pptx.shape.text import Text as Text
from tppt.pptx.slide import Slide as Slide
from tppt.pptx.table import Table as Table
from tppt.pptx.table import TableCellStyle as TableCellStyle
from tppt.template.slide_layout import Placeholder as Placeholder
from tppt.template.slide_layout import SlideLayout as SlideLayout
from tppt.template.slide_master import Layout as Layout
from tppt.template.slide_master import SlideMaster as SlideMaster
from tppt.template.slide_master import slide_master as slide_master

from . import types as types

__version__ = importlib.metadata.version("tppt")

T = TypeVar("T")
P = ParamSpec("P")


def apply(
    func: Callable[Concatenate[T, P], T], *args: P.args, **kwargs: P.kwargs
) -> Callable[[T], T]:
    """
    Partially applies the given function `func` with arguments `args` and keyword arguments `kwargs`,
    returning a new function that takes only the first argument.

    Args:
        func: A function that takes a first argument of type `T` and variable arguments `P`, returning `T`
        *args: Variable positional arguments to partially apply to `func`
        **kwargs: Variable keyword arguments to partially apply to `func`

    Returns:
        A function that takes a single argument `x` and calls `func(x, *args, **kwargs)`
    """

    def wrapper(x: T) -> T:
        return func(x, *args, **kwargs)

    return wrapper
