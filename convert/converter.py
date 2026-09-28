"""Temperature conversion between Celsius and Fahrenheit."""


def convert(value: float, unit: str) -> tuple:
    """Convert a temperature to the other unit.

    Returns ``(converted_value, target_unit)``. Raises ``ValueError`` for
    any unit other than ``"C"`` or ``"F"``.
    """
    if unit == "C":
        return (float(value) * 9 / 5 + 32, "F")
    if unit == "F":
        return ((float(value) - 32) * 5 / 9, "C")
    raise ValueError("unit must be C or F")
