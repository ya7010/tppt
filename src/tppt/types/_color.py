"""Color types for tppt."""

from pptx.dml.color import RGBColor
from tppt.exception import ColorInvalidFormatError


class Color:
    """Represents a color in RGB or by name."""

    def __init__(self, value: str | tuple[int, int, int]):
        """Initialize a Color instance."""
        if isinstance(value, str):
            if not value.startswith("#"):
                raise ColorInvalidFormatError(value)

            match len(value):
                case 4:
                    r = int(value[1:2], 16)
                    g = int(value[2:3], 16)
                    b = int(value[3:4], 16)

                    self.value = RGBColor(r, g, b)
                case 7:
                    r = int(value[1:3], 16)
                    g = int(value[3:5], 16)
                    b = int(value[5:7], 16)

                    self.value = RGBColor(r, g, b)
                case _:
                    raise ColorInvalidFormatError(value)

        else:
            r, g, b = value
            self.value = RGBColor(r, g, b)

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
            return "Color())"
        return f"Color({self.value})"
