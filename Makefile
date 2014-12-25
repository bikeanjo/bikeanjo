.PHONY: pre-ci setup-ci all tests

NPM=npm
NOINPUT=

all:
	npm install
	bower install
	pip install -r requirements.txt
	./bikeanjo.py migrate ${NOINPUT}
	grunt all

pre-ci:
	curl https://raw.githubusercontent.com/creationix/nvm/v0.21.0/install.sh | bash
	nvm install 0.10
	nvm use 0.10

setup-ci: NOINPUT=--noinput
setup-ci: pre-ci all

tests:
	py.test
	flake8

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;
