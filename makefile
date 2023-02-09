.PHONY: all setup package pypitest pypi
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
endif

SOURCE = pipeline_integrity
TESTS = tests

FLAKE8 = $(PYTHON) -m flake8 --max-line-length=120
PYLINT = $(PYTHON) -m pylint
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PIP = $(PYTHON) -m pip install

all: tests

test:
	$(PTEST) -s $(TESTS)/test/$(T)

flake8:
	$(FLAKE8) $(SOURCE)
	$(FLAKE8) $(TESTS)/test

lint:
	$(PYLINT) $(TESTS)/test
	$(PYLINT) $(SOURCE)

pep257:
	$(PYTHON) -m pep257 $(SOURCE)
	$(PYTHON) -m pep257 --match='.*\.py' $(TESTS)/test

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip

setup2: setup_python2 setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r $(TESTS)/requirements.txt
	$(PIP) -r deploy.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv

setup_python2:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv
