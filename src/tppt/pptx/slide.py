"""Slide wrapper implementation."""

import os
from typing import IO, TYPE_CHECKING, Any, Callable, Self, Unpack, overload

from pptx.slide import Slide as PptxSlide

from tppt.types import FilePath

from .converter import PptxConvertible, to_pptx_length
from .placeholder import SlidePlaceholder
from .shape import RangeProps, Shape
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
        self._shape_registry: list[Callable[[Slide], Shape[Any]]] = []
        self._placeholder_registry = placeholder_registry

    @overload
    def text(self, text: str, **kwargs: Unpack[TextProps]) -> Self: ...

    @overload
    def text(
        self, text: Callable[[Text], Text], **kwargs: Unpack[RangeProps]
    ) -> Self: ...

    def text(
        self,
        text: str | Callable[[Text], Text],
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

    def picture(
        self, image_file: FilePath | IO[bytes], **kwargs: Unpack[PictureProps]
    ) -> Self:
        if isinstance(image_file, os.PathLike):
            image_file = os.fspath(image_file)

        data = PictureData(type="picture", image_file=image_file, **kwargs)

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

    def _build(self, slide: PptxSlide) -> Slide:
        tppt_slide = Slide(slide)

        self._placeholder_registry(tppt_slide)
        for register in self._shape_registry:
            register(tppt_slide)

        return tppt_slide
