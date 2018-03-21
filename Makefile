.PHONY: pre-ci setup-ci all assets tests
.SILENT: all

GRUNT=./node_modules/grunt-cli/bin/grunt
BOWER=./node_modules/bower/bin/bower
NOINPUT=--noinput

VIRTUALENVWRAPPER_HOOK_DIR="${HOME}/.virtualenvs"
PIP="${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/pip"
PYTHON="${VIRTUALENVWRAPPER_HOOK_DIR}/bikeanjo/bin/python"

POSTGRES_HOST="127.0.0.1"

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

assets:
	npm install
	${BOWER} install
	${GRUNT} all
	${GRUNT} watch

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
	flake8 --ignore=E501 --exclude="*/migrations,front/apps.py,bikeanjo/settings.py" front cyclists cities bikeanjo

clean:
	find . -type f -name '*.py[co]' -exec rm {} \;

upgrade: clean
	git pull
	npm install
	${BOWER} install
	${PIP} install -r requirements.txt
	${PYTHON} manage.py migrate
	${PYTHON} manage.py update_translation_fields
	${PYTHON} manage.py collectstatic --noinput
	${PYTHON} manage.py compilemessages
	${GRUNT} all

messages:
	${PYTHON} manage.py makemessages -d django --all\
		--ignore=node_modules\
		--ignore=bower_components\
		--ignore=local_data\
		--ignore=data

resetdb:
	test "${ACCIDENT}" = "no"
	psql -Upostgres -h${POSTGRES_HOST} postgres -c 'drop database if exists bikeanjo;'
	psql -Upostgres -h${POSTGRES_HOST} postgres -c 'drop user if exists bikeanjo;'
	psql -Upostgres -h${POSTGRES_HOST} postgres -c "create user bikeanjo with password 'bikeanjo';"
	psql -Upostgres -h${POSTGRES_HOST} postgres -c 'create database bikeanjo owner bikeanjo;'
	psql -Upostgres -h${POSTGRES_HOST} bikeanjo -c 'create extension postgis;'
	psql -Upostgres -h${POSTGRES_HOST} bikeanjo -c 'create extension unaccent;'
	psql -Upostgres -h${POSTGRES_HOST} bikeanjo -c 'create extension fuzzystrmatch;'

remove-fuzzy-trans:
	sed -i -z -r -e 's/((#[^\n]+\n)*)(#, fuzzy[^\n]*\n)(#\| msgid[^\n]+\n)(#[^\n]+\n)*((msgid[^\n]+\n)("[^"]+"\n)*)(msgstr[^\n]+\n)("[^"]+"\n)*/\1\6msgstr ""/g' \
		`find locale -name "*.po"`
