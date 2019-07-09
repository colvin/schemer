# $Id$

PROJECT_ROOT	= $(shell git rev-parse --show-toplevel)

DESTDIR		= /usr/local
BIN_USR		= root
BIN_GRP		= wheel
BIN_MOD		= 755

default: install

install:
	install -o $(BIN_USR) -g $(BIN_GRP) -m $(BIN_MOD) schemer $(PREFIX)/bin/schemer

test:
	pytest -v

clean:
	find . -name "*.py[c|o]" -o -name __pycache__ -exec rm -rf {} +
	find . -name .pytest_cache -exec rm -rf {} +

config:
	git config --local include.path ../.gitconfig

rcs-tag:
	git stash save
	rm .git/index
	git checkout HEAD -- $(PROJECT_ROOT)
	git stash pop || true
