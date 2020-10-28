.PHONY: clean clean-test clean-pyc clean-build docs help venv
.DEFAULT_GOAL := help

PROJECT_NAME = meetup2apricot
PYTHON_INTERPRETER = python3.9

ifeq (,$(shell which virtualenvwrapper.sh))
BASH_CMD_ACTIVATE_VENV = venv/bin/activate
MAKE_VENV = $(PYTHON_INTERPRETER) -m venv venv
else
BASH_CMD_ACTIVATE_VENV = source `which virtualenvwrapper.sh`; workon $(PROJECT_NAME)
MAKE_VENV = bash -c "source `which virtualenvwrapper.sh`; mkvirtualenv --python=$(PYTHON_INTERPRETER) -a . $(PROJECT_NAME)"
endif

venv-cmd = bash -c "$(BASH_CMD_ACTIVATE_VENV); $(1)"


define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := $(PYTHON_INTERPRETER) -c "$$BROWSER_PYSCRIPT"

help:
	@$(PYTHON_INTERPRETER) -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 meetup2apricot tests

test: ## run tests quickly with the default Python
	$(call venv-cmd,py.test tests)

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source meetup2apricot -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/meetup2apricot.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ meetup2apricot
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

gitlog: ## show the Git graphical history
	git log --oneline --graph --decorate --all

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	$(PYTHON_INTERPRETER) setup.py sdist
	$(PYTHON_INTERPRETER) setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	$(PYTHON_INTERPRETER) setup.py install

venv: ## create a Python virtual environment
	bash -c "$(BASH_CMD_ACTIVATE_VENV)" || $(MAKE_VENV)

dev: venv ## install required Python packages for local development
	$(call venv-cmd,pip install -U pip pip-tools)
	$(call venv-cmd,pip-sync requirements/test-requirements.txt requirements/dev-requirements.txt requirements/requirements.txt)
