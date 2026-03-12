"""Slide wrapper implementation."""

import os
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Self,
    TypeVar,
    Unpack,
    cast,
    overload,
)

from pptx.chart.data import ChartData as PptxChartData
from pptx.slide import Slide as PptxSlide
from pptx.slide import _BaseSlide as _PptxBaseSlide

from tppt.pptx.chart.chart import Chart, ChartData, ChartProps, to_pptx_chart_type
from tppt.pptx.shape.picture import (
    Movie,
    MovieData,
    MovieProps,
    PptxMovie,
    to_pptx_movie_mime_type,
)
from tppt.types import Color, FilePath, Length, LiteralColor, LiteralLength

from .converter import PptxConvertible, to_pptx_length, to_pptx_rgb_color
from .shape import BaseShape, RangeProps, Shape
from .shape.picture import Picture, PictureData, PictureProps
from .shape.placeholder import SlidePlaceholder
from .shape.text import Text, TextData, TextProps
from .slide_layout import SlideLayout
from .table.table import DataFrame, Table, TableData, TableProps, dataframe2list

if TYPE_CHECKING:
    from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE

    from tppt.pptx.shape.background import Background

    from .notes_slide import NotesSlide

_GenericPptxBaseSlide = TypeVar("_GenericPptxBaseSlide", bound=_PptxBaseSlide)


class _BaseSlide(PptxConvertible[_GenericPptxBaseSlide]):
    @property
    def background(self) -> "Background":
        """Background of the slide."""
        from tppt.pptx.shape.background import Background

        return Background(self._pptx.background)

    @property
    def name(self) -> str:
        return self._pptx.name

    @name.setter
    def name(self, value: str) -> None:
        self._pptx.name = value

    def set_name(self, value: str) -> Self:
        self.name = value
        return self


class Slide(_BaseSlide[PptxSlide]):
    """Slide wrapper with type safety."""

    @property
    def follow_master_background(self) -> bool:
        return self._pptx.follow_master_background

    @property
    def notes_slide(self) -> "NotesSlide | None":
        """Get the notes slide."""
        if not self._pptx.has_notes_slide:
            return None

        from .notes_slide import NotesSlide

        return NotesSlide(self._pptx.notes_slide)

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
    def shapes(self) -> list[BaseShape]:
        """Get all shapes in the slide."""
        return [BaseShape(shape) for shape in self._pptx.shapes]

    @property
    def slide_id(self) -> int:
        """Get the slide id."""
        return self._pptx.slide_id

    @property
    def slide_layout(self) -> SlideLayout:
        """Get the slide layout."""
        return SlideLayout.from_pptx(self._pptx.slide_layout)


class SlideBuilder:
    """Slide builder."""

    class AddShapeProps(RangeProps, total=False):
        fill_color: Color | LiteralColor
        fill_alpha: float
        line_color: Color | LiteralColor
        line_width: Length | LiteralLength
        text: str
        font_size: Length | LiteralLength
        font_color: Color | LiteralColor

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
                **kwargs,
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
                    # NOTE: Type hint of python-pptx is incorrect. Expected Movie, but GraphicFrame is returned.
                    # Ref: https://github.com/scanny/python-pptx/pull/1057/commits/56338fa314d2c5bceb8b1756a50ed64ea8984abe
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
                    chart_data=cast(PptxChartData, data["chart_data"]),
                )
            )
            if isinstance(data, Callable):
                return data(chart_obj)
            else:
                return chart_obj

        self._shape_registry.append(_register)

        return self

    @overload
    def add_shape(
        self,
        shape_type: "MSO_AUTO_SHAPE_TYPE",
        /,
        **kwargs: Unpack[AddShapeProps],
    ) -> Self: ...

    @overload
    def add_shape(
        self,
        shape_type: "MSO_AUTO_SHAPE_TYPE",
        shape: Callable[[Shape], Shape],
        /,
        **kwargs: Unpack[AddShapeProps],
    ) -> Self: ...

    def add_shape(
        self,
        shape_type: "MSO_AUTO_SHAPE_TYPE",
        shape: Callable[[Shape], Shape] | None = None,
        /,
        fill_color: "Color | LiteralColor | None" = None,
        fill_alpha: float | None = None,
        line_color: "Color | LiteralColor | None" = None,
        line_width: "Length | LiteralLength | None" = None,
        text: str | None = None,
        font_size: "Length | LiteralLength | None" = None,
        font_color: "Color | LiteralColor | None" = None,
        **kwargs: Unpack[RangeProps],
    ) -> Self:
        """Add a shape to the slide."""

        def _register(slide: Slide) -> Shape:
            shape_obj = Shape(
                slide.to_pptx().shapes.add_shape(
                    shape_type,
                    to_pptx_length(kwargs["left"]),
                    to_pptx_length(kwargs["top"]),
                    to_pptx_length(kwargs["width"]),
                    to_pptx_length(kwargs["height"]),
                )
            )

            if fill_color is not None:
                rgb, alpha = to_pptx_rgb_color(fill_color)
                shape_obj.fill.solid().fore_color.set_rgb(fill_color)

            if fill_alpha is not None:
                from lxml.etree import _Element

                from pptx.oxml.ns import _nsmap as namespace
                from pptx.oxml.xmlchemy import OxmlElement

                pptx_shape = shape_obj.to_pptx()
                solid_fill = cast(
                    _Element,
                    pptx_shape.fill._xPr.solidFill,  # type: ignore[union-attr]
                )
                # Remove existing alpha element if any
                existing_alpha = solid_fill.find("a:alpha", namespace)
                if existing_alpha is not None:
                    solid_fill.remove(existing_alpha)
                alpha_elem = OxmlElement("a:alpha")
                alpha_elem.attrib["val"] = str(int(fill_alpha * 100000))
                # Find srgbClr or other color child to append alpha to
                for child in solid_fill:
                    child.append(alpha_elem)
                    break

            if line_color is not None:
                shape_obj.line.fill.solid().fore_color.set_rgb(line_color)

            if line_width is not None:
                from tppt.types._length import EnglishMetricUnits

                pptx_len = to_pptx_length(line_width)
                shape_obj.line.set_width(EnglishMetricUnits(int(pptx_len)))

            if text is not None:
                shape_obj.text = text

            if font_size is not None or font_color is not None:
                tf = shape_obj.to_pptx().text_frame
                if tf.paragraphs:
                    paragraph = tf.paragraphs[0]
                    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
                    if font_size is not None:
                        run.font.size = to_pptx_length(font_size)
                    if font_color is not None:
                        rgb_val, _ = to_pptx_rgb_color(font_color)
                        run.font.color.rgb = rgb_val

            if shape is not None:
                return shape(shape_obj)
            else:
                return shape_obj

        self._shape_registry.append(_register)
        return self

    def tap(self, callback: Callable[[Slide], None]) -> Self:
        """Register a callback for direct slide access."""
        self._shape_registry.append(callback)
        return self

    def _build(self, slide: PptxSlide) -> Slide:
        tppt_slide = Slide(slide)

        self._placeholder_registry(tppt_slide)
        for register in self._shape_registry:
            register(tppt_slide)

        return tppt_slide
