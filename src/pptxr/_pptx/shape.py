"""Shape wrapper implementation."""

from typing import Self, cast

from pptx.shapes.base import BaseShape as PptxShape

from pptxr._pptx.types import PptxConvertible


class Shape(PptxConvertible[PptxShape]):
    """Shape wrapper with type safety."""

    def __init__(self, pptx_shape: PptxShape) -> None:
        """Initialize shape."""
        self._pptx: PptxShape = pptx_shape

    def get_text(self) -> str:
        """Get shape text."""
        return self._pptx.text  # type: ignore

    def set_text(self, text: str) -> None:
        """Set shape text."""
        self._pptx.text = text  # type: ignore

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return cast(PptxShape, self._pptx)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxShape) -> Self:
        """Create from pptx shape."""
        if not isinstance(pptx_obj, PptxShape):
            raise TypeError(f"Expected PptxShape, got {type(pptx_obj)}")
        return cls(pptx_obj)
