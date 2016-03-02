# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import select_template
from django.utils.timezone import now, timedelta

from emailqueue.models import QueuedMail

logger = logging.getLogger('front.notifications')

__all__ = (
    'enqueue_30days_notification_for_closed_requests',
)


def enqueue_30days_notification_for_closed_requests(helprequest):
    site = Site.objects.filter(id=settings.SITE_ID).first()
    subject = u'Seu pedido #%d foi atendido?' % helprequest.id
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient = helprequest.requester

    data = {
        'helprequest': helprequest,
        'recipient': recipient,
        'site': site,
    }

    mail = QueuedMail.objects.filter(to=recipient, subject=subject).first()
    if mail:
        return mail

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
    )
