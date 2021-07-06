# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import resolve
from django.utils import translation
from django.contrib.auth.models import AnonymousUser


class ForceDefaultLanguageMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class BikeanjoSessionConfigMiddleware(object):
    def process_request(self, request):
        request.session.set_expiry(getattr(settings, 'SESSION_COOKIE_AGE_FOR_INCOMPLETE_REGISTER', 21600))
        if request.user.is_authenticated() and request.user.accepted_agreement:
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)


class BikeanjoLocaleMiddleware(object):
    '''
    This middleware should be used after Authentication middleware and Locale
    middleware and before Common middleware, like this: \n
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middlewares.BikeanjoLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    '''
    def process_request(self, request):
        if hasattr(request, 'user') and \
                not isinstance(request.user, AnonymousUser) \
                and request.user.language:
            translation.activate(request.user.language)
            request.LANGUAGE_CODE = translation.get_language()

        elif request.session.get('language') in [l[0] for l in settings.LANGUAGES]:
            translation.activate(request.session.get('language'))
            request.LANGUAGE_CODE = translation.get_language()


class ViewNameMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path).url_name
        request.url_name = url_name
