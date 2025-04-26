"""Length types for tppt."""

from typing import Literal, assert_never

# Constants for unit conversion
INCHES_PER_POINT = 1 / 72  # 1 point = 1/72 inches
POINTS_PER_INCH = 72  # 1 inch = 72 points
CM_PER_INCH = 2.54  # 1 inch = 2.54 cm
MM_PER_INCH = 25.4  # 1 inch = 25.4 mm
MM_PER_CM = 10  # 1 cm = 10 mm
EMUS_PER_INCH = 914400  # 1 inch = 914400 EMU
EMUS_PER_CM = 360000  # 1 cm = 360000 EMU
EMUS_PER_MM = 36000  # 1 mm = 36000 EMU
EMUS_PER_PT = 12700  # 1 pt = 12700 EMU

LiteralPoint = tuple[int, Literal["pt"]]
LiteralCentimeter = tuple[float, Literal["cm"]]
LiteralInch = tuple[float, Literal["in"]]
LiteralMillimeter = tuple[float, Literal["mm"]]
LiteralEmu = tuple[int, Literal["emu"]]

LiteralLength = (
    LiteralPoint | LiteralCentimeter | LiteralInch | LiteralMillimeter | LiteralEmu
)


class Inchs:
    """Class representing inches"""

    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Inchs":
        if isinstance(other, tuple):
            other = to_length(other)
        return Inchs(self.value + to_inche(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Inchs":
        if isinstance(other, tuple):
            other = to_length(other)
        return Inchs(self.value - to_inche(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Inchs":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_inche(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Inchs":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_inche(other).value
        return self

    def __mul__(self, other: int | float) -> "Inchs":
        return Inchs(self.value * other)

    def __truediv__(self, other: int | float) -> "Inchs":
        return Inchs(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inchs):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class Points:
    """Class representing points"""

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Points":
        if isinstance(other, tuple):
            other = to_length(other)
        return Points(self.value + to_point(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Points":
        if isinstance(other, tuple):
            other = to_length(other)
        return Points(self.value - to_point(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Points":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_point(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Points":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_point(other).value
        return self

    def __mul__(self, other: int | float) -> "Points":
        return Points(int(self.value * other))

    def __truediv__(self, other: int | float) -> "Points":
        return Points(int(self.value / other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Points):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class Centimeters:
    """Class representing centimeters"""

    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Centimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        return Centimeters(self.value + to_centimeter(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Centimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        return Centimeters(self.value - to_centimeter(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Centimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_centimeter(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Centimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_centimeter(other).value
        return self

    def __mul__(self, other: int | float) -> "Centimeters":
        return Centimeters(self.value * other)

    def __truediv__(self, other: int | float) -> "Centimeters":
        return Centimeters(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Centimeters):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class Millimeters:
    """Class representing millimeters"""

    def __init__(self, value: float):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "Millimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        return Millimeters(self.value + to_millimeter(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "Millimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        return Millimeters(self.value - to_millimeter(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "Millimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_millimeter(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "Millimeters":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_millimeter(other).value
        return self

    def __mul__(self, other: int | float) -> "Millimeters":
        return Millimeters(self.value * other)

    def __truediv__(self, other: int | float) -> "Millimeters":
        return Millimeters(self.value / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Millimeters):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


class EnglishMetricUnits:
    """Class representing English Metric Units (EMU)"""

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: "Length | LiteralLength") -> "EnglishMetricUnits":
        if isinstance(other, tuple):
            other = to_length(other)
        return EnglishMetricUnits(self.value + to_emu(other).value)

    def __sub__(self, other: "Length | LiteralLength") -> "EnglishMetricUnits":
        if isinstance(other, tuple):
            other = to_length(other)
        return EnglishMetricUnits(self.value - to_emu(other).value)

    def __iadd__(self, other: "Length | LiteralLength") -> "EnglishMetricUnits":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value += to_emu(other).value
        return self

    def __isub__(self, other: "Length | LiteralLength") -> "EnglishMetricUnits":
        if isinstance(other, tuple):
            other = to_length(other)
        self.value -= to_emu(other).value
        return self

    def __mul__(self, other: int | float) -> "EnglishMetricUnits":
        return EnglishMetricUnits(int(self.value * other))

    def __truediv__(self, other: int | float) -> "EnglishMetricUnits":
        return EnglishMetricUnits(int(self.value / other))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EnglishMetricUnits):
            raise NotImplementedError(f"Cannot compare {type(self)} with {type(other)}")
        return self.value == other.value


Length = Inchs | Points | Centimeters | Millimeters | EnglishMetricUnits


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
                return Inchs(value)
            case "cm":
                return Centimeters(value)
            case "pt":
                return Points(int(value))
            case "mm":
                return Millimeters(value)
            case "emu":
                return EnglishMetricUnits(int(value))
            case _:
                assert_never(unit)
    else:
        return length


def to_literal_length(
    length: LiteralLength | Length, unit: Literal["in", "cm", "pt", "mm", "emu"]
) -> LiteralLength:
    """Convert internal length representation to public length representation

    Args:
        length (_Length): Internal length representation
        unit (Literal["in", "cm", "pt", "mm", "emu"]): Desired unit

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
        case "mm":
            return (to_millimeter(length).value, "mm")
        case "emu":
            return (to_emu(length).value, "emu")
        case _:
            assert_never(unit)


def to_optional_length(length: Length | LiteralLength | None) -> Length | None:
    if length is None:
        return None
    return to_length(length)


def to_centimeter(length: Length | LiteralLength) -> Centimeters:
    """Convert any length to centimeters

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Centimeter: Length in centimeters
    """
    if isinstance(length, tuple):
        return to_centimeter(to_length(length))

    match length:
        case Inchs():
            return Centimeters(length.value * CM_PER_INCH)
        case Points():
            return Centimeters(length.value * INCHES_PER_POINT * CM_PER_INCH)
        case Centimeters():
            return length
        case Millimeters():
            return Centimeters(length.value / MM_PER_CM)
        case EnglishMetricUnits():
            return Centimeters(length.value / EMUS_PER_CM)
        case _:
            assert_never(length)


def to_inche(length: Length | LiteralLength) -> Inchs:
    """Convert any length to inches

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Inch: Length in inches
    """
    if isinstance(length, tuple):
        return to_inche(to_length(length))

    match length:
        case Inchs():
            return length
        case Points():
            return Inchs(float(length.value) * INCHES_PER_POINT)
        case Centimeters():
            return Inchs(length.value / CM_PER_INCH)
        case Millimeters():
            return Inchs(length.value / MM_PER_INCH)
        case EnglishMetricUnits():
            return Inchs(length.value / EMUS_PER_INCH)
        case _:
            assert_never(length)


def to_point(length: Length | LiteralLength) -> Points:
    """Convert any length to points

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Point: Length in points
    """
    if isinstance(length, tuple):
        return to_point(to_length(length))

    match length:
        case Inchs():
            return Points(int(length.value * POINTS_PER_INCH))
        case Points():
            return length
        case Centimeters():
            return Points(int(length.value / CM_PER_INCH * POINTS_PER_INCH))
        case Millimeters():
            return Points(int(length.value / MM_PER_INCH * POINTS_PER_INCH))
        case EnglishMetricUnits():
            return Points(int(length.value / EMUS_PER_PT))
        case _:
            assert_never(length)


def to_millimeter(length: Length | LiteralLength) -> Millimeters:
    """Convert any length to millimeters

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Millimeter: Length in millimeters
    """
    if isinstance(length, tuple):
        return to_millimeter(to_length(length))

    match length:
        case Inchs():
            return Millimeters(length.value * MM_PER_INCH)
        case Points():
            return Millimeters(length.value * INCHES_PER_POINT * MM_PER_INCH)
        case Centimeters():
            return Millimeters(length.value * MM_PER_CM)
        case Millimeters():
            return length
        case EnglishMetricUnits():
            return Millimeters(length.value / EMUS_PER_MM)
        case _:
            assert_never(length)


def to_emu(length: Length | LiteralLength) -> EnglishMetricUnits:
    """Convert any length to English Metric Units (EMU)

    Args:
        length (_Length | Length): Length in any unit

    Returns:
        _Emu: Length in EMU
    """
    if isinstance(length, tuple):
        return to_emu(to_length(length))

    match length:
        case Inchs():
            return EnglishMetricUnits(int(length.value * EMUS_PER_INCH))
        case Points():
            return EnglishMetricUnits(int(length.value * EMUS_PER_PT))
        case Centimeters():
            return EnglishMetricUnits(int(length.value * EMUS_PER_CM))
        case Millimeters():
            return EnglishMetricUnits(int(length.value * EMUS_PER_MM))
        case EnglishMetricUnits():
            return length
        case _:
            assert_never(length)
