"""Color types for pptxr."""

from typing import Tuple, Union


class Color:
    """Represents a color in RGB or by name."""

    value: Union[str, Tuple[int, int, int]]

    def __init__(self, value: Union[str, Tuple[int, int, int]]):
        """Initialize a Color instance."""
        self.value = value

    @property
    def is_rgb(self) -> bool:
        """Check if the color is defined as RGB."""
        return isinstance(self.value, tuple)

    @property
    def is_named(self) -> bool:
        """Check if the color is defined as a named color."""
        return isinstance(self.value, str)

    def __repr__(self) -> str:
        """Return string representation."""
        if self.is_rgb:
            r, g, b = self.value
            return f"Color(RGB({r}, {g}, {b}))"
        return f"Color({self.value})"
