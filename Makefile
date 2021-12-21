IMAGE = fibraville-backend:latest
CONTAINER = fibraville-backend
MANAGECMD = docker exec -it $(CONTAINER)

all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the container
	docker build --tag $(IMAGE) .
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker run -dit --name $(CONTAINER) -v $(shell pwd):/deploy -p 8000:8000 $(IMAGE) /bin/bash

test: ## Run tests
	$(MANAGECMD) python3 manage.py test

restart: ## Restart the container
	docker restart $(CONTAINER)

cmd: ## Access bash
	$(MANAGECMD) /bin/bash

up:
	docker restart $(CONTAINER)
	$(MANAGECMD) /bin/bash -c "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"

down:
	docker stop $(CONTAINER)

remove:
	docker stop $(CONTAINER) || true && docker rm $(CONTAINER) || true
	docker rmi $(IMAGE)
