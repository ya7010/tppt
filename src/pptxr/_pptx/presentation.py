"""Presentation wrapper implementation."""

from typing import IO, cast

from pptx import Presentation as PptxPresentation
from pptx.presentation import Presentation as PptxPresentationType

from pptxr._pptx.converters import save_presentation
from pptxr._pptx.slide import Slide
from pptxr._pptx.types import PptxConvertible
from pptxr.abstract.presentation import AbstractPresentation, PresentationFactory
from pptxr.types import FilePath


class Presentation(AbstractPresentation, PptxConvertible):
    """Presentation wrapper with type safety."""

    def __init__(self, pptx_presentation: PptxPresentationType | None = None) -> None:
        """Initialize presentation."""
        if pptx_presentation is None:
            self._presentation = PptxPresentation()
        else:
            self._presentation = pptx_presentation

    def get_slides(self) -> list[Slide]:
        """Get all slides in the presentation."""
        return [Slide(slide) for slide in self._presentation.slides]

    def add_slide(self, layout_type: str) -> Slide:
        """Add a slide with specified layout."""
        layout_map = {
            "TITLE": 0,
            "TITLE_AND_CONTENT": 1,
            "SECTION_HEADER": 2,
            "TWO_CONTENT": 3,
            "COMPARISON": 4,
            "TITLE_ONLY": 5,
            "BLANK": 6,
            "CONTENT_WITH_CAPTION": 7,
            "PICTURE_WITH_CAPTION": 8,
            "TITLE_AND_VERTICAL_TEXT": 9,
            "VERTICAL_TITLE_AND_TEXT": 10,
        }
        layout = self._presentation.slide_layouts[layout_map[layout_type]]
        slide = self._presentation.slides.add_slide(layout)
        return Slide(slide)

    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save presentation to file."""
        save_presentation(self._presentation, file)

    def to_pptx(self) -> PptxPresentation:
        """Convert to pptx presentation."""
        return cast(PptxPresentation, self._presentation)

    @classmethod
    def from_pptx(cls, pptx_obj: PptxPresentation) -> "Presentation":
        """Create from pptx presentation."""
        if not isinstance(pptx_obj, PptxPresentationType):
            raise TypeError(f"Expected PptxPresentation, got {type(pptx_obj)}")
        return cls(pptx_obj)


class PptxPresentationFactory(PresentationFactory):
    """Factory for creating PPTX presentations."""

    def create_presentation(self) -> Presentation:
        """Create a new presentation."""
        return Presentation()

    def load_presentation(self, path: str) -> Presentation:
        """Load presentation from file."""
        return Presentation(PptxPresentation(path))
