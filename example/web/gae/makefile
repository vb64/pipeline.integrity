.PHONY: all setup run runru po mo
# make tests >debug.log 2>&1
ifeq ($(OS),Windows_NT)
GCLOUD = $(LOCALAPPDATA)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd
PYTHON = venv/Scripts/python.exe
PYBABEL = venv/Scripts/pybabel.exe
MSGFMT = msgfmt.exe
else
GCLOUD = gcloud
PYTHON = ./venv/bin/python
PYBABEL = ./venv/bin/pybabel
MSGFMT = msgfmt
endif

SOURCE = source
LOCALE = locale
PO = LC_MESSAGES/messages.po
MO = LC_MESSAGES/messages.mo
PIP = $(PYTHON) -m pip install
DEPLOY = $(GCLOUD) app deploy --project wot-online-hours

VERSION = test4

all: run

run:
	$(PYTHON) $(SOURCE)/main.py

deploy:
	$(DEPLOY) --version $(VERSION) $(SOURCE)/app.yaml

setup: setup_python setup_pip

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r $(SOURCE)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
