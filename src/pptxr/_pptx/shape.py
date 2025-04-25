"""Shape wrapper implementation."""

from typing import cast

from pptx.shapes.base import BaseShape as PptxShapeType

from pptxr._pptx.presentation import PptxConvertible


class Shape(PptxConvertible):
    """Shape wrapper with type safety."""

    def __init__(self, pptx_shape: PptxShapeType) -> None:
        """Initialize shape."""
        self._pptx = pptx_shape

    def get_text(self) -> str:
        """Get shape text."""
        return self._pptx.text  # type: ignore

    def set_text(self, text: str) -> None:
        """Set shape text."""
        self._pptx.text = text  # type: ignore

    def to_pptx(self) -> PptxShapeType:
        """Convert to pptx shape."""
        return cast(PptxShapeType, self._pptx)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxShapeType) -> "Shape":
        """Create from pptx shape."""
        if not isinstance(pptx_obj, PptxShapeType):
            raise TypeError(f"Expected PptxShape, got {type(pptx_obj)}")
        return cls(pptx_obj)
