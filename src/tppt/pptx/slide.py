"""Slide wrapper implementation."""

import os
from typing import IO, TYPE_CHECKING, Any, Callable, Self, Unpack, cast

from pptx.slide import Slide as PptxSlide

from tppt.types import FilePath

from .converter import PptxConvertible, to_pptx_length
from .placeholder import SlidePlaceholder
from .shape import Shape
from .shape.picture import Picture, PictureData, PictureProps
from .shape.table import DataFrame, Table, TableData, TableProps, dataframe2list
from .shape.text import Text, TextData, TextProps
from .slide_layout import SlideLayout
from .snotes_slide import NotesSlide

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
    def shapes(self) -> list[Shape]:
        """Get all shapes in the slide."""
        return [Shape(shape) for shape in self._pptx.shapes]

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
        return cast(PptxSlide, self._pptx)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxSlide) -> Self:
        """Create from pptx slide."""
        return cls(pptx_obj)


class SlideBuilder:
    """Slide builder."""

    def __init__(
        self,
        slide_layout: SlideLayout,
    ) -> None:
        self._slide_layout = slide_layout
        self._shape_registry: list[Callable[[Slide], Shape[Any]]] = []

    def text(self, text: str, **kwargs: Unpack[TextProps]) -> Self:
        data = TextData(type="text", text=text, **kwargs)

        self._shape_registry.append(
            lambda slide: Text(
                slide.to_pptx().shapes.add_textbox(
                    to_pptx_length(data["left"]),
                    to_pptx_length(data["top"]),
                    to_pptx_length(data["width"]),
                    to_pptx_length(data["height"]),
                ),
                data,
            )
        )

        return self

    def picture(
        self, image_file: FilePath | IO[bytes], **kwargs: Unpack[PictureProps]
    ) -> Self:
        data = PictureData(type="picture", image_file=image_file, **kwargs)

        if isinstance(data["image_file"], os.PathLike):
            image_file = os.fspath(data["image_file"])
        else:
            image_file = data["image_file"]

        self._shape_registry.append(
            lambda slide: Picture(
                slide.to_pptx().shapes.add_picture(
                    image_file,
                    to_pptx_length(data["left"]),
                    to_pptx_length(data["top"]),
                    to_pptx_length(data.get("width")),
                    to_pptx_length(data.get("height")),
                ),
                data,
            )
        )

        return self

    def table(self, data: DataFrame, **kwargs: Unpack[TableProps]) -> Self:
        data = dataframe2list(data)
        rows, cols = len(data), len(data[0])
        table_data: TableData = {"type": "table", "data": data, **kwargs}

        self._shape_registry.append(
            lambda slide: Table(
                slide.to_pptx().shapes.add_table(
                    rows,
                    cols,
                    to_pptx_length(table_data["left"]),
                    to_pptx_length(table_data["top"]),
                    to_pptx_length(table_data["width"]),
                    to_pptx_length(table_data["height"]),
                ),
                table_data,
            )
        )
        return self

    def build(self, slide: PptxSlide) -> Slide:
        tppt_slide = Slide(slide)
        for register in self._shape_registry:
            register(tppt_slide)

        return tppt_slide
