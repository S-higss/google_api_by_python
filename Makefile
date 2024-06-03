.DEFAULT_GOAL := help
.PHONY: push-all	## Reflect all changes under the current directory
push-all:
	git add .
	git commit -m "commit all changes"
	git push origin HEAD

.PHONY: install
install:
	@pip install -r requirements.txt

.PHONY: run	## run main.py
run:
	python main.py

.PHONY: history
history:	## commit and push all changes to repo
	@echo "Enter your commit message:"; \
	read message; \
	git add .; \
	git commit -m "$$message"; \
	git push origin HEAD

.PHONY: help
help:	## show commands
	@grep -E '^[[:alnum:]_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'