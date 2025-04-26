from abc import abstractmethod
from typing import Any

from pptx.slide import SlideLayouts as PptxSlideLayouts


class TpptException(Exception):
    """Base exception for tppt."""

    @property
    @abstractmethod
    def message(self) -> str: ...

    @property
    def extra(self) -> dict[str, Any]:
        return {}

    def __str__(self) -> str:
        return self.message


class ColorInvalidFormatError(TpptException, ValueError):
    """Color format is invalid."""

    def __init__(self, color: str) -> None:
        self.color = color

    @property
    def message(self) -> str:
        return f"Invalid color format: {self.color}"


class SlideLayoutIndexError(TpptException, IndexError):
    """Slide layout index is out of range."""

    def __init__(self, index: int, slide_layouts: PptxSlideLayouts) -> None:
        self.index = index
        self.slide_layouts = slide_layouts

    @property
    def message(self) -> str:
        return f"Slide layout index {self.index} is out of range. Available slide layouts: {[layout.name for layout in self.slide_layouts]}"


class SlideMasterAttributeMustBeSlideLayoutError(TpptException, ValueError):
    """Slide master attribute must be a slide layout."""

    def __init__(self, slide_layout_name: str) -> None:
        self.slide_layout_name = slide_layout_name

    @property
    def message(self) -> str:
        return f"The slide master attribute must be a slide layout. The {self.slide_layout_name} layout is not a slide layout."


class SlideMasterAttributeNotFoundError(TpptException, ValueError):
    """Slide master attribute not found."""

    def __init__(self, slide_layout_name: str) -> None:
        self.slide_layout_name = slide_layout_name

    @property
    def message(self) -> str:
        return f"The slide master does not have an attribute for the {self.slide_layout_name} layout"
