.PHONY: all setup run runru po mo
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
PYBABEL = venv/Scripts/pybabel.exe
MSGFMT = msgfmt.exe
else
PYTHON = ./venv/bin/python
PYBABEL = ./venv/bin/pybabel
MSGFMT = msgfmt
endif

SOURCE = source
LOCALE = locale
PO = LC_MESSAGES/messages.po
MO = LC_MESSAGES/messages.mo
PIP = $(PYTHON) -m pip install

all: run

run:
	$(PYTHON) $(SOURCE)/main.py

setup: setup_python setup_pip mo

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
