# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    """ Add created_date and modified_date in models that extends this class """

    created_date = models.DateTimeField(_('Created date'), auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(_('Modified date'), auto_now=True, editable=False)

    class Meta:
        abstract = True


class QueuedMail(BaseModel):
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    sender = models.EmailField(_('From'), default=getattr(settings, 'DEFAULT_FROM_EMAIL', ''))
    date = models.DateField(_('Date'))
    tag = models.CharField(_('Tag'), max_length=64, blank=True, db_index=True)
    sent = models.DateTimeField(_('Sent'), null=True, editable=False)
    subject = models.CharField(_('Subject'), max_length=128)
    html_content = models.TextField(_('HTML Content'))
    text_content = models.TextField(_('Text Content'))
    errors = models.CharField(_('Error'), max_length=256, editable=False)

    class Meta:
        verbose_name = _('Queued Email')
        verbose_name_plural = _('Queued Emails')
