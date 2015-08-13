# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from front.models import Match

logger = logging.getLogger('front.review_matches')
SITE = Site.objects.filter(id=settings.SITE_ID).first()


class Command(BaseCommand):
    help = 'Revisa tabela Match'

    def handle(self, *args, **options):
        limit = now() - timedelta(3)

        queryset = Match.objects.select_related('helprequest')\
                                .filter(rejected_date__isnull=True,
                                        created_date__lt=limit,
                                        helprequest__status='new')

        for match in queryset:
            helprequest = match.helprequest
            match.rejected_date = now()
            match.reason = 'time expired'
            match.save()

            age = (now() - match.created_date).days
            logger.info('Match(id=%d) has %d days and expired.' % (match.id, age))

            tries = Match.objects.filter(helprequest=helprequest).count()

            if tries >= 3:
                logger.info('HelpRequest(id=%d) was rejected after %d tries.' % (helprequest.id, tries))
                helprequest.status = 'rejected'
                helprequest.save()
            else:
                helprequest.assign_bikeanjo()
