from typing import IO, Literal, Self

from pptx.shapes.picture import Picture as PptxPicture

from tppt.types import FilePath

from . import BaseShape, RangeProps


class PictureProps(RangeProps):
    """Picture properties."""


class PictureData(PictureProps):
    """Picture data."""

    type: Literal["picture"]

    image_file: FilePath | IO[bytes]


class Picture(BaseShape[PptxPicture]):
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
