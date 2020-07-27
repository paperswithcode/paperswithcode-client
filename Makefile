.PHONY: help default docs build release clean test check fmt
.DEFAULT_GOAL := help
PROJECT := paperswithcode

help:                ## Show help.
	@grep -E '^[a-zA-Z2_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


docs:                    ## Build documentation.
	@cd docs && make html && open _build/html/index.html


build:               ## Build the source and wheel distribution packages.
	@python3 setup.py sdist bdist_wheel


release: build       ## Build and upload the package to PyPI.
	@twine upload --repository-url  https://upload.pypi.org/legacy/ dist/*
	@rm -fr build dist "$(PROJECT).egg-info"


clean:               ## Cleanup the project
	@find . -type d -name __pycache__ -delete
	@find . -type f -name "*.py[cod]" -delete
	@rm -fr build dist "$(PROJECT).egg-info"
	@rm -fr docs/_build/*


test:                ## Run tests and code checks.
	@py.test -v --cov "$(PROJECT)" "$(PROJECT)"


check:               ## Run code checks.
	@flake8 "$(PROJECT)"
	@pydocstyle "$(PROJECT)"


fmt:                 ## Format the code.
	@black --target-version=py37 --safe --line-length=79 "$(PROJECT)"
