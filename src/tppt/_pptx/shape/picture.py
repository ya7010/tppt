from typing import IO, Literal, NotRequired, Self, TypedDict

from pptx.shapes.picture import Picture as PptxPicture
from tppt.types import FilePath
from tppt.types._length import Length, LiteralLength

from . import Shape


class PictureProps(TypedDict):
    """Picture properties."""

    left: Length | LiteralLength
    top: Length | LiteralLength
    width: NotRequired[Length | LiteralLength]
    height: NotRequired[Length | LiteralLength]


class PictureData(PictureProps):
    """Picture data."""

    type: Literal["picture"]

    image_file: FilePath | IO[bytes]


class Picture(Shape[PptxPicture]):
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
