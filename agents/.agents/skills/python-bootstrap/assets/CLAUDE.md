# Project Rules

## Package Manager
- Python 3.13.7 with `uv`
- Install deps: `uv sync --dev`
- Run commands: `uv run <cmd>`

## Git Hooks
- Use `prek` (NOT `pre-commit`): `prek run --all-files`
- Install hooks: `prek install`

## Testing
- Run tests: `uv run pytest -v`
- Run with coverage: `uv run pytest --cov=src --cov-report=term-missing -v`

## Linting & Formatting
- Lint: `uv run ruff check .`
- Fix: `uv run ruff check --fix .`
- Format: `uv run ruff format .`
- Type check: `uv run pyright`

## CI
- Run all checks: `make ci`
