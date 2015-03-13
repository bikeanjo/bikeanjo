.PHONY: pre-ci setup-ci all tests
.SILENT: all

GRUNT=grunt
BOWER=bower
NOINPUT=

PIP="${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/pip"
PYTHON="${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/python"

all:
	bash -c "\
		test -z ${VIRTUAL_ENV} && \
		test ! -d ${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo && \
		test -n ${VIRTUALENVWRAPPER_SCRIPT} && \
		source ${VIRTUALENVWRAPPER_SCRIPT} && \
	 	mkvirtualenv bikeanjo -p /usr/bin/python2 || \
	 	exit 0"
	npm install
	${BOWER} install
	${PIP} install -r requirements.txt
	${PYTHON} manage.py migrate ${NOINPUT}
	${GRUNT} all

pre-ci:
	npm install grunt-cli bower

setup-ci: GRUNT=./node_modules/grunt-cli/bin/grunt
setup-ci: BOWER=./node_modules/bower/bin/bower
setup-ci: NOINPUT=--noinput
setup-ci: PIP=`which pip`
setup-ci: PYTHON=`which python2`
setup-ci: pre-ci all

tests:
	py.test
	flake8

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;
