import pytest

from tppt.types._length import (
    Centimeter,
    Inch,
    Point,
    to_centimeter,
    to_inche,
    to_length,
    to_literal_length,
    to_point,
)


def test_to_centimeter():
    """Test conversion to centimeters"""
    # Test from inches
    assert to_centimeter(Inch(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test from points
    assert to_centimeter(Point(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test from centimeters
    assert to_centimeter(Centimeter(2.54)).value == 2.54
    assert to_centimeter((2.54, "cm")).value == 2.54


def test_to_inche():
    """Test conversion to inches"""
    # Test from inches
    assert to_inche(Inch(1)).value == 1.0
    assert to_inche((1.0, "in")).value == 1.0

    # Test from points
    assert to_inche(Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test from centimeters
    assert to_inche(Centimeter(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0


def test_to_point():
    """Test conversion to points"""
    # Test from inches
    assert to_point(Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test from points
    assert to_point(Point(72)).value == 72
    assert to_point((72, "pt")).value == 72

    # Test from centimeters
    assert to_point(Centimeter(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_length_operations():
    """Test operations on internal length representations"""
    # Test addition
    assert (Inch(1) + Inch(1)).value == 2.0
    assert (Point(72) + Point(72)).value == 144
    assert (Centimeter(2.54) + Centimeter(2.54)).value == 5.08

    # Test addition with Length tuples
    assert (Inch(1) + (1.0, "in")).value == 2.0
    assert (Point(72) + (72, "pt")).value == 144
    assert (Centimeter(2.54) + (2.54, "cm")).value == 5.08

    # Test subtraction
    assert (Inch(2) - Inch(1)).value == 1.0
    assert (Point(144) - Point(72)).value == 72
    assert (Centimeter(5.08) - Centimeter(2.54)).value == 2.54

    # Test subtraction with Length tuples
    assert (Inch(2) - (1.0, "in")).value == 1.0
    assert (Point(144) - (72, "pt")).value == 72
    assert (Centimeter(5.08) - (2.54, "cm")).value == 2.54

    # Test multiplication
    assert (Inch(1) * 2).value == 2.0
    assert (Point(72) * 2).value == 144
    assert (Centimeter(2.54) * 2).value == 5.08

    # Test division
    assert (Inch(2) / 2).value == 1.0
    assert (Point(144) / 2).value == 72
    assert (Centimeter(5.08) / 2).value == 2.54

    # Test in-place operations with Length tuples
    inch = Inch(1)
    inch += (1.0, "in")
    assert inch.value == 2.0

    point = Point(72)
    point += (72, "pt")
    assert point.value == 144

    cm = Centimeter(2.54)
    cm += (2.54, "cm")
    assert cm.value == 5.08

    inch = Inch(2)
    inch -= (1.0, "in")
    assert inch.value == 1.0

    point = Point(144)
    point -= (72, "pt")
    assert point.value == 72

    cm = Centimeter(5.08)
    cm -= (2.54, "cm")
    assert cm.value == 2.54


def test_conversion_between_units():
    """Test conversion between different units"""
    # Test inch to point
    assert to_point(Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test inch to centimeter
    assert to_centimeter(Inch(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test point to inch
    assert to_inche(Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test point to centimeter
    assert to_centimeter(Point(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test centimeter to inch
    assert to_inche(Centimeter(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0

    # Test centimeter to point
    assert to_point(Centimeter(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_to_public_conversion():
    """Test conversion between internal and public representations"""
    # Test inch conversion
    assert to_length((1.0, "in")) == Inch(1.0)
    assert to_literal_length(Inch(1.0), "in") == (1.0, "in")
    assert to_literal_length(Inch(1.0), "cm") == (2.54, "cm")
    assert to_literal_length(Inch(1.0), "pt") == (72, "pt")

    # Test point conversion
    assert to_length((72, "pt")) == Point(72)
    assert to_literal_length(Point(72), "in") == (1.0, "in")
    assert to_literal_length(Point(72), "cm") == (2.54, "cm")
    assert to_literal_length(Point(72), "pt") == (72, "pt")

    # Test centimeter conversion
    assert to_length((2.54, "cm")) == Centimeter(2.54)
    assert to_literal_length(Centimeter(2.54), "in") == (1.0, "in")
    assert to_literal_length(Centimeter(2.54), "cm") == (2.54, "cm")
    assert to_literal_length(Centimeter(2.54), "pt") == (72, "pt")


def test_invalid_unit():
    """Test handling of invalid units"""
    with pytest.raises(AssertionError):
        to_length((1.0, "invalid"))  # type: ignore

    with pytest.raises(AssertionError):
        to_literal_length(Inch(1.0), "invalid")  # type: ignore
