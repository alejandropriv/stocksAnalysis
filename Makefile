PYTHON = python3

.PHONY = prepare_venv

VENV_NAME?=magicstocksenv
PYTHON=${VENV_NAME}/bin/python

prepare_venv:
	$(VENV_NAME)/bin/activate
	pip install -r requirements.txt

