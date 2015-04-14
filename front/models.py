# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
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
    ('none', _("I don't know how to ride a bike")),
    ('beginner', _("I don't know how to ride in traffic")),
    ('intermediate', _('I use my bike rarely')),
    ('advanced', _('I use my bike almost every day')),
)


class Cyclist(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField(default=date.today, null=True)
    city = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    help_with = models.CharField(choices=HELP_WITH, max_length=16, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    role = models.CharField(choices=CYCLIST_ROLES, max_length=32, blank=True)
    state = models.CharField(max_length=32, blank=True)

    def __unicode__(self):
        return self.user.__unicode__()


class Track(models.Model):
    cyclist = models.ForeignKey(Cyclist)
    start = models.CharField(max_length=64)
    end = models.CharField(max_length=64)
    track = models.MultiPointField()


class Point(models.Model):
    cyclist = models.ForeignKey(Cyclist)
    address = models.CharField(max_length=128)
    coords = models.PointField()
