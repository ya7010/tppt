from dataclasses import dataclass
from typing import Literal, Union, assert_never

# Constants for unit conversion
INCHES_PER_POINT = 1 / 72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72  # 1 inch = 72 points
MM_PER_INCH = 25.4  # 1 inch = 25.4 mm


@dataclass
class _Inch:
    """Class representing inches"""

    value: float

    def __add__(self, other: "_Length") -> "_Inch":
        return _Inch(self.value + to_inche(other).value)

    def __sub__(self, other: "_Length") -> "_Inch":
        return _Inch(self.value - to_inche(other).value)

    def __iadd__(self, other: "_Length") -> "_Inch":
        self.value += to_inche(other).value
        return self

    def __isub__(self, other: "_Length") -> "_Inch":
        self.value -= to_inche(other).value
        return self

    def __mul__(self, other: Union[int, float]) -> "_Inch":
        return _Inch(self.value * other)

    def __truediv__(self, other: Union[int, float]) -> "_Inch":
        return _Inch(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Inch):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


@dataclass
class _Point:
    """Class representing points"""

    value: int

    def __add__(self, other: "_Length") -> "_Point":
        return _Point(self.value + to_point(other).value)

    def __sub__(self, other: "_Length") -> "_Point":
        return _Point(self.value - to_point(other).value)

    def __iadd__(self, other: "_Length") -> "_Point":
        self.value += to_point(other).value
        return self

    def __isub__(self, other: "_Length") -> "_Point":
        self.value -= to_point(other).value
        return self

    def __mul__(self, other: Union[int, float]) -> "_Point":
        return _Point(int(self.value * other))

    def __truediv__(self, other: Union[int, float]) -> "_Point":
        return _Point(int(self.value / other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Point):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


@dataclass
class _Millimeter:
    """Class representing millimeters"""

    value: float

    def __add__(self, other: "_Length") -> "_Millimeter":
        return _Millimeter(self.value + to_millimeter(other).value)

    def __sub__(self, other: "_Length") -> "_Millimeter":
        return _Millimeter(self.value - to_millimeter(other).value)

    def __iadd__(self, other: "_Length") -> "_Millimeter":
        self.value += to_millimeter(other).value
        return self

    def __isub__(self, other: "_Length") -> "_Millimeter":
        self.value -= to_millimeter(other).value
        return self

    def __mul__(self, other: Union[int, float]) -> "_Millimeter":
        return _Millimeter(self.value * other)

    def __truediv__(self, other: Union[int, float]) -> "_Millimeter":
        return _Millimeter(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Millimeter):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


_Length = Union[_Inch, _Point, _Millimeter]

Length = Union[
    tuple[int, Literal["pt"]],
    tuple[float, Literal["in"]],
    tuple[float, Literal["mm"]],
]


def _to_internal_length(length: Length) -> _Length:
    """Convert public length representation to internal length representation

    Args:
        length (Length): Public length representation

    Returns:
        _Length: Internal length representation
    """
    value, unit = length
    match unit:
        case "in":
            return _Inch(value)
        case "mm":
            return _Millimeter(value)
        case "pt":
            return _Point(int(value))
        case _:
            assert_never(unit)


def _to_public_length(length: _Length, unit: Literal["in", "mm", "pt"]) -> Length:
    """Convert internal length representation to public length representation

    Args:
        length (_Length): Internal length representation
        unit (Literal["in", "mm", "pt"]): Desired unit

    Returns:
        Length: Public length representation
    """
    match unit:
        case "in":
            return (to_inche(length).value, "in")
        case "mm":
            return (to_millimeter(length).value, "mm")
        case "pt":
            return (to_point(length).value, "pt")
        case _:
            assert_never(unit)


def to_millimeter(length: Union[_Length, Length]) -> _Millimeter:
    """Convert any length to millimeters

    Args:
        length (Union[_Length, Length]): Length in any unit

    Returns:
        _Millimeter: Length in millimeters
    """
    if isinstance(length, tuple):
        return to_millimeter(_to_internal_length(length))

    match length:
        case _Inch():
            return _Millimeter(length.value * MM_PER_INCH)
        case _Point():
            return _Millimeter(length.value * INCHES_PER_POINT * MM_PER_INCH)
        case _Millimeter():
            return length
        case _:
            assert_never(length)


def to_inche(length: Union[_Length, Length]) -> _Inch:
    """Convert any length to inches

    Args:
        length (Union[_Length, Length]): Length in any unit

    Returns:
        _Inch: Length in inches
    """
    if isinstance(length, tuple):
        return to_inche(_to_internal_length(length))

    match length:
        case _Inch():
            return length
        case _Point():
            return _Inch(float(length.value) * INCHES_PER_POINT)
        case _Millimeter():
            return _Inch(length.value / MM_PER_INCH)
        case _:
            assert_never(length)


def to_point(length: Union[_Length, Length]) -> _Point:
    """Convert any length to points

    Args:
        length (Union[_Length, Length]): Length in any unit

    Returns:
        _Point: Length in points
    """
    if isinstance(length, tuple):
        return to_point(_to_internal_length(length))

    match length:
        case _Inch():
            return _Point(int(length.value * POINTS_PER_INCH))
        case _Point():
            return length
        case _Millimeter():
            return _Point(int(length.value / MM_PER_INCH * POINTS_PER_INCH))
        case _:
            assert_never(length)
