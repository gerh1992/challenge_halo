build: ## Build flask server container
	docker-compose build

test: ## Execute integration tests
	docker-compose up -d
	docker-compose run --rm flask -m pytest -s
	docker-compose down

run: ## Spin up flask server and redis container
	docker-compose up

.PHONY: help

help: ## List commands.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help