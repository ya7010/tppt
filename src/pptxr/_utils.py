from typing import Callable, TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R")


def optional_map(
    func: Callable[[_T], _R],
    value: _T | None,
) -> _R | None:
    if value is None:
        return None
    return func(value)
