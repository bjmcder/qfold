"""Entry point for qfold command-line interface."""

import sys

import typer
from rich.console import Console
from textual.app import App

app_cli = typer.Typer(rich_markup_mode="rich")
console = Console()

@app_cli.callback(invoke_without_command=True)
def default_callback(ctx: typer.Context) -> None:
    """Default callback for qfold command."""
    if ctx.invoked_subcommand is None:
        console.print(
            "qfold - Lattice Protein Folding Models", style="bold"
        )


def main() -> None:
    """Main entry point for qfold command."""
    # Check if --app flag is present
    if "--app" in sys.argv:
        # Remove --app from argv to avoid typer parsing it
        sys.argv.remove("--app")

        # Launch Textual app (placeholder for now)
        textual_app = App()
        textual_app.run()
    else:
        # Use typer CLI with Rich formatting
        app_cli()


if __name__ == "__main__":
    main()
