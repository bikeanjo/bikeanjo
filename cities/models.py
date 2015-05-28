# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    name = models.CharField(_('Name'), max_length=64)
    acronym = models.CharField(_('Acronym'), max_length=4)

    def __unicode__(self):
        return self.name


class State(models.Model):
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')

    country = models.ForeignKey(Country)
    name = models.CharField(_('Name'), max_length=64)
    acronym = models.CharField(_('Acronym'), max_length=4)

    def __unicode__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    state = models.ForeignKey(State)
    name = models.CharField(_('Name'), max_length=64)

    def __unicode__(self):
        return self.name
