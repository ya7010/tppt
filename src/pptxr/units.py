from dataclasses import dataclass
from typing import Literal, Union, assert_never

# Constants for unit conversion
INCHES_PER_POINT = 1 / 72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72  # 1 inch = 72 points
CM_PER_INCH = 2.54  # 1 inch = 2.54 cm


Length = Union[
    tuple[int, Literal["pt"]],
    tuple[float, Literal["in"]],
    tuple[float, Literal["cm"]],
]


@dataclass
class _Inch:
    """Class representing inches"""

    value: float

    def __add__(self, other: Union["_Length", Length]) -> "_Inch":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Inch(self.value + to_inche(other).value)

    def __sub__(self, other: Union["_Length", Length]) -> "_Inch":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Inch(self.value - to_inche(other).value)

    def __iadd__(self, other: Union["_Length", Length]) -> "_Inch":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        self.value += to_inche(other).value
        return self

    def __isub__(self, other: Union["_Length", Length]) -> "_Inch":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
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

    def __add__(self, other: Union["_Length", Length]) -> "_Point":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Point(self.value + to_point(other).value)

    def __sub__(self, other: Union["_Length", Length]) -> "_Point":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Point(self.value - to_point(other).value)

    def __iadd__(self, other: Union["_Length", Length]) -> "_Point":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        self.value += to_point(other).value
        return self

    def __isub__(self, other: Union["_Length", Length]) -> "_Point":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
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
class _Centimeter:
    """Class representing centimeters"""

    value: float

    def __add__(self, other: Union["_Length", Length]) -> "_Centimeter":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Centimeter(self.value + to_centimeter(other).value)

    def __sub__(self, other: Union["_Length", Length]) -> "_Centimeter":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        return _Centimeter(self.value - to_centimeter(other).value)

    def __iadd__(self, other: Union["_Length", Length]) -> "_Centimeter":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        self.value += to_centimeter(other).value
        return self

    def __isub__(self, other: Union["_Length", Length]) -> "_Centimeter":
        if isinstance(other, tuple):
            other = _to_internal_length(other)
        self.value -= to_centimeter(other).value
        return self

    def __mul__(self, other: Union[int, float]) -> "_Centimeter":
        return _Centimeter(self.value * other)

    def __truediv__(self, other: Union[int, float]) -> "_Centimeter":
        return _Centimeter(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Centimeter):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


_Length = Union["_Inch", "_Point", "_Centimeter"]


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
        case "cm":
            return _Centimeter(value)
        case "pt":
            return _Point(int(value))
        case _:
            assert_never(unit)


def _to_public_length(length: _Length, unit: Literal["in", "cm", "pt"]) -> Length:
    """Convert internal length representation to public length representation

    Args:
        length (_Length): Internal length representation
        unit (Literal["in", "cm", "pt"]): Desired unit

    Returns:
        Length: Public length representation
    """
    match unit:
        case "in":
            return (to_inche(length).value, "in")
        case "cm":
            return (to_centimeter(length).value, "cm")
        case "pt":
            return (to_point(length).value, "pt")
        case _:
            assert_never(unit)


def to_centimeter(length: Union[_Length, Length]) -> _Centimeter:
    """Convert any length to centimeters

    Args:
        length (Union[_Length, Length]): Length in any unit

    Returns:
        _Centimeter: Length in centimeters
    """
    if isinstance(length, tuple):
        return to_centimeter(_to_internal_length(length))

    match length:
        case _Inch():
            return _Centimeter(length.value * CM_PER_INCH)
        case _Point():
            return _Centimeter(length.value * INCHES_PER_POINT * CM_PER_INCH)
        case _Centimeter():
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
        case _Centimeter():
            return _Inch(length.value / CM_PER_INCH)
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
        case _Centimeter():
            return _Point(int(length.value / CM_PER_INCH * POINTS_PER_INCH))
        case _:
            assert_never(length)
