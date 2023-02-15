.PHONY: all setup run
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
else
PYTHON = ./venv/bin/python
endif

PIP = $(PYTHON) -m pip install

all: run

run:
	$(PYTHON) -m flask --debug --env-file .env run

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
