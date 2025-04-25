"""Type definitions for pptx wrapper."""

from typing import Protocol, Self, TypeVar, runtime_checkable

PT = TypeVar("PT")


@runtime_checkable
class PptxConvertible(Protocol[PT]):
    """Protocol for objects that can be converted to and from pptx objects."""

    def to_pptx(self) -> PT:
        """Convert to pptx object."""
        ...

    @classmethod
    def from_pptx(cls, pptx_obj: PT) -> Self:
        """Create from pptx object."""
        ...
