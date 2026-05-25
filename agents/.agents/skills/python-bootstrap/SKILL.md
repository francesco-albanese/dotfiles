---
name: python-bootstrap
description: Bootstrap Python projects with uv, ruff, pyright, prek, and pytest. Supports library, lambda, fastapi, and cli project types. Use when bootstrapping, initializing, or scaffolding a new Python project or creating a Python lambda, FastAPI service, CLI app, or library.
argument-hint: "[project-name] [type]"
allowed-tools: Bash, Write, Read, AskUserQuestion
---

# Python Bootstrap

Bootstrap Python 3.13 projects with uv, ruff, pyright, prek, pytest.

## Quick Start

When user requests Python project initialization:

1. **Ask project type** via `AskUserQuestion`:
   - library (default) — `src/<package>/` layout
   - lambda — AWS Lambda with handler boilerplate
   - fastapi — FastAPI with uvicorn, pydantic-settings
   - cli — Typer CLI with `__main__.py`

2. **Ask or infer project name** from context

3. **Run bootstrap script**:
   ```bash
   python ~/.claude/skills/python-bootstrap/scripts/bootstrap_project.py \
     --project-name <name> --type <type> --output-dir <path>
   ```

4. **Auto-initialize**:
   ```bash
   cd <project-name> && git init && uv venv --python 3.13 && uv sync --dev
   ```

5. **Verify**:
   ```bash
   make ci
   ```

## Project Structure (generated)

```
<project-name>/
├── src/<package_name>/
│   ├── __init__.py
│   └── (type-specific files)
├── tests/
│   ├── conftest.py
│   └── test_placeholder.py
├── pyproject.toml
├── Dockerfile
├── Makefile
├── prek.toml
├── .python-version
├── .gitignore
└── CLAUDE.md
```

## Tooling Stack

- Python 3.13.7, uv package manager
- ruff (lint + format), pyright (type check)
- prek (git hooks), pytest + pytest-cov + pytest-mock
- Docker multi-stage builds
