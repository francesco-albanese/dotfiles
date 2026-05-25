.PHONY: setup-venv install-deps test test-cov lint lint-fix fmt typecheck check ci docker-build lambda-build

setup-venv:
	uv venv --python 3.13

install-deps:
	uv sync --dev

test:
	uv run pytest -v

test-cov:
	uv run pytest --cov=src --cov-report=term-missing -v

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

fmt:
	uv run ruff format .

typecheck:
	uv run pyright

check:
	uv run prek run --all-files

ci: lint typecheck test

docker-build:
	docker build -t {{PROJECT_NAME}} .

lambda-build:
	docker build --platform linux/arm64 -t {{PROJECT_NAME}} .
