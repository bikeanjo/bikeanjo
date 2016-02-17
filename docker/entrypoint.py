#!/usr/bin/env python

import os
import sys
import subprocess
import django
import environ
import psycopg2

from django.conf import settings
from django.core.management import execute_from_command_line

env = environ.Env()
environ.Env.read_env('/app/.env')

database = settings.DATABASES.get('default')

conn = psycopg2.connect(
    user='postgres',
    host='postgis',
    password=env('POSTGIS_ENV_POSTGRES_PASSWORD')
)
conn.set_isolation_level(0)

cur = conn.cursor()

cur.execute("SELECT count(1) > 0 FROM pg_user WHERE usename='%(USER)s';" % database)
user_exists = cur.fetchone()[0]

cur.execute("SELECT count(1) FROM pg_database WHERE datname='%(NAME)s';" % database)
db_exists = cur.fetchone()[0]

if not user_exists:
    cur.execute("CREATE USER %(USER)s WITH PASSWORD '%(PASSWORD)s';" % database)

if not db_exists:
    cur.execute("CREATE DATABASE %(NAME)s OWNER %(USER)s;" % database)
    cur.close()
    conn.close()

    conn = psycopg2.connect(
        dbname=database.get('NAME'),
        user='postgres',
        host='postgis',
        password=env('POSTGIS_ENV_POSTGRES_PASSWORD')
    )
    conn.set_isolation_level(0)
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION  IF NOT EXISTS postgis;" % database)
    cur.execute("CREATE EXTENSION  IF NOT EXISTS unaccent;" % database)

cur.close()
conn.close()

execute_from_command_line(['manage.py', 'migrate'])
subprocess.call(sys.argv[1:])
