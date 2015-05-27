from django.db import models
from django.utils.translation import ugettext_lazy as _


class State(models.Model):
    name = models.CharField(_('Name'), max_length=64)
    acronym = models.CharField(_('Acronym'), max_length=4)


class City(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(_('Name'), max_length=64)
