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
LOCALE = $(SOURCE)/locale
PO = LC_MESSAGES/messages.po
MO = LC_MESSAGES/messages.mo
PIP = $(PYTHON) -m pip install
PRJ = wot-online-hours
DEPLOY = $(GCLOUD) app deploy --project $(PRJ)
BACK = backend

BACK_VERSION = days14
VERSION = fix777

all: run

run:
	$(PYTHON) $(SOURCE)/main.py

back:
	$(PYTHON) $(BACK)/main.py

po:
	$(PYBABEL) extract -F $(LOCALE)/babel.cfg -o $(LOCALE)/messages.pot .
	$(PYBABEL) update -i $(LOCALE)/messages.pot -d $(LOCALE) -l ru

mo:
	$(MSGFMT) $(LOCALE)/ru/$(PO) -o $(LOCALE)/ru/$(MO)
	$(MSGFMT) $(LOCALE)/en/$(PO) -o $(LOCALE)/en/$(MO)

deploy: mo
	$(DEPLOY) --version $(VERSION) $(SOURCE)/app.yaml

deployback:
	$(DEPLOY) --version $(BACK_VERSION) $(BACK)/app.yaml

cron:
	$(DEPLOY) cron.yaml

auth:
	$(GCLOUD) auth application-default login
	$(GCLOUD) auth application-default set-quota-project $(PRJ)

setup: setup_python setup_pip mo

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r $(SOURCE)/requirements.txt
	$(PIP) -r $(BACK)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv
