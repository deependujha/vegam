# credits: https://github.com/deependujha
# credits: https://github.com/meta-pytorch/OpenEnv/blob/main/src/openenv/cli/commands/init.py
from pathlib import Path
from typing import Dict, List, Tuple
from importlib import resources


def _replace_in_content(content: str, replacements: Dict[str, str]) -> str:
    """Replace all occurrences in content using case-sensitive replacements."""
    result = content
    # Sort by length (longest first) to avoid partial replacements
    for old, new in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(old, new)
    return result


def _should_rename_file(
    filename: str, replacements: Dict[str, str]
) -> Tuple[bool, str]:
    """
    Check if a file should be renamed and return the new name.

    Handles template placeholders in filenames like:
    - if replacements has "__PATTERN__": "my_project", then:
    - `__PATTERN___environment.py` → `my_project_environment.py`
    """
    # Check for template placeholder
    for old, new in replacements.items():
        if old in filename:
            new_filename = filename.replace(old, new)
            return True, new_filename

    return False, filename


def _copy_and_template_file(
    src_path: Path,
    dest_path: Path,
    replacements: Dict[str, str],
) -> None:
    """Copy a file and apply template replacements."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Read source file
        content = src_path.read_bytes()

        # Try to decode as text and apply replacements
        try:
            text = content.decode("utf-8")
            # Normalize line endings to LF before applying replacements
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            text = _replace_in_content(text, replacements)
            dest_path.write_text(text, encoding="utf-8", newline="\n")
        except UnicodeDecodeError:
            # Binary file, just copy
            dest_path.write_bytes(content)
    except Exception as e:
        raise RuntimeError(
            f"Failed to copy template file {src_path} to {dest_path}: {e}"
        ) from e


def _copy_template_directory(
    template_pkg: str,
    template_dir: str,
    dest_dir: Path,
    replacements: Dict[str, str],
) -> List[Path]:
    """Recursively copy template directory and apply replacements."""
    created_files: List[Path] = []

    # Get the package path using importlib.resources but avoid importing the template package
    # We'll use the package's __file__ to get the directory path
    import importlib

    try:
        # Import the parent package (not the template package itself)
        if "." in template_pkg:
            parent_pkg = ".".join(template_pkg.split(".")[:-1])
            pkg = importlib.import_module(parent_pkg)
            template_path = Path(pkg.__file__).parent / template_pkg.split(".")[-1]
        else:
            pkg = importlib.import_module(template_pkg.split(".")[0])
            template_path = Path(pkg.__file__).parent / template_pkg.split(".")[-1]
    except Exception:
        # Fallback: try to use resources.files but handle import errors
        try:
            base = resources.files(template_pkg.split(".")[0])
            template_path = base.joinpath(*template_pkg.split(".")[1:])
            if not template_path.exists():
                raise FileNotFoundError(f"Template directory not found: {template_pkg}")
        except Exception as e:
            raise FileNotFoundError(
                f"Template directory not found: {template_pkg}"
            ) from e

    if template_dir:
        template_path = template_path / template_dir

    if not template_path.exists() or not template_path.is_dir():
        raise FileNotFoundError(
            f"Template directory not found: {template_pkg}.{template_dir}"
        )

    # Walk through all files in template directory using Path
    for item in template_path.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(template_path)
            dest_path = dest_dir / rel_path

            # Apply filename templating
            should_rename, new_name = _should_rename_file(dest_path.name, replacements)
            if should_rename:
                dest_path = dest_path.parent / new_name

            # Copy and apply replacements
            _copy_and_template_file(item, dest_path, replacements)
            created_files.append(dest_path)

    return created_files
