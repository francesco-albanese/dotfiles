#!/usr/bin/env python3
"""Bootstrap a new Python project with uv, ruff, pyright, prek, pytest."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

PROJECT_TYPES = ("library", "lambda", "fastapi", "cli")
PLACEHOLDERS = {"{{PROJECT_NAME}}": "", "{{PACKAGE_NAME}}": ""}


def to_snake_case(name: str) -> str:
    """Convert project name to valid Python package name."""
    return re.sub(r"[^a-z0-9]", "_", name.lower()).strip("_")


def substitute(content: str, project_name: str, package_name: str) -> str:
    """Replace placeholders in template content."""
    return content.replace("{{PROJECT_NAME}}", project_name).replace(
        "{{PACKAGE_NAME}}", package_name
    )


def create_dirs(output_dir: Path, package_name: str) -> None:
    """Create project directory structure."""
    for d in [
        output_dir / "src" / package_name,
        output_dir / "tests",
    ]:
        d.mkdir(parents=True, exist_ok=True)


def copy_asset(asset_dir: Path, output_dir: Path, filename: str, project_name: str, package_name: str, dest_name: str | None = None) -> None:
    """Copy an asset file with placeholder substitution."""
    src = asset_dir / filename
    if not src.exists():
        return
    content = src.read_text()
    content = substitute(content, project_name, package_name)
    dst = output_dir / (dest_name or filename)
    dst.write_text(content)


def copy_asset_binary(asset_dir: Path, output_dir: Path, filename: str, dest_name: str | None = None) -> None:
    """Copy an asset file without substitution."""
    src = asset_dir / filename
    if not src.exists():
        return
    shutil.copy2(src, output_dir / (dest_name or filename))


def create_init_py(output_dir: Path, package_name: str) -> None:
    """Create __init__.py in the package directory."""
    init = output_dir / "src" / package_name / "__init__.py"
    init.write_text("")


def create_placeholder_test(output_dir: Path, package_name: str) -> None:
    """Create a placeholder test file."""
    test_file = output_dir / "tests" / "test_placeholder.py"
    test_file.write_text(f'def test_import():\n    import {package_name}  # noqa: F401\n')


def create_library_sources(output_dir: Path, package_name: str) -> None:
    """Create source files for library type."""
    pass  # __init__.py is enough


def create_lambda_sources(output_dir: Path, package_name: str) -> None:
    """Create source files for lambda type."""
    handler = output_dir / "src" / package_name / "handler.py"
    handler.write_text(
        '''from typing import Any


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Lambda handler."""
    return {
        "statusCode": 200,
        "body": "ok",
    }
'''
    )


def create_fastapi_sources(output_dir: Path, package_name: str) -> None:
    """Create source files for fastapi type."""
    pkg = output_dir / "src" / package_name

    # main.py
    (pkg / "main.py").write_text(
        '''from fastapi import FastAPI

from .settings import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
'''
    )

    # settings.py
    (pkg / "settings.py").write_text(
        '''from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", case_sensitive=False)

    app_name: str = "{{APP_NAME}}"
    debug: bool = False


settings = Settings()
'''.replace("{{APP_NAME}}", package_name)
    )

    # routers/
    routers = pkg / "routers"
    routers.mkdir(exist_ok=True)
    (routers / "__init__.py").write_text("")


def create_cli_sources(output_dir: Path, package_name: str) -> None:
    """Create source files for cli type."""
    pkg = output_dir / "src" / package_name

    # main.py
    (pkg / "main.py").write_text(
        '''import typer

app = typer.Typer()


@app.command()
def hello(name: str = "world") -> None:
    """Say hello."""
    typer.echo(f"Hello {name}!")


if __name__ == "__main__":
    app()
'''
    )

    # __main__.py
    (pkg / "__main__.py").write_text(
        '''from .main import app

app()
'''
    )


SOURCE_CREATORS = {
    "library": create_library_sources,
    "lambda": create_lambda_sources,
    "fastapi": create_fastapi_sources,
    "cli": create_cli_sources,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap a Python project")
    parser.add_argument("--project-name", required=True, help="Project name (e.g., my-api)")
    parser.add_argument(
        "--type",
        default="library",
        choices=PROJECT_TYPES,
        dest="project_type",
        help="Project type (default: library)",
    )
    parser.add_argument("--output-dir", default=".", help="Output directory (default: cwd)")

    args = parser.parse_args()

    project_name = args.project_name
    project_type = args.project_type
    package_name = to_snake_case(project_name)
    output_dir = Path(args.output_dir).resolve() / project_name
    script_dir = Path(__file__).parent
    asset_dir = script_dir.parent / "assets"

    print(f"Bootstrapping Python {project_type} project: {project_name}")
    print(f"  Package name: {package_name}")
    print(f"  Output: {output_dir}")

    # Create directories
    create_dirs(output_dir, package_name)

    # Copy common assets with substitution
    copy_asset(asset_dir, output_dir, f"pyproject.toml.{project_type}", project_name, package_name, "pyproject.toml")
    copy_asset(asset_dir, output_dir, "Makefile", project_name, package_name)
    copy_asset(asset_dir, output_dir, "CLAUDE.md", project_name, package_name)

    # Copy Dockerfile (library and cli share Dockerfile.library)
    dockerfile_type = project_type if project_type in ("lambda", "fastapi") else "library"
    dockerfile_src = f"Dockerfile.{dockerfile_type}"
    copy_asset(asset_dir, output_dir, dockerfile_src, project_name, package_name, "Dockerfile")

    # Copy common assets without substitution
    for f in (".python-version", "prek.toml", ".gitignore"):
        copy_asset_binary(asset_dir, output_dir, f)

    # Copy conftest.py to tests/
    src_conftest = asset_dir / "conftest.py"
    if src_conftest.exists():
        shutil.copy2(src_conftest, output_dir / "tests" / "conftest.py")

    # Create __init__.py
    create_init_py(output_dir, package_name)

    # Create type-specific source files
    SOURCE_CREATORS[project_type](output_dir, package_name)

    # Create placeholder test
    create_placeholder_test(output_dir, package_name)

    print(f"\nProject bootstrapped: {output_dir}")
    print("\nNext steps:")
    print(f"  cd {output_dir}")
    print("  git init && uv venv --python 3.13 && uv sync --dev")
    print("  make ci")


if __name__ == "__main__":
    main()
