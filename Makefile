.DEFAULT_GOAL := help

.PHONY: init
init: ## Setup the requirements
	$(info --- Setup ---)
	@poetry install

.PHONY: format
format: ## Format the code
	$(info --- Python format ---)
	@poetry run black mysqldump_analyzer tests
	@poetry run isort mysqldump_analyzer tests

.PHONY: style
style: init ## Run check
	$(info Check Python isort)
	@poetry run isort --check-only mysqldump_analyzer tests
	$(info Check Python black)
	@poetry run black --check mysqldump_analyzer tests
	$(info Check Python mypy)
	@poetry run mypy

.PHONY: test-unit
test-unit: init ## Run unit test
	$(info --- Run Python unit-test ---)
	@poetry run pytest

.PHONY: install
install: ## Run install
	$(info --- Run Install ---)
	@poetry install --only main

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
