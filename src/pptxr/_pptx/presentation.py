"""Presentation wrapper implementation."""

import os
from typing import IO, Self

from pptx.presentation import Presentation as PptxPresentation

from pptxr.types import FilePath

from .slide import SlideBuilder
from .slide_master import SlideMaster
from .types import PptxConvertible


class Presentation(PptxConvertible[PptxPresentation]):
    """Presentation wrapper with type safety."""

    def __init__(self, presentation: PptxPresentation) -> None:
        """Initialize presentation."""
        self._pptx = presentation

    @property
    def slide_master(self) -> SlideMaster:
        """
        Get the slide master.

        This tool supports only one slide master.
        """
        return SlideMaster.from_pptx(self._pptx.slide_masters[0])

    @classmethod
    def builder(cls) -> "PresentationBuilder":
        """Get a builder for the presentation."""
        return PresentationBuilder()

    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save presentation to file."""
        if isinstance(file, os.PathLike):
            file = os.fspath(file)
        self._pptx.save(file)

    def to_pptx(self) -> PptxPresentation:
        """Convert to pptx presentation."""
        return self._pptx

    @classmethod
    def from_pptx(cls, pptx_obj: PptxPresentation) -> Self:
        """Create from pptx presentation."""
        return cls(pptx_obj)


class PresentationBuilder:
    """Builder for presentations."""

    def __init__(self) -> None:
        """Initialize the builder."""
        import pptx

        self._pptx = pptx.Presentation()

    def slide(self, slide: SlideBuilder, /) -> Self:
        """Add a slide to the presentation."""

        slide._build(self._pptx)

        return self

    def build(self) -> Presentation:
        """Build the presentation."""

        return Presentation(self._pptx)
