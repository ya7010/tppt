"""Data classes for PowerPoint presentation."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Any, List, Optional, Union

from .types import LiteralLength, ShapeType


@dataclass
class Text:
    """Text data class."""

    content: str
    font_size: Optional[LiteralLength] = None
    font_family: Optional[str] = None
    font_color: Optional[str] = None


@dataclass
class Image:
    """Image data class."""

    path: Union[str, Path]
    width: Optional[LiteralLength] = None
    height: Optional[LiteralLength] = None


@dataclass
class Shape:
    """Shape data class."""

    type: ShapeType
    left: LiteralLength
    top: LiteralLength
    width: LiteralLength
    height: LiteralLength
    text: Optional[str] = None


@dataclass
class Slide:
    """Slide data class."""

    layout_type: str
    shapes: List[Shape] = field(default_factory=list)


@dataclass
class SlideTemplate:
    """Base class for slide templates."""

    title: Optional[str] = None
    subtitle: Optional[str] = None


@dataclass
class Presentation:
    """Presentation data class."""

    slides: List[Slide] = field(default_factory=list)
    _wrapper: Optional[Any] = field(default=None, init=False)

    def __post_init__(self) -> None:
        """Initialize the wrapper."""
        from ._presentation import PptxPresentationWrapper

        self._wrapper = PptxPresentationWrapper()

    def get_slides(self) -> List[Slide]:
        """Get all slides."""
        return self.slides

    def add_slide(self, layout_type: str) -> Slide:
        """Add a new slide."""
        slide = Slide(layout_type=layout_type)
        self.slides.append(slide)
        if self._wrapper is not None:
            self._wrapper.add_slide(slide)
        return slide

    def save(self, path: Union[str, Path, IO[bytes]]) -> None:
        """Save the presentation."""
        if self._wrapper is not None:
            self._wrapper.save(path)
