"""Slide builder implementation for pptxr."""

from pathlib import Path
from typing import Any, Self, Union

from .._data import ImageBone, SlideBone, TextBone


class SlideBuilder:
    """Builder class for creating slides."""

    bones: SlideBone

    def __init__(self):
        """Initialize a SlideBuilder instance."""
        self.bones = SlideBone()

    def text(self, text: str, /, **kwargs: Any) -> Self:
        """Add a text element to the slide."""
        self.bones.elements.append(TextBone(text=text, **kwargs))
        return self

    def image(self, path: Union[str, Path], /, **kwargs: Any) -> Self:
        """Add an image element to the slide."""
        self.bones.elements.append(ImageBone(path=path, **kwargs))
        return self

    def build(self) -> SlideBone:
        """Build the slide structure."""
        return self.bones
