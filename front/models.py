# -*- coding: utf-8 -*-
import hashlib
import json
import logging
from collections import OrderedDict
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance as D
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from cyclists.models import User
from cities.models import City, Country
logger = logging.getLogger('front.models')

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


class BaseModel(models.Model):
    """
    All models here should extends this. All models will have
    the created_date and modified_date properties
    """
    created_date = models.DateTimeField(_('Date of creation'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Date of change'), auto_now=True, editable=False)

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
        if 'bikeanjo' in self.core_filters:
            return self.filter(bikeanjo_access__lt=models.F('helpreply__created_date'))
        elif 'requester' in self.core_filters:
            return self.filter(requester_access__lt=models.F('helpreply__created_date'))
        return self.none()


class HelpRequest(BaseModel):
    class Meta:
        verbose_name = _('Help request')
        verbose_name_plural = _('Help requests')

    STATUS = OrderedDict((
        ('new', _('New')),
        ('open', _('Open')),
        ('attended', _('Attended')),
        ('finalized', _('Finished')),
        ('canceled', _('Canceled')),
        ('rejected', _('Rejected')),
        ('eba', _('Closed by EBA')),
    ))
    HELP_OPTIONS = dict(HELP_REQUEST)

    requester = models.ForeignKey(User, related_name='helprequested_set')
    bikeanjo = models.ForeignKey(User, related_name='helpbikeanjo_set', null=True)
    help_with = models.IntegerField(_('Help with'), default=0)  # choices=HELP_REQUEST
    message = models.TextField(_('Message'))

    status = models.CharField(_('Status'), max_length=16, choices=STATUS.items(), default='new')
    closed_by = models.CharField(_('Closed by'), max_length=12, choices=CYCLIST_ROLES, blank=True)

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
        bikeanjos = User.objects.filter(
            role='bikeanjo',
            available=True,
            is_active=True,
            accepted_agreement=True
        ).exclude(
            match__isnull=False,
            match__helprequest=self
        )

        DISTANCE = 10000

        # 3 ponto, 12 rota
        if self.help_with | 12 and self.track:
            best = (None, None, None)
            linestring = self.track.track
            center = linestring.centroid

            near_cities = City.objects.distance(center).order_by('distance')[:2]

            qs = Track.objects.filter(user__in=bikeanjos)
            available = qs.filter(user__city__in=near_cities)

            saida_pedido = linestring[0]
            chegada_pedido = linestring[-1]

            nota = 999999999
            caminho = None

            for model in available:
                distancia = self.distance([model.track[0], model.track[-1]])
                d2 = self.distance([model.track[0], saida_pedido, chegada_pedido, model.track[-1]])
                total = abs(d2 - distancia)

                if total < nota:
                    nota = total
                    caminho = model
                    best = [nota, caminho, model.user]

            return best

        elif self.help_with | 3 and self.point_set.count() > 0:
            nota = 1000000  # metros
            lugar = None

            requester_points = self.point_set.values_list('coords', flat=True)
            for point in requester_points:
                closest = Point.objects\
                               .filter(user__in=bikeanjos,
                                       coords__distance_lte=(point, D(m=DISTANCE)))\
                               .distance(point)\
                               .order_by('distance')\
                               .first()

                if closest and closest.distance.standard < nota:
                    nota = closest.distance.standard
                    lugar = closest

            if lugar:
                return nota, lugar, lugar.user

        return None, None, None

    def assign_bikeanjo(self):
        if not self.requester.accepted_agreement:
            return None

        if self.bikeanjo is None and self.status == 'new':
            score, track, bikeanjo = self.find_bikeanjo()

            if not bikeanjo:
                logger.debug("Can't find Bikeanjo to HelpRequest(id=%d)" % (self.id))
                return

            logger.debug('HelpRequest(id=%d) has a new Bikeanjo(id=%d)' % (self.id, bikeanjo.id))
            self.bikeanjo = bikeanjo
            self.save()

            Match.objects.create(
                bikeanjo=bikeanjo,
                helprequest=self,
                score=score,
            )


class HelpReply(BaseModel):
    class Meta:
        verbose_name = _('Reply to the request')
        verbose_name_plural = _('Replies to the request')
        ordering = ['-created_date']

    author = models.ForeignKey(User)
    helprequest = models.ForeignKey(HelpRequest)
    message = models.TextField(_('Message'))


class Track(BaseModel):
    class Meta:
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')

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


class ReadedAnnotationMixin(object):
    # migration breaks if remove this
    pass


class Message(BaseModel):
    TARGET_ROLES = (
        ('all', _('All')),
    ) + CYCLIST_ROLES

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_date']

    title = models.CharField(_('Title'), max_length=128)
    content = models.TextField(_('Content'))
    image = models.ImageField(_('Image'), upload_to='messages', null=True, blank=True)

    target_roles = models.CharField(_('Target'), choices=TARGET_ROLES, default=TARGET_ROLES[0][0], max_length=16)
    target_city = models.ForeignKey(City, null=True, blank=True)
    target_country = models.ForeignKey(Country, null=True, blank=True)


class ReadedMessage(BaseModel):
    class Meta:
        unique_together = (('user', 'message',))

    user = models.ForeignKey(User)
    message = models.ForeignKey(Message, related_name='readed_by')


class Category(models.Model):
    class Meta:
        verbose_name = _('Event category')
        verbose_name_plural = _('Event categories')

    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


def default_to_first_site():
    site = Site.objects.first()
    return site.id if site else 1


class Event(BaseModel):
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-created_date']

    site = models.ForeignKey(Site, default=default_to_first_site)
    title = models.CharField(_('Title'), max_length=128, blank=True)
    slug = models.SlugField(_('Slug'), max_length=128)
    content = models.TextField(_('Content'), blank=True)
    image = models.ImageField(_('Image'), upload_to='events', null=True, blank=True)
    date = models.DateTimeField(_('Date'))
    v1_city = models.CharField(_('City'), max_length='64', editable=False, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    address = models.CharField(_('Address'), max_length='128', blank=True)
    address_link = models.CharField(_('Address link'), max_length='255', blank=True)
    subscription_link = models.CharField(_('Link'), max_length='255', blank=True)
    price = models.CharField(_('Price'), max_length='128', blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    def get_image_url(self):
        if not self.image:
            return
        url = {
            'host': self.site.domain,
            'url': self.image.url,
        }
        return 'https://%(host)s%(url)s' % url

    def get_absolute_url(self):
        url = {
            'host': self.site.domain,
            'url': reverse('dashboard_event_detail', args=[self.slug]),
        }
        return 'https://%(host)s%(url)s' % url

    def json_ld(self):
        ld = OrderedDict()
        ld["@context"] = "http://schema.org"
        ld["@type"] = "Event"
        ld["name"] = self.title
        ld["startDate"] = self.date.isoformat()
        ld["url"] = self.subscription_link or self.get_absolute_url()

        if self.image:
            ld["image"] = self.get_image_url()

        ld['location'] = OrderedDict()
        ld['location']["@type"] = "Place"

        ld['location']['name'] = getattr(self.city, 'name', '')
        ld['location']['address'] = OrderedDict()
        ld['location']['address']["@type"] = "PostalAddress"
        ld['location']['address']['addressLocality'] = getattr(self.city, 'name', '')

        if self.address:
            ld['location']['address']['streetAddress'] = self.address

        if self.address_link:
            ld['location']['address']['url'] = self.address_link

        return json.dumps(ld)

    def __unicode__(self):
        return self.title


class Feedback(BaseModel):
    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    author = models.ForeignKey(User)
    message = models.TextField(_('Message'))


class ContactMessage(BaseModel):
    class Meta:
        verbose_name = _('Contact message')
        verbose_name_plural = _('Contact messages')

    name = models.CharField(_('Name'), max_length=128)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), default='Contato', max_length=128)
    message = models.TextField(_('Message'))


class Testimony(BaseModel):
    class Meta:
        verbose_name = _('Testimony')
        verbose_name_plural = _('Testimonies')

    author = models.ForeignKey(User)
    message = models.CharField(_('Message'), max_length=255)


class Subscriber(BaseModel):
    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    email = models.EmailField(_('Email'), unique=True)
    token = models.CharField(_('Token'), max_length=64, editable=False)
    valid = models.BooleanField(_('Valid'), default=False)

    def save(self, *args, **kwargs):
        self.token = hashlib.sha256(settings.SECRET_KEY + self.email).hexdigest()
        super(Subscriber, self).save(*args, **kwargs)


class TipForCycling(BaseModel):
    TARGETS = (
        ('all', _('All')),
    ) + CYCLIST_ROLES

    class Meta:
        verbose_name = _('Cycling tip')
        verbose_name_plural = _('Cycling tips')

    title = models.CharField(_('Title'), max_length=128, blank=True)
    content = models.TextField(_('Content'), blank=True)
    image = models.ImageField(_('Image'), upload_to='tips', null=True, blank=True)
    link = models.CharField(_('Link'), max_length='255', blank=True)
    target = models.CharField(_('Target'), choices=TARGETS, default=TARGETS[0][0], max_length=16)

    def get_image_url(self):
        if self.image:
            return self.image.url

    def __unicode__(self):
        return self.title
