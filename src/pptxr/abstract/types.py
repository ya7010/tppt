"""Abstract types for presentation objects."""

import pathlib
from abc import ABC, abstractmethod
from typing import IO, TypeAlias, TypeVar

from pptxr.units import Length, LiteralLength

FilePath: TypeAlias = str | pathlib.Path


class Shape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def get_text(self) -> str:
        """Get shape text."""
        pass

    @abstractmethod
    def set_text(self, text: str) -> None:
        """Set shape text."""
        pass


class Slide(ABC):
    """Abstract base class for slides."""

    @abstractmethod
    def get_shapes(self) -> list[Shape]:
        """Get all shapes in the slide."""
        pass

    @abstractmethod
    def add_shape(
        self,
        shape_type: str,
        left: Length | LiteralLength,
        top: Length | LiteralLength,
        width: Length | LiteralLength,
        height: Length | LiteralLength,
    ) -> Shape:
        """Add a shape to the slide."""
        pass

    @abstractmethod
    def get_title(self) -> Shape | None:
        """Get slide title shape."""
        pass


class Presentation(ABC):
    """Abstract base class for presentations."""

    @abstractmethod
    def get_slides(self) -> list[Slide]:
        """Get all slides in the presentation."""
        raise NotImplementedError()

    @abstractmethod
    def add_slide(self, layout_type: str) -> Slide:
        """Add a slide with specified layout."""
        raise NotImplementedError()

    @abstractmethod
    def save(self, file: FilePath | IO[bytes]) -> None:
        """Save presentation to file."""
        raise NotImplementedError()


T = TypeVar("T", bound=Presentation)


class PresentationFactory(ABC):
    """Abstract factory for creating presentations."""

    @abstractmethod
    def create_presentation(self) -> Presentation:
        """Create a new presentation."""
        pass

    @abstractmethod
    def load_presentation(self, path: str) -> Presentation:
        """Load presentation from file."""
        pass
