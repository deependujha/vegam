# credits: https://github.com/deependujha
"""C++ project scaffolding commands."""

import typer
from pathlib import Path

cpp_app = typer.Typer(help="🛠️ Create C++ projects and files")


@cpp_app.command()
def create(
    name: str = typer.Argument(..., help="Name of the C++ file/project to create"),
):
    """Create a new C++ file."""
    file_path = Path.cwd() / f"{name}.cpp"

    # Check if file already exists
    if file_path.exists():
        typer.echo(f"❌ File {name}.cpp already exists!", err=True)
        raise typer.Exit(code=1)

    # Create C++ file with basic template
    template = f"""#include <iostream>

int main() {{
    std::cout << "Hello from {name}!" << std::endl;
    return 0;
}}
"""

    file_path.write_text(template)
    typer.echo(f"✅ Created {name}.cpp in {Path.cwd()}")


@cpp_app.command()
def init(name: str = typer.Argument(..., help="Name of the project to initialize")):
    """Initialize a new C++ project structure."""
    project_dir = Path.cwd() / name

    if project_dir.exists():
        typer.echo(f"❌ Directory {name} already exists!", err=True)
        raise typer.Exit(code=1)

    # Create project structure
    project_dir.mkdir()
    (project_dir / "src").mkdir()
    (project_dir / "include").mkdir()
    (project_dir / "build").mkdir()

    # Create main.cpp
    (project_dir / "src" / "main.cpp").write_text(
        f"""#include <iostream>

int main() {{
    std::cout << "Hello from {name}!" << std::endl;
    return 0;
}}
"""
    )

    # Create CMakeLists.txt
    (project_dir / "CMakeLists.txt").write_text(
        f"""cmake_minimum_required(VERSION 3.10)
project({name} CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable({name} src/main.cpp)
target_include_directories({name} PRIVATE include)
"""
    )

    # Create README
    (project_dir / "README.md").write_text(
        f"# {name}\n\nA C++ project created with Vegam CLI\n"
    )

    typer.echo(f"✅ Initialized C++ project {name} in {project_dir}")
