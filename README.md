[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/bikeanjo/bikeanjo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Build Status](https://travis-ci.org/bikeanjo/bikeanjo.svg)](https://travis-ci.org/bikeanjo/bikeanjo)

Bike Anjo
=========

pre-install
-----------

* sudo pacman -S postgresql
* sudo pacman -S postgis
* sudo pacman -S nodejs

install:
--------

* npm install
* ./node_modules/bower/bin/bower install
* ./node_modules/grunt-cli/bin/grunt all
* virtualenv -p /usr/bin/python2 bikeanjo
* pip install -r requirements.txt
* psql -U postgres -c 'CREATE EXTENSION postgis;'
* psql -U postgres -c 'CREATE DATABASE bikeanjo;'
* ./manage.py migrate

run:
----

you need to run both the django process and grunt to build static assets:

* ./manage.py runserver
* grunt all

then you can open [http://localhost:8000](http://localhost:8000) on your browser.

tests:
----

* make tests

[nossa trello board](https://trello.com/b/jRVE7t8B/cocriacao-nova-plataforma-bike-anjo)



http://gis.stackexchange.com/a/19440
