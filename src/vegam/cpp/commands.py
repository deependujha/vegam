# credits: https://github.com/deependujha

from typing import Annotated

import typer
from rich.console import Console

console = Console()

app = typer.Typer(help="vegam: scaffold C++ projects at speed ⚡")


@app.command("cpp")
def create_cpp_project(
    project_name: Annotated[
        str,
        typer.Argument(help="Project name (snake_case, e.g. my_project)"),
    ],
    cuda: Annotated[
        bool,
        typer.Option("--cuda", help="Enable CUDA support"),
    ] = False,
    python: Annotated[
        bool,
        typer.Option("--python", help="Add Python bindings (nanobind + PyPI setup)"),
    ] = False,
    go: Annotated[
        bool,
        typer.Option("--go", help="Add Go bindings via cgo"),
    ] = False,
    output_dir: Annotated[
        str | None,
        typer.Option("--output-dir", "-o", help="Output directory"),
    ] = None,
) -> None:
    console.print("🚀 [bold green]Scaffolding preview[/bold green]\n")

    console.print(f"[cyan]Project:[/cyan] {project_name}")
    console.print(f"[cyan]CUDA:[/cyan] {cuda}")
    console.print(f"[cyan]Python bindings:[/cyan] {python}")
    console.print(f"[cyan]Go bindings:[/cyan] {go}")
    console.print(f"[cyan]Output dir:[/cyan] {output_dir or 'current directory'}")

    if cuda or python or go:
        console.print(
            "\n❌ [bold red]Scaffolding is not yet implemented for CUDA, Python bindings, or Go bindings[/bold red]"
        )
    console.print("\n⚡ Actual scaffolding coming soon...")
