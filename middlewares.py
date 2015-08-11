# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import resolve


class ForceDefaultLanguageMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class BikeanjoSessionConfigMiddleware(object):
    def process_request(self, request):
        request.session.set_expiry(getattr(settings, 'SESSION_COOKIE_AGE_FOR_INCOMPLETE_REGISTER', 600))
        if request.user.is_authenticated() and request.user.accepted_agreement:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)


class ViewNameMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path).url_name
        request.url_name = url_name
