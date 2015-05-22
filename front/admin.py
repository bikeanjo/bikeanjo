from urllib import urlencode
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from front import models

admin.site.site_title = _('Bikeanjo')
admin.site.site_header = _('Bikeanjo administration')
admin.site.index_title = _('Site administration')


class CustomUserAdmin(UserAdmin):
    def full_name(self, obj):
        return obj.get_full_name() or obj.username
    full_name.short_description = _('Full name')

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
                '{} <small><a href="{}?{}">{}</a></small>',
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
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_helprequest_changelist'),
                urlencode(query),
                _('List')
            )

        return counter
    finalized_requests.short_description = _('Finalized requests')

    def lookup_allowed(self, lookup, value):
        allow = [
            'contentreadlog__object_id',
            'contentreadlog__content_type__model',
            'contentreadlog__content_type__app_label',
        ]

        if lookup in allow:
            return True

        return super(CustomUserAdmin, self).lookup_allowed(lookup, value)


@admin.register(models.Requester)
class Requester(CustomUserAdmin):
    list_display = ('full_name', 'is_active', 'city', 'active_requests',
                    'finalized_requests',)


@admin.register(models.Bikeanjo)
class Bikenjo(CustomUserAdmin):
    list_display = ('full_name', 'is_active', 'city', 'active_requests',
                    'finalized_requests', 'service_rating', 'tracks', 'points')

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
                '{} <small><a href="{}?{}">{}</a></small>',
                counter,
                reverse('admin:front_point_changelist'),
                urlencode(query),
                _('List')
            )
        return counter
    points.short_description = _('Points')


@admin.register(models.Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('user', 'start', 'end', 'track',)


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('address', 'coords',)


class HelpReplyInline(admin.TabularInline):
    extra = 0
    model = models.HelpReply
    ordering = ['id']
    readonly_fields = ['created_date', 'author', 'message']


@admin.register(models.HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    inlines = [HelpReplyInline]
    search_fields = ('requester_name', 'bikeanjo_name',)
    list_display = ('requester_name', 'bikeanjo_name', 'get_help_label_',
                    'status', 'requester_rating', 'requester_eval',)

    def get_help_label_(self, obj):
        return obj.get_help_label()
    get_help_label_.short_description = _('Help with')

    def requester_name(self, obj):
        return obj.requester.get_full_name() or obj.requester.username
    requester_name.short_description = _('Requester name')

    def bikeanjo_name(self, obj):
        if obj.bikeanjo is None:
            return ''
        return obj.bikeanjo.get_full_name()
    bikeanjo_name.short_description = _('Bikeanjo name')


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'readed_by_')
    search_fields = ('title',)

    def readed_by_(self, obj):
        return obj.readed_by.count()
    readed_by_.short_description = _('Readed by')


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'address',)
