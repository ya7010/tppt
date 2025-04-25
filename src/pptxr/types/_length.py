"""Length types for pptxr."""

from typing import Literal, assert_never

# Constants for unit conversion
INCHES_PER_POINT = 1 / 72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72  # 1 inch = 72 points
CM_PER_INCH = 2.54  # 1 inch = 2.54 cm

LiteralPoint = tuple[int, Literal["pt"]]
LiteralInch = tuple[float, Literal["in"]]
LiteralCentimeter = tuple[float, Literal["cm"]]

LiteralLength = LiteralPoint | LiteralInch | LiteralCentimeter


class Inch:
    """Class representing inches"""

    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Inch":
        if isinstance(other, tuple):
            other = to_length(other)
        return Inch(self.value + to_inche(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Inch":
        if isinstance(other, tuple):
            other = to_length(other)
        return Inch(self.value - to_inche(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Inch":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_inche(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Inch":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_inche(other).value
        return self

    def __mul__(self, other: int | float) -> "Inch":
        return Inch(self.value * other)

    def __truediv__(self, other: int | float) -> "Inch":
        return Inch(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inch):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class Point:
    """Class representing points"""

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Point":
        if isinstance(other, tuple):
            other = to_length(other)
        return Point(self.value + to_point(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Point":
        if isinstance(other, tuple):
            other = to_length(other)
        return Point(self.value - to_point(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Point":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_point(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Point":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_point(other).value
        return self

    def __mul__(self, other: int | float) -> "Point":
        return Point(int(self.value * other))

    def __truediv__(self, other: int | float) -> "Point":
        return Point(int(self.value / other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class Centimeter:
    """Class representing centimeters"""

    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Centimeter":
        if isinstance(other, tuple):
            other = to_length(other)
        return Centimeter(self.value + to_centimeter(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Centimeter":
        if isinstance(other, tuple):
            other = to_length(other)
        return Centimeter(self.value - to_centimeter(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Centimeter":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_centimeter(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Centimeter":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_centimeter(other).value
        return self

    def __mul__(self, other: int | float) -> "Centimeter":
        return Centimeter(self.value * other)

    def __truediv__(self, other: int | float) -> "Centimeter":
        return Centimeter(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Centimeter):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


Length = Inch | Point | Centimeter


def to_length(length: LiteralLength | Length) -> Length:
    """Convert public length representation to internal length representation

    Args:
        length (Length): Public length representation

    Returns:
        _Length: Internal length representation
    """

    if isinstance(length, tuple):
        value, unit = length
        match unit:
            case "in":
                return Inch(value)
            case "cm":
                return Centimeter(value)
            case "pt":
                return Point(int(value))
            case _:
                assert_never(unit)
    else:
        return length


def to_literal_length(
    length: LiteralLength | Length, unit: Literal["in", "cm", "pt"]
) -> LiteralLength:
    """Convert internal length representation to public length representation

    Args:
        length (_Length): Internal length representation
        unit (Literal["in", "cm", "pt"]): Desired unit

    Returns:
        Length: Public length representation
    """
    if isinstance(length, tuple):
        return length

    match unit:
        case "in":
            return (to_inche(length).value, "in")
        case "cm":
            return (to_centimeter(length).value, "cm")
        case "pt":
            return (to_point(length).value, "pt")
        case _:
            assert_never(unit)


def to_optional_length(length: Length | LiteralLength | None) -> Length | None:
    if length is None:
        return None
    return to_length(length)


def to_centimeter(length: Length | LiteralLength) -> Centimeter:
    """Convert any length to centimeters

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Centimeter: Length in centimeters
    """
    if isinstance(length, tuple):
        return to_centimeter(to_length(length))

    match length:
        case Inch():
            return Centimeter(length.value * CM_PER_INCH)
        case Point():
            return Centimeter(length.value * INCHES_PER_POINT * CM_PER_INCH)
        case Centimeter():
            return length
        case _:
            assert_never(length)


def to_inche(length: Length | LiteralLength) -> Inch:
    """Convert any length to inches

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Inch: Length in inches
    """
    if isinstance(length, tuple):
        return to_inche(to_length(length))

    match length:
        case Inch():
            return length
        case Point():
            return Inch(float(length.value) * INCHES_PER_POINT)
        case Centimeter():
            return Inch(length.value / CM_PER_INCH)
        case _:
            assert_never(length)


def to_point(length: Length | LiteralLength) -> Point:
    """Convert any length to points

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Point: Length in points
    """
    if isinstance(length, tuple):
        return to_point(to_length(length))

    match length:
        case Inch():
            return Point(int(length.value * POINTS_PER_INCH))
        case Point():
            return length
        case Centimeter():
            return Point(int(length.value / CM_PER_INCH * POINTS_PER_INCH))
        case _:
            assert_never(length)
