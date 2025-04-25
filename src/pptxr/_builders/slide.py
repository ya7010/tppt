"""Slide builder implementation for pptxr."""

from pathlib import Path
from typing import Any, Self, Union

from .._data import Image, Slide, Text


class SlideBuilder:
    """Builder class for creating slides."""

    bones: Slide

    def __init__(self):
        """Initialize a SlideBuilder instance."""
        self.bones = Slide()

    def text(self, text: str, /, **kwargs: Any) -> Self:
        """Add a text element to the slide."""
        self.bones.elements.append(Text(text=text, **kwargs))
        return self

    def image(self, path: Union[str, Path], /, **kwargs: Any) -> Self:
        """Add an image element to the slide."""
        self.bones.elements.append(Image(path=path, **kwargs))
        return self

    def build(self) -> Slide:
        """Build the slide structure."""
        return self.bones
