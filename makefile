.PHONY: all setup package pypitest pypi
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PTEST = venv/Scripts/pytest.exe
COVERAGE = venv/Scripts/coverage.exe
PYBABEL = venv/Scripts/pybabel.exe
else
PYTHON = ./venv/bin/python
PTEST = ./venv/bin/pytest
COVERAGE = ./venv/bin/coverage
PYBABEL = ./venv/bin/pybabel
endif

SOURCE = pipeline_integrity
TESTS = tests
LOCALE_ASME = $(SOURCE)/method/asme/locale

FLAKE8 = $(PYTHON) -m flake8
PYLINT = $(PYTHON) -m pylint
PYLINT2 = $(PYLINT) --rcfile .pylintrc2
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

lint2:
	$(PYLINT2) $(TESTS)/test
	$(PYLINT2) $(SOURCE)

pep257:
	$(PYTHON) -m pydocstyle $(SOURCE)
	$(PYTHON) -m pydocstyle --match='.*\.py' $(TESTS)/test

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

tests2: flake8 pep257 lint2
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

po: po_asme

po_asme:
	$(PYBABEL) extract -F $(LOCALE_ASME)/babel.cfg -o $(LOCALE_ASME)/messages.pot .
	$(PYBABEL) update -i $(LOCALE_ASME)/messages.pot -d $(LOCALE_ASME) -l ru

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip
	$(PIP) -r deploy.txt

setup2: setup_python2 setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r $(TESTS)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv

setup_python2:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv
