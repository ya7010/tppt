import pytest

from pptxr.units import (
    _Inch,
    _Millimeter,
    _Point,
    _to_internal_length,
    _to_public_length,
    to_inche,
    to_millimeter,
    to_point,
)


def test_to_millimeter():
    """Test conversion to millimeters"""
    # Test from inches
    assert to_millimeter(_Inch(1)).value == 25.4
    assert to_millimeter((1.0, "in")).value == 25.4

    # Test from points
    assert to_millimeter(_Point(72)).value == 25.4
    assert to_millimeter((72, "pt")).value == 25.4

    # Test from millimeters
    assert to_millimeter(_Millimeter(25.4)).value == 25.4
    assert to_millimeter((25.4, "mm")).value == 25.4


def test_to_inche():
    """Test conversion to inches"""
    # Test from inches
    assert to_inche(_Inch(1)).value == 1.0
    assert to_inche((1.0, "in")).value == 1.0

    # Test from points
    assert to_inche(_Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test from millimeters
    assert to_inche(_Millimeter(25.4)).value == 1.0
    assert to_inche((25.4, "mm")).value == 1.0


def test_to_point():
    """Test conversion to points"""
    # Test from inches
    assert to_point(_Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test from points
    assert to_point(_Point(72)).value == 72
    assert to_point((72, "pt")).value == 72

    # Test from millimeters
    assert to_point(_Millimeter(25.4)).value == 72
    assert to_point((25.4, "mm")).value == 72


def test_internal_length_operations():
    """Test operations on internal length representations"""
    # Test addition
    assert (_Inch(1) + _Inch(1)).value == 2.0
    assert (_Point(72) + _Point(72)).value == 144
    assert (_Millimeter(25.4) + _Millimeter(25.4)).value == 50.8

    # Test subtraction
    assert (_Inch(2) - _Inch(1)).value == 1.0
    assert (_Point(144) - _Point(72)).value == 72
    assert (_Millimeter(50.8) - _Millimeter(25.4)).value == 25.4

    # Test multiplication
    assert (_Inch(1) * 2).value == 2.0
    assert (_Point(72) * 2).value == 144
    assert (_Millimeter(25.4) * 2).value == 50.8

    # Test division
    assert (_Inch(2) / 2).value == 1.0
    assert (_Point(144) / 2).value == 72
    assert (_Millimeter(50.8) / 2).value == 25.4


def test_conversion_between_units():
    """Test conversion between different units"""
    # Test inch to point
    assert to_point(_Inch(1)).value == 72
    assert to_point((1.0, "in")).value == 72

    # Test inch to millimeter
    assert to_millimeter(_Inch(1)).value == 25.4
    assert to_millimeter((1.0, "in")).value == 25.4

    # Test point to inch
    assert to_inche(_Point(72)).value == 1.0
    assert to_inche((72, "pt")).value == 1.0

    # Test point to millimeter
    assert to_millimeter(_Point(72)).value == 25.4
    assert to_millimeter((72, "pt")).value == 25.4

    # Test millimeter to inch
    assert to_inche(_Millimeter(25.4)).value == 1.0
    assert to_inche((25.4, "mm")).value == 1.0

    # Test millimeter to point
    assert to_point(_Millimeter(25.4)).value == 72
    assert to_point((25.4, "mm")).value == 72


def test_internal_to_public_conversion():
    """Test conversion between internal and public representations"""
    # Test inch conversion
    assert _to_internal_length((1.0, "in")) == _Inch(1.0)
    assert _to_public_length(_Inch(1.0), "in") == (1.0, "in")
    assert _to_public_length(_Inch(1.0), "mm") == (25.4, "mm")
    assert _to_public_length(_Inch(1.0), "pt") == (72, "pt")

    # Test point conversion
    assert _to_internal_length((72, "pt")) == _Point(72)
    assert _to_public_length(_Point(72), "in") == (1.0, "in")
    assert _to_public_length(_Point(72), "mm") == (25.4, "mm")
    assert _to_public_length(_Point(72), "pt") == (72, "pt")

    # Test millimeter conversion
    assert _to_internal_length((25.4, "mm")) == _Millimeter(25.4)
    assert _to_public_length(_Millimeter(25.4), "in") == (1.0, "in")
    assert _to_public_length(_Millimeter(25.4), "mm") == (25.4, "mm")
    assert _to_public_length(_Millimeter(25.4), "pt") == (72, "pt")


def test_invalid_unit():
    """Test handling of invalid units"""
    with pytest.raises(AssertionError):
        _to_internal_length((1.0, "invalid"))  # type: ignore

    with pytest.raises(AssertionError):
        _to_public_length(_Inch(1.0), "invalid")  # type: ignore
