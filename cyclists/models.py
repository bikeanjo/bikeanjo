# -*- coding: utf-8 -*-
import os
from datetime import date
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from bikeanjo.settings import LANGUAGES

from cities.models import Country, City, CityAlias

GENDER = (
    ('male', _('Male')),
    ('female', _('Female')),
)

CYCLIST_ROLES = (
    ('bikeanjo', _('Bike Anjo')),
    ('requester', _('New cyclist')),
)


HELP_OFFER = (
    (1, _('Teach someone how to ride a bike')),  # Ensinando alguém a pedalar
    (2, _('Commute together with beginners on their first rides')),  # Acompanhando iniciantes nas pedaladas
    (4, _('Suggest safe routes')),  # Recomendando rotas mais seguras
    (8, _('Participate on Bike Anjo events')),  # Participando dos eventos dos Bikes Anjos
)

HELP_REQUEST = (
    (1, _('Learn to ride a bike')),  # Aprender a pedalar
    (2, _('Practice riding')),  # Praticar pedaladas
    (4, _('Route recommendation')),  # Recomendar rota
    (8, _('Commute together')),  # Acompanhamento no trânsito
)

HELP = HELP_OFFER + HELP_REQUEST

BIKEANJO_EXPERIENCE = (
    ('less than 1 year', _('Less than 1 year')),
    ('from 1 to 2 years', _('From 1 to 2 years')),
    ('from 2 to 4 years', _('From 2 to 4 years')),
    ('more than 4 years', _('More than 4 years')),
)

REQUESTER_EXPERIENCE = (
    ('do not know pedaling yet', _('I still don\'t know how to ride a bike')),
    ('no experience in traffic', _('I know how to ride a bike, but have not traffic experience')),
    ('already ride a long time', _('I bike for many years now, but not on a daily basis')),
    ('use bike almost every day', _('I ride my bike almost every day')),
)

EXPERIENCE = BIKEANJO_EXPERIENCE + REQUESTER_EXPERIENCE

BIKE_USE = (
    ('everyday', _('Everyday'),),
    ('just few days a week/month', _('Only a few days per week/month'),),
    ('once a week', _('Once a week'),),
    ('no, i use for leisure', _('I only use my bike for leisure or on weekends'),),
)


class AvatarStorage(FileSystemStorage):
    subfolder = 'avatars'

    def get_available_name(self, name):
        if self.exists(name):
            os.remove(name)
        return name

    def url(self, name):
        basename = os.path.basename(name)
        subfolder = getattr(type(self), 'subfolder', '')
        relative = os.path.join(subfolder, basename)
        return super(AvatarStorage, self).url(relative)


def get_upload_path(user, filename):
    base_folder = os.path.join(settings.MEDIA_ROOT, AvatarStorage.subfolder)
    extension = filename.rsplit('.', 1)[-1]
    new_name = '%s.%s' % (user.username, extension)
    return os.path.join(base_folder, new_name)


class User(AbstractUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    avatar = models.ImageField(_('Avatar'), upload_to=get_upload_path,
                               storage=AvatarStorage(), blank=True)

    v1_country = models.CharField(_('Country'), max_length=32, blank=True)
    v1_city = models.CharField(_('City'), max_length=64, blank=True)

    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    city_alias = models.ForeignKey(CityAlias, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    gender = models.CharField(_('Gender'), max_length=24, blank=True)
    birthday = models.DateField(_('Date of birth'), default=date.today, null=True)
    ride_experience = models.CharField(_('Ride experience'), choices=EXPERIENCE, max_length=32, blank=True)
    bike_use = models.CharField(_('Bike use'), choices=BIKE_USE, max_length=32, blank=True)
    help_with = models.IntegerField(_('Help with'), default=0)  # choices=HELP
    initiatives = models.TextField(blank=True)
    role = models.CharField(_('Role'), choices=CYCLIST_ROLES, max_length=32, blank=True)
    accepted_agreement = models.BooleanField(_('Accepted Terms of Use'), default=False)
    available = models.BooleanField(_('Available'), default=True)

    language = models.CharField(_('Language'), max_length=8, choices=LANGUAGES, default=LANGUAGES[0][0])

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        social = self.socialaccount_set.first()
        if social:
            return social.get_avatar_url()
        return os.path.join(settings.STATIC_URL, 'imgs', 'empty-avatar.png')

    def help_labels(self):
        for code, label in HELP_OFFER:
            if code >= self.help_with:
                break
            if self.help_with & code:
                yield label

    def is_valid(self):
        return self.accepted_agreement

    def has_bikeanjo_near(self):
        return User.object.filter(role='bikeanjo', city=self.city).exists()


class BikeanjoManager(models.Manager):
    def get_queryset(self):
        return super(BikeanjoManager, self).get_queryset().filter(role='bikeanjo')


class RequesterManager(models.Manager):
    def get_queryset(self):
        return super(RequesterManager, self).get_queryset().filter(role='requester')


class Bikeanjo(User):
    class Meta:
        verbose_name = _('Bike Anjo')
        verbose_name_plural = _('Bike anjos')
        proxy = True
    objects = BikeanjoManager()


class Requester(User):
    class Meta:
        verbose_name = _('New cyclist')
        verbose_name_plural = _('New cyclists')
        proxy = True
    objects = RequesterManager()
