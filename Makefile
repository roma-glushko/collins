.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

PACKAGES?=collins tests

.venv: pyproject.toml poetry.lock
	@poetry install

install: ## Install the project
	@poetry install

test-lint: ## Run lints in the check mode (useful for CI)
	@poetry run isort $(PACKAGES) -c
	@poetry run black --check $(PACKAGES)
	@poetry run flake8 $(PACKAGES)
	@poetry run mypy --pretty $(PACKAGES)

lint: ## Lint the source code
	@poetry run isort $(PACKAGES)
	@poetry run black $(PACKAGES)
	@poetry run flake8 $(PACKAGES)
	@poetry run mypy --pretty $(PACKAGES)