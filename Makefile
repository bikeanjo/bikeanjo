.PHONY: pre-ci setup-ci all tests

NPM=npm
NOINPUT=

all:
	${NPM} install
	bower install
	pip install -r requirements.txt
	./bikeanjo.py migrate ${NOINPUT}
	grunt all

pre-ci:
	sudo add-apt-repository -y ppa:chris-lea/node.js
	sudo apt-get -y update
	sudo apt-get -y install nodejs
	sudo npm install -g grunt-cli bower

setup-ci: NPM=sudo npm
setup-ci: NOINPUT=--noinput
setup-ci: pre-ci all

tests:
	py.test
	flake8

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;
