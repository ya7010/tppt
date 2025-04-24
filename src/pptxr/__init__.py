"""PowerPoint presentation creation library."""

import os
from abc import ABC, abstractmethod
from typing import (
    IO,
    Generic,
    Literal,
    NotRequired,
    Self,
    TypeAlias,
    TypedDict,
    Unpack,
)

import pptx
from typing_extensions import TypeVar

from pptxr._data import Slide
from pptxr.units import Length

from ._pptx import PptxPresentationFactory
from .types import FilePath
from .units import LiteralLength

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


class SlideBuilder(ABC):
    """Builder class for creating slides."""

    def __init__(self):
        pass

    @abstractmethod
    def build(self) -> Slide:
        """Build the slide."""
        raise NotImplementedError()


class DefaultSlideBuilder(SlideBuilder):
    """Default slide builder."""

    def __init__(self, slide: Slide):
        self._slide = slide

    def text(self, text: str, /, **kwargs: Unpack[TextParams]) -> Self:
        self._slide.components.append(Text(type="text", text=text, **kwargs))
        return self

    def image(self, **kwargs: Unpack[ImageParams]) -> Self:
        self._slide.components.append(Image(type="image", **kwargs))
        return self

    def build(self) -> Slide:
        """Build the slide."""
        return self._slide


_GenericSlideBuilder = TypeVar(
    "_GenericSlideBuilder",
    default=DefaultSlideBuilder,
    bound=SlideBuilder,
)


class SlideTemplate(Generic[_GenericSlideBuilder]):
    """Interface for slide templates.

    This interface defines the contract for slide templates.
    Users can implement their own templates by subclassing this class
    and implementing the build method.
    """

    @abstractmethod
    def builder(
        self,
    ) -> _GenericSlideBuilder:
        """Build a slide using this template."""
        raise NotImplementedError()


class SlideMaster(Generic[_GenericSlideBuilder]):
    """Slide master for a presentation."""

    def __init__(self, file: FilePath | IO[bytes] | None = None):
        """Initialize slide master."""
        if file is None:
            self._presentation = pptx.Presentation()
        else:
            if isinstance(file, os.PathLike):
                file = os.fspath(file)
            self._presentation = pptx.Presentation(file)


class Presentation:
    """Class for creating presentations."""

    def __init__(self):
        """Initialize presentation."""
        self._factory = PptxPresentationFactory()
        self._presentation = self._factory.create_presentation()

    @property
    def slides(self) -> list[Slide]:
        """Get slides."""
        return []

    def save(self, path: FilePath | IO[bytes]) -> None:
        """Save presentation to file.

        Args:
            path (str): Path to save presentation
        """
        if isinstance(path, os.PathLike):
            path = str(path)

        self._presentation.save(path)

    @classmethod
    def builder(
        cls,
        slide_master: SlideMaster[_GenericSlideBuilder] | None = None,
    ) -> "PresentationBuilder[_GenericSlideBuilder]":
        """Create a new presentation builder.

        Returns:
            PresentationBuilder: Newly created presentation builder
        """
        if slide_master is None:
            slide_master = SlideMaster()
        return PresentationBuilder(slide_master)


class PresentationBuilder(Generic[_GenericSlideBuilder]):
    """Builder class for creating presentations."""

    def __init__(self, slide_master: SlideMaster[_GenericSlideBuilder]):
        """Initialize presentation builder."""
        self._presentation = Presentation()
        self.slide_master = slide_master
        self.slides: list[Slide] = []

    def add_slide(  # type: ignore
        self,
        slide: Slide | SlideTemplate[_GenericSlideBuilder] | _GenericSlideBuilder,
    ) -> "PresentationBuilder[_GenericSlideBuilder]":
        """Add a slide to the presentation."""
        if isinstance(slide, SlideTemplate):
            # Using template
            slide = slide.builder()

        if isinstance(slide, SlideBuilder):
            # Using builder
            slide = slide.build()

        self.slides.append(slide)

        return self

    def build(self) -> "Presentation":
        """Build the presentation.

        Returns:
            Presentation: Built presentation
        """

        return self._presentation
