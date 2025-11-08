"""CLI command definitions for qfold."""

from typing import Optional

import typer

from qfold.app.display import display_sequence
from qfold.io import process_sequence


def create_cli_app() -> typer.Typer:
    """
    Create and configure the Typer CLI application.

    Returns:
        Configured Typer application instance.
    """
    app_cli = typer.Typer(rich_markup_mode="rich")

    @app_cli.callback(invoke_without_command=True)
    def default_callback(
        ctx: typer.Context,
        sequence: Optional[str] = typer.Option(
            None,
            "--sequence",
            "-s",
            help="Protein sequence to process",
        ),
        alphabet: str = typer.Option(
            "auto",
            "--alphabet",
            "-a",
            help="Protein sequence alphabet (hp, auto)",
        ),
    ) -> None:
        """Default callback for qfold command."""
        if ctx.invoked_subcommand is None:
            if sequence is None:
                from rich.console import Console

                console = Console()
                console.print(
                    "qfold - Lattice Protein Folding Models", style="bold"
                )
                console.print("\nUse --sequence or -s to provide a sequence.")
            else:
                try:
                    seq_obj = process_sequence(sequence, alphabet)
                    display_sequence(seq_obj)
                except ValueError as e:
                    from rich.console import Console

                    console = Console()
                    console.print(f"Error: {e}", style="bold red")
                    raise typer.Exit(1) from None

    return app_cli

