# Architecture

A small Python command-line tool that converts temperatures between Celsius and Fahrenheit. The user types a command like `convert 100 C` and the tool prints the converted value, or a clear error if the input is invalid.

**Built with A plain Python command-line script with no web framework, no database, and no external services. The tool only does a simple calculation and prints the result, so the Python standard library is enough.**

- Language: python
- Framework: none
- Storage: none
- Tests: pytest

## Parts

- **CLI parser**: Reads the command-line arguments, validates that there are exactly a number and a unit, and reports friendly errors for bad input. (convert/cli.py)
- **Temperature converter**: Converts a numeric temperature between Celsius and Fahrenheit and returns the result. (convert/converter.py)
- **Entry point**: Wires the parser to the converter and prints the result or error message when the script is run. (convert/__main__.py)

## Data

- **Temperature**: value: decimal number, unit: 'C' or 'F'

## How it's used

- ``convert <number> <C|F>` prints `<result> <target_unit>` (e.g. `convert 100 C` -> `212.0 F`; `convert 32 F` -> `0.0 C`). Unknown unit prints `Error: unit must be C or F` and exits with code 1. Non-number prints `Error: temperature must be a number` and exits with code 1.`: The only way a user interacts with the tool.
- ``convert(value: float, unit: str) -> tuple[float, str]` returns `(converted_value, target_unit)` and raises `ValueError` for unknown units.`: Used by the CLI and by the test suite to check conversions directly.

## Trade-offs

- Use `argparse` from the Python standard library instead of a third-party CLI framework. rather than Click, Typer: The command has only two arguments, so a heavy dependency adds no value and could break.
- Build a command-line tool rather than a library or web service. rather than Reusable Python library, Web API: The customer explicitly asked for a command-line tool.
- Support only Celsius and Fahrenheit. rather than Also support Kelvin and Rankine: The customer only asked for conversions between C and F.

## Risks

- Users may type units in lowercase or full words like 'celsius'; the tool only accepts 'C' or 'F'.
- Very large numbers could produce floating-point rounding differences in output.
- There are no external dependencies to break, but the tool must be run with Python installed.

## Not included

- Web interface or API
- Graphical user interface
- Other temperature units such as Kelvin or Rankine
- Saving conversion history to a file or database
- Packaging or distribution via PyPI

