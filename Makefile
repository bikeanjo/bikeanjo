.PHONY: pre-ci setup-ci all tests

NPM=npm

all:
	${NPM} install
	bower install
	pip install -r requirements.tx
	./bikeanjo.py syncdb
	grunt all

pre-ci:
	sudo add-apt-repository -y ppa:chris-lea/node.js
	sudo apt-get -y update
	sudo apt-get -y install nodejs
	sudo npm install -g grunt-cli bower

setup-ci: NPM=sudo npm
setup-ci: pre-ci all

tests:
	py.test
	flake8

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;
