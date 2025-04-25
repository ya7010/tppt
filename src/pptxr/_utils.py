from typing import Any, Callable, TypeVar

_T = TypeVar("_T")
_U = TypeVar("_U")
_R = TypeVar("_R")


def optional_map(
    func: Callable[[_T | Any], _R],
    value: _T | None,
) -> _R | None:
    if value is None:
        return None
    return func(value)
