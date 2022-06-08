
PYTHON=python3
PIP=$(PYTHON) -m pip

REQUIREMENTS=./requirements.txt

SRC=./src
RESOURCES=./resources
MAIN=$(SRC)/main.py
DATA=$(shell find $(RESOURCES) -name '*.png')

all: 
	pyinstaller --onefile --noconsole -n Nano-Golf --icon=resources/icon.icns --windowed --noconfirm --clean --add-data="resources/*:resources" $(MAIN)




init: 
	$(PIP) install -r $(REQUIREMENTS)

