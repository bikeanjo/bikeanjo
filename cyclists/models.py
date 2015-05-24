# -*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

GENDER = (
    ('male', _('Male')),
    ('female', _('Female')),
)

CYCLIST_ROLES = (
    ('bikeanjo', _('Bikeanjo')),
    ('requester', _('Requester')),
)


HELP_OFFER = (
    (1, _('Teach someone to ride a bike')),  # Ensinando alguém a pedalar
    (2, _('Follow beginners on cycling')),  # Acompanhando iniciantes nas pedaladas
    (4, _('Advice about safe routes')),  # Recomendando rotas mais seguras
    (8, _('Participating in the events of Bike Anjos')),  # Participando dos eventos dos Bikes Anjos
)

HELP_REQUEST = (
    (1, _('Learn to ride a bike')),  # Aprender a pedalar
    (2, _('Pratice cycling')),  # Praticar pedaladas
    (4, _('Route recomendation')),  # Recomendar rota
    (8, _('Monitoring on traffic')),  # Acompanhamento no trânsito
)

HELP = HELP_OFFER + HELP_REQUEST

BIKEANJO_EXPERIENCE = (
    ('less than 1 year', _('Less than 1 year')),
    ('from 1 to 2 years', _('From 1 to 2 years')),
    ('from 2 to 4 years', _('From 2 to 4 years')),
    ('more than 4 years', _('More than 4 years')),
)

REQUESTER_EXPERIENCE = (
    ('do not know pedaling yet', _('I do not know pedaling yet')),
    ('no experience in traffic', _('I know cycling, but have no experience in traffic')),
    ('already ride a long time', _('Already ride a long time but not daily')),
    ('use bike almost every day', _('I use bike almost every day')),
)

EXPERIENCE = BIKEANJO_EXPERIENCE + REQUESTER_EXPERIENCE

BIKE_USE = (
    ('everyday', _('Everyday'),),
    ('just few days a week/month', _('Just few days a week/month'),),
    ('once a week', _('Once a week'),),
    ('no, i use for leisure', _('No, I use for leisure'),),
)


class User(AbstractUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    country = models.CharField(_('Country'), max_length=32, blank=True)
    city = models.CharField(_('City'), max_length=32, blank=True)
    gender = models.CharField(_('Gender'), max_length=24, blank=True)
    birthday = models.DateField(_('Birthday'), default=date.today, null=True)
    ride_experience = models.CharField(_('Ride experience'), choices=EXPERIENCE, max_length=32, blank=True)
    bike_use = models.CharField(_('Bike use'), choices=BIKE_USE, max_length=32, blank=True)
    help_with = models.IntegerField(_('Help with'), default=0)  # choices=HELP
    initiatives = models.CharField(_('Initiatives'), max_length=256, blank=True)
    role = models.CharField(_('Role'), choices=CYCLIST_ROLES, max_length=32, blank=True)
    accepted_agreement = models.BooleanField(_('Accepted agreement'), default=False)

    def get_avatar_url(self):
        social = self.socialaccount_set.first()
        if social:
            return social.get_avatar_url()
        # TODO: avatar field
        return 'http://placehold.it/85x85'

    def help_labels(self):
        for code, label in HELP_OFFER:
            if self.help_with >= code:
                break
            if self.help_with & code:
                yield label


class BikeanjoManager(models.Manager):
    def get_queryset(self):
        return super(BikeanjoManager, self).get_queryset().filter(role='bikeanjo')


class RequesterManager(models.Manager):
    def get_queryset(self):
        return super(RequesterManager, self).get_queryset().filter(role='requester')


class Bikeanjo(User):
    class Meta:
        verbose_name = _('Bikeanjo')
        verbose_name_plural = _('Bikeanjos')
        proxy = True
    objects = BikeanjoManager()


class Requester(User):
    class Meta:
        verbose_name = _('Requester')
        verbose_name_plural = _('Requesters')
        proxy = True
    objects = RequesterManager()
