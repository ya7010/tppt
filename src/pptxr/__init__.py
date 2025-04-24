import os
from dataclasses import dataclass
from enum import Enum
from typing import (
    Any,
    Literal,
    NotRequired,
    Optional,
    Self,
    TypedDict,
    Union,
    Unpack,
    assert_never,
    overload,
)

from pptx import Presentation as PptxPresentation
from pptx.chart.data import ChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


# Type definitions for units
class Inch:
    """Class representing inches"""

    def __init__(self, value: float):
        self.value = float(value)

    def __add__(self, other: "Length") -> Self:
        return Inch(self.value + to_inche(other))

    def __sub__(self, other: "Length") -> Self:
        return Inch(self.value - to_inche(other))

    def __iadd__(self, other: "Length") -> Self:
        self.value += to_inche(other)
        return self

    def __isub__(self, other: "Length") -> Self:
        self.value -= to_inche(other)
        return self

    def __mul__(self, other: Union[int, float]) -> Self:
        return Inch(self.value * other)

    def __truediv__(self, other: Union[int, float]) -> Self:
        return Inch(self.value / other)


class Point:
    """Class representing points"""

    def __init__(self, value: int):
        self.value = int(value)

    def __add__(self, other: "Length") -> Self:
        return Point(self.value + to_point(other))

    def __sub__(self, other: "Length") -> Self:
        return Point(self.value - to_point(other))

    def __iadd__(self, other: "Length") -> Self:
        self.value += to_point(other)
        return self

    def __isub__(self, other: "Length") -> Self:
        self.value -= to_point(other)
        return self

    def __mul__(self, other: Union[int, float]) -> Self:
        return Point(int(self.value * other))

    def __truediv__(self, other: Union[int, float]) -> Self:
        return Point(int(self.value / other))


Length = Union[Inch, Point]

# Constants for unit conversion
INCHES_PER_POINT = 1 / 72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72  # 1 inch = 72 points


def to_inche(length: Length) -> Inch:
    """Convert any length to inches

    Args:
        length (Length): Length in any unit

    Returns:
        float: Length in inches
    """
    match length:
        case Inch():
            return length.value
        case Point():
            return Inch(float(length.value) * INCHES_PER_POINT)
        case _:
            assert_never(length)


def to_point(length: Length) -> Point:
    """Convert any length to points

    Args:
        length (Length): Length in any unit

    Returns:
        int: Length in points
    """
    match length:
        case Inch():
            return int(length.value * POINTS_PER_INCH)
        case Point():
            return length.value
        case _:
            assert_never(length)


class SlideLayout(Enum):
    """Enumeration defining slide layout types"""

    TITLE = 0
    """Title-only layout"""
    TITLE_AND_CONTENT = 1
    """Title and content layout"""
    SECTION_HEADER = 2
    """Section header layout"""
    TWO_CONTENT = 3
    """Layout with two content areas"""
    COMPARISON = 4
    """Comparison layout"""
    TITLE_ONLY = 5
    """Title-only layout"""
    BLANK = 6
    """Blank layout"""
    CONTENT_WITH_CAPTION = 7
    """Content with caption layout"""
    PICTURE_WITH_CAPTION = 8
    """Picture with caption layout"""
    TITLE_AND_VERTICAL_TEXT = 9
    """Title and vertical text layout"""
    VERTICAL_TITLE_AND_TEXT = 10
    """Vertical title and text layout"""


class LayoutType(Enum):
    """Enumeration defining layout types"""

    FLEX = "flex"
    """Flexbox layout"""
    GRID = "grid"
    """Grid layout"""
    ABSOLUTE = "absolute"
    """Absolute positioning layout"""


class Align(Enum):
    """Enumeration defining element alignment"""

    START = "start"
    """Align to start position"""
    CENTER = "center"
    """Align to center"""
    END = "end"
    """Align to end position"""


class Justify(Enum):
    """Enumeration defining element justification"""

    START = "start"
    """Justify to start"""
    CENTER = "center"
    """Justify to center"""
    END = "end"
    """Justify to end"""
    SPACE_BETWEEN = "space-between"
    """Distribute space between elements"""
    SPACE_AROUND = "space-around"
    """Distribute space around elements"""


class Layout(TypedDict):
    """Data class representing layout settings"""

    type: NotRequired[LayoutType]
    """Layout type"""
    direction: NotRequired[str]
    """Layout direction ("row" or "column")"""
    align: NotRequired[Align]
    """Element alignment"""
    justify: NotRequired[Justify]
    """Element justification"""
    gap: NotRequired[Length]
    """Gap between elements"""
    padding: NotRequired[dict[str, Length]]
    """Padding (top, right, bottom, left)"""
    width: NotRequired[Length]
    """Width"""
    height: NotRequired[Length]
    """Height"""


class Text(TypedDict):
    """Data class representing text element"""

    type: Literal["text"]
    """Type of component"""
    text: str
    """Text content"""
    size: NotRequired[Length]
    """Font size"""
    bold: NotRequired[bool]
    """Whether text is bold"""
    italic: NotRequired[bool]
    """Whether text is italic"""
    color: NotRequired[str]
    """Text color"""
    layout: NotRequired[Layout]
    """Layout settings"""


@dataclass
class Shape:
    """Data class representing shape"""

    type: str
    """Shape type"""
    left: Length
    """Position from left edge"""
    top: Length
    """Position from top edge"""
    width: Length
    """Width"""
    height: Length
    """Height"""
    text: Optional[Text] = None
    """Text within shape"""


class Image(TypedDict):
    """Data class representing image element"""

    type: Literal["image"]
    """Type of component"""

    path: str
    """Path to image file"""

    width: NotRequired[Length]
    """Width"""

    height: NotRequired[Length]
    """Height"""

    layout: NotRequired[Layout]
    """Layout settings"""


class Chart(TypedDict):
    """Data class representing chart element"""

    type: Literal["chart"]
    """Type of component"""
    chart_type: str
    """Chart type ("bar", "line", "pie", etc.)"""
    data: list[dict[str, Any]]
    """Chart data"""
    width: NotRequired[Length]
    """Width"""
    height: NotRequired[Length]
    """Height"""
    layout: NotRequired[Layout]
    """Layout settings"""


@dataclass
class TableCell:
    """Data class representing table cell"""

    text: str
    """Cell text content"""
    size: Optional[Length] = None
    """Font size"""
    bold: bool = False
    """Whether text is bold"""
    italic: bool = False
    """Whether text is italic"""
    color: Optional[str] = None
    """Text color"""
    background: Optional[str] = None
    """Background color"""
    align: PP_ALIGN = PP_ALIGN.LEFT
    """Text alignment"""


class Table(TypedDict):
    """Data class representing table element"""

    type: Literal["table"]
    """Type of component"""
    rows: int
    """Number of rows"""
    cols: int
    """Number of columns"""
    data: list[list[TableCell]]
    """Table data"""
    width: NotRequired[Length]
    """Width"""
    height: NotRequired[Length]
    """Height"""
    layout: NotRequired[Layout]
    """Layout settings"""


Component = Union[Text, Image, Chart, Table]
"""Union type representing any component type"""


class Container(TypedDict):
    """Data class representing container"""

    components: list[Component]
    """Components within container"""
    layout: Layout
    """Layout settings"""


class Slide(TypedDict):
    """Data class representing slide"""

    layout: SlideLayout
    """Slide layout"""
    title: NotRequired[Text]
    """Slide title"""
    containers: NotRequired[list[Container]]
    """Containers within slide"""


class Presentation:
    """Class for creating presentations"""

    def __init__(self):
        """Initialize presentation"""
        self._presentation = PptxPresentation()

    @property
    def slide_layouts(self):
        """Get slide layouts"""
        return self._presentation.slide_layouts

    @property
    def slides(self):
        """Get slides"""
        return self._presentation.slides

    def save(self, path: os.PathLike) -> None:
        """Save presentation to file

        Args:
            path (str): Path to save presentation
        """
        self._presentation.save(os.fspath(path))

    @classmethod
    def builder(cls) -> "_PresentationBuilder":
        """Create a new presentation builder

        Returns:
            PresentationBuilder: Newly created presentation builder
        """
        return _PresentationBuilder()


class _PresentationBuilder:
    """Builder class for creating presentations"""

    def __init__(self):
        """Initialize presentation builder"""
        self.presentation = Presentation()
        self.slides: list[Slide] = []

    @overload
    def add_slide(self, slide: Slide, /) -> "_PresentationBuilder": ...

    @overload
    def add_slide(self, **kwargs: Unpack[Slide]) -> "_PresentationBuilder": ...

    def add_slide(
        self, slide: Slide = None, /, **kwargs: Unpack[Slide]
    ) -> "_PresentationBuilder":
        """Add a slide to the presentation

        Args:
            slide (Slide): Slide to add

        Returns:
            PresentationBuilder: Self instance for method chaining
        """
        if slide is None:
            slide = kwargs
        self.slides.append(slide)
        return self

    def _apply_layout(self, shape, layout: Layout):
        """Apply layout to a shape

        Args:
            shape: Target shape
            layout (Layout): Layout settings to apply
        """
        if layout.get("width"):
            shape.width = Inches(to_inche(layout["width"]))
        if layout.get("height"):
            shape.height = Inches(to_inche(layout["height"]))
        if layout.get("align"):
            if layout["align"] == Align.CENTER:
                shape.left = (
                    Inches(to_inche(shape.left))
                    + (Inches(8.5) - Inches(to_inche(shape.width))) / 2
                )
            elif layout["align"] == Align.END:
                shape.left = (
                    Inches(to_inche(shape.left))
                    + Inches(8.5)
                    - Inches(to_inche(shape.width))
                )

    def _add_component(
        self, slide_obj, component: Component, left: Length, top: Length
    ):
        """Add a component to a slide

        Args:
            slide_obj: Target slide
            component (Component): Component to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        if component["type"] == "text":
            shape = slide_obj.shapes.add_textbox(
                Inches(float(to_inche(left))),
                Inches(float(to_inche(top))),
                Inches(float(to_inche(component["layout"]["width"])))
                if component.get("layout") and component["layout"].get("width")
                else Inches(3),
                Inches(float(to_inche(component["layout"]["height"])))
                if component.get("layout") and component["layout"].get("height")
                else Inches(1),
            )
            text_frame = shape.text_frame
            text_frame.text = component["text"]
            if component.get("size"):
                text_frame.paragraphs[0].font.size = Pt(
                    int(to_point(component["size"]))
                )
            if component.get("bold"):
                text_frame.paragraphs[0].font.bold = component["bold"]
            if component.get("italic"):
                text_frame.paragraphs[0].font.italic = component["italic"]

        elif component["type"] == "image":
            shape = slide_obj.shapes.add_picture(
                component["path"],
                Inches(float(to_inche(left))),
                Inches(float(to_inche(top))),
                Inches(float(to_inche(component["width"])))
                if component.get("width")
                else None,
                Inches(float(to_inche(component["height"])))
                if component.get("height")
                else None,
            )

        elif component["type"] == "chart":
            chart_data = ChartData()
            chart_data.categories = [item["category"] for item in component["data"]]
            chart_data.add_series(
                "Series 1", [item["value"] for item in component["data"]]
            )

            x, y = Inches(float(to_inche(left))), Inches(float(to_inche(top)))
            cx = (
                Inches(float(to_inche(component["layout"]["width"])))
                if component.get("layout") and component["layout"].get("width")
                else Inches(6)
            )
            cy = (
                Inches(float(to_inche(component["layout"]["height"])))
                if component.get("layout") and component["layout"].get("height")
                else Inches(4)
            )

            shape = slide_obj.shapes.add_chart(
                XL_CHART_TYPE.BAR_CLUSTERED
                if component["chart_type"] == "bar"
                else XL_CHART_TYPE.LINE,
                x,
                y,
                cx,
                cy,
                chart_data,
            )

        elif component["type"] == "table":
            table = slide_obj.shapes.add_table(
                component["rows"],
                component["cols"],
                Inches(float(to_inche(left))),
                Inches(float(to_inche(top))),
                Inches(float(to_inche(component["layout"]["width"])))
                if component.get("layout") and component["layout"].get("width")
                else Inches(6),
                Inches(float(to_inche(component["layout"]["height"])))
                if component.get("layout") and component["layout"].get("height")
                else Inches(2),
            ).table

            for i, row in enumerate(component["data"]):
                for j, cell in enumerate(row):
                    table_cell = table.cell(i, j)
                    table_cell.text = cell.text

                    if cell.get("size"):
                        table_cell.text_frame.paragraphs[0].font.size = Pt(
                            int(to_point(cell.get("size")))
                        )
                    if cell.get("bold"):
                        table_cell.text_frame.paragraphs[0].font.bold = True
                    if cell.get("italic"):
                        table_cell.text_frame.paragraphs[0].font.italic = True
                    if cell.get("color"):
                        table_cell.text_frame.paragraphs[
                            0
                        ].font.color.rgb = RGBColor.from_string(cell.get("color"))
                    if cell.get("background"):
                        table_cell.fill.solid()
                        table_cell.fill.fore_color.rgb = RGBColor.from_string(
                            cell.get("background")
                        )

                    table_cell.text_frame.paragraphs[0].alignment = cell.get("align")

        if component.get("layout"):
            self._apply_layout(shape, component["layout"])

    def _add_container(
        self, slide_obj, container: Container, left: Length, top: Length
    ):
        """Add a container to a slide

        Args:
            slide_obj: Target slide
            container (Container): Container to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """
        current_left = left
        current_top = top

        for component in container["components"]:
            self._add_component(slide_obj, component, current_left, current_top)

            if container["layout"]["direction"] == "row":
                current_left += Inch(2)  # Default spacing
            else:
                current_top += Inch(1)  # Default spacing

    def build(self) -> "Presentation":
        """Build the presentation

        Returns:
            Presentation: Built presentation
        """
        for slide in self.slides:
            slide_layout = self.presentation.slide_layouts[slide["layout"].value]
            slide_obj = self.presentation.slides.add_slide(slide_layout)

            if slide.get("title"):
                title_shape = slide_obj.shapes.title
                title_shape.text = slide["title"]["text"]
                if slide["title"].get("size"):
                    title_shape.text_frame.paragraphs[0].font.size = Pt(
                        int(to_point(slide["title"]["size"]))
                    )
                if slide["title"].get("bold"):
                    title_shape.text_frame.paragraphs[0].font.bold = slide["title"][
                        "bold"
                    ]
                if slide["title"].get("italic"):
                    title_shape.text_frame.paragraphs[0].font.italic = slide["title"][
                        "italic"
                    ]

            if slide.get("containers"):
                for container in slide["containers"]:
                    self._add_container(
                        slide_obj, container, Inch(1), Inch(2)
                    )  # Default position

        return self.presentation


def create_image(
    path: str,
    width: Optional[Length] = None,
    height: Optional[Length] = None,
    layout: Optional[Layout] = None,
) -> Image:
    """Create an image component with type field automatically set

    Args:
        path (str): Path to image file
        width (Optional[Length], optional): Width. Defaults to None.
        height (Optional[Length], optional): Height. Defaults to None.
        layout (Optional[Layout], optional): Layout settings. Defaults to None.

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


def create_text(
    text: str,
    size: Optional[Length] = None,
    bold: bool = False,
    italic: bool = False,
    color: Optional[str] = None,
    layout: Optional[Layout] = None,
) -> Text:
    """Create a text component with type field automatically set

    Args:
        text (str): Text content
        size (Optional[Length], optional): Font size. Defaults to None.
        bold (bool, optional): Whether text is bold. Defaults to False.
        italic (bool, optional): Whether text is italic. Defaults to False.
        color (Optional[str], optional): Text color. Defaults to None.
        layout (Optional[Layout], optional): Layout settings. Defaults to None.

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


def create_chart(
    chart_type: str,
    data: list[dict[str, Any]],
    width: Optional[Length] = None,
    height: Optional[Length] = None,
    layout: Optional[Layout] = None,
) -> Chart:
    """Create a chart component with type field automatically set

    Args:
        chart_type (str): Chart type ("bar", "line", "pie", etc.)
        data (list[dict[str, Any]]): Chart data
        width (Optional[Length], optional): Width. Defaults to None.
        height (Optional[Length], optional): Height. Defaults to None.
        layout (Optional[Layout], optional): Layout settings. Defaults to None.

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


def create_table(
    rows: int,
    cols: int,
    data: list[list[TableCell]],
    width: Optional[Length] = None,
    height: Optional[Length] = None,
    layout: Optional[Layout] = None,
) -> Table:
    """Create a table component with type field automatically set

    Args:
        rows (int): Number of rows
        cols (int): Number of columns
        data (list[list[TableCell]]): Table data
        width (Optional[Length], optional): Width. Defaults to None.
        height (Optional[Length], optional): Height. Defaults to None.
        layout (Optional[Layout], optional): Layout settings. Defaults to None.

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


def create_layout(
    type: LayoutType = LayoutType.FLEX,
    direction: str = "row",
    align: Align = Align.START,
    justify: Justify = Justify.START,
    gap: Length = Inch(0.1),
    padding: Optional[dict[str, Length]] = None,
    width: Optional[Length] = None,
    height: Optional[Length] = None,
) -> Layout:
    """Create a layout with default values

    Args:
        type (LayoutType, optional): Layout type. Defaults to LayoutType.FLEX.
        direction (str, optional): Layout direction ("row" or "column"). Defaults to "row".
        align (Align, optional): Element alignment. Defaults to Align.START.
        justify (Justify, optional): Element justification. Defaults to Justify.START.
        gap (Length, optional): Gap between elements. Defaults to Inch(0.1).
        padding (Optional[dict[str, Length]], optional): Padding (top, right, bottom, left). Defaults to None.
        width (Optional[Length], optional): Width. Defaults to None.
        height (Optional[Length], optional): Height. Defaults to None.

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


def create_slide(
    layout: SlideLayout,
    title: Optional[Text] = None,
    containers: Optional[list[Container]] = None,
) -> Slide:
    """Create a slide with specified layout, title, and containers.

    Args:
        layout (SlideLayout): Layout type for the slide
        title (Optional[Text], optional): Title text component. Defaults to None.
        containers (Optional[list[Container]], optional): list of containers. Defaults to None.

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
