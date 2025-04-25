"""Slide builder implementation for pptxr."""

from typing import Self, Unpack

from pptxr.types import FilePath
from pptxr.types.length import to_length, to_optional_length

from .._data import Image, ImageParams, Slide, Text, TextParams


class SlideBuilder:
    """Builder class for creating slides."""

    bones: Slide

    def __init__(self):
        """Initialize a SlideBuilder instance."""
        self.bones = Slide()

    def text(self, text: str, /, **kwargs: Unpack[TextParams]) -> Self:
        """Add a text element to the slide."""
        self.bones.elements.append(
            Text(
                text=text,
                x=to_length(kwargs["x"]),
                y=to_length(kwargs["y"]),
                height=to_optional_length(kwargs.get("height")),
                width=to_optional_length(kwargs.get("width")),
                color=kwargs.get("color"),
            )
        )
        return self

    def image(self, path: FilePath, /, **kwargs: Unpack[ImageParams]) -> Self:
        """Add an image element to the slide."""
        self.bones.elements.append(
            Image(
                path=path,
                x=to_length(kwargs["x"]),
                y=to_length(kwargs["y"]),
            )
        )
        return self

    def build(self) -> Slide:
        """Build the slide structure."""
        return self.bones
