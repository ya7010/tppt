"""Abstract classes for presentation components."""

from abc import ABC, abstractmethod
from typing import IO, List, Optional, Union

from pptxr.types import FilePath, Length, LiteralLength


class AbstractShape(ABC):
    """Abstract base class for shapes."""

    @abstractmethod
    def get_text(self) -> str:
        """Get shape text."""
        pass

    @abstractmethod
    def set_text(self, text: str) -> None:
        """Set shape text."""
        pass


class AbstractSlide(ABC):
    """Abstract base class for slides."""

    @abstractmethod
    def get_shapes(self) -> List[AbstractShape]:
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
    ) -> AbstractShape:
        """Add a shape to the slide."""
        pass

    @abstractmethod
    def get_title(self) -> Optional[AbstractShape]:
        """Get slide title shape."""
        pass


class AbstractPresentation(ABC):
    """Abstract base class for presentations."""

    @abstractmethod
    def get_slides(self) -> List[AbstractSlide]:
        """Get all slides in the presentation."""
        pass

    @abstractmethod
    def add_slide(self, layout_type: str) -> AbstractSlide:
        """Add a slide with specified layout."""
        pass

    @abstractmethod
    def save(self, file: Union[FilePath, IO[bytes]]) -> None:
        """Save presentation to file."""
        pass


class PresentationFactory(ABC):
    """Factory for creating presentations."""

    @abstractmethod
    def create_presentation(self) -> AbstractPresentation:
        """Create a new presentation."""
        pass

    @abstractmethod
    def load_presentation(self, path: str) -> AbstractPresentation:
        """Load presentation from file."""
        pass
