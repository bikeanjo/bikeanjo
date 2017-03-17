# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from front.models import BaseModel


def default_to_first_site():
    return Site.objects.values_list('id', flat=True).first() or 1


class SlideItem(BaseModel):
    class Meta:
        verbose_name = _('Slide')
        verbose_name_plural = _('Slides')
        ordering = ['order']

    active = models.BooleanField(_('Active'), default=True)
    title = models.CharField(_('Title'), max_length=256)
    alt = models.CharField(_('Alternative text'), max_length=256)
    image = models.ImageField(_('Image'), upload_to='slides')
    order = models.PositiveIntegerField(_('Order'), default=0)
    site = models.ForeignKey(Site, default=default_to_first_site)

    def get_image_url(self):
        if not self.image:
            return
        url = {
            'host': self.site.domain,
            'url': self.image.url,
        }
        return 'http://%(host)s%(url)s' % url
