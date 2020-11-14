# Inspired by "A successful pip-tools workflow for managing Python package
# requirements" by James Cooke,
# https://jamescooke.info/a-successful-pip-tools-workflow-for-managing-python-package-requirements.html

# Use this Makefile with a Python virtual environment activated.

# Requirements files:
#   requirements.in         Python packages needed to run
#   test-requirements.in    Additional packages needed for testing
#   dev-requirements.in     Additional packages needed for development

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

clean:
	- rm *.txt

rebuild: clean all

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

# Dependency chain
dev-requirements.txt: test-requirements.txt
test-requirements.txt: requirements.txt
