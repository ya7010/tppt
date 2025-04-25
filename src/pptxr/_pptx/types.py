"""Type definitions for pptx conversion layer."""

from typing import Protocol, TypeVar, runtime_checkable

from pptx.presentation import Presentation as PptxPresentation
from pptx.shapes.base import BaseShape as PptxShape
from pptx.slide import Slide as PptxSlide

T = TypeVar("T", bound="PptxConvertible")


@runtime_checkable
class PptxConvertible(Protocol):
    """Protocol for objects that can be converted to and from pptx objects."""

    def to_pptx(self) -> PptxPresentation | PptxSlide | PptxShape:
        """Convert to pptx object."""
        ...

    @classmethod
    def from_pptx(
        cls, pptx_obj: PptxPresentation | PptxSlide | PptxShape
    ) -> "PptxConvertible":
        """Create from pptx object."""
        ...


class PptxConverter:
    """Utility class for converting pptx objects."""

    @staticmethod
    def to_pptx(obj: PptxConvertible) -> PptxPresentation | PptxSlide | PptxShape:
        """Convert object to pptx format."""
        return obj.to_pptx()
