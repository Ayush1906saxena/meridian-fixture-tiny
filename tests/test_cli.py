"""Unit and edge-case tests for the CLI parser and command."""

import subprocess
import sys

import pytest

from convert.cli import parse_args


def run_convert(*args):
    return subprocess.run(
        [sys.executable, "-m", "convert", *args],
        capture_output=True,
        text=True,
    )


class TestParseArgs:
    def test_valid_input_returns_float_and_unit(self):
        assert parse_args(["100", "C"]) == (100.0, "C")

    def test_decimal_string_becomes_float(self):
        assert parse_args(["36.6", "C"]) == (36.6, "C")

    def test_non_number_raises_friendly_error(self):
        with pytest.raises(ValueError) as excinfo:
            parse_args(["abc", "C"])
        assert "temperature must be a number" in str(excinfo.value)

    def test_unknown_unit_raises_friendly_error(self):
        with pytest.raises(ValueError) as excinfo:
            parse_args(["100", "K"])
        assert "unit must be C or F" in str(excinfo.value)

    def test_wrong_argument_count_raises_usage_error(self):
        for argv in ([], ["100"], ["100", "C", "extra"]):
            with pytest.raises(ValueError) as excinfo:
                parse_args(argv)
            assert "usage" in str(excinfo.value)


class TestCLIEdgeCases:
    def test_cli_accepts_decimal_number(self):
        result = run_convert("36.6", "C")
        assert result.returncode == 0
        value_str, unit = result.stdout.strip().split()
        assert unit == "F"
        assert float(value_str) == pytest.approx(97.88)

    def test_cli_accepts_negative_number(self):
        result = run_convert("-40", "C")
        assert result.returncode == 0
        assert result.stdout.strip() == "-40.0 F"
        assert result.stderr == ""

    def test_cli_single_argument_prints_usage_error(self):
        result = run_convert("100")
        assert result.returncode == 1
        assert "usage" in result.stderr
        assert result.stdout == ""

    def test_cli_empty_value_rejected_as_non_number(self):
        result = run_convert("", "C")
        assert result.returncode == 1
        assert result.stderr.strip() == "Error: temperature must be a number"
        assert result.stdout == ""

    def test_cli_empty_unit_rejected_as_unknown_unit(self):
        result = run_convert("100", "")
        assert result.returncode == 1
        assert result.stderr.strip() == "Error: unit must be C or F"
        assert result.stdout == ""
