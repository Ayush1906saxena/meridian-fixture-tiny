"""Edge-case tests for the temperature converter."""

import pytest

from convert.converter import convert


class TestConvertBoundaries:
    def test_zero_celsius_to_fahrenheit(self):
        assert convert(0, "C") == (32.0, "F")

    def test_zero_fahrenheit_to_celsius(self):
        value, unit = convert(0, "F")
        assert value == pytest.approx(-160 / 9)
        assert unit == "C"


class TestConvertRejectsBadUnits:
    def test_lowercase_units_rejected(self):
        with pytest.raises(ValueError):
            convert(100, "c")
        with pytest.raises(ValueError):
            convert(100, "f")

    def test_full_word_units_rejected(self):
        with pytest.raises(ValueError):
            convert(100, "celsius")
        with pytest.raises(ValueError):
            convert(100, "fahrenheit")

    def test_empty_unit_rejected(self):
        with pytest.raises(ValueError):
            convert(100, "")
