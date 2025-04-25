from typing import NotRequired, Self, TypedDict

from pptx.shapes.autoshape import Shape as PptxShape

from pptxr._pptx.types import PptxConvertible
from pptxr.types._color import Color
from pptxr.types._length import Length, LiteralLength


class TextProps(TypedDict):
    """Text properties."""

    font_size: NotRequired[Length | LiteralLength]
    font_color: NotRequired[Color]
    font_name: NotRequired[str]


class Text(PptxConvertible[PptxShape]):
    """Text data class."""

    def __init__(self, pptx_obj: PptxShape) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxShape) -> Self:
        """Create from pptx shape."""
        return cls(pptx_obj)
