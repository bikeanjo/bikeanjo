# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import datetime, timedelta
from front.models import HelpRequest, Match

SITE = Site.objects.filter(id=settings.SITE_ID).first()


def send_email(helprequest, recipient, subject, templates=[]):
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.requester

        data = {
            'helprequest': instance,
            'recipient': recipient,
            'site': SITE,
        }

        text_template, html_template = templates
        text = select_template([text_template]).render(data)
        html = select_template([html_template]).render(data)

        msg = EmailMultiAlternatives(subject, text, from_email, [recipient.email])
        msg.attach_alternative(html, "text/html")
        msg.send()


class Command(BaseCommand):
    help = 'Revisa tabela Match'

    def handle(self, *args, **options):
        today = datetime.today()
        limit = today - timedelta(3)

        queryset = Match.objects.select_related('helprequest')\
                                .filter(rejected_date__isnull=True,
                                        created_date__gt=limit,
                                        helprequest__status='new')

        for match in queryset:
            helprequest = match.helprequest
            match.rejected_date = today
            match.reason = 'time expired'
            match.save()

            tries = Match.objects.filter(helprequest=helprequest).count()

            if tries < 3:
                score, path, bikeanjo = helprequest.find_bikeanjo()
                helprequest.bikeanjo = bikeanjo

                if bikeanjo:
                    new_match = Match(bikeanjo=bikeanjo, helprequest=helprequest)
                    new_match.save()
            else:
                helprequest.status = 'rejected'

            helprequest.save()
