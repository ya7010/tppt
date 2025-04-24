import pytest

from pptxr.units import (
    _Centimeter,
    _Inch,
    _Point,
    _to_internal_length,
    _to_public_length,
    to_centimeter,
    to_inche,
    to_point,
)


def test_to_centimeter():
    """Test conversion to centimeters"""
    # Test from inches
    assert to_centimeter(_Inch(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test from points
    assert to_centimeter(_Point(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test from centimeters
    assert to_centimeter(_Centimeter(2.54)).value == 2.54
    assert to_centimeter((2.54, "cm")).value == 2.54


def test_to_inche():
    """Test conversion to inches"""
    # Test from inches
    assert to_inche(_Inch(1)).value == 1.0
    assert to_inche((1.0, "in")).value == 1.0

    # Test from points
    assert to_inche(_Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test from centimeters
    assert to_inche(_Centimeter(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0


def test_to_point():
    """Test conversion to points"""
    # Test from inches
    assert to_point(_Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test from points
    assert to_point(_Point(72)).value == 72
    assert to_point((72, "pt")).value == 72

    # Test from centimeters
    assert to_point(_Centimeter(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_length_operations():
    """Test operations on internal length representations"""
    # Test addition
    assert (_Inch(1) + _Inch(1)).value == 2.0
    assert (_Point(72) + _Point(72)).value == 144
    assert (_Centimeter(2.54) + _Centimeter(2.54)).value == 5.08

    # Test addition with Length tuples
    assert (_Inch(1) + (1.0, "in")).value == 2.0
    assert (_Point(72) + (72, "pt")).value == 144
    assert (_Centimeter(2.54) + (2.54, "cm")).value == 5.08

    # Test subtraction
    assert (_Inch(2) - _Inch(1)).value == 1.0
    assert (_Point(144) - _Point(72)).value == 72
    assert (_Centimeter(5.08) - _Centimeter(2.54)).value == 2.54

    # Test subtraction with Length tuples
    assert (_Inch(2) - (1.0, "in")).value == 1.0
    assert (_Point(144) - (72, "pt")).value == 72
    assert (_Centimeter(5.08) - (2.54, "cm")).value == 2.54

    # Test multiplication
    assert (_Inch(1) * 2).value == 2.0
    assert (_Point(72) * 2).value == 144
    assert (_Centimeter(2.54) * 2).value == 5.08

    # Test division
    assert (_Inch(2) / 2).value == 1.0
    assert (_Point(144) / 2).value == 72
    assert (_Centimeter(5.08) / 2).value == 2.54

    # Test in-place operations with Length tuples
    inch = _Inch(1)
    inch += (1.0, "in")
    assert inch.value == 2.0

    point = _Point(72)
    point += (72, "pt")
    assert point.value == 144

    cm = _Centimeter(2.54)
    cm += (2.54, "cm")
    assert cm.value == 5.08

    inch = _Inch(2)
    inch -= (1.0, "in")
    assert inch.value == 1.0

    point = _Point(144)
    point -= (72, "pt")
    assert point.value == 72

    cm = _Centimeter(5.08)
    cm -= (2.54, "cm")
    assert cm.value == 2.54


def test_conversion_between_units():
    """Test conversion between different units"""
    # Test inch to point
    assert to_point(_Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test inch to centimeter
    assert to_centimeter(_Inch(1)).value == 2.54
    assert to_centimeter((1.0, "in")).value == 2.54

    # Test point to inch
    assert to_inche(_Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test point to centimeter
    assert to_centimeter(_Point(72)).value == 2.54
    assert to_centimeter((72, "pt")).value == 2.54

    # Test centimeter to inch
    assert to_inche(_Centimeter(2.54)).value == 1.0
    assert to_inche((2.54, "cm")).value == 1.0

    # Test centimeter to point
    assert to_point(_Centimeter(2.54)).value == 72
    assert to_point((2.54, "cm")).value == 72


def test_internal_to_public_conversion():
    """Test conversion between internal and public representations"""
    # Test inch conversion
    assert _to_internal_length((1.0, "in")) == _Inch(1.0)
    assert _to_public_length(_Inch(1.0), "in") == (1.0, "in")
    assert _to_public_length(_Inch(1.0), "cm") == (2.54, "cm")
    assert _to_public_length(_Inch(1.0), "pt") == (72, "pt")

    # Test point conversion
    assert _to_internal_length((72, "pt")) == _Point(72)
    assert _to_public_length(_Point(72), "in") == (1.0, "in")
    assert _to_public_length(_Point(72), "cm") == (2.54, "cm")
    assert _to_public_length(_Point(72), "pt") == (72, "pt")

    # Test centimeter conversion
    assert _to_internal_length((2.54, "cm")) == _Centimeter(2.54)
    assert _to_public_length(_Centimeter(2.54), "in") == (1.0, "in")
    assert _to_public_length(_Centimeter(2.54), "cm") == (2.54, "cm")
    assert _to_public_length(_Centimeter(2.54), "pt") == (72, "pt")


def test_invalid_unit():
    """Test handling of invalid units"""
    with pytest.raises(AssertionError):
        _to_internal_length((1.0, "invalid"))  # type: ignore

    with pytest.raises(AssertionError):
        _to_public_length(_Inch(1.0), "invalid")  # type: ignore
