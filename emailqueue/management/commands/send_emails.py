# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives

from emailqueue.models import QueuedMail

logger = logging.getLogger('emailqueue.send_emails')
SITE = Site.objects.filter(id=settings.SITE_ID).first()


class Command(BaseCommand):
    help = 'Envia emails de hoje'

    def handle(self, *args, **options):
        today = now().date()
        mails = QueuedMail.objects.filter(date=today)

        if mails.count() == 0:
            logger.info('No emails for today')
        else:
            logger.info('We will send %d email today' % mails.count())

        for mail in mails:
            msg = EmailMultiAlternatives(mail.subject, mail.text_content, mail.sender, [mail.to.email])
            msg.attach_alternative(mail.html_content, "text/html")
            msg.send()

            mail.sent = now()
            mail.save()

