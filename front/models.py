# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)

SERVICES = (
    ('router', _('Choose good routes')),
    ('monitor', _('Monitor cycling in traffic')),
    ('teach', _('Teaching pedaling')),
    ('workshop', _('Institutional events')),
)


class Cyclist(models.Model):
    user = models.OneToOneField(User)

    is_volunteer = models.BooleanField(default=False)

    bio = models.CharField(_('biography'), max_length=140)
    date_of_birth = models.DateField(_('date of birth'))
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER)
    phone = models.CharField(_('phone number'), max_length=32)
    years_experience = models.PositiveSmallIntegerField(
                                                    _('years of experience'))

    address = models.CharField(_('address'), max_length=64)
    address_number = models.PositiveSmallIntegerField(_('number'))
    address_complement = models.CharField(_('complement'), max_length=16)
    locality = models.CharField(_('locality'), max_length=32)
    state = models.CharField(_('state'), max_length=32)

    level_in_mechanics = models.PositiveSmallIntegerField(_('Mechanics'))
    level_in_security = models.PositiveSmallIntegerField(_('Security'))
    level_in_legislation = models.PositiveSmallIntegerField(_('Legislation'))
    level_in_routes = models.PositiveSmallIntegerField(_('Routes'))
