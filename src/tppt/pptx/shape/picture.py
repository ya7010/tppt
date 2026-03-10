from typing import (
    Any,
    IO,
    TYPE_CHECKING,
    Literal,
    NotRequired,
    Self,
    TypedDict,
    assert_never,
    cast,
)

from pptx.opc.constants import CONTENT_TYPE
from pptx.shapes.picture import Movie as PptxMovie
from pptx.shapes.picture import Picture as PptxPicture

from tppt.types import FilePath, Length, LiteralLength

from . import BaseShape, RangeProps

if TYPE_CHECKING:
    from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

    from tppt.pptx.dml.line import LineFormat


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


class Picture(BaseShape[PptxPicture]):
    """Picture data class."""

    def __init__(
        self,
        pptx_obj: PptxPicture,
        data: PictureData | None = None,
        /,
    ) -> None:
        self._pptx = pptx_obj

    @property
    def auto_shape_type(self) -> "MSO_AUTO_SHAPE_TYPE | None":
        """Auto shape type of the picture."""
        return self._pptx.auto_shape_type

    @property
    def crop_bottom(self) -> float:
        """Crop bottom of the picture as a float between 0.0 and 1.0."""
        return self._pptx.crop_bottom

    @crop_bottom.setter
    def crop_bottom(self, value: float) -> None:
        self._pptx.crop_bottom = value

    def set_crop_bottom(self, value: float) -> Self:
        """Set crop bottom and return self for method chaining."""
        self.crop_bottom = value
        return self

    @property
    def crop_left(self) -> float:
        """Crop left of the picture as a float between 0.0 and 1.0."""
        return self._pptx.crop_left

    @crop_left.setter
    def crop_left(self, value: float) -> None:
        self._pptx.crop_left = value

    def set_crop_left(self, value: float) -> Self:
        """Set crop left and return self for method chaining."""
        self.crop_left = value
        return self

    @property
    def crop_right(self) -> float:
        """Crop right of the picture as a float between 0.0 and 1.0."""
        return self._pptx.crop_right

    @crop_right.setter
    def crop_right(self, value: float) -> None:
        self._pptx.crop_right = value

    def set_crop_right(self, value: float) -> Self:
        """Set crop right and return self for method chaining."""
        self.crop_right = value
        return self

    @property
    def crop_top(self) -> float:
        """Crop top of the picture as a float between 0.0 and 1.0."""
        return self._pptx.crop_top

    @crop_top.setter
    def crop_top(self, value: float) -> None:
        self._pptx.crop_top = value

    def set_crop_top(self, value: float) -> Self:
        """Set crop top and return self for method chaining."""
        self.crop_top = value
        return self

    @property
    def image(self) -> Any:
        """Image object for the picture."""
        return self._pptx.image

    @property
    def line(self) -> "LineFormat":
        """Line format of the picture."""
        from tppt.pptx.dml.line import LineFormat

        return LineFormat(self._pptx.line)


MOVIE_MIME_TYPE = Literal[
    "video/x-ms-asf",
    "video/avi",
    "video/quicktime",
    "video/mp4",
    "video/mpeg",
    "video/msvideo",
    "video/x-ms-wmv",
    "video/x-msvideo",
]


def to_pptx_movie_mime_type(mime_type: MOVIE_MIME_TYPE) -> str:
    """Convert movie mime type to pptx movie mime type."""
    match mime_type:
        case "video/x-ms-asf":
            return CONTENT_TYPE.ASF
        case "video/avi":
            return CONTENT_TYPE.AVI
        case "video/quicktime":
            return CONTENT_TYPE.MOV
        case "video/mp4":
            return CONTENT_TYPE.MP4
        case "video/mpeg":
            return CONTENT_TYPE.MPG
        case "video/msvideo":
            return CONTENT_TYPE.MS_VIDEO
        case "video/x-ms-wmv":
            return CONTENT_TYPE.WMV
        case "video/x-msvideo":
            return CONTENT_TYPE.X_MS_VIDEO
        case _:
            assert_never(mime_type)


class MovieProps(RangeProps):
    """Movie properties."""

    poster_frame_image: NotRequired[FilePath | IO[bytes]]

    mime_type: MOVIE_MIME_TYPE
    """
    Mime type of the movie.

    NOTE: The Movie shape is an experimental feature of python-pptx, and specifying the mime_type is recommended.
    """


class MovieData(MovieProps):
    """Movie data."""

    type: Literal["movie"]

    movie_file: FilePath | IO[bytes]


class Movie(BaseShape[PptxMovie]):
    """Movie data class."""

    def __init__(
        self,
        pptx_obj: PptxMovie,
        data: MovieData | None = None,
        /,
    ) -> None:
        self._pptx = pptx_obj

    @property
    def poster_frame(self) -> Any:
        """Poster frame image for the movie."""
        return self._pptx.poster_frame

    @property
    def media_type(self) -> str | None:
        """Media type (MIME type) of the movie."""
        return cast(str | None, self._pptx.media_type)
