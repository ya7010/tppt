"""PowerPoint presentation creation library."""

import os
import pathlib
from dataclasses import dataclass
from typing import (
    IO,
    Any,
    Literal,
    NotRequired,
    TypedDict,
    Unpack,
    overload,
)

from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN

from ._pptx import PptxPresentationFactory
from .abstract.types import Slide as AbstractSlide
from .units import (
    Inch,
    LiteralLength,
    to_inche,
    to_length,
)

SlideLayout = Literal[
    "TITLE",
    "TITLE_AND_CONTENT",
    "SECTION_HEADER",
    "TWO_CONTENT",
    "COMPARISON",
    "TITLE_ONLY",
    "BLANK",
    "CONTENT_WITH_CAPTION",
    "PICTURE_WITH_CAPTION",
    "TITLE_AND_VERTICAL_TEXT",
    "VERTICAL_TITLE_AND_TEXT",
]

LayoutType = Literal["flex", "grid", "absolute"]

Align = Literal["start", "center", "end"]

Justify = Literal["start", "center", "end", "space-between", "space-around"]


class Layout(TypedDict):
    """Data class representing layout settings."""

    type: NotRequired[LayoutType]
    """Layout type"""

    direction: NotRequired[str]
    """Layout direction ("row" or "column")"""

    align: NotRequired[Align]
    """Element alignment"""

    justify: NotRequired[Justify]
    """Element justification"""

    gap: NotRequired[LiteralLength]
    """Gap between elements"""

    padding: NotRequired[dict[str, LiteralLength]]
    """Padding (top, right, bottom, left)"""

    width: NotRequired[LiteralLength]
    """Width"""

    height: NotRequired[LiteralLength]
    """Height"""


class Text(TypedDict):
    """Data class representing text element."""

    type: Literal["text"]
    """Type of component"""

    text: str | None
    """Text content"""

    size: LiteralLength | None
    """Font size"""

    bold: NotRequired[bool]
    """Whether text is bold"""

    italic: NotRequired[bool]
    """Whether text is italic"""

    color: str | None
    """Text color"""

    layout: NotRequired[Layout]
    """Layout settings"""


@dataclass
class Shape:
    """Data class representing shape."""

    type: str
    """Shape type"""

    left: LiteralLength
    """Position from left edge"""

    top: LiteralLength
    """Position from top edge"""

    width: LiteralLength
    """Width"""

    height: LiteralLength
    """Height"""

    text: Text | None = None
    """Text within shape"""


class Image(TypedDict):
    """Data class representing image element."""

    type: Literal["image"]
    """Type of component"""

    path: str
    """Path to image file"""

    width: NotRequired[LiteralLength]
    """Width"""

    height: NotRequired[LiteralLength]
    """Height"""

    layout: NotRequired[Layout]
    """Layout settings"""


class Chart(TypedDict):
    """Data class representing chart element."""

    type: Literal["chart"]
    """Type of component"""

    chart_type: str
    """Chart type ("bar", "line", "pie", etc.)"""

    data: list[dict[str, Any]]
    """Chart data"""

    width: NotRequired[LiteralLength]
    """Width"""

    height: NotRequired[LiteralLength]
    """Height"""

    layout: NotRequired[Layout]
    """Layout settings"""


@dataclass
class TableCell:
    """Data class representing table cell."""

    text: str
    """Cell text content"""

    size: LiteralLength | None = None
    """Font size"""

    bold: bool = False
    """Whether text is bold"""

    italic: bool = False
    """Whether text is italic"""

    color: str | None = None
    """Text color"""

    background: str | None = None
    """Background color"""

    align: PP_ALIGN = PP_ALIGN.LEFT
    """Text alignment"""


class TableParams(TypedDict):
    """Data class representing table element."""

    type: Literal["table"]
    """Type of component"""

    rows: int
    """Number of rows"""

    cols: int
    """Number of columns"""

    data: list[list[TableCell]]
    """Table data"""

    width: NotRequired[LiteralLength]
    """Width"""

    height: NotRequired[LiteralLength]
    """Height"""

    layout: NotRequired[Layout]
    """Layout settings"""


class Table(TableParams):
    """Data class representing table element."""

    type: Literal["table"]
    """Type of component"""


Component = Text | Image | Chart | Table
"""Union type representing any component type"""


class Container(TypedDict):
    """Data class representing container."""

    components: list[Component]
    """Components within container"""

    layout: Layout
    """Layout settings"""


class Slide(TypedDict):
    """Data class representing slide."""

    layout: SlideLayout
    """Slide layout"""

    title: NotRequired[Text]
    """Slide title"""

    containers: NotRequired[list[Container]]
    """Containers within slide"""


class SlideTemplate:
    """Interface for slide templates.

    This interface defines the contract for slide templates.
    Users can implement their own templates by subclassing this class
    and implementing the build method.
    """

    def build(self) -> Slide:
        """Build a slide using this template."""
        raise NotImplementedError()


class Presentation:
    """Class for creating presentations."""

    def __init__(self):
        """Initialize presentation."""
        self._factory = PptxPresentationFactory()
        self._presentation = self._factory.create_presentation()

    @property
    def slides(self) -> list[AbstractSlide]:
        """Get slides."""
        return self._presentation.get_slides()

    def save(self, path: str | pathlib.Path | IO[bytes]) -> None:
        """Save presentation to file.

        Args:
            path (str): Path to save presentation
        """
        if isinstance(path, os.PathLike):
            path = str(path)

        self._presentation.save(path)

    @classmethod
    def builder(cls) -> "PresentationBuilder":
        """Create a new presentation builder.

        Returns:
            PresentationBuilder: Newly created presentation builder
        """
        return PresentationBuilder()


class PresentationBuilder:
    """Builder class for creating presentations."""

    def __init__(self):
        """Initialize presentation builder."""
        self._presentation = Presentation()
        self.slides: list[Slide] = []

    @overload
    def add_slide(self, slide: Slide | SlideTemplate, /) -> "PresentationBuilder": ...

    @overload
    def add_slide(self, /, **kwargs: Unpack[Slide]) -> "PresentationBuilder": ...

    def add_slide(  # type: ignore
        self,
        slide: Slide | SlideTemplate | None = None,
        /,
        **kwargs: Unpack[Slide],
    ) -> "PresentationBuilder":
        """Add a slide to the presentation."""
        if isinstance(slide, SlideTemplate):
            # Using template
            slide = slide.build(**kwargs)
        elif slide is None:
            slide = kwargs

        self.slides.append(slide)
        return self

    def _add_component(
        self,
        slide_obj: AbstractSlide,
        component: Component,
        left: LiteralLength,
        top: LiteralLength,
    ) -> None:
        """Add a component to a slide.

        Args:
            slide_obj (AbstractSlide): Target slide
            component (Component): Component to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        # 共通の位置計算を最適化
        internal_left = to_length(left)
        internal_top = to_length(top)
        left_inches = to_inche(internal_left).value
        top_inches = to_inche(internal_top).value

        if component["type"] == "text":
            # レイアウト情報を一度だけ取得
            layout = component.get("layout", {}) or {}
            width = layout.get("width")
            height = layout.get("height")

            internal_width = to_length(width) if width else Inch(3)
            internal_height = to_length(height) if height else Inch(1)

            shape = slide_obj.add_shape(
                MSO_SHAPE_TYPE.TEXT_BOX,
                left_inches,
                top_inches,
                to_inche(internal_width).value,
                to_inche(internal_height).value,
            )
            shape.set_text(component["text"])
            # TODO: Apply text formatting

        elif component["type"] == "image":
            # TODO: Implement image component
            pass

        elif component["type"] == "chart":
            # TODO: Implement chart component
            pass

        elif component["type"] == "table":
            # TODO: Implement table component
            pass

    def _add_container(
        self,
        slide_obj: AbstractSlide,
        container: Container,
        left: LiteralLength,
        top: LiteralLength,
    ) -> None:
        """Add a container to a slide.

        Args:
            slide_obj (AbstractSlide): Target slide
            container (Container): Container to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        current_left = left
        current_top = top

        for component in container["components"]:
            self._add_component(slide_obj, component, current_left, current_top)

            if container["layout"]["direction"] == "row":
                current_left = (current_left[0] + 2, current_left[1])  # Default spacing
            else:
                current_top = (current_top[0] + 1, current_top[1])  # Default spacing

    def build(self) -> "Presentation":
        """Build the presentation.

        Returns:
            Presentation: Built presentation
        """
        for slide in self.slides:
            slide_obj = self._presentation._presentation.add_slide(slide["layout"])

            if title := slide.get("title"):
                title_shape = slide_obj.get_title()
                if title_shape:
                    title_shape.set_text(title["text"])
                    # TODO: Apply title formatting

            if containers := slide.get("containers"):
                for container in containers:
                    self._add_container(
                        slide_obj, container, (1, "in"), (2, "in")
                    )  # Default position

        return self._presentation


def image(
    path: str | pathlib.Path,
    width: LiteralLength | None = None,
    height: LiteralLength | None = None,
    layout: Layout | None = None,
) -> Image:
    """Create an image component with type field automatically set.

    Args:
        path (str | pathlib.Path): Path to image file
        width (Length | None, optional): Width. Defaults to None.
        height (Length | None, optional): Height. Defaults to None.
        layout (Layout | None, optional): Layout settings. Defaults to None.

    Returns:
        Image: Created image component
    """
    return {
        "type": "image",
        "path": path,
        "width": width,
        "height": height,
        "layout": layout,
    }


def text(
    text: str,
    size: LiteralLength | None = None,
    bold: bool = False,
    italic: bool = False,
    color: str | None = None,
    layout: Layout | None = None,
) -> Text:
    """Create a text component with type field automatically set.

    Args:
        text (str): Text content
        size (Length | None, optional): Font size. Defaults to None.
        bold (bool, optional): Whether text is bold. Defaults to False.
        italic (bool, optional): Whether text is italic. Defaults to False.
        color (str | None, optional): Text color. Defaults to None.
        layout (Layout | None, optional): Layout settings. Defaults to None.

    Returns:
        Text: Created text component
    """
    return {
        "type": "text",
        "text": text,
        "size": size,
        "bold": bold,
        "italic": italic,
        "color": color,
        "layout": layout,
    }


def chart(
    chart_type: str,
    data: list[dict[str, Any]],
    width: LiteralLength | None = None,
    height: LiteralLength | None = None,
    layout: Layout | None = None,
) -> Chart:
    """Create a chart component with type field automatically set.

    Args:
        chart_type (str): Chart type ("bar", "line", "pie", etc.)
        data (list[dict[str, Any]]): Chart data
        width (Length | None, optional): Width. Defaults to None.
        height (Length | None, optional): Height. Defaults to None.
        layout (Layout | None, optional): Layout settings. Defaults to None.

    Returns:
        Chart: Created chart component
    """
    return {
        "type": "chart",
        "chart_type": chart_type,
        "data": data,
        "width": width,
        "height": height,
        "layout": layout,
    }


def table(
    rows: int,
    cols: int,
    data: list[list[TableCell]],
    width: LiteralLength | None = None,
    height: LiteralLength | None = None,
    layout: Layout | None = None,
) -> Table:
    """Create a table component with type field automatically set.

    Args:
        rows (int): Number of rows
        cols (int): Number of columns
        data (list[list[TableCell]]): Table data
        width (Length | None, optional): Width. Defaults to None.
        height (Length | None, optional): Height. Defaults to None.
        layout (Layout | None, optional): Layout settings. Defaults to None.

    Returns:
        Table: Created table component
    """
    return {
        "type": "table",
        "rows": rows,
        "cols": cols,
        "data": data,
        "width": width,
        "height": height,
        "layout": layout,
    }


def layout(
    type: LayoutType = "flex",
    direction: str = "row",
    align: Align = "start",
    justify: Justify = "start",
    gap: LiteralLength = (0.1, "in"),
    padding: dict[str, LiteralLength] | None = None,
    width: LiteralLength | None = None,
    height: LiteralLength | None = None,
) -> Layout:
    """Create a layout with default values.

    Args:
        type (LayoutType, optional): Layout type. Defaults to "flex".
        direction (str, optional): Layout direction ("row" or "column"). Defaults to "row".
        align (Align, optional): Element alignment. Defaults to "start".
        justify (Justify, optional): Element justification. Defaults to "start".
        gap (Length, optional): Gap between elements. Defaults to (0.1, "in").
        padding (dict[str, Length] | None, optional): Padding (top, right, bottom, left). Defaults to None.
        width (Length | None, optional): Width. Defaults to None.
        height (Length | None, optional): Height. Defaults to None.

    Returns:
        Layout: Created layout
    """
    return {
        "type": type,
        "direction": direction,
        "align": align,
        "justify": justify,
        "gap": gap,
        "padding": padding,
        "width": width,
        "height": height,
    }


def slide(
    layout: SlideLayout,
    title: Text | None = None,
    containers: list[Container] | None = None,
) -> Slide:
    """Create a slide with specified layout, title, and containers.

    Args:
        layout (SlideLayout): Layout type for the slide
        title (Text | None, optional): Title text component. Defaults to None.
        containers (list[Container] | None, optional): list of containers. Defaults to None.

    Returns:
        Slide: Created slide object
    """
    if containers is None:
        containers = []
    return {
        "layout": layout,
        "title": title,
        "containers": containers,
    }
