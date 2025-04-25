"""Data classes for pptxr."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, NotRequired, Optional, Tuple, TypedDict, Union

from pptxr.types import Color, Length, LiteralLength


class TextParams(TypedDict):
    """Parameters for a text element."""

    x: Length | LiteralLength
    y: Length | LiteralLength
    width: NotRequired[Length | LiteralLength]
    height: NotRequired[Length | LiteralLength]
    color: NotRequired[Color]


class ImageParams(TypedDict):
    """Parameters for an image element."""

    x: Length | LiteralLength
    y: Length | LiteralLength
    width: NotRequired[Length | LiteralLength]
    height: NotRequired[Length | LiteralLength]


@dataclass
class Text:
    """Represents a text element for a slide."""

    text: str
    x: Length
    y: Length
    width: Length | None = None
    height: Length | None = None
    color: Color | None = None


@dataclass
class Image:
    """Represents an image element for a slide."""

    path: Union[str, Path]
    x: Optional[Union[Length, Tuple[float, str]]] = None
    y: Optional[Union[Length, Tuple[float, str]]] = None
    width: Optional[Union[Length, Tuple[float, str]]] = None
    height: Optional[Union[Length, Tuple[float, str]]] = None


@dataclass
class Slide:
    """Represents a slide structure."""

    elements: List[Union[Text, Image]] = field(default_factory=list)


@dataclass
class SlideTemplate:
    """Base class for slide templates."""

    title: Optional[str] = None
    subtitle: Optional[str] = None
