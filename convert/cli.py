"""Command-line parsing and output for the temperature converter."""

import sys

from convert.converter import convert


def parse_args(argv):
    """Parse ``argv`` into ``(value, unit)``.

    Raises ``ValueError`` with a friendly message for bad input.
    """
    if len(argv) != 2:
        raise ValueError("usage: convert <number> <C|F>")

    raw_value, unit = argv

    try:
        value = float(raw_value)
    except ValueError:
        raise ValueError("temperature must be a number")

    if unit not in ("C", "F"):
        raise ValueError("unit must be C or F")

    return value, unit


def main(argv=None):
    """Run the CLI, printing the result or an error and returning an exit code."""
    if argv is None:
        argv = sys.argv[1:]

    try:
        value, unit = parse_args(argv)
        result, target_unit = convert(value, unit)
    except ValueError as exc:
        print("Error: {}".format(exc), file=sys.stderr)
        return 1

    print("{} {}".format(result, target_unit))
    return 0
