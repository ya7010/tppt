"""Type definitions for pptx conversion layer."""

from typing import Any, Protocol, TypeVar

# pyright: ignore
# type: ignore


class PptxConvertible(Protocol):
    """Protocol for objects that can be converted to and from pptx objects."""

    def to_pptx(self) -> Any:
        """Convert to pptx object."""
        ...

    @classmethod
    def from_pptx(cls, pptx_obj: Any) -> "PptxConvertible":
        """Create from pptx object."""
        ...


T = TypeVar("T", bound=PptxConvertible)


class PptxConverter:
    """Utility class for converting pptx objects."""

    @staticmethod
    def to_pptx(obj: PptxConvertible) -> Any:
        """Convert object to pptx format."""
        return obj.to_pptx()

    @staticmethod
    def from_pptx(pptx_obj: Any, target_cls: type[T]) -> T:
        """Convert pptx object to target class."""
        return target_cls.from_pptx(pptx_obj)
