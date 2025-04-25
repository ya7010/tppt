from typing import Self, TypedDict

from pptx.shapes.autoshape import Shape as PptxShape

from pptxr.types._length import Length, LiteralLength

from .converter import PptxConvertible


class TextProps(TypedDict):
    """Text properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: Length | LiteralLength
    height: Length | LiteralLength


class TextData(TextProps):
    """Text data."""

    contents: str


class Text(PptxConvertible[PptxShape]):
    """Text data class."""

    def __init__(self, pptx_obj: PptxShape, data: TextData | None = None, /) -> None:
        if data:
            pptx_obj.text = data["contents"]

        self._pptx = pptx_obj

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxShape) -> Self:
        """Create from pptx shape."""
        return cls(pptx_obj)
