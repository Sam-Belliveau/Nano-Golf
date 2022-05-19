
PYTHON=python3
PIP=$(PYTHON) -m pip

REQUIREMENTS=./requirements.txt

SRC=./src
MAIN=$(SRC)/main.py

all: init
	$(PYTHON) $(MAIN)
	
init: 
	$(PIP) install -r $(REQUIREMENTS)

