# -*- coding: utf-8 -*-


class ForceDefaultLanguageMiddleware(object):
    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']
