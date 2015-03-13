.PHONY: pre-ci setup-ci all tests
.SILENT: all

GRUNT=grunt
BOWER=bower
NOINPUT=

all:
	bash -c "\
		test -z ${VIRTUAL_ENV} && \
		test -n ${VIRTUALENVWRAPPER_SCRIPT} && \
		source ${VIRTUALENVWRAPPER_SCRIPT} && \
	 	mkvirtualenv bikeanjo -p /usr/bin/python2 || \
	 	echo 'skipped virtualenv creation'"
	npm install
	${BOWER} install
	${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/pip install -r requirements.txt
	${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/python manage.py migrate ${NOINPUT}
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
