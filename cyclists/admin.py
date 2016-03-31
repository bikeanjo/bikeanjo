# -*- coding: utf-8 -*-
from urllib import urlencode
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.models import FlatPage

from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin

from front import models
from cities.models import City

import admin_resources as resources
import cyclists


class CityListFilter(admin.SimpleListFilter):
    title = _('City')
    parameter_name = 'city'
    template = 'admin/custom-filter.html'
    empty_value = '0'

    def lookups(self, request, model_admin):
        return model_admin.model.objects\
                          .exclude(city=None)\
                          .values_list('city__id', 'city__name')\
                          .order_by('city__name')\
                          .distinct()

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.empty_value:
                return queryset.filter(city=None)
            else:
                return queryset.filter(city=self.value())
        return queryset


class CountryListFilter(admin.SimpleListFilter):
    title = _('Country')
    parameter_name = 'country'
    template = 'admin/custom-filter.html'
    empty_value = '0'

    def lookups(self, request, model_admin):
        return model_admin.model.objects\
                          .exclude(country=None)\
                          .values_list('country__id', 'country__name')\
                          .order_by('country__name')\
                          .distinct()

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == self.empty_value:
                return queryset.filter(country=None)
            else:
                return queryset.filter(country=self.value())
        return queryset


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    list_filter = ('date_joined', 'last_login', 'accepted_agreement')
    resource_class = resources.UserResource

    def get_queryset(self, request):
        return super(CustomUserAdmin, self).get_queryset(request).select_related('city', 'country')

    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    full_name.short_description = _('Full name')
    full_name.admin_order_field = 'first_name'

    def active_requests(self, obj):
        counter = 0
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.active().count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.active().count()
        else:
            return '-'

        if counter > 0:
            query = {
                obj.role: obj.id,
                'status__in': 'new,open',
            }
            return format_html(
                u'{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_helprequest_changelist'),
                urlencode(query),
                _('List')
            )

        return counter
    active_requests.short_description = _('Active requests')

    def finalized_requests(self, obj):
        counter = 0
        if obj.role == 'bikeanjo':
            counter = obj.helpbikeanjo_set.filter(status='finalized').count()
        elif obj.role == 'requester':
            counter = obj.helprequested_set.filter(status='finalized').count()
        else:
            return '-'

        if counter > 0:
            query = {
                obj.role: obj.id,
                'status__in': 'finalized',
            }
            return format_html(
                u'{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_helprequest_changelist'),
                urlencode(query),
                _('List')
            )

        return counter
    finalized_requests.short_description = _('Finished requests')

    def lookup_allowed(self, lookup, value):
        allow = [
            'contentreadlog__object_id',
            'contentreadlog__content_type__model',
            'contentreadlog__content_type__app_label',
        ]

        if lookup in allow:
            return True

        return super(CustomUserAdmin, self).lookup_allowed(lookup, value)


@admin.register(cyclists.models.User)
class User(CustomUserAdmin):
    list_display = ('full_name', 'email', 'role', 'date_joined',
                    'last_login', 'city', 'country', 'accepted_agreement')
    list_filter = ('role', CityListFilter, CountryListFilter, 'date_joined',
                   'last_login', 'accepted_agreement')


@admin.register(cyclists.models.Requester)
class Requester(CustomUserAdmin):
    list_display = ('full_name', 'date_joined', 'last_login', 'city', 'country',
                    'active_requests', 'finalized_requests',)
    list_filter = (CityListFilter, CountryListFilter, 'date_joined', 'last_login')


@admin.register(cyclists.models.Bikeanjo)
class Bikeanjo(CustomUserAdmin):
    list_display = ('full_name', 'date_joined', 'last_login', 'available', 'city', 'country',
                    'active_requests', 'finalized_requests', 'service_rating',
                    'tracks', 'points')
    list_filter = (CityListFilter, CountryListFilter, 'available', 'date_joined', 'last_login')

    def service_rating(self, obj):
        if obj.role != 'bikeanjo':
            return '-'
        rating = obj.helpbikeanjo_set\
                    .filter(status='finalized')\
                    .aggregate(avg_rating=models.models.Avg('requester_rating'))\
                    .values()[0]
        return rating or 0
    service_rating.short_description = _('Service rating')

    def tracks(self, obj):
        counter = obj.track_set.count()
        if counter > 0:
            query = {'user': obj.id}
            return format_html(
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_track_changelist'),
                urlencode(query),
                _('List')
            )
        return counter
    tracks.short_description = _('Tracks')

    def points(self, obj):
        counter = obj.point_set.count()
        if counter > 0:
            query = {'user': obj.id}
            return format_html(
                u'{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_point_changelist'),
                urlencode(query),
                _('List')
            )
        return counter
    points.short_description = _('Points')
