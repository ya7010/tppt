"""Presentation wrapper implementation."""

import os
from typing import IO, Any, Generic, Self

from pptx.presentation import Presentation as PptxPresentation

from tppt._pptx.tree import presentation_to_dict
from tppt._tppt.slide_master import GenericTpptSlideMaster
from tppt.types import FilePath

from .converter import PptxConvertible
from .slide import SlideBuilder
from .slide_master import SlideMaster


class Presentation(PptxConvertible[PptxPresentation]):
    """Presentation wrapper with type safety."""

    def __init__(
        self,
        presentation: PptxPresentation,
    ) -> None:
        """Initialize presentation."""
        self._pptx = presentation

    @property
    def slide_master(self) -> SlideMaster:
        """
        Get the slide master.

        This tool supports only one slide master.
        """
        return SlideMaster.from_pptx(self._pptx.slide_masters[0])

    @property
    def tree(self) -> dict[str, Any]:
        """Get the node tree of the presentation."""
        return presentation_to_dict(self._pptx)

    @classmethod
    def builder(
        cls, slide_master: GenericTpptSlideMaster | None = None
    ) -> "PresentationBuilder[GenericTpptSlideMaster]":
        """Get a builder for the presentation."""
        return PresentationBuilder(slide_master)

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


class PresentationBuilder(Generic[GenericTpptSlideMaster]):
    """Builder for presentations."""

    def __init__(self, slide_master: GenericTpptSlideMaster | None = None) -> None:
        """Initialize the builder."""
        import pptx

        self._pptx = pptx.Presentation()
        self._slide_master = slide_master

    def slide(self, slide: SlideBuilder, /) -> Self:
        """Add a slide to the presentation."""

        slide._build(self)

        return self

    def build(self) -> Presentation:
        """Build the presentation."""

        return Presentation(self._pptx)

    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save the presentation to a file."""
        self.build().save(file)
