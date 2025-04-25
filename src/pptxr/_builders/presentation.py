"""Presentation builder implementation for pptxr."""

from pathlib import Path
from typing import List, Optional, Self, Union

from .._data import Slide
from .._slide_master import SlideMaster
from .slide import SlideBuilder


class PresentationBuilder:
    """Builder class for creating presentations."""

    slides: List[Slide]
    slide_master: Optional[SlideMaster]
    template_path: Optional[Path]

    def __init__(
        self,
        slide_master: Optional[SlideMaster] = None,
        template_path: Optional[Union[str, Path]] = None,
    ):
        """Initialize a PresentationBuilder instance."""
        self.slides = []
        self.slide_master = slide_master
        self.template_path = Path(template_path) if template_path else None

    def slide(self, slide_builder: Union[SlideBuilder, Slide]) -> Self:
        """Add a slide to the presentation."""
        if isinstance(slide_builder, SlideBuilder):
            self.slides.append(slide_builder.build())
        else:
            self.slides.append(slide_builder)
        return self

    def build(self):
        """Build the presentation."""
        # Import here to avoid circular imports
        from .._presentation import Presentation

        return Presentation(
            slides=self.slides,
            slide_master=self.slide_master,
            template_path=self.template_path,
        )
