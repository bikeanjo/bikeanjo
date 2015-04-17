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

HELP_WITH = (
    ('advice', _('Advice about safe routes')),
    ('escort', _('Follow someone in a ride')),
    ('teach', _('Teach someone to ride a bike')),
    ('workshop', _('Talk in workshop')),
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
    help_with = models.CharField(choices=HELP_WITH, max_length=16, blank=True)
    initiatives = models.CharField(max_length=256, blank=True)
    role = models.CharField(choices=CYCLIST_ROLES, max_length=32, blank=True)

    def __unicode__(self):
        return self.user.__unicode__()


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
        return json.dumps(d)


class Point(models.Model):
    cyclist = models.ForeignKey(Cyclist)
    address = models.CharField(max_length=128)
    coords = models.PointField()
