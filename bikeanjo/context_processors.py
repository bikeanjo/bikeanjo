# -*- coding:utf-8 -*-
from django.conf import settings


def bikeconf(request):
    return {
        'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', '')
    }
