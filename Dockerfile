FROM debian:stretch
MAINTAINER Fabio Montefuscolo <contato@bikeanjo.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN apt-get install -y \
    curl               \
    curl               \
    git                \
    gunicorn           \
    libgeos-dev        \
    libjpeg-dev        \
    libpq-dev          \
    nginx              \
    python             \
    python-dev         \
    python-pip         \
    supervisor

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y nodejs

RUN useradd -m -u 1000 -s /bin/bash bikeanjo \
    && mkdir /app

# Prefer to use mdillon/postgis
ENV DJANGO_DATABASE_URL='postgis://bikeanjo:bikeanjo@postgis/bikeanjo'
ENV DJANGO_SETTINGS_MODULE='bikeanjo.settings'
ENV PYTHONPATH='/app'
ENV GUNICORN_LOG_LEVEL='info'
ENV GUNICORN_EXTRA_FLAGS=''

COPY . /app
WORKDIR /app
RUN pip install setuptools_scm && pip install -r requirements.txt
RUN chown -R bikeanjo /app

USER bikeanjo
RUN npm install
RUN node node_modules/bower/bin/bower install
RUN node node_modules/grunt-cli/bin/grunt all
RUN python manage.py collectstatic --noinput

USER root
EXPOSE 80 8000
ENTRYPOINT  ["/app/docker/entrypoint.py"]
CMD ["supervisord", "-c", "/app/docker/supervisord.conf"]
