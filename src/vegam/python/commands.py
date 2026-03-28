# credits: https://github.com/deependujha

import typer
import subprocess
from pathlib import Path
from vegam.utils import _copy_template_directory
from typing import Annotated
from rich.console import Console
from rich.panel import Panel
from rich.progress import SpinnerColumn, TextColumn, Progress
from vegam.python.helpers import (
    add_pytest_config,
    add_mypy_config,
    initial_readme_content,
    get_git_username,
)

console = Console()

app = typer.Typer(help="vegam: scaffold Python projects at speed ⚡")


@app.command()
def create_python_project(
    project_name: Annotated[
        str,
        typer.Argument(help="Project name (snake_case, e.g. my_project)"),
    ],
    output_dir: Annotated[
        str | None,
        typer.Option("--output-dir", "-o", help="Output directory"),
    ] = None,
) -> None:
    base_dir = Path(output_dir).resolve() if output_dir else Path.cwd().resolve()
    project_path = base_dir / project_name

    console.print(
        Panel.fit(
            f"[bold cyan]vegam[/bold cyan] → creating python project [bold]{project_name}[/bold]\n"
            f"[dim]{project_path}[/dim]",
            border_style="cyan",
        )
    )

    # -----------------------------
    # Step 1: uv init
    # -----------------------------
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description="Initializing project with uv...", total=None)

        subprocess.run(
            ["uv", "init", "--package", project_name],
            cwd=base_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

    # -----------------------------
    # Step 2: apply templates
    # -----------------------------
    template_pkg = "vegam.templates.python_project"
    replacements = {
        "__GIT_USERNAME__": get_git_username(),
        "__PROJECT_NAME__": project_name,
    }
    created_files = _copy_template_directory(
        template_pkg,
        "",
        project_path,
        replacements,
    )

    console.print(f"[green]✓[/green] Created {len(created_files)} files")

    # -----------------------------
    # Step 3: add dependencies
    # -----------------------------
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task(description="Installing dev dependencies...", total=None)

        for dep in ["pytest", "mypy", "pre-commit", "pytest-cov", "ruff"]:
            subprocess.run(
                ["uv", "add", "--dev", dep],
                cwd=project_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,  # we want to see if any dependency fails to install
                check=True,
            )

    console.print("[green]✓[/green] Added dev dependencies (pytest, mypy, pre-commit)")

    # -----------------------------
    # Step 4: update pyproject & README.md
    # -----------------------------
    pyproject_path = project_path / "pyproject.toml"
    content = pyproject_path.read_text()

    content = add_pytest_config(content)
    content = add_mypy_config(content)

    pyproject_path.write_text(content)

    readme_path = project_path / "README.md"
    readme_content = initial_readme_content(project_name)
    readme_path.write_text(readme_content)

    console.print("[green]✓[/green] configured pytest and mypy, and created README.md")

    # -----------------------------
    # Step 5: git init & pre-commit install
    # -----------------------------
    subprocess.run(
        ["git", "init"],
        cwd=project_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # make scripts executable
    for script in (project_path / "scripts").glob("*"):
        subprocess.run(
            ["chmod", "+x", str(script)],
            cwd=project_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    subprocess.run(
        ["uv", "run", "pre-commit", "install"],
        cwd=project_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # run pre-commit 3 times, so hooks are installed and any fixes are applied to the codebase. This ensures a clean initial commit.
    for pre_commit_run in range(3):
        subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        result = subprocess.run(
            ["git", "commit", "-m", "chore: initial commit by vegam CLI"],
            cwd=project_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode == 0:
            break
        elif pre_commit_run == 2:
            console.print(
                "[red]❌ Pre-commit errors still exist after 3 attempts. Please fix them manually or open an issue on GitHub.[/red]"
            )

    console.print(
        "[green]✓[/green] Initialized git repository & installed pre-commit hooks"
    )

    # -----------------------------
    # Final output
    # -----------------------------
    console.print(
        Panel.fit(
            f"[bold green]Project ready![/bold green]\n\n"
            f"[bold]Next steps:[/bold]\n"
            f"  cd {project_name}\n"
            f"  uv run pytest\n",
            border_style="green",
        )
    )
