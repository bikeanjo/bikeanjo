# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Lookup
from django.db.models.fields import Field
from django.db.models import Manager as GeoManager


@Field.register_lookup
class LowerMatch(Lookup):
    lookup_name = 'lowermatch'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = ['^' + str(p) for p in rhs_params]
        return 'LOWER(%s) ~ LOWER(%s)' % (lhs, rhs), params


class Country(models.Model):
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    name = models.CharField(_('Name'), db_index=True, max_length=64)
    acronym = models.CharField(_('Acronym'), db_index=True, max_length=4)

    def __unicode__(self):
        return self.name


class CountryAlias(models.Model):
    class Meta:
        verbose_name = _('Alias')
        verbose_name_plural = _('Aliases')
        unique_together = (('country', 'name',),)

    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING)
    name = models.CharField(_('Alias name'), max_length=1024, db_index=True)

class State(models.Model):
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')

    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    name = models.CharField(_('Name'), max_length=64)
    acronym = models.CharField(_('Acronym'), max_length=4)

    def __unicode__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    country = models.ForeignKey(Country, null=True, on_delete=models.DO_NOTHING)
    state = models.ForeignKey(State, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(_('Name'), max_length=64, db_index=True)
    tz = models.CharField(_('Timezone'), max_length=40, blank=True)
    point = models.PointField(null=True)

    objects = GeoManager()

    def __unicode__(self):
        return self.name


class CityAlias(models.Model):
    class Meta:
        verbose_name = _('Alias')
        verbose_name_plural = _('Aliases')
        unique_together = (('city', 'name',),)

    city = models.ForeignKey(City,on_delete=models.DO_NOTHING)
    name = models.CharField(_('Alias name'), max_length=1024, db_index=True)
