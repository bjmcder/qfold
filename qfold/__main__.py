"""Entry point for qfold command-line interface."""

import sys

from qfold.app.cli import app_cli
from qfold.app.textual import launch_textual_app


def main() -> None:
    """Main entry point for qfold command."""
    # Check if --app flag is present
    if "--app" in sys.argv:
        # Remove --app from argv to avoid typer parsing it
        sys.argv.remove("--app")
        # Launch Textual app
        launch_textual_app()
    else:
        # Use typer CLI with Rich formatting
        app_cli()


if __name__ == "__main__":
    main()
