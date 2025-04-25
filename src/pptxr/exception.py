from abc import abstractmethod
from typing import Any

from pptx.slide import SlideLayouts as PptxSlideLayouts


class PptxrException(Exception):
    """Base exception for pptxr."""

    @property
    @abstractmethod
    def message(self) -> str: ...

    @property
    def extra(self) -> dict[str, Any]:
        return {}

    def __str__(self) -> str:
        return self.message


class ColorInvalidFormatError(PptxrException, ValueError):
    """Color format is invalid."""

    def __init__(self, color: str) -> None:
        self.color = color

    @property
    def message(self) -> str:
        return f"Invalid color format: {self.color}"


class SlideLayoutIndexError(PptxrException, IndexError):
    """Slide layout index is out of range."""

    def __init__(self, index: int, slide_layouts: PptxSlideLayouts) -> None:
        self.index = index
        self.slide_layouts = slide_layouts

    @property
    def message(self) -> str:
        return f"Slide layout index {self.index} is out of range. Available slide layouts: {[layout.name for layout in self.slide_layouts]}"
