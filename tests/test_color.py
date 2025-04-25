"""Tests for tppt.types._color module."""

import unittest

from tppt.exception import ColorInvalidFormatError
from tppt.types._color import Color


class TestColor(unittest.TestCase):
    """Test cases for Color class."""

    def test_init_with_rgb_hex_short(self):
        """Test initialization with short hex color code (#RGB)."""
        color = Color("#123")
        assert color.r == 0x11
        assert color.g == 0x22
        assert color.b == 0x33

    def test_init_with_rgb_hex_long(self):
        """Test initialization with long hex color code (#RRGGBB)."""
        color = Color("#123456")
        assert color.r == 0x12
        assert color.g == 0x34
        assert color.b == 0x56

    def test_init_with_rgb_tuple(self):
        """Test initialization with RGB tuple."""
        color = Color(10, 20, 30)
        assert color.r == 10
        assert color.g == 20
        assert color.b == 30

    def test_invalid_format_no_hash(self):
        """Test initialization with invalid format (no # prefix)."""
        with self.assertRaises(ColorInvalidFormatError):
            Color("123456")

    def test_invalid_format_wrong_length(self):
        """Test initialization with invalid format (wrong length)."""
        with self.assertRaises(ColorInvalidFormatError):
            Color("#12345")  # 6 characters (including #) is invalid

    def test_repr(self):
        """Test string representation."""
        color = Color(10, 20, 30)
        assert repr(color) == "Color(10, 20, 30)"
