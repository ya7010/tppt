"""Presentation wrapper implementation."""

from typing import IO, Self, cast

from pptx.presentation import PptxPresentation

from pptxr._pptx.converters import save_presentation
from pptxr._pptx.slide import Slide
from pptxr._pptx.types import PptxConvertible
from pptxr.types import FilePath, SlideLayoutType


class Presentation(PptxConvertible[PptxPresentation]):
    """Presentation wrapper with type safety."""

    def __init__(self, pptx_presentation: PptxPresentation | None = None) -> None:
        """Initialize presentation."""
        self._presentation: PptxPresentation = (
            pptx_presentation if pptx_presentation is not None else PptxPresentation()
        )

    def get_slides(self) -> list[Slide]:
        """Get all slides in the presentation."""
        return [Slide(slide) for slide in self._presentation.slides]

    def add_slide(self, layout_type: SlideLayoutType) -> Slide:
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
    def from_pptx(cls, pptx_obj: PptxPresentation) -> Self:
        """Create from pptx presentation."""
        if not isinstance(pptx_obj, PptxPresentation):
            raise TypeError(f"Expected PptxPresentation, got {type(pptx_obj)}")
        return cls(pptx_obj)


class PptxPresentationFactory:
    """A factory class for creating PowerPoint presentations."""

    def __init__(self, template_path: FilePath | None = None) -> None:
        """Initialize a new presentation factory."""
        self._template_path = template_path
        self._presentation = (
            PptxPresentation(template_path) if template_path else PptxPresentation()
        )

    def add_slide(self, layout_type: SlideLayoutType) -> Slide:
        """Add a slide to the presentation."""
        return self._presentation.slides.add_slide(self._presentation.slide_layouts[0])

    def save(self, path: FilePath) -> None:
        """Save the presentation to a file."""
        self._presentation.save(str(path))
