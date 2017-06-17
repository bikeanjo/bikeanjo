# -*- coding: utf-8 -*-
from collections import OrderedDict
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import HelpRequest


class RequestStatusListFilter(admin.SimpleListFilter):
    title = _('Status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        status = OrderedDict()
        status.update(HelpRequest.STATUS)
        status['_noba'] = _('Requests without a bikeanjo')
        return status.items()

    def queryset(self, request, queryset):
        value = self.value()
        if value in HelpRequest.STATUS:
            return queryset.filter(status=value)
        if value == '_noba':
            return queryset.filter(status='new', bikeanjo=None)
        return queryset
