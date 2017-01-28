# -*- coding:utf-8 -*-
from django.conf import settings


def bikeconf(request):
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', ''),
        'GOOGLE_SITE_VERIFICATION': getattr(settings, 'GOOGLE_SITE_VERIFICATION', ''),
        'GOOGLE_API_KEY': getattr(settings, 'GOOGLE_API_KEY', ''),
    }


def languages(request):
    return {'languages': settings.LANGUAGES}
