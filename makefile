
PYTHON=python3
PIP=$(PYTHON) -m pip

REQUIREMENTS=./requirements.txt

SRC=./src
RESOURCES=./resources
MAIN=$(SRC)/main.py
DATA=$(shell find $(RESOURCES) -name '*.png')

all:
	python3 $(MAIN)

build: 
	pyinstaller --onefile --noconsole -n Nano-Golf --icon=resources/icon.icns --windowed --noconfirm --clean --add-data="resources/*:resources" $(MAIN)




init: 
	$(PIP) install -r $(REQUIREMENTS)

