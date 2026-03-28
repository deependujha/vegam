# credits: https://github.com/deependujha
"""Python project scaffolding commands."""

import typer
from pathlib import Path

python_app = typer.Typer(help="📦 Create Python projects and files")


@python_app.command()
def create(
    name: str = typer.Argument(..., help="Name of the Python file/project to create"),
):
    """Create a new Python file or project."""
    file_path = Path.cwd() / f"{name}.py"

    # Check if file already exists
    if file_path.exists():
        typer.echo(f"❌ File {name}.py already exists!", err=True)
        raise typer.Exit(code=1)

    # Create Python file with basic template
    template = f'''"""
{name} module.

Created by Vegam CLI.
"""


def main():
    """Main entry point."""
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
'''

    file_path.write_text(template)
    typer.echo(f"✅ Created {name}.py in {Path.cwd()}")


@python_app.command()
def init(name: str = typer.Argument(..., help="Name of the project to initialize")):
    """Initialize a new Python project structure."""
    project_dir = Path.cwd() / name

    if project_dir.exists():
        typer.echo(f"❌ Directory {name} already exists!", err=True)
        raise typer.Exit(code=1)

    # Create project structure
    project_dir.mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "src" / name).mkdir()
    (project_dir / "tests").mkdir()

    # Create __init__.py files
    (project_dir / "src" / name / "__init__.py").write_text('"""Python package."""\n')
    (project_dir / "tests" / "__init__.py").write_text("")

    # Create main module
    (project_dir / "src" / name / "main.py").write_text(
        f'''"""
Main module for {name}.

Created by Vegam CLI.
"""


def main():
    """Main entry point."""
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
'''
    )

    # Create README
    (project_dir / "README.md").write_text(f"# {name}\n\nCreated with Vegam CLI\n")

    # Create pyproject.toml
    (project_dir / "pyproject.toml").write_text(
        f"""[project]
name = "{name}"
version = "0.1.0"
description = "A Python project"
authors = [
    {{ name = "Your Name", email = "you@example.com" }}
]
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["uv_build>=0.10.8,<0.11.0"]
build-backend = "uv_build"
"""
    )

    typer.echo(f"✅ Initialized Python project {name} in {project_dir}")
