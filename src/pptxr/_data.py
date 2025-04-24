"""Data classes for pptxr."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple, TypedDict, Union

from .types import Color, Length


class TextParams(TypedDict, total=False):
    """Parameters for a text element."""

    x: Union[Length, Tuple[float, str]]
    y: Union[Length, Tuple[float, str]]
    width: Union[Length, Tuple[float, str]]
    height: Union[Length, Tuple[float, str]]
    color: Union[Color, str, Tuple[int, int, int]]


class ImageParams(TypedDict, total=False):
    """Parameters for an image element."""

    x: Union[Length, Tuple[float, str]]
    y: Union[Length, Tuple[float, str]]
    width: Union[Length, Tuple[float, str]]
    height: Union[Length, Tuple[float, str]]


@dataclass
class TextBone:
    """Represents a text element for a slide."""

    text: str
    x: Optional[Union[Length, Tuple[float, str]]] = None
    y: Optional[Union[Length, Tuple[float, str]]] = None
    width: Optional[Union[Length, Tuple[float, str]]] = None
    height: Optional[Union[Length, Tuple[float, str]]] = None
    color: Optional[Union[Color, str, Tuple[int, int, int]]] = None


@dataclass
class ImageBone:
    """Represents an image element for a slide."""

    path: Union[str, Path]
    x: Optional[Union[Length, Tuple[float, str]]] = None
    y: Optional[Union[Length, Tuple[float, str]]] = None
    width: Optional[Union[Length, Tuple[float, str]]] = None
    height: Optional[Union[Length, Tuple[float, str]]] = None


@dataclass
class SlideBone:
    """Represents a slide structure."""

    elements: List[Union[TextBone, ImageBone]] = field(default_factory=list)


@dataclass
class SlideTemplate:
    """Base class for slide templates."""

    title: Optional[str] = None
    subtitle: Optional[str] = None
