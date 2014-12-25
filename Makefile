.PHONY: pre-ci setup-ci all tests

GRUNT=grunt
BOWER=bower
NOINPUT=

all:
	npm install
	${BOWER} install
	pip install -r requirements.txt
	./bikeanjo.py migrate ${NOINPUT}
	${GRUNT} all

pre-ci:
	npm install grunt-cli bower

setup-ci: GRUNT=./node_modules/grunt-cli/bin/grunt
setup-ci: BOWER=./node_modules/bower/bin/bower
setup-ci: NOINPUT=--noinput
setup-ci: pre-ci all

tests:
	py.test
	flake8

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;
