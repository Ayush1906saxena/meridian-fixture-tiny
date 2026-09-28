"""Acceptance tests for the temperature conversion CLI.

Interface the product must provide:
- convert/converter.py exposes `convert(value: float, unit: str) -> tuple[float, str]`.
- convert/__main__.py is the entry point, run as `python -m convert <number> <C|F>`.
- convert/cli.py wires parsing, conversion and printing.
"""

import subprocess
import sys

import pytest

from convert.converter import convert


def run_convert(*args):
    return subprocess.run(
        [sys.executable, "-m", "convert", *args],
        capture_output=True,
        text=True,
    )


class TestConverter:
    def test_celsius_to_fahrenheit(self):
        assert convert(100, "C") == (212.0, "F")

    def test_fahrenheit_to_celsius(self):
        assert convert(32, "F") == (0.0, "C")

    def test_negative_temperature(self):
        assert convert(-40, "C") == (-40.0, "F")
        assert convert(-40, "F") == (-40.0, "C")

    def test_decimal_temperature(self):
        assert convert(37, "C") == (98.6, "F")
        assert convert(98.6, "F") == (37.0, "C")

    def test_unknown_unit_raises(self):
        with pytest.raises(ValueError):
            convert(0, "K")


class TestCLI:
    def test_cli_celsius_to_fahrenheit(self):
        result = run_convert("100", "C")
        assert result.returncode == 0
        assert result.stdout.strip() == "212.0 F"
        assert result.stderr == ""

    def test_cli_fahrenheit_to_celsius(self):
        result = run_convert("32", "F")
        assert result.returncode == 0
        assert result.stdout.strip() == "0.0 C"
        assert result.stderr == ""

    def test_cli_rejects_non_number(self):
        result = run_convert("abc", "C")
        assert result.returncode == 1
        assert result.stderr.strip() == "Error: temperature must be a number"
        assert result.stdout == ""

    def test_cli_rejects_unknown_unit(self):
        result = run_convert("100", "K")
        assert result.returncode == 1
        assert result.stderr.strip() == "Error: unit must be C or F"
        assert result.stdout == ""

    def test_cli_rejects_lowercase_unit(self):
        result = run_convert("100", "c")
        assert result.returncode == 1
        assert "Error:" in result.stderr
        assert result.stdout == ""

    def test_cli_rejects_missing_arguments(self):
        result = run_convert()
        assert result.returncode != 0
        assert result.stderr.strip()
        assert result.stdout == ""

    def test_cli_rejects_too_many_arguments(self):
        result = run_convert("100", "C", "extra")
        assert result.returncode != 0
        assert result.stderr.strip()
        assert result.stdout == ""
