import pytest

from tppt.types._length import (
    Centimeters,
    Inchs,
    Points,
    to_centimeter,
    to_inche,
    to_length,
    to_literal_length,
    to_point,
)


def test_to_centimeter():
    """Test conversion to centimeters"""
    # Test from inches
    assert to_centimeter(Inchs(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test from points
    assert to_centimeter(Points(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test from centimeters
    assert to_centimeter(Centimeters(2.54)).value == 2.54
    assert to_centimeter((2.54, "cm")).value == 2.54


def test_to_inche():
    """Test conversion to inches"""
    # Test from inches
    assert to_inche(Inchs(1)).value == 1.0
    assert to_inche((1.0, "in")).value == 1.0

    # Test from points
    assert to_inche(Points(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test from centimeters
    assert to_inche(Centimeters(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0


def test_to_point():
    """Test conversion to points"""
    # Test from inches
    assert to_point(Inchs(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test from points
    assert to_point(Points(72)).value == 72
    assert to_point((72, "pt")).value == 72

    # Test from centimeters
    assert to_point(Centimeters(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_length_operations():
    """Test operations on internal length representations"""
    # Test addition
    assert (Inchs(1) + Inchs(1)).value == 2.0
    assert (Points(72) + Points(72)).value == 144
    assert (Centimeters(2.54) + Centimeters(2.54)).value == 5.08

    # Test addition with Length tuples
    assert (Inchs(1) + (1.0, "in")).value == 2.0
    assert (Points(72) + (72, "pt")).value == 144
    assert (Centimeters(2.54) + (2.54, "cm")).value == 5.08

    # Test subtraction
    assert (Inchs(2) - Inchs(1)).value == 1.0
    assert (Points(144) - Points(72)).value == 72
    assert (Centimeters(5.08) - Centimeters(2.54)).value == 2.54

    # Test subtraction with Length tuples
    assert (Inchs(2) - (1.0, "in")).value == 1.0
    assert (Points(144) - (72, "pt")).value == 72
    assert (Centimeters(5.08) - (2.54, "cm")).value == 2.54

    # Test multiplication
    assert (Inchs(1) * 2).value == 2.0
    assert (Points(72) * 2).value == 144
    assert (Centimeters(2.54) * 2).value == 5.08

    # Test division
    assert (Inchs(2) / 2).value == 1.0
    assert (Points(144) / 2).value == 72
    assert (Centimeters(5.08) / 2).value == 2.54

    # Test in-place operations with Length tuples
    inch = Inchs(1)
    inch += (1.0, "in")
    assert inch.value == 2.0

    point = Points(72)
    point += (72, "pt")
    assert point.value == 144

    cm = Centimeters(2.54)
    cm += (2.54, "cm")
    assert cm.value == 5.08

    inch = Inchs(2)
    inch -= (1.0, "in")
    assert inch.value == 1.0

    point = Points(144)
    point -= (72, "pt")
    assert point.value == 72

    cm = Centimeters(5.08)
    cm -= (2.54, "cm")
    assert cm.value == 2.54


def test_conversion_between_units():
    """Test conversion between different units"""
    # Test inch to point
    assert to_point(Inchs(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test inch to centimeter
    assert to_centimeter(Inchs(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test point to inch
    assert to_inche(Points(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test point to centimeter
    assert to_centimeter(Points(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test centimeter to inch
    assert to_inche(Centimeters(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0

    # Test centimeter to point
    assert to_point(Centimeters(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_to_public_conversion():
    """Test conversion between internal and public representations"""
    # Test inch conversion
    assert to_length((1.0, "in")) == Inchs(1.0)
    assert to_literal_length(Inchs(1.0), "in") == (1.0, "in")
    assert to_literal_length(Inchs(1.0), "cm") == (2.54, "cm")
    assert to_literal_length(Inchs(1.0), "pt") == (72, "pt")

    # Test point conversion
    assert to_length((72, "pt")) == Points(72)
    assert to_literal_length(Points(72), "in") == (1.0, "in")
    assert to_literal_length(Points(72), "cm") == (2.54, "cm")
    assert to_literal_length(Points(72), "pt") == (72, "pt")

    # Test centimeter conversion
    assert to_length((2.54, "cm")) == Centimeters(2.54)
    assert to_literal_length(Centimeters(2.54), "in") == (1.0, "in")
    assert to_literal_length(Centimeters(2.54), "cm") == (2.54, "cm")
    assert to_literal_length(Centimeters(2.54), "pt") == (72, "pt")


def test_invalid_unit():
    """Test handling of invalid units"""
    with pytest.raises(AssertionError):
        to_length((1.0, "invalid"))  # type: ignore

    with pytest.raises(AssertionError):
        to_literal_length(Inchs(1.0), "invalid")  # type: ignore
