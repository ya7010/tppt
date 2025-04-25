from typing import Self

from pptx.shapes.autoshape import Shape as PptxShape

from pptxr._pptx.converter import PptxConvertible


class Title(PptxConvertible[PptxShape]):
    """Title of the slide."""

    def __init__(self, pptx_obj: PptxShape) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxShape:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxShape) -> Self:
        """Create from pptx shape."""
        return cls(pptx_obj)
