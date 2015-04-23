# -*- coding: utf-8 -*-
import json
from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

GENDER = (
    ('male', _('Male')),
    ('female', _('Female')),
)

CYCLIST_ROLES = (
    ('volunteer', _('Volunteer')),
    ('requester', _('Requester')),
)


HELP = (
    (1, _('Teach someone to ride a bike')),  # Ensinando alguém a pedalar
    (2, _('Follow beginners on cycling')),  # Acompanhando iniciantes nas pedaladas
    (4, _('Advice about safe routes')),  # Recomendando rotas mais seguras
    (8, _('Participating in the events of Bike Anjos')),  # Participando dos eventos dos Bikes Anjos
)

EXPERIENCE = (
    ('less than 1 year', _('Less than 1 year')),
    ('from 1 to 2 years', _('From 1 to 2 years')),
    ('from 2 to 4 years', _('From 2 to 4 years')),
    ('more than 4 years', _('More than 4 years')),
)

BIKE_USE = (
    ('everyday', _('Everyday'),),
    ('just few days a week/month', _('Just few days a week/month'),),
    ('once a week', _('Once a week'),),
    ('no, i use for leisure', _('No, I use for leisure'),),
)


class Cyclist(models.Model):
    user = models.OneToOneField(User)
    country = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=24, blank=True)
    birthday = models.DateField(default=date.today, null=True)
    ride_experience = models.CharField(choices=EXPERIENCE, max_length=32, blank=True)
    bike_use = models.CharField(choices=BIKE_USE, max_length=32, blank=True)
    help_with = models.IntegerField(default=0)  # choices=HELP
    initiatives = models.CharField(max_length=256, blank=True)
    role = models.CharField(choices=CYCLIST_ROLES, max_length=32, blank=True)

    def __unicode__(self):
        return self.user.__unicode__()

    def help_labels(self):
        return (label for code, label in HELP if self.help_with & code > 0)


class Track(models.Model):
    cyclist = models.ForeignKey(Cyclist)
    start = models.CharField(max_length=128)
    end = models.CharField(max_length=128)
    track = models.LineStringField()

    def json(self):
        d = {
            'type': 'LineString',
            'coordinates': [p for p in self.track],
            'properties': {
                'start': self.start,
                'end': self.end,
            },
        }
        if self.id:
            d['properties']['id'] = self.id
        return d


class Point(models.Model):
    cyclist = models.ForeignKey(Cyclist)
    address = models.CharField(max_length=128)
    coords = models.PointField()

    def json(self):
        d = {
            'type': 'LineString',
            'coordinates': self.coords.get_coords(),
            'properties': {
                'address': self.address,
            },
        }
        if self.id:
            d['properties']['id'] = self.id
        return d
