# Define the Python interpreter to be used (change this if needed)
PYTHON ?= python3

# Determine the installation directory for the script
INSTALL_DIR := $(shell $(PYTHON) -m site --user-base)/bin

install:
	$(PYTHON) note_app.py install --install-dir $(INSTALL_DIR)

uninstall:
	$(PYTHON) note_app.py uninstall --install-dir $(INSTALL_DIR)

.PHONY: install uninstall
