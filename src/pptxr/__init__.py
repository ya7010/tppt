"""PowerPoint presentation creation library."""

import os
from typing import (
    IO,
    Literal,
    NotRequired,
    TypeAlias,
    TypedDict,
    Unpack,
    overload,
)

from pptxr.units import Length

from ._pptx import PptxPresentationFactory
from .abstract.types import FilePath
from .abstract.types import Slide as AbstractSlide
from .units import (
    LiteralLength,
    to_length,
)

SlideIndex: TypeAlias = int

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

Direction = Literal["row", "column"]
Align = Literal["start", "center", "end"]

Justify = Literal["start", "center", "end", "space-between", "space-around"]
Padding: TypeAlias = dict[Literal["top", "right", "bottom", "left"], Length]


class Layout(TypedDict):
    """Data class representing layout settings."""

    type: NotRequired[LayoutType]
    """Layout type"""

    direction: NotRequired[Direction]
    """Layout direction ("row" or "column")"""

    align: NotRequired[Align]
    """Element alignment"""

    justify: NotRequired[Justify]
    """Element justification"""

    gap: NotRequired[Length | LiteralLength]
    """Gap between elements"""

    padding: NotRequired[Padding]
    """Padding (top, right, bottom, left)"""

    width: NotRequired[Length | LiteralLength]
    """Width"""

    height: NotRequired[Length | LiteralLength]
    """Height"""


class TextParams(TypedDict):
    """Data class representing text element."""

    size: NotRequired[LiteralLength]
    """Font size"""

    bold: NotRequired[bool]
    """Whether text is bold"""

    italic: NotRequired[bool]
    """Whether text is italic"""

    color: NotRequired[str]
    """Text color"""

    layout: NotRequired[Layout]
    """Layout settings"""


class Text(TextParams):
    """Data class representing text element."""

    type: Literal["text"]
    """Type of component"""

    text: str


class ImageParams(TypedDict):
    """Data class representing image element."""

    path: FilePath
    """Path to image file"""

    width: NotRequired[LiteralLength]
    """Width"""

    height: NotRequired[LiteralLength]
    """Height"""

    layout: NotRequired[Layout]
    """Layout settings"""


class Image(ImageParams):
    """Data class representing image element."""

    type: Literal["image"]
    """Type of component"""


Component = Text | Image
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

    def save(self, path: FilePath | IO[bytes]) -> None:
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
            slide = slide.build()
        elif slide is None:
            slide = kwargs

        self.slides.append(slide)
        return self

    def _add_component(
        self,
        slide_obj: AbstractSlide,
        component: Component,
        left: Length | LiteralLength,
        top: Length | LiteralLength,
    ) -> None:
        """Add a component to a slide.

        Args:
            slide_obj (AbstractSlide): Target slide
            component (Component): Component to add
            left (Length): Position from left edge
            top (Length): Position from top edge
        """

        if component["type"] == "text":
            pass

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
        current_left = to_length(left)
        current_top = to_length(top)

        for component in container["components"]:
            self._add_component(slide_obj, component, current_left, current_top)

            if layout := container["layout"]:
                if layout.get("direction", "row") == "row":
                    current_left = current_left + (2, "in")  # Default spacing
                else:
                    current_top = current_top + (1, "in")  # Default spacing

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
                    if text := title["text"]:
                        title_shape.set_text(text)

            if containers := slide.get("containers"):
                for container in containers:
                    self._add_container(
                        slide_obj, container, (1, "in"), (2, "in")
                    )  # Default position

        return self._presentation


def image(
    **kwargs: Unpack[ImageParams],
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
        **kwargs,
    }


def text(
    text: str,
    /,
    **kwargs: Unpack[TextParams],
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
        **kwargs,
    }


def layout(
    **kwargs: Unpack[Layout],
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
    return kwargs


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
        "containers": containers,
    }
