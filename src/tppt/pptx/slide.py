"""Slide wrapper implementation."""

import os
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Self,
    Unpack,
    cast,
    overload,
)

from pptx.slide import Slide as PptxSlide

from tppt.pptx.chart.chart import Chart, ChartData, ChartProps, to_pptx_chart_type
from tppt.pptx.shape.picture import (
    Movie,
    MovieData,
    MovieProps,
    PptxMovie,
    to_pptx_movie_mime_type,
)
from tppt.types import FilePath

from .converter import PptxConvertible, to_pptx_length
from .shape import BaseShape, RangeProps
from .shape.picture import Picture, PictureData, PictureProps
from .shape.placeholder import SlidePlaceholder
from .shape.text import Text, TextData, TextProps
from .slide_layout import SlideLayout
from .snotes_slide import NotesSlide
from .table.table import DataFrame, Table, TableData, TableProps, dataframe2list

if TYPE_CHECKING:
    pass


class Slide(PptxConvertible[PptxSlide]):
    """Slide wrapper with type safety."""

    def __init__(self, pptx_slide: PptxSlide) -> None:
        """Initialize slide."""
        self._pptx: PptxSlide = pptx_slide

    @property
    def name(self) -> str | None:
        """String representing the internal name of this slide.

        Returns an empty string if no name is assigned.
        """
        if name := self._pptx.name:
            return name
        return None

    @property
    def slide_id(self) -> int:
        """Get the slide id."""
        return self._pptx.slide_id

    @property
    def shapes(self) -> list[BaseShape]:
        """Get all shapes in the slide."""
        return [BaseShape(shape) for shape in self._pptx.shapes]

    @property
    def placeholders(self) -> list[SlidePlaceholder]:
        """Get all placeholders in the slide."""
        return [
            SlidePlaceholder(
                placeholder,  # type: ignore
            )
            for placeholder in self._pptx.placeholders
        ]

    @property
    def slide_layout(self) -> SlideLayout:
        """Get the slide layout."""
        return SlideLayout.from_pptx(self._pptx.slide_layout)

    @property
    def notes_slide(self) -> NotesSlide | None:
        """Get the notes slide."""
        if not self._pptx.has_notes_slide:
            return None
        return NotesSlide.from_pptx(self._pptx.notes_slide)

    def to_pptx(self) -> PptxSlide:
        """Convert to pptx slide."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlide) -> Self:
        """Create from pptx slide."""
        return cls(pptx_obj)


class SlideBuilder:
    """Slide builder."""

    def __init__(
        self,
        slide_layout: SlideLayout,
        placeholder_registry: Callable[[Slide], None],
    ) -> None:
        self._slide_layout = slide_layout
        self._shape_registry: list[Callable[[Slide], Any]] = []
        self._placeholder_registry = placeholder_registry

    @overload
    def text(self, text: str, /, **kwargs: Unpack[TextProps]) -> Self: ...

    @overload
    def text(
        self, text: Callable[[Text], Text], /, **kwargs: Unpack[RangeProps]
    ) -> Self: ...

    def text(
        self,
        text: str | Callable[[Text], Text],
        /,
        **kwargs: Unpack[TextProps],
    ) -> Self:
        def _register(slide: Slide) -> Text:
            data = TextData(
                type="text",
                text=text if isinstance(text, str) else "",
                top=kwargs["top"],
                left=kwargs["left"],
                width=kwargs["width"],
                height=kwargs["height"],
            )

            text_obj = Text(
                slide.to_pptx().shapes.add_textbox(
                    to_pptx_length(data["left"]),
                    to_pptx_length(data["top"]),
                    to_pptx_length(data["width"]),
                    to_pptx_length(data["height"]),
                ),
                data,
            )
            if isinstance(text, Callable):
                return text(text_obj)
            else:
                return text_obj

        self._shape_registry.append(_register)

        return self

    @overload
    def picture(
        self, image: FilePath | IO[bytes], /, **kwargs: Unpack[PictureProps]
    ) -> Self: ...

    @overload
    def picture(
        self,
        image: Callable[[Picture], Picture],
        /,
        image_file: FilePath | IO[bytes],
        **kwargs: Unpack[PictureProps],
    ) -> Self: ...

    def picture(
        self,
        image: FilePath | IO[bytes] | Callable[[Picture], Picture],
        image_file: FilePath | IO[bytes] | None = None,
        **kwargs: Unpack[PictureProps],
    ) -> Self:
        if not isinstance(image, Callable):
            image_file = image

        assert image_file
        if isinstance(image_file, os.PathLike):
            image_file = os.fspath(image_file)

        def _register(slide: Slide) -> Picture:
            data = PictureData(type="picture", image_file=image_file, **kwargs)
            picture_obj = Picture(
                slide.to_pptx().shapes.add_picture(
                    image_file,
                    to_pptx_length(data["left"]),
                    to_pptx_length(data["top"]),
                    to_pptx_length(data.get("width")),
                    to_pptx_length(data.get("height")),
                ),
                data,
            )
            if isinstance(image, Callable):
                return image(picture_obj)
            else:
                return picture_obj

        self._shape_registry.append(_register)

        return self

    @overload
    def movie(
        self, movie: FilePath | IO[bytes], /, **kwargs: Unpack[MovieProps]
    ) -> Self: ...

    @overload
    def movie(
        self,
        movie: Callable[[Movie], Movie],
        /,
        movie_file: FilePath | IO[bytes],
        **kwargs: Unpack[MovieProps],
    ) -> Self: ...

    def movie(
        self,
        movie: FilePath | IO[bytes] | Callable[[Movie], Movie],
        /,
        movie_file: FilePath | IO[bytes] | None = None,
        **kwargs: Unpack[MovieProps],
    ) -> Self:
        if not isinstance(movie, Callable):
            movie_file = movie

        assert movie_file
        if isinstance(movie_file, os.PathLike):
            movie_file = os.fspath(movie_file)

        poster_frame_image = kwargs.get("poster_frame_image")
        if isinstance(poster_frame_image, os.PathLike):
            poster_frame_image = os.fspath(poster_frame_image)

        mime_type = to_pptx_movie_mime_type(kwargs["mime_type"])

        def _register(slide: Slide) -> Movie:
            data = MovieData(type="movie", movie_file=movie_file, **kwargs)
            movie_obj = Movie(
                cast(
                    PptxMovie,
                    slide.to_pptx().shapes.add_movie(
                        movie_file,
                        to_pptx_length(data["left"]),
                        to_pptx_length(data["top"]),
                        to_pptx_length(data.get("width")),
                        to_pptx_length(data.get("height")),
                        poster_frame_image=poster_frame_image,
                        mime_type=mime_type,
                    ),
                ),
                data,
            )
            if isinstance(movie, Callable):
                return movie(movie_obj)
            else:
                return movie_obj

        self._shape_registry.append(_register)

        return self

    @overload
    def table(self, data: DataFrame, /, **kwargs: Unpack[TableProps]) -> Self: ...

    @overload
    def table(
        self,
        data: Callable[[Table], Table],
        /,
        rows: int,
        cols: int,
        **kwargs: Unpack[TableProps],
    ) -> Self: ...

    def table(
        self,
        data: DataFrame | Callable[[Table], Table],
        /,
        rows: int | None = None,
        cols: int | None = None,
        **kwargs: Unpack[TableProps],
    ) -> Self:
        if isinstance(data, Callable):
            assert rows is not None
            assert cols is not None
            table_data: TableData = {"type": "table", "data": [], **kwargs}
        else:
            data = dataframe2list(data)
            rows, cols = len(data), len(data[0])

            table_data: TableData = {
                "type": "table",
                "data": data,
                **kwargs,
            }

        def _register(slide: Slide) -> Table:
            table_obj = Table(
                slide.to_pptx()
                .shapes.add_table(
                    rows,
                    cols,
                    to_pptx_length(table_data["left"]),
                    to_pptx_length(table_data["top"]),
                    to_pptx_length(table_data["width"]),
                    to_pptx_length(table_data["height"]),
                )
                .table,
                table_data,
            )

            if isinstance(data, Callable):
                return data(table_obj)
            else:
                return table_obj

        self._shape_registry.append(_register)

        return self

    def chart(
        self,
        data: Callable[[Chart], Chart] | None = None,
        /,
        **kwargs: Unpack[ChartProps],
    ) -> Self:
        chart_type = to_pptx_chart_type(kwargs["chart_type"])

        def _register(slide: Slide) -> Chart:
            data: ChartData = {
                "type": "chart",
                **kwargs,
            }

            chart_obj = Chart(
                slide.to_pptx().shapes.add_chart(
                    chart_type=chart_type,
                    x=to_pptx_length(data["x"]),
                    y=to_pptx_length(data["y"]),
                    cx=to_pptx_length(data["cx"]),
                    cy=to_pptx_length(data["cy"]),
                    chart_data=data["chart_data"],
                )
            )
            if isinstance(data, Callable):
                return data(chart_obj)
            else:
                return chart_obj

        self._shape_registry.append(_register)

        return self

    def _build(self, slide: PptxSlide) -> Slide:
        tppt_slide = Slide(slide)

        self._placeholder_registry(tppt_slide)
        for register in self._shape_registry:
            register(tppt_slide)

        return tppt_slide
