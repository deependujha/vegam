# credits: https://github.com/deependujha

import typer
from importlib.metadata import version as importlib_version

# Main CLI app
vegam_app = typer.Typer(
    help="🚀 Vegam: Opinionated CLI to scaffold production-ready projects"
)


@vegam_app.command()
def version() -> str:
    """Get the current project version."""
    curr_version = importlib_version("vegam")
    typer.echo(f"vegam CLI version: {curr_version}")


# Import and register commands (must be after vegam_app creation)
from vegam.cli.python_commands import python_app  # noqa: E402
from vegam.cli.cpp_commands import cpp_app  # noqa: E402

# Register language-specific command groups
vegam_app.add_typer(python_app, name="python")
vegam_app.add_typer(cpp_app, name="cpp")
