"""Entry point for qfold command-line interface."""

import sys
from qfold import __version__


def main() -> None:
    """Main entry point for qfold command."""
    print(f"qfold {__version__}")


if __name__ == "__main__":
    main()

