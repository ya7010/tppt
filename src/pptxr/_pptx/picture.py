from typing import IO, Literal, NotRequired, Self, TypedDict

from pptx.shapes.picture import Picture as PptxPicture

from pptxr.types._length import Length, LiteralLength

from .converter import PptxConvertible


class PictureProps(TypedDict):
    """Picture properties."""

    image_file: str | IO[bytes]
    left: Length | LiteralLength
    top: Length | LiteralLength
    width: NotRequired[Length | LiteralLength]
    height: NotRequired[Length | LiteralLength]


class PictureData(PictureProps):
    """Picture data."""

    type: Literal["picture"]


class Picture(PptxConvertible[PptxPicture]):
    """Picture data class."""

    def __init__(
        self,
        pptx_obj: PptxPicture,
        data: PictureData | None = None,
        /,
    ) -> None:
        self._pptx = pptx_obj

    def to_pptx(self) -> PptxPicture:
        """Convert to pptx shape."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxPicture) -> Self:
        """Create from pptx shape."""
        return cls(pptx_obj)
