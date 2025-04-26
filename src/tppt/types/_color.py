"""Color types for tppt."""

from typing import TypeAlias, overload

from tppt.exception import ColorInvalidFormatError

LiteralColor: TypeAlias = tuple[int, int, int] | str


class Color:
    """Represents a color in RGB or by hex code.

    Examples:
        >>> Color("#00B")
        >>> Color("#00BB00")
        >>> Color(255, 0, 0)
    """

    @overload
    def __init__(self, r: str): ...

    @overload
    def __init__(self, r: int, g: int, b: int): ...

    def __init__(self, r: str | int, g: int | None = None, b: int | None = None):
        """Initialize a Color instance."""
        if isinstance(r, str):
            if not r.startswith("#"):
                raise ColorInvalidFormatError(r)

            match len(r):
                case 4:
                    # Note that #123 is the same as #112233
                    self.r = int(r[1:2] * 2, 16)
                    self.g = int(r[2:3] * 2, 16)
                    self.b = int(r[3:4] * 2, 16)

                case 7:
                    self.r = int(r[1:3], 16)
                    self.g = int(r[3:5], 16)
                    self.b = int(r[5:7], 16)

                case _:
                    raise ColorInvalidFormatError(r)

        else:
            self.r = r
            self.g = g  # type: ignore
            self.b = b  # type: ignore

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Color({self.r}, {self.g}, {self.b})"


def to_color(color: Color | LiteralColor) -> Color:
    if isinstance(color, Color):
        return color
    else:
        if isinstance(color, tuple):
            return Color(*color)
        else:
            return Color(color)
