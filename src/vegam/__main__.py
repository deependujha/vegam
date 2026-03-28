# credits: https://github.com/deependujha

import typer
from importlib.metadata import version as importlib_version

from vegam.python.commands import create_python_project

# Main CLI app
vegam_app = typer.Typer(
    help="🚀 Vegam: Opinionated CLI to scaffold production-ready projects"
)


@vegam_app.command()
def version() -> str:
    """Get the current project version."""
    curr_version = importlib_version("vegam")
    typer.echo(f"vegam CLI version: {curr_version}")


# Register commands
vegam_app.command(name="python", help="Initialize a new OpenEnv environment")(
    create_python_project
)
