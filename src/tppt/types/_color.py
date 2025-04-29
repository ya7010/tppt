"""Color types for tppt."""

from typing import NamedTuple, TypeAlias, assert_never, overload

from tppt.exception import ColorInvalidFormatError

LiteralColor: TypeAlias = tuple[int, int, int] | str


class RGBColor(NamedTuple):
    r: int
    g: int
    b: int


@overload
def to_rgb_color(color: RGBColor | LiteralColor) -> RGBColor: ...


@overload
def to_rgb_color(color: RGBColor | LiteralColor | None) -> RGBColor | None: ...


def to_rgb_color(color: RGBColor | LiteralColor | None) -> RGBColor | None:
    match color:
        case None:
            return None
        case tuple():
            return RGBColor(*color)
        case str():
            if not color.startswith("#"):
                raise ColorInvalidFormatError(color)

            match len(color):
                case 4:
                    # Note that #123 is the same as #112233
                    r = int(color[1:2] * 2, 16)
                    g = int(color[2:3] * 2, 16)
                    b = int(color[3:4] * 2, 16)
                    return RGBColor(r, g, b)

                case 7:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    return RGBColor(r, g, b)

                case _:
                    raise ColorInvalidFormatError(color)
        case _:
            assert_never(color)
