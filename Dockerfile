FROM debian:jessie
MAINTAINER Fabio Montefuscolo <fabio.montefuscolo@hacklab.com.br>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN apt-get install -y python python-pip python-dev
RUN apt-get install -y libpq-dev libgeos-dev libjpeg-dev
RUN apt-get install -y nginx gunicorn supervisor
RUN apt-get install -y npm
RUN apt-get install -y git

RUN useradd -m -u 1000 -s /bin/bash bikeanjo
RUN mkdir /app

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN chown -R bikeanjo /app

USER bikeanjo
RUN npm install
RUN nodejs node_modules/bower/bin/bower install

RUN nodejs node_modules/grunt-cli/bin/grunt all
#RUN python manage.py collectstatic --noinput
