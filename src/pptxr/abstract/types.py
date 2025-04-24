"""Abstract types for presentation objects."""

from abc import ABC, abstractmethod
from typing import TypeVar


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
        self, shape_type: str, left: float, top: float, width: float, height: float
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
        pass

    @abstractmethod
    def add_slide(self, layout_type: str) -> Slide:
        """Add a slide with specified layout."""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Save presentation to file."""
        pass


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
