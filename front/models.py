# -*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime, date
from collections import OrderedDict
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from cyclists.models import User

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


class BaseModel(models.Model):
    """
    All models here should extends this. All models will have
    the created_date and modified_date properties
    """
    created_date = models.DateTimeField(_('Created date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified date'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class HelpStatusManager(models.Manager):
    def open(self):
        return self.filter(status='open')

    def active(self):
        return self.filter(status__in=['new', 'open'])

    def matching(self):
        return self.exclude(bikeanjo=None).filter(status='new')

    def orphan(self):
        return self.filter(bikeanjo=None)

    def unread(self):
        base = self.filter(status='open')
        if 'bikeanjo' in self.core_filters:
            return base.filter(bikeanjo_access__lt=models.F('helpreply__created_date'))
        elif 'requester' in self.core_filters:
            return base.filter(requester_access__lt=models.F('helpreply__created_date'))
        return self.none()


class HelpRequest(BaseModel):
    class Meta:
        verbose_name = _('Help request')
        verbose_name_plural = _('Help requests')

    STATUS = OrderedDict((
        ('new', _('New')),
        ('open', _('Open')),
        ('attended', _('Attended')),
        ('finalized', _('Finalized')),
        ('canceled', _('Canceled')),
        ('rejected', _('Rejected')),
    ))
    HELP_OPTIONS = dict(HELP_REQUEST)

    requester = models.ForeignKey(User, related_name='helprequested_set')
    bikeanjo = models.ForeignKey(User, related_name='helpbikeanjo_set', null=True)
    help_with = models.IntegerField(_('Help with'), default=0)  # choices=HELP_REQUEST
    status = models.CharField(_('Status'), max_length=16, choices=STATUS.items(), default='new')

    requester_access = models.DateTimeField(_('Access date'), default=timezone.now, editable=False)
    bikeanjo_access = models.DateTimeField(_('Access date'), default=timezone.now, editable=False)
    requester_rating = models.PositiveSmallIntegerField(_('Rating'), default=0)
    requester_eval = models.TextField(_('Evaluation'), blank=True)

    track = models.ForeignKey('Track', null=True, blank=True)

    objects = HelpStatusManager()

    def get_help_label(self):
        return HelpRequest.HELP_OPTIONS.get(self.help_with, '')

    def help_labels(self):
        for code, label in HELP:
            if self.help_with >= code:
                break
            if self.help_with & code:
                yield label

    @staticmethod
    def distance(points):
        total = 0
        last = points[0]

        for point in points:
            total += abs(last[0] - point[0]) + abs(last[1] - point[1])
            last = point

        return total

    def find_bikeanjo(self):
        city = self.requester.city
        bikeanjos = User.objects.filter(role='bikeanjo').exclude(match__isnull=False, match__helprequest=self)
        notas = []
        # 3 ponto, 12 rota
        if self.help_with | 12 and self.track:
            saida_pedido = self.track.track[0]
            chegada_pedido = self.track.track[-1]
            for bikeanjo in bikeanjos:
                nota = 999999999
                caminho = None
                for track in bikeanjo.track_set.all():
                    distancia = self.distance([track.track[0], track.track[-1]])
                    d2 = self.distance([track.track[0], saida_pedido, chegada_pedido, track.track[-1]])
                    total = abs(d2 - distancia)
                    if total < nota:
                        nota = total
                        caminho = track
                notas.append([nota, caminho, bikeanjo])
            notas.sort(key=lambda nota: nota[0])

            if len(notas) > 0:
                return notas[0]

        return None, None, None


class HelpReply(BaseModel):
    class Meta:
        verbose_name = _('Help reply')
        verbose_name_plural = _('Help replies')

    author = models.ForeignKey(User)
    helprequest = models.ForeignKey(HelpRequest)
    message = models.TextField(_('Message'))

    class Meta:
        ordering = ['-created_date']


class Track(BaseModel):
    class Meta:
        verbose_name = _('Track')
        verbose_name_plural = _('Tracks')

    user = models.ForeignKey(User)
    start = models.CharField(_('Start'), max_length=128)
    end = models.CharField(_('End'), max_length=128)
    track = models.LineStringField()

    objects = models.GeoManager()

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
        return json.dumps(d)


class Point(BaseModel):
    class Meta:
        verbose_name = _('Point')
        verbose_name_plural = _('Points')

    user = models.ForeignKey(User)
    helprequest = models.ForeignKey(HelpRequest, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=128)
    coords = models.PointField()

    objects = models.GeoManager()

    def json(self):
        d = {
            'type': 'Point',
            'coordinates': self.coords.get_coords(),
            'properties': {
                'address': self.address,
            },
        }
        if self.id:
            d['properties']['id'] = self.id
        return json.dumps(d)


class Match(BaseModel):
    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')
        unique_together = (('bikeanjo', 'helprequest',),)

    bikeanjo = models.ForeignKey(User)
    helprequest = models.ForeignKey(HelpRequest)
    score = models.FloatField(_('Score'), default=0)
    rejected_date = models.DateTimeField(_('Rejected date'), null=True)
    reason = models.CharField(_('Reason'), max_length=128, blank=True)

    def __repr__(self):
        return u'Match(helprequest_id=%s, bikeanjo_id=%s, rejected_date=%.10s)'\
            % (self.helprequest_id, self.bikeanjo_id, self.rejected_date)


class ContentReadLog(models.Model):
    class Meta:
        verbose_name = _('Content read log')
        verbose_name_plural = _('Content read logs')

    user = models.ForeignKey(User)
    created_date = models.DateTimeField(_('Created date'), auto_now_add=True, editable=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadedAnnotationMixin(object):
    @classmethod
    def user_access_annotated(cls, user, order_by={'field': None, 'order': 'ASC'}):
        this_table = cls._meta.db_table
        that_table = ContentReadLog._meta.db_table
        type_id = ContentType.objects.get_for_model(cls).id

        select_fields = ['%s.%s' % (this_table, field.column) for field in cls._meta.fields]
        select_fields.append('%s.created_date AS readed_date' % that_table)
        select_fields = ','.join(select_fields)

        join_fields = '%(this_table)s.id = %(that_table)s.object_id\
                       AND %(that_table)s.content_type_id = %(type_id)s\
                       AND %(that_table)s.user_id IN (%(user_id)d, NULL)' % ({
            'this_table': this_table,
            'that_table': that_table,
            'user_id': user.id,
            'type_id': type_id,
        })

        query = 'SELECT %(select_fields)s FROM %(this_table)s\
                 LEFT OUTER JOIN %(that_table)s ON %(join_fields)s' % ({
            'select_fields': select_fields,
            'this_table': this_table,
            'that_table': that_table,
            'join_fields': join_fields,
        })

        if order_by['field']:
            query += ' ORDER BY %(this_table)s.%(field)s %(order)s' % ({
                'this_table': this_table,
                'field': order_by['field'],
                'order': order_by['order'],
            })

        return cls.objects.raw(query)


class Message(BaseModel, ReadedAnnotationMixin):
    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_date']

    title = models.CharField(_('Title'), max_length=128)
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to='messages', null=True, blank=True)

    readed_by = GenericRelation(ContentReadLog, related_query_name='messages')


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Event(BaseModel, ReadedAnnotationMixin):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-created_date']

    title = models.CharField(_('Title'), max_length=128)
    slug = models.SlugField(_('Slug'), max_length=128)
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to='events', null=True, blank=True)
    date = models.DateField(_('Date'))
    city = models.CharField(_('City'), max_length='64')
    address = models.CharField(_('Address'), max_length='128', blank=True)
    address_link = models.CharField(_('Address link'), max_length='255', blank=True)
    link = models.CharField(_('Link'), max_length='255', blank=True)
    price = models.IntegerField(_('Price'), default=0, blank=True)

    category = models.ForeignKey(Category, null=True, blank=True)
    readed_by = GenericRelation(ContentReadLog, related_query_name='events')

    def get_image_url():
        if self.image:
            return self.image.url

    def __unicode__(self):
        return self.title


class Feedback(BaseModel):
    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    author = models.ForeignKey(User)
    message = models.CharField(_('Message'), max_length=255)


class ContactMessage(BaseModel):
    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')

    email = models.EmailField(_('Email'))
    message = models.CharField(_('Message'), max_length=255)


class Testimony(BaseModel):
    class Meta:
        verbose_name = _('Testimony')
        verbose_name_plural = _('Testimonies')

    author = models.ForeignKey(User)
    message = models.CharField(_('Message'), max_length=255)


class Subscriber(BaseModel):
    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')

    email = models.EmailField(_('Email'), unique=True)
    token = models.CharField(_('Token'), max_length=64, editable=False)
    valid = models.BooleanField(_('Valid'), default=False)

    def save(self, *args, **kwargs):
        self.token = hashlib.sha256(settings.SECRET_KEY + self.email).hexdigest()
        super(Subscriber, self).save(*args, **kwargs)
