"""Presentation module for pptxr."""

from pathlib import Path
from typing import List, Optional, Union

from ._builders.presentation import PresentationBuilder
from ._data import SlideBone
from ._slide_master import SlideMaster


class Presentation:
    """Represents a PowerPoint presentation."""

    slides: List[SlideBone]
    slide_master: Optional[SlideMaster]
    template_path: Optional[Path]

    def __init__(
        self,
        slides: List[SlideBone],
        slide_master: Optional[SlideMaster] = None,
        template_path: Optional[Path] = None,
    ):
        """Initialize a Presentation instance."""
        self.slides = slides
        self.slide_master = slide_master
        self.template_path = template_path

    @classmethod
    def builder(
        cls,
        slide_master: Optional[SlideMaster] = None,
        template_path: Optional[Union[str, Path]] = None,
    ) -> PresentationBuilder:
        """Create a PresentationBuilder instance."""
        return PresentationBuilder(
            slide_master=slide_master, template_path=template_path
        )

    def save(self, path: Union[str, Path]) -> None:
        """Save the presentation to a file."""
        # This is a placeholder implementation
        print(f"Saving presentation to {path}")
        # In a real implementation, this would create and save a .pptx file
