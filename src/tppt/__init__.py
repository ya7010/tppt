"""Typed Python PowerPoint Tool"""

import importlib.metadata
from typing import Callable, Concatenate, ParamSpec, TypeVar

from tppt.pptx.presentation import Presentation
from tppt.template.slide_layout import Placeholder, SlideLayout
from tppt.template.slide_master import Layout, SlideMaster, slide_master

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


__all__ = [
    "Presentation",
    "SlideLayout",
    "Placeholder",
    "SlideLayout",
    "SlideMaster",
    "Layout",
    "slide_master",
    "apply",
]
