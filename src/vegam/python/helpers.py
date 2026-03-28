# credits: https://github.com/deependujha

import subprocess


def add_mypy_config(original_content: str) -> str:
    if "[tool.mypy]" in original_content:
        return original_content

    return (
        original_content
        + r"""

[tool.mypy]
files = [ "src" ]
exclude = [ ]
install_types = true
non_interactive = true
disallow_untyped_defs = true
ignore_missing_imports = true
show_error_codes = true
warn_redundant_casts = true
warn_unused_configs = true
warn_unused_ignores = true
allow_redefinition = true
disable_error_code = "attr-defined"
warn_no_return = false

[[tool.mypy.overrides]]
# generate with:
# mypy --no-error-summary 2>&1 | tr ':' ' ' | awk '{print $1}' | sort | uniq | sed 's/\.py//g; s|src/||g; s|\/|\.|g'
module = [ ]
ignore_errors = true
"""
    )


def add_pytest_config(original_content: str) -> str:
    if "[tool.pytest.ini_options]" in original_content:
        return original_content

    return (
        original_content
        + r"""

[tool.pytest.ini_options]
testpaths = [ "tests" ]
norecursedirs = [ ".git", ".github", "dist", "build", "docs" ]
addopts = [
  "--strict-markers",
  "--doctest-modules",
  "--color=yes",
  "--disable-pytest-warnings",
]
markers = [ "cloud: Run the cloud tests for example" ]
filterwarnings = [ "error::FutureWarning" ]
xfail_strict = true
junit_duration_report = "call"
"""
    )


def initial_readme_content(project_name: str) -> str:
    return f"""# {project_name}"""


def get_git_username() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Your Name"
