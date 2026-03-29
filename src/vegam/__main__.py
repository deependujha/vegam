# credits: https://github.com/deependujha

from importlib.metadata import version as importlib_version

import typer

from vegam.cpp.commands import create_cpp_project
from vegam.python.commands import create_python_project

# Main CLI app
vegam_app = typer.Typer(
    help="🚀 Vegam: Opinionated CLI to scaffold production-ready, opinionated, multi-language projects "
    "(Python/C++/CUDA)"
)


@vegam_app.command()
def version() -> None:
    """Get the current project version."""
    curr_version = importlib_version("vegam")
    typer.echo(f"vegam CLI version: {curr_version}")


# Register commands
vegam_app.command(
    name="python",
    help="scaffold Python projects at speed ⚡",
)(create_python_project)

vegam_app.command(
    name="cpp",
    help="scaffold C++/CUDA & multi-language projects at speed ⚡",
)(create_cpp_project)
