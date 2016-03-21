# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils.timezone import now, timedelta
from django.utils import translation
from emailqueue.models import QueuedMail

from front.utils import set_language

logger = logging.getLogger('front.notifications')

__all__ = (
    'enqueue_30days_notification_for_closed_requests',
)


def dequeue_30days_notification_for_closed_requests(helprequest):
    tag = '30_days_closed_%d' % helprequest.id
    QueuedMail.objects.filter(tag=tag).delete()


def enqueue_30days_notification_for_closed_requests(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = u'Seu pedido #%d foi atendido?' % helprequest.id
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester
    tag = '30_days_closed_%d' % helprequest.id

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    mail = QueuedMail.objects.filter(tag=tag).first()
    if mail:
        return mail

    with translation.override(set_language(recipient)):
        template_name = 'emails/30days_notification_for_closed_requests.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/30days_notification_for_closed_requests.txt'
        text = select_template([template_name]).render(data)

    return QueuedMail.objects.create(
        to=recipient,
        date=(now() + timedelta(30)).date(),
        subject=subject,
        html_content=html,
        text_content=text,
        tag=tag
    )


def dequeue_15days_notification_for_open_requests(helprequest):
    tag = '15_days_open_%d' % helprequest.id
    QueuedMail.objects.filter(tag=tag).delete()


def enqueue_15days_notification_for_open_requests(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = u'Você já atendeu o pedido #%d?' % helprequest.id
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.bikeanjo
    tag = '15_days_open_%d' % helprequest.id

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    mail = QueuedMail.objects.filter(tag=tag).first()
    if mail:
        return mail

    with translation.override(set_language(recipient)):
        template_name = 'emails/15days_notification_for_open_requests.html'
        html = select_template([template_name]).render(data)

        template_name = 'emails/15days_notification_for_open_requests.txt'
        text = select_template([template_name]).render(data)

    return QueuedMail.objects.create(
        to=recipient,
        date=(now() + timedelta(15)).date(),
        subject=subject,
        html_content=html,
        text_content=text,
        tag=tag
    )
