.PHONY: help
help:
	@echo "🛠 Available Commands"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## Run the server app
	@poetry run uvicorn livearea.main:app --reload --port 3003