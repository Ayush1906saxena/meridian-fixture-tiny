"""Entry point: ``python -m convert <number> <C|F>``."""

import sys

from convert.cli import main

if __name__ == "__main__":
    sys.exit(main())
