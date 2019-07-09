# $Id$

PROJECT_ROOT	= $(shell git rev-parse --show-toplevel)

default:

test:
	pytest -v

clean:
	find . -name "*.py[c|o]" -o -name __pycache__ -exec rm -rf {} +

config:
	git config --local include.path ../.gitconfig

rcs-tag:
	git stash save
	rm .git/index
	git checkout HEAD -- $(PROJECT_ROOT)
	git stash pop || true
