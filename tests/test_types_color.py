"""Tests for tppt.types._color module."""

import unittest

from tppt.exception import ColorInvalidFormatError
from tppt.types._color import RGBColor, to_rgb_color


class TestColor(unittest.TestCase):
    """Test cases for Color class."""

    def test_init_with_rgb_hex_short(self):
        """Test initialization with short hex color code (#RGB)."""
        color = to_rgb_color("#123")
        r, g, b = color
        assert r == 0x11
        assert g == 0x22
        assert b == 0x33

    def test_init_with_rgb_hex_long(self):
        """Test initialization with long hex color code (#RRGGBB)."""
        color = to_rgb_color("#123456")
        r, g, b = color
        assert r == 0x12
        assert g == 0x34
        assert b == 0x56

    def test_init_with_rgb_tuple(self):
        """Test initialization with RGB tuple."""
        color = RGBColor(10, 20, 30)
        r, g, b = color
        assert r == 10
        assert g == 20
        assert b == 30

    def test_invalid_format_no_hash(self):
        """Test initialization with invalid format (no # prefix)."""
        with self.assertRaises(ColorInvalidFormatError):
            to_rgb_color("123456")

    def test_invalid_format_wrong_length(self):
        """Test initialization with invalid format (wrong length)."""
        with self.assertRaises(ColorInvalidFormatError):
            to_rgb_color("#12345")  # 6 characters (including #) is invalid


class TestToColor(unittest.TestCase):
    """Test cases for to_color function."""

    def test_to_color_with_tuple(self):
        """Test to_color with a RGB tuple."""
        result = to_rgb_color((10, 20, 30))
        assert isinstance(result, RGBColor)
        r, g, b = result
        assert r == 10
        assert g == 20
        assert b == 30

    def test_to_color_with_str(self):
        """Test to_color with a hex string."""
        result = to_rgb_color("#123456")
        assert isinstance(result, RGBColor)
        r, g, b = result
        assert r == 0x12
        assert g == 0x34
        assert b == 0x56

    def test_to_color_with_short_hex(self):
        """Test to_color with a short hex string."""
        result = to_rgb_color("#123")
        assert isinstance(result, RGBColor)
        r, g, b = result
        assert r == 0x11
        assert g == 0x22
        assert b == 0x33
