# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)

CYCLIST_ROLES = (
    ('volunteer', _('Volunteer')),
    ('recipient', _('Recipient')),
)


class Service(models.Model):
    label = models.CharField(max_length=64)


class Cyclist(models.Model):
    user = models.OneToOneField(User)

    role = models.CharField(_('role'), choices=CYCLIST_ROLES, max_length=32,
                            blank=True)

    bio = models.CharField(_('biography'), max_length=140, blank=True)

    date_of_birth = models.DateField(_('date of birth'),
                                     default=datetime(1984, 10, 22),
                                     null=True)

    gender = models.CharField(_('gender'), max_length=1, choices=GENDER,
                              blank=True)

    phone = models.CharField(_('phone number'), max_length=32, blank=True)

    years_experience = models.PositiveSmallIntegerField(
                                                    _('years of experience'),
                                                    default=0, null=True)

    address = models.CharField(_('address'), max_length=64, blank=True)

    address_number = models.PositiveSmallIntegerField(_('number'), default=0,
                                                      null=True)

    address_complement = models.CharField(_('complement'), max_length=16,
                                          blank=True)

    locality = models.CharField(_('locality'), max_length=32, blank=True)

    state = models.CharField(_('state'), max_length=32, blank=True)

    level_in_mechanics = models.PositiveSmallIntegerField(_('Mechanics'),
                                                          null=True,
                                                          default=0)

    level_in_security = models.PositiveSmallIntegerField(_('Security'),
                                                         null=True,
                                                         default=0)

    level_in_legislation = models.PositiveSmallIntegerField(_('Legislation'),
                                                            null=True,
                                                            default=0)

    level_in_routes = models.PositiveSmallIntegerField(_('Routes'), default=0,
                                                       null=True)

    services = models.ManyToManyField(Service, _('provide services'))

    def __unicode__(self):
        return self.user.__unicode__()
