# -*- coding: utf-8 -*-
import re
import datetime
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


class CreatedDateListFilter(admin.SimpleListFilter):
    title = _('Date')
    parameter_name = 'created_date'
    template = 'admin/created_date_filter.html'
    regex = re.compile('^(?P<day>\d\d)/(?P<month>\d\d)/(?P<year>20\d\d)$')

    def lookups(self, request, model_admin):
        return (('datepicker', self.value()),)

    def choices(self, *args):
        choice = {
            'display': u'datepicker',
            'name': 'created_date',
            'query_string': '?created_date=%s&q=' % self.value(),
            'selected': True,
            'val': self.parse(self.value())
        }
        return [choice]

    def value(self):
        return super(CreatedDateListFilter, self).value() or ''

    def parse(self, request):
        value = self.value()
        result = []
        for date in value.split(','):
            match = self.regex.match(date)
            if(match):
                date = {k: int(v) for k, v in match.groupdict().items()}
                date = datetime.date(**date)
                result.append(date)

        key = self.parameter_name
        if len(result) == 1:
            return {key: result[0]}
        elif len(result) == 2:
            return {
                "%s__gte" % key: result[0],
                "%s__lte" % key: result[1],
            }
        return {}

    def queryset(self, request, queryset):
        dates = self.parse(request)
        return queryset.filter(**dates)
