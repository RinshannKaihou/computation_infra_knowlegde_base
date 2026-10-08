PYTHON ?= python3
RUN_PYTHON = $(if $(wildcard .venv/bin/python),.venv/bin/python,$(PYTHON))

.PHONY: setup setup-dev check build test lint

setup:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

setup-dev:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install -r requirements-dev.txt

check:
	PYTHONPATH=src $(RUN_PYTHON) -m kb.cli check

build:
	PYTHONPATH=src $(RUN_PYTHON) -m kb.cli build

test:
	PYTHONPATH=src $(RUN_PYTHON) -m coverage run --source=kb -m pytest -q
	$(RUN_PYTHON) -m coverage report --fail-under=90

lint: check
