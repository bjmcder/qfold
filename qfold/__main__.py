"""Entry point for qfold command-line interface."""
import typer
import rich

from rich.console import Console

def main() -> None:
    """Main entry point for qfold command."""

    rich.print("Hello, World!")


if __name__ == "__main__":
    typer.run(main)

