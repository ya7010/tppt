"""Presentation wrapper implementation."""

import os
from typing import IO, TYPE_CHECKING, Any, Callable, Generic, Self, cast, overload

from pptx.presentation import Presentation as PptxPresentation

from tppt.pptx.tree import ppt2dict
from tppt.template.default import DefaultSlideMaster
from tppt.template.slide_layout import SlideLayout, SlideLayoutProxy
from tppt.template.slide_master import (
    GenericTpptSlideMaster,
    SlideMasterProxy,
)
from tppt.types import FilePath
from tppt.types._length import Length, LiteralLength

from .converter import PptxConvertible, to_pptx_length, to_tppt_length
from .slide import SlideBuilder
from .slide_master import SlideMaster

if TYPE_CHECKING:
    from tppt.pptx.slide import Slide


class Presentation(PptxConvertible[PptxPresentation]):
    """Presentation wrapper with type safety."""

    def __init__(
        self,
        pptx: PptxPresentation | FilePath,
    ) -> None:
        """Initialize presentation."""
        if isinstance(pptx, (os.PathLike, str)):
            from pptx import Presentation

            pptx = Presentation(os.fspath(pptx))
        self._pptx = pptx

    @property
    def slides(self) -> "list[Slide]":
        """Get the slides."""
        from tppt.pptx.slide import Slide

        return [Slide.from_pptx(slide) for slide in self._pptx.slides]

    @property
    def slide_master(self) -> SlideMaster:
        """
        Get the slide master.

        This tool supports only one slide master.
        """
        return SlideMaster.from_pptx(self._pptx.slide_masters[0])

    @property
    def slide_width(self) -> Length | None:
        return to_tppt_length(self._pptx.slide_width)

    @slide_width.setter
    def slide_width(self, value: Length | LiteralLength) -> None:
        self._pptx.slide_width = to_pptx_length(value)

    @property
    def slide_height(self) -> Length | None:
        return to_tppt_length(self._pptx.slide_height)

    @slide_height.setter
    def slide_height(self, value: Length | LiteralLength) -> None:
        self._pptx.slide_height = to_pptx_length(value)

    @property
    def tree(self) -> dict[str, Any]:
        """Get the node tree of the presentation."""
        return ppt2dict(self._pptx)

    @overload
    @classmethod
    def builder(
        cls,
    ) -> "PresentationBuilder[DefaultSlideMaster]": ...

    @overload
    @classmethod
    def builder(
        cls,
        slide_master: "type[GenericTpptSlideMaster]",
    ) -> "PresentationBuilder[GenericTpptSlideMaster]": ...

    @classmethod
    def builder(
        cls,
        slide_master=None,
    ):
        """Get a builder for the presentation."""

        if slide_master is None:
            slide_master = DefaultSlideMaster
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

    def __init__(
        self,
        slide_master: "type[GenericTpptSlideMaster]",
    ) -> None:
        """Initialize the builder."""
        import pptx

        if (
            slide_master_source := slide_master.__slide_master_source__
        ) and slide_master_source != "default":
            self._pptx = pptx.Presentation(os.fspath(slide_master_source))
        else:
            self._pptx = pptx.Presentation()

        self._slide_master = slide_master

    def slide_width(self, value: Length | LiteralLength) -> Self:
        """Set the slide width."""
        self._pptx.slide_width = to_pptx_length(value)
        return self

    def slide_height(self, value: Length | LiteralLength) -> Self:
        """Set the slide height."""
        self._pptx.slide_height = to_pptx_length(value)
        return self

    def slide(
        self,
        slide: Callable[[type[GenericTpptSlideMaster]], SlideLayout | SlideBuilder],
        /,
    ) -> Self:
        """Add a slide to the presentation."""
        slide_master = SlideMasterProxy(self._slide_master, Presentation(self._pptx))
        template_slide_layout = cast(
            SlideLayoutProxy,
            slide(cast(type[GenericTpptSlideMaster], slide_master)),
        )

        slide_builder = cast(
            SlideBuilder,
            template_slide_layout.builder()
            if isinstance(template_slide_layout, SlideLayoutProxy)
            else template_slide_layout,
        )

        slide_layout = slide_builder._slide_layout.to_pptx()
        new_slide = self._pptx.slides.add_slide(slide_layout)

        slide_builder._build(new_slide)

        return self

    def build(self) -> Presentation:
        """Build the presentation."""

        return Presentation(self._pptx)

    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save the presentation to a file."""
        self.build().save(file)
