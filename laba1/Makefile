.PHONY: all venv clear

#read what is the diff between := and =
SHELL := /bin/bash

SOURCES := $(shell find . -name '*.py' -not -path '*./.venv/*' -not -path '*./.git/*' -print)

PROG := caesar.py
HOST := 127.0.0.1
DOCKERNAME := caesar
STDINPUTFILE := hello
STDOUTPUTFILE := hello_enc
STDFLAGS := $(STDINPUTFILE) $(STDOUTPUTFILE)

all: lint

venv: .venv/bin/activate
.venv/bin/activate: requirements.txt
	@python3 -m venv ./.venv

	@.venv/bin/python -m pip install -r requirements.txt

	@touch .venv/bin/activate

black: venv
	@.venv/bin/black --target-version=py38 --line-length=100 -- $(SOURCES)

lint: venv
	-.venv/bin/pylint -- $(SOURCES)

	-.venv/bin/flake8 -- $(SOURCES)
	
$(STDINPUTFILE):
	touch $(STDINPUTFILE)
	echo "Hello World" > $(STDINPUTFILE)

run: venv $(STDINPUTFILE)
	.venv/bin/python3 $(PROG) $(STDFLAGS)
	cat $(STDOUTPUTFILE)

clean:
	rm -rf .venv
	find -iname "*.pyc" -delete
	find -iname "$(STDINPUTFILE)" -delete
	find -iname "$(STDOUTPUTFILE)" -delete
	
$(DOCKERNAME):
	sudo docker build \
	    --file=./Dockerfile \
	    --tag=$(DOCKERNAME) .
	
docker-run: $(DOCKERNAME)
	sudo docker run $(DOCKERNAME)
