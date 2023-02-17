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

LOCALE = locale
PO = LC_MESSAGES/messages.po
MO = LC_MESSAGES/messages.mo
PIP = $(PYTHON) -m pip install

all: run

run:
	$(PYTHON) -m flask --debug --env-file .env run

runru:
	$(PYTHON) -m flask --debug --env-file .envru run

po:
	$(PYBABEL) extract -F $(LOCALE)/babel.cfg -o $(LOCALE)/messages.pot .
	$(PYBABEL) update -i $(LOCALE)/messages.pot -d $(LOCALE) -l ru

mo:
	$(MSGFMT) $(LOCALE)/ru/$(PO) -o $(LOCALE)/ru/$(MO)
	$(MSGFMT) $(LOCALE)/en/$(PO) -o $(LOCALE)/en/$(MO)

setup: setup_python setup_pip mo

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
