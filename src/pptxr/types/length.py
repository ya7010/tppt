"""Length and unit types for pptxr."""

from enum import Enum
from typing import Self, Tuple, Union


class Unit(Enum):
    """Represents units for measurements in pptxr."""

    PT = "pt"
    INCH = "in"
    CM = "cm"
    MM = "mm"
    PERCENT = "%"


class Length:
    """Represents a length with a value and unit."""

    value: float
    unit: Unit

    def __init__(self, value: float, unit: Union[Unit, str]):
        """Initialize a Length instance."""
        self.value = value
        self.unit = unit if isinstance(unit, Unit) else Unit(unit)

    @classmethod
    def from_tuple(cls, length_tuple: Tuple[float, str]) -> Self:
        """Create a Length instance from a tuple (value, unit)."""
        return cls(length_tuple[0], length_tuple[1])

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Length({self.value}, {self.unit.value})"
